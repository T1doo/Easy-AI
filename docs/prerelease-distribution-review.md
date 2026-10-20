# 当前预发布分发核查（2026-10-20）

本次只核查发布材料，不改产品、构建或许可状态，不发布。用户已授权自有仓库 Pre-release；这不等于为项目选择开源许可证。本文件和 [说明草稿](release-drafts/THIRD-PARTY-NOTICES.draft.md) 不授予 Easy-AI 自身的新权利。`legalReviewComplete=false`、`distributionReady=false` 不变；标志本身不是第三方许可禁令。

## 证据范围

| 对象 | 实际证据 | 不能据此声称 |
| --- | --- | --- |
| 当前二进制候选源码 | main `1e427fb49e444f7feea451cbffd4353e8e969bed`；[CI39425106599](https://github.com/T1doo/Easy-AI/actions/runs/39425106599) 两平台成功，Windows 日志记录 CPython 3.11.9、Electron 44.9.0、PyInstaller 6.18.0 和 PYZ 构建 | 当前 Windows 包已本地逐项审计 |
| 当前候选 ZIP | CI 报告 435284263 字节，SHA256 `ed31980b5df073cc070eec9b06428bb857d547f47c677cde23647ea2fb7812ea`；artifact `12265522152` | 已取得这些字节或已核实其中所有许可证 |
| 下载状态 | 连接器文件交付失败；一次 CLI 备用下载被 artifact 存储拒绝，所得文件 0 字节；已停止下载 | 下载已恢复、已有可上传包或可以换通道绕过 |
| 可读的历史 Windows 包 | 源码 `43474263d8b61ab12bc50ef554259013c4a326d6`，ZIP SHA256 `4779ee31b553f8a09690cf1a59af36ace910998d405b31e90c8cb1301d5c2200`；本次只读清单、许可、SBOM、部分 PE 版本字符串及 PYZ 目录 | 历史包可以替代当前候选；其原生文件版本必然等于当前包 |
| 构建方式 | [构建入口](../scripts/python-task.mjs) 为默认 `--onedir`，未选择外置 Paramiko 源码；本地 Linux TOC 也有 Paramiko | Linux 构建 TOC 是当前 Windows 成品证明 |

机器可读事实、输入 SHA256 和历史包取证见 [证据 JSON](evidence/prerelease-distribution-20261020.json)。本次没有执行任何 Windows 二进制、重建、重跑 CI、训练或 SSH。

## Paramiko：实际收集方式与最小交付路径

应用锁定 `paramiko==4.0.0`。其元数据声明 `LGPL-2.1`，源码文件头允许 2.1 或以后版本；本次按 2.1 核对。[许可原文](https://github.com/paramiko/paramiko/blob/4.0.0/LICENSE) 第 4、6 节规定源码及组合可执行作品的条件。

历史 Windows sidecar 的只读 CArchive/PYZ 目录中确有 **43 个 Paramiko 模块**。ZIP 中存在 dist-info/许可证，但没有外置 `paramiko/*.py` 源码目录。[PyInstaller 说明](https://pyinstaller.org/en/v6.18.0/advanced-topics.html#python-imports-in-a-bundled-app) 与安装的 6.18.0 导入器实现一致：先查 PYZ，未找到才回退文件系统。当前相同构建入口和 CI 的 PYZ 日志支持“默认将库收进可执行文件”的判断；当前 Windows 精确成员清单仍待取得包后核实。

因此，不能把通常 Python 的动态 import 等同于此冻结包已满足 LGPL 2.1 第 6(b) 节。现有证据没有证明用户放入另一份库即可替换内嵌模块。无需现在改冻结架构：可准备第 6(a)/(d) 节所需的对应源码和重建材料，实际可用后随二进制从同一 Release 提供。**此为拟采用路径，尚未履行。** LGPL 不要求自动把 Easy-AI 全部改成 LGPL。

具体未落实项是：

1. 锁文件指定的完整 Paramiko 4.0.0 sdist；不是从 wheel 拷出的若干 `.py` 文件。后续本轮已实际从锁中官方 URL 取得，1630743 字节及 SHA256 `6a25f07b380cc9c9a88d2b920ad37167ac4667f8d9886ccebd8f90f654b5d69f` 与锁完全一致，259 项归档目录可读；**已本地准备，尚未公开托管**。
2. 供用户修改库后重建组合可执行作品的完整材料：精确 Easy-AI 源码、锁文件、构建脚本、必要数据/工具及使用说明；同时核实相应工具可取得。已有源码和冻结入口是基础，不等于已验证完整材料闭包。特别是构建脚本 `uv sync --frozen` 会还原锁定库，必须给出在独立构建副本中重新锁定/安装修改库的具体步骤；本轮未实测，不能声称可重建。
3. 对作品自身的使用条款必须允许用户为本人使用修改作品，以及为调试这些修改进行逆向工程。不能用“所有权利保留”草率否定这两项，也不能代表权利人新增这些授权。
4. 每份作品的显著 Paramiko 使用说明、原许可和版权通知，以及实际可访问的源码/重建材料链接。若运行中展示版权通知，还需核实该展示是否包含 LGPL 所需的库通知；本轮没有修改 UI。

不采用第 6(c) 节的三年书面提供承诺；草稿不许诺未来履行。源码交付清单见 [SOURCE-DELIVERY 草稿](release-drafts/SOURCE-DELIVERY.draft.md)。

## 原生依赖与分发材料

以下“历史实见”均绑定 `43474263…`，当前 Windows 精确核验仍未完成。上游许可证允许的保留/复制工作可直接准备，不需要让用户逐项“接受新协议”。实际条件必须完成；仅复制许可文本不证明源码或可替换性条件已满足。

| 组件/版本 | 收集和许可事实 | 可准备材料；剩余事实缺口 |
| --- | --- | --- |
| Electron 44.9.0，Chromium/Node 及伴随 DLL | 应用锁定 Electron；其 [DEPS](https://github.com/electron/electron/blob/v44.9.0/DEPS) 指向 Chromium 152.0.7977.167、Node v24.22.0。历史包有 `easyai.exe`、DirectX/SwiftShader/Vulkan DLL，根 `LICENSE`、`LICENSE.electron.txt` 和 `LICENSES.chromium.html` | 保留匹配该 Electron 归档的原 notices；根 `LICENSE` 是 Electron 的 MIT 文本，**不是 Easy-AI 的项目许可证**。20MB Chromium notices 含构建工具/未必进入运行时的组件，不能仅搜索 GPL/LGPL 字样就判整个应用许可 |
| Electron 附带 FFmpeg | 历史包有 `ffmpeg.dll`，Chromium notices 有 FFmpeg LGPL 2.1+ 说明。[FFmpeg 官方分发清单](https://ffmpeg.org/legal.html) 强调对应源码、修改和构建方式 | 上游精确修订源码归档、Electron 补丁及 GN 参数已实际取得；同一源码的 Chrome/win/x64 config.h 中 GPL/nonfree/version3 均为 0。仍须核实成品对应、完整构建闭包及兼容 DLL 替换，尚未公开托管源码；上游配置不能冒充成品核验 |
| CPython 3.11.9 | 当前 CI 解释器版本明确；历史包 `python311.dll` 版本也是 3.11.9，含 Python stdlib 扩展及 `base_library.zip`。PSF 和历史许可允许源码/二进制再分发，需保留相应声明 | 已按原字节准备 [CPython LICENSE](release-drafts/licenses/LICENSE.CPython-3.11.9.txt) 和 [3.11.9 第三方许可原文](release-drafts/licenses/THIRD-PARTY.CPython-3.11.9.rst)。历史包没有单独的这两项 Python 归属文件；现有 dist-info 收集器不会自动覆盖解释器。是否由其他精确 notices 全部覆盖仍须逐项核对 |
| Python 的 OpenSSL / libffi | 历史 `libcrypto-3.dll` 字符串为 OpenSSL 3.0.13；有 `libssl-3.dll`、`libffi-8.dll`。CPython 3.11.9 [构建清单](https://github.com/python/cpython/blob/v3.11.9/PCbuild/get_externals.bat) 指向 OpenSSL 3.0.13、libffi 3.4.4 | 已准备上游 Apache-2.0/ MIT 原文；libffi 3.4.4 目前是上游构建依据，尚非当前成品版本证明。需对应原生文件、版权/NOTICE 与 CPython 实际构建来源；CFFI 自身 MIT-0 不能替代 libffi 的署名条件 |
| cryptography 50.0.2 | 锁定版；历史 `_rust.pyd` 和 wheel SBOM 实见，SBOM 列静态 OpenSSL **4.0.3** 及 39 项 Rust 组件。当前 CI hook 也报告并非动态链接 OpenSSL；[官方 wheel 说明](https://cryptography.io/en/latest/installation/#building-cryptography-on-windows) 解释 Windows 静态依赖 | 保留现有 Apache/BSD 文本及 SBOM，补对应 OpenSSL/原生组件 attribution。不能拿 Python 的 OpenSSL 3.0.13 当作此静态副本。SBOM 是识别入口，不等于每项 copyright/NOTICE 已保留；其 build-time 项也不能一概算作随包运行时代码 |
| cryptography 的 Rust 闭包 | 历史 SBOM 含 `unicode-ident` 的 `(MIT OR Apache-2.0) AND Unicode-3.0`、`target-lexicon` 的 `Apache-2.0 WITH LLVM-exception`；`self_cell` 为 `Apache-2.0 OR GPL-2.0-only` | 分别核对实际进入二进制的组件及原声明；不能用一份笼统 MIT 覆盖 Unicode/LLVM 附加文本。双许可组件可按其已有 Apache 分支分发，并不要求把 GPL 分支也施加给项目；当前 SBOM 仍需与成品及原始 notices 对应 |
| bcrypt 5.0.0、PyNaCl 1.6.2 | 历史 `_bcrypt.pyd`、`nacl/_sodium.pyd`；Apache-2.0；PyNaCl 原 notices 已含 libsodium ISC 文本 | 保留现有许可/版权；核对 wheel 内嵌 Rust/本地库的实际版本和 notices 范围。包版本不能自动代表所有静态子组件版本 |
| CFFI 2.1.1、pydantic-core 2.41.5 | 历史 `_cffi_backend…pyd`、`_pydantic_core…pyd`；分别 MIT-0、MIT；libffi 是另一个许可对象 | 保留原文；核对实际嵌入组件的版权/许可，不能只用 Python distribution 的单字段判完整闭包 |
| mypy 1.19.1、librt 0.16.0 | 历史包实际含许多 mypy `.pyd` 和 librt `.pyd`，PYZ 也有二者；两者 notices 为 MIT | 保留声明即可准备；不可因为它们属于 dev group 就从实际分发核查删除。本轮不清理产品依赖或重建 |
| PyInstaller 6.18.0 | 构建工具 GPL，加明确 bootloader/loader 组合分发例外；runtime hooks 为 Apache-2.0。历史 PYZ 没有 `PyInstaller` 包根，存在正常 loader/hooks | [官方原文](https://pyinstaller.org/en/v6.18.0/license.html) 不要求被打包应用自动采用 GPL。已准备原 COPYING 供核对；若分发工具本体或修改工具另按对应规则处理，不能把例外扩大到所有第三方库 |
| Microsoft VC/UCRT/API-set DLL | 历史包有 VCRUNTIME140 14.38.33126.1、ucrtbase 10.0.26100.1742 及 API-set DLL；不是 PSF/MIT 自动覆盖的文件 | [Microsoft 规则](https://learn.microsoft.com/en-us/cpp/windows/redistributing-visual-cpp-files?view=msvc-170) 要求核对分发许可和 REDIST 来源；[UCRT 说明](https://learn.microsoft.com/en-us/cpp/windows/universal-crt-deployment?view=msvc-170) 说明 Windows 10+ 已内含 UCRT。现清单未给出每个实际 DLL 的可再分发来源证明；不能把 CI 机器可读或文件由 System32 收集等同为再分发授权。需要事实来源/适用许可依据，不代表要求用户现在购买或接受新协议 |

前端 Blockly/React/Monaco 及普通 Python 包的既有 MIT/BSD/Apache/ISC notices 已由收集器保留，可按其条件沿用。双许可不等于要接受两套互斥条款。`collectNotices` 的声明范围是“前端依赖图和已安装 Python 元数据”，不是精确 native/system 法律审核；当前补充文件也没有改变其范围。

补充原始依据：Electron 44.9.0 的 [上游 GN 参数](https://github.com/electron/electron/blob/v44.9.0/build/args/all.gn) 实写 `ffmpeg_branding="Chrome"`、`proprietary_codecs=true`，这两个选项不能直接等同 `--enable-gpl` 或 `--enable-nonfree`。Chromium Git 服务读取 DEPS 遇到 HTTP 503 后，从其官方 GitHub 镜像成功读取 [152.0.7977.167 DEPS](https://github.com/chromium/chromium/blob/152.0.7977.167/DEPS)：FFmpeg 为 `2b68d2babae73714846961fb0ee47e3b3d2e39a9`。Electron 的 [FFmpeg 补丁清单](https://github.com/electron/electron/blob/v44.9.0/patches/ffmpeg/.patches) 只有 `link_with_loader_path.patch`，所读补丁仅改 macOS 的链接路径条件分支。后续已从官方修订归档地址实际取得 18820712 字节源码，11339 项目录可读，SHA256 `b2efa6554ccfd49303794a6fc4da0e53882ccd656bf514d890fdc8a4222b6877`；源码、补丁与已读配置已在本地材料包，仍未证明当前 DLL 对应或完整重建成功。本次没有重试任何被拒 artifact 通道。已备的 OpenSSL 文件只是原 Apache 许可文本，不能替代具体版权/NOTICE 或声称所有原生署名已补齐。

## 权利人实际需要决定什么

无须为了创建 GitHub Release 被迫选一个开源许可证；[GitHub 官方说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) 也明确没有此义务。这里需要决定的是拟分发的 LGPL 组合作品自身的许可条件，不是点击“接受所有第三方协议”。

最小可评审选择有两个，均 **未采纳、未生效**：

| 选项 | 权利范围和影响 |
| --- | --- |
| 仅授予本次预发布所需的有限使用/修改权 | 对权利人有权授权的 Easy-AI 部分，允许接收者下载、安装、运行、为本人使用复制和修改/重建，并允许为调试这些修改进行逆向工程；明确不限制第三方许可证已经授予的权利。不据此授予项目的一般转售或再分发权。这可保留不开源整个项目的选择，但还必须实际提供 LGPL 对应源码/重建材料 |
| 权利人另行选择完整项目许可证，例如 MIT | 授予更广的项目复制、修改、再分发等权利；须确认覆盖所拥有代码/素材，第三方仍保留原许可。不是解决 Paramiko/FFmpeg 源码缺失或 Microsoft DLL 来源问题的替代手段 |

有限许可的评审文本放在 [SOURCE-DELIVERY 草稿](release-drafts/SOURCE-DELIVERY.draft.md)，不得把草稿复制为已生效条款。既有“把 Release 做好”授权不能推导为已选 MIT、GPL 或已作长期源码承诺。

## 可直接完成与仍待事实的边界

已准备：核查说明、显著 notices 草稿、源码交付清单、原版第三方许可副本及可核对的哈希。所有文件只在 `docs/`，不进入当前冻结候选，不修改 main 或现有包装流程。

后续真实材料增量：已在本环境单独准备 21989315 字节源码材料 ZIP，SHA256 `8b1984dbcaaac226db9228bdeee8aa02eea637e5c76d236229559327b3accd91`，18 文件，含完整 Paramiko/FFmpeg/精确 Easy-AI 源码归档、补丁、配置、六份原许可及重建评审说明。归档 CRC、内容清单/哈希核对通过；没有安装、执行源码、训练、重建产品或公开上传。精确候选源码归档为 1353982 字节/SHA256 `c71d044125c3f3bc9d4049ceffb2fe602031a68adca4cf4415ff5e93fc394ca0`。本地路径和源清单见证据 JSON，不能据此承诺另一环境可访问或把“本地已备”写成“已发布提供”。

README 单点收尾已另经正常 [PR #2](https://github.com/T1doo/Easy-AI/pull/2) 合入 main `68b834680bb0e824dda34a8d2f9a003512dfe90e`。合并差异严格只有 README 一个空格；GitHub 实际 main 渲染通过，除 README 外全部受跟踪文件与已绿 `1e427fb…` 一致，原方案哈希不变。该 PR 没有包含本许可材料，文档 CI 明确跳过，未将旧 CI 改记为新 SHA 通过。

本轮文档检查已核对 JSON、相对链接、原方案哈希、输入与目标 main 的逐字节一致性，以及六份原文的来源/哈希。新写说明与 JSON 的 whitespace 检查通过；全量 diff 检查会报告原版 PyInstaller COPYING 三处行尾空格、Paramiko 一处行尾空格及原始末尾空行，均与所读原文/历史包完全一致，刻意保留原字节，不能把全量 `diff --check` 报为通过。没有运行产品测试或构建。

待落实：当前 Windows 包字节；精确包内归属/原生闭包；已备源码的实际发布及完整可重建/替换材料验证；Microsoft DLL 分发来源依据；权利人选择的最小自身许可。没有新增“必须律师签字”等代理门槛，也没有把全部事项写成需要用户接受。

如果只是附加说明、原 notices、源码与使用授权，可以作为已核验原二进制旁的 Release 附件交付，无须为修改正文重建产品；必须准确写明哪些材料在包外，不能宣称已嵌入旧 ZIP。若发现必须修改冻结布局/运行中版权展示或替换原生输入，则需要有意义的新构建和审计，当前任务不执行。
