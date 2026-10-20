# Easy-AI 第三方组件说明（待完成的分发草稿）

**草稿，未发布；不是完成审核声明，也不是 Easy-AI 的项目许可证。** 目标二进制源码为 `1e427fb49e444f7feea451cbffd4353e8e969bed`；当前尚未取得精确 Windows 包。方括号字段未填实前不能作为已履行说明发布。

Easy-AI 使用 Paramiko 4.0.0 提供 SSH 功能。Paramiko 及其使用受 GNU LGPL 2.1 约束；原源码文件允许 2.1 或以后版本，此处按 2.1 交付。版权归原作者所有，包括 Robey Pointer 及后续贡献者；各源码中的原版权声明应保留。完整许可为 [LICENSE.Paramiko-4.0.0.txt](licenses/LICENSE.Paramiko-4.0.0.txt)。

Paramiko 对应源码：[同一 Release 中已实际上传并核验的源代码附件链接，未提供]。修改库后重建 Easy-AI 的材料和说明：[同一 Release 中已实际上传的重建材料链接，未提供]。这些字段不是承诺未来提供源码，当前也没有三年书面提供承诺。

Windows Electron 运行时包含 FFmpeg 组件。已定位的上游链为 Electron 44.9.0 → Chromium 152.0.7977.167 → FFmpeg `2b68d2babae73714846961fb0ee47e3b3d2e39a9`，但精确 DLL 对应及完整构建配置仍待核实。匹配源码、修改和构建材料：[同一 Release 附件链接，未提供]。FFmpeg 原 LGPL/其他文件声明应保留；不能只用 Electron 的 MIT 覆盖 FFmpeg。

Electron 本身采用 MIT；包根 `LICENSE`、`LICENSE.electron.txt` 属于 Electron，不能据此认定 Easy-AI 自身采用 MIT。Chromium/Node 及相关第三方原文以精确包的 `LICENSES.chromium.html` 为准。原生文件应与该运行时来源一致。

CPython 3.11.9 采用 PSF 和其历史许可，见 [原 LICENSE](licenses/LICENSE.CPython-3.11.9.txt) 及 [CPython 第三方许可原文](licenses/THIRD-PARTY.CPython-3.11.9.rst)。[libffi 3.4.4 原许可](licenses/LICENSE.libffi-3.4.4.txt) 为上游 CPython 构建参考，最终版本对应仍待核对。[OpenSSL 原许可](licenses/LICENSE.OpenSSL-Apache-2.0.txt) 适用于所核查的 OpenSSL 3.0.13 与 4.0.3 许可文本；不能将两份二进制视作同一副本。

应用 Python 包及前端库的原 notices 应保留在 `resources/notices/`。cryptography 的 SBOM 用于定位静态 OpenSSL/Rust 依赖，还需对应其原版权/NOTICE；SBOM 本身不替代所有许可原文。PyNaCl 的 libsodium 采用 ISC，原 notice 应一同保留。Microsoft DLL 需有适用再分发依据，不能以本说明代授予许可。

PyInstaller 的 bootloader/loader 有组合分发例外，见 [原 COPYING](licenses/COPYING.PyInstaller-6.18.0.txt)；该例外不改变 Paramiko 等第三方的许可条件。

Easy-AI 自身许可：[权利人决定，未生效]。第三方权利由各原许可证直接授予；本草稿不增加限制或自动改变项目许可。若本说明作为包外附件提供，应标明“附加分发材料”，不得声称已写入原 ZIP 或应用界面。
