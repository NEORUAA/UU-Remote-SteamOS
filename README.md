# SteamOS 版 UU 远程

使用 Steam 已安装的 **Proton**，在 **SteamOS 桌面模式和游戏模式**下运行网易 UU 远程。启动器会自动识别 Plasma 或 gamescope 会话，并通过 Proton 显示 UU 管理窗口。远程画面和输入使用当前会话；关闭管理窗口后，远程服务仍会在后台运行。

本项目是 [UU Remote Ubuntu Plus](https://github.com/llmir/uu-remote-ubuntu-plus) 的 SteamOS 专用分支，上游基于 [Lachlan Chen 的 UU Remote Ubuntu Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)。本分支已移除 Ubuntu/GNOME 安装器、用户服务、TigerVNC 管理窗口，以及无关的剪贴板、终端和原生采集实验功能，保留原项目的 MIT 许可证及可复用的 UU 补丁和输入代码。

## 安装

需要 x86-64 SteamOS、正在运行的 Plasma Wayland 或 gamescope 会话，以及已安装官方 Proton 的 Steam。桌面模式使用 SteamOS 自带的 KRDP/FreeRDP；游戏模式使用系统的 GStreamer/PipeWire 和 libei 库。

已验证的组合为 SteamOS 3.8.28、KRDP/Plasma 6.4.3、Proton 11.0 和 UU 远程 4.42.0.2770。目前 KRDP 兼容补丁仅适用于 6.4.3，其他版本需要先审核，再启用协议修正。

在内置存储或 SD 卡上选择一个可写的真实目录，将仓库放在其 `project` 子目录中，启动器即可自动推断安装根目录：

```sh
install_root="/absolute/path/to/UURemote"
mkdir -p "$install_root"
# Copy this checkout into "$install_root/project", then:
cd "$install_root/project"
./scripts/uu-steamos doctor
./install.sh
./scripts/uu-steamos open
```

也可以将仓库放在其他位置，并在每个操作前传入 `--root "$install_root"`，安装命令同样使用 `./install.sh --root "$install_root"`。默认安装根目录为当前用户的 `~/.local/share/uu-remote-steamos`。

启动器没有硬编码用户名、设备 IP、SD 卡标签或 Steam 库路径。它会从 Steam 库列表中查找已安装的 Proton，并将选定路径保存在安装目录内的 `config/settings.json`。

`setup` 会将固定版本的工具下载到安装目录内，并编译辅助程序，不会安装系统软件包或独立 Wine。安装包、构建工具、兼容层数据、缓存和日志均保存在安装根目录中。Steam 自带的大型 Proton 运行时直接复用，不会复制一份。

打开安装目录中的 `UU Remote.desktop`，即可启动后台服务并显示 UU 管理窗口。登录后，从手机或电脑上的 UU 控制端连接。重新安装和清理会保留现有账号数据。

在游戏模式中，将 `UU Remote.desktop` 添加为非 Steam 应用。目标为原生可执行脚本 `scripts/uu-steamos`，启动选项为 `--root "/absolute/path/to/UURemote" open`。**不要勾选“强制使用特定 Steam Play 兼容性工具”**：启动器内部会选择已安装的 Proton，Steam 不应再通过 Proton 运行这个 Python 启动器。

关闭 UU 窗口后，Steam 快捷方式会恢复为可启动状态，UU 远程后台继续运行。再次启动即可唤起管理窗口。Steam 的“停止”按钮结束前台快捷方式；要停止后台服务，请使用 `uu-steamos stop`。

## 使用和清理

```sh
./scripts/uu-steamos start     # Backend only
./scripts/uu-steamos open      # Start and show the native UU manager
./scripts/uu-steamos status
./scripts/uu-steamos stop
./scripts/uu-steamos prune     # Stopped session: remove build tools and diagnostics
./scripts/uu-steamos open      # Runs without compilers or installer downloads
```

- `start`：仅启动后台服务。
- `open`：启动后台服务并显示 UU 管理窗口。
- `status`：查看运行状态。
- `stop`：停止后台服务。
- `prune`：在停止会话后清理构建工具和诊断文件。

执行 `prune` 后，应用无需编译器或安装包即可再次运行；需要重新构建时，`setup` 会重新下载固定版本的工具链。请保留安装目录中的 `project`、`compatdata`、`build/compat`、`tools/runtime`、Proton 元数据、配置和 TLS 密钥。

本项目不会安装持久服务、系统应用菜单项或自动启动文件。启动时使用临时 systemd 用户单元，让后台服务在 SSH 断开后继续运行。卸载时，先停止 UU，再自行删除安装目录。

配置选项、运行架构、验收记录和限制见 [SteamOS 适配说明](docs/steamos-proton.md)。

音频转发已禁用。本分支不支持剪贴板、文件传输、远程终端和多显示器。游戏模式采集 gamescope 合成后的画面，包括 Steam 界面和当前获得焦点的游戏。UU 管理窗口、远端设备桌面窗口及其弹窗归属于现有 Steam 快捷方式的应用 ID。

## 开发

Mac 仓库用于保存源码；安装和实际验收在 SteamOS 上进行。源码测试命令为 `python3 -B -m unittest discover -s tests -v`。实际 Proton 光标加载测试见 [贡献指南](CONTRIBUTING.md)。

UU 远程软件本身遵循网易的许可条款，本项目采用 MIT 许可证。
