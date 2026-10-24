"""Application journal fsync is durable even when the catalog checkpoint fails."""

import hashlib
import json
from pathlib import Path

import pytest

from easyai.runtime.supervisor import ManagedSupervisor
from easyai.domain.program import ProgramIR
from easyai.services.event_journal import EventJournal
from easyai.services.run_service import RunService
from test_run_service import prepare


def test_cancelled_event_survives_catalog_failure_and_cannot_restart(owned, monkeypatch):
    service = owned[1]
    original = prepare(owned)
    root = service.root

    def failed_catalog():
        raise OSError("simulated crash before catalog checkpoint")

    with monkeypatch.context() as patch:
        patch.setattr(service, "_persist", failed_catalog)
        with pytest.raises(OSError, match="simulated crash"):
            service.cancel(original.run_id)
    service.close()  # No supervisor exists; close cannot conceal the interrupted checkpoint.

    catalog = json.loads((root / "catalog.json").read_bytes())
    assert catalog["entries"][original.run_id]["run"]["status"] == "CREATED"
    log = Path(original.config.run_root) / "logs/events.jsonl"
    persisted = [json.loads(line) for line in log.read_bytes().splitlines()]
    assert persisted[-1]["type"] == "status_changed"
    assert persisted[-1]["payload"]["status"] == "CANCELLED"

    def forbid_launch(_supervisor):
        pytest.fail("A durably cancelled run attempted to launch a training process")

    monkeypatch.setattr(ManagedSupervisor, "start", forbid_launch)
    recovered = RunService(root)
    try:
        assert recovered.get(original.run_id).status == "CANCELLED"
        assert recovered.events(original.run_id)[-1].payload["status"] == "CANCELLED"
        with pytest.raises(ValueError, match="RUN_PROCESS_IDENTITY_UNKNOWN"):
            recovered.start(original.run_id)
    finally:
        recovered.close()


@pytest.mark.parametrize("terminal", ["FAILED", "SUCCEEDED"])
def test_durable_terminal_application_event_does_not_regress_to_old_catalog(owned, terminal):
    service = owned[1]
    original = prepare(owned)
    root = service.root
    # This checkpoint represents an already validated local terminal transition:
    # its complete application event reached fsync, but catalog replacement did not.
    service._journal(original.run_id).append("status_changed", None, {"status": terminal})
    service.close()
    catalog = json.loads((root / "catalog.json").read_bytes())
    assert catalog["entries"][original.run_id]["run"]["status"] == "CREATED"
    recovered = RunService(root)
    try:
        assert recovered.get(original.run_id).status == terminal
        assert recovered.get(original.run_id).sync_state == "complete"
        events = recovered.events(original.run_id)
        assert events[-1].payload["status"] == terminal
        assert len(events) == 2
    finally:
        recovered.close()


@pytest.mark.parametrize(
    ("failure", "status", "sync_state"),
    [
        (None, "SUCCEEDED", "complete"),
        ("missing-artifacts", "FAILED", "error"),
        ("management", "FAILED", "complete"),
    ],
)
def test_terminal_states_survive_catalog_checkpoint_crash(
    owned, monkeypatch, failure, status, sync_state
):
    service = owned[1]
    original = prepare(owned)
    root = service.root
    run_root = Path(original.config.run_root)
    program = ProgramIR.model_validate_json((run_root / "program.ir.json").read_bytes())
    epochs = 1 if program.execution_mode == "quick" else program.training.epochs
    # Synthetic protocol evidence only: no child process, model or data is used.
    # Artifact bytes exercise integrity/required-output policy, not model loading
    # or image decoding. They are deliberately labeled synthetic in this test only.
    runtime = EventJournal(run_root / "logs/runtime-events.jsonl", original.run_id, "runtime")
    try:
        if failure != "missing-artifacts":
            outputs = run_root / "outputs"
            outputs.mkdir()
            producers = [(program.training.origin.block_id, "model", None, None)]
            for phase, figures in (
                ("before", program.training.before),
                ("epoch_end", program.training.body),
                ("after", program.training.after),
            ):
                for figure in figures:
                    for epoch in range(1, epochs + 1) if phase == "epoch_end" else [None]:
                        producers.append((figure.id, "figure", phase, epoch))
            for index, (block, kind, phase, epoch) in enumerate(producers):
                content = f"synthetic protocol artifact {index}\n".encode()
                relative = f"outputs/fixture-{index}.bin"
                (run_root / relative).write_bytes(content)
                runtime.append(
                    "artifact_created",
                    block,
                    {
                        "artifactId": f"fixture-{index}",
                        "runId": original.run_id,
                        "kind": kind,
                        "relativePath": relative,
                        "mimeType": "application/octet-stream",
                        "sizeBytes": len(content),
                        "sha256": hashlib.sha256(content).hexdigest(),
                        "producerBlockId": block,
                        "contributorBlockIds": [block],
                        "phase": phase,
                        "epoch": epoch,
                        "syncState": "ready",
                    },
                )
        for epoch in range(1, epochs + 1):
            runtime.append(
                "epoch_completed",
                program.training.origin.block_id,
                {
                    "epoch": epoch,
                    "train_loss": 1.0,
                    "test_accuracy": 0.0,
                    "train_samples": 1,
                    "test_samples": 1,
                    "elapsed_seconds": 0.01,
                },
            )
        runtime.append(
            "pipeline_completed",
            program.training.origin.block_id,
            {"epochs": epochs, "executionMode": program.execution_mode},
        )
        exit_payload = {"exitCode": 0}
        if failure == "management":
            exit_payload["managementFailed"] = True
        runtime.append("process_exited", None, exit_payload)
    finally:
        runtime.close()

    def failed_catalog():
        raise OSError("simulated terminal checkpoint crash")

    with monkeypatch.context() as patch:
        patch.setattr(service, "_persist", failed_catalog)
        with pytest.raises(OSError, match="terminal checkpoint crash"):
            service.get(original.run_id)
    service.close()
    catalog = json.loads((root / "catalog.json").read_bytes())
    assert catalog["entries"][original.run_id]["run"]["status"] == "CREATED"

    recovered = RunService(root)
    try:
        restored = recovered.get(original.run_id)
        assert restored.status == status
        assert restored.sync_state == sync_state
        events = recovered.events(original.run_id)
        assert events[-1].payload == {"status": status, "syncState": sync_state}
        assert recovered.get(original.run_id) == restored
        assert recovered.events(original.run_id) == events
        with pytest.raises(ValueError, match="RUN_PROCESS_IDENTITY_UNKNOWN"):
            recovered.start(original.run_id)
    finally:
        recovered.close()
