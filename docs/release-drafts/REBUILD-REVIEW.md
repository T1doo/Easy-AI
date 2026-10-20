# 已准备的源码材料与重建说明

这是本地准备完成的源码材料，不是已发布附件，不授予 Easy-AI 新许可，也不是三年源码提供承诺。精确 Windows 二进制仍未取得；不能据此宣称成品许可审核或完整重建验证通过。

实际已有：锁定的 Paramiko 4.0.0 完整 sdist、精确 Easy-AI 候选源码、固定上游修订的 FFmpeg 完整源码、Electron FFmpeg 补丁清单/补丁、Electron GN 参数、FFmpeg Chrome/win/x64 config.h，以及第三方许可原文。字节与 SHA256 见 SOURCE_MATERIALS.json/SHA256SUMS。

二进制候选来源仍为 `1e427fb49e444f7feea451cbffd4353e8e969bed`。main 的 README 修复合并提交为 `68b834680bb0e824dda34a8d2f9a003512dfe90e`；除 README 一个空格外，所有受跟踪文件与候选源码一致。两者不能在 provenance 中混称。

## 可评审的修改 Paramiko 重建路径（本轮未执行）

1. 在用户自己的独立工作目录解包 Easy-AI 源码，初始化独立 Git 仓库并记录所用原源码 SHA；不要修改原发布包或教师环境。源码归档不含 `.git`，构建入口要求干净、已提交的工作树。
2. 将完整 Paramiko 源码置于此独立仓库内，例如 `vendor/paramiko`，在该副本修改库。保留其原版权/许可及修改记录，不只修改一个既有 `.venv`：打包入口会新建环境并按锁还原依赖。
3. 在独立副本的 `services/backend/pyproject.toml` 配置 uv 的本地来源，例如 `[tool.uv.sources]` 下 `paramiko = { path = "../../vendor/paramiko" }`；路径必须位于被跟踪的源码树内。重新生成该副本的 uv.lock 并检查其确实指向修改后的源码，准备所需缓存和构建工具；原发布锁不覆盖或伪造。这里是修改版的重建路径，不声称原候选已使用本地库。
4. 在有相应依赖/缓存的 Windows x64 构建环境按已有项目入口准备 Node 24.19.0、pnpm 11.25.0、uv 0.12.23、CPython 3.11.9，并执行 pnpm 的冻结安装、setup。Windows 打包入口还要求有效的 PNPM_HOME（应指向包含该 pnpm JS 入口的目录）。依赖获取和本地库构建需求须由重建者核对；本轮没有为此安装、联网恢复环境或运行命令。
5. 将修改后的库、来源配置和新锁正常提交到独立 Git 仓库，保留干净工作树。使用 `node scripts/build-candidate.mjs` 的正常构建流程，使新源码快照、新应用环境、新 sidecar、ASAR 和清单由构建器重新生成。使用修改版自己的真实提交身份，不能把它伪装成原 SHA，也不能关闭 sandbox、身份、哈希或 manifest 校验。
6. 核对修改版 PYZ/产物确实采用修改库，并实际启动验证；此步骤本轮 NOT RUN。本文给出与当前构建入口相符的可评审步骤，不能替代该实测或证明所有工具/许可条件已经齐备。

## FFmpeg 材料边界

源码归档对应 Chromium 的 FFmpeg 修订 `2b68d2babae73714846961fb0ee47e3b3d2e39a9`。Electron 44.9.0 的 FFmpeg 补丁清单只有 link_with_loader_path.patch；补丁修改 macOS 条件下的链接路径。Chrome/win/x64/config.h 已从同一归档读取，CONFIG_GPL、CONFIG_NONFREE、CONFIG_VERSION3 均为 0。

这已经准备了源码、已知补丁和对应平台配置。尚未验证实际发布 DLL 与这些材料的对应关系，也未准备/验证完整 Chromium/Electron 工具链闭包及兼容 DLL 替换。不得把上游配置检查写成当前二进制验证通过。

## 尚未生效的事项

权利人仍需决定 Easy-AI 自有部分的最小使用/修改/调试逆向权限或其他所选许可；这里未作任何选择。Microsoft DLL 的适用分发来源依据、精确原生 notices 闭包、当前二进制取得和重建/替换实测仍未完成。所有 legalReviewComplete/distributionReady 标志保持 false。

归档仅含受跟踪项目源码和官方第三方源码/许可；没有用户环境、训练数据、权重或真实账号凭据。上游源码中的公开测试素材仍按上游许可保留。当前没有上传 GitHub Release。
