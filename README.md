# UU Remote SteamOS

让 SteamDeck 在桌面模式和游戏模式下运行网易 UU 远程，复用 Steam 自带的 **Proton**，无需另装 Wine。

你可以从手机或电脑远控 SteamDeck，也可以在 Deck 上连接其他设备。支持 H.264 硬件解码、60 fps 串流，以及鼠标、键盘、滚轮和 Steam Input 手柄。关闭 UU 管理窗口后，远程服务继续在后台运行，再次打开快捷方式即可唤起窗口。

本项目是 [UU Remote Ubuntu Plus](https://github.com/llmir/uu-remote-ubuntu-plus) 的 SteamOS 专用分支，上游基于 [UU Remote Ubuntu Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)。

## 运行要求

| 组件 | 当前适配范围 |
| --- | --- |
| 系统 | x86-64 SteamOS，Plasma Wayland 桌面模式或 gamescope 游戏模式 |
| SteamOS / Plasma | SteamOS 3.8.28 / Plasma 6.4.3 |
| 兼容层 | Steam 安装的官方 Proton 11.0，限兼容清单中的构建 |
| UU 远程 | 4.42.0.2770 |
| 桌面转发 | 系统自带的 KRDP 6.4.3 和 FreeRDP |
| 游戏模式转发 | 系统自带的 KWin/Xwayland、GStreamer/PipeWire 和 libei |

启动器会自动查找 Steam 库中的 Proton，并根据当前会话选择桌面或游戏模式。硬解兼容文件按完整哈希匹配，支持的 Proton 11 构建见 [视频兼容清单](patches/steamos-video.json)。

## 安装

在 Steam 中安装 Proton 11.0，然后进入桌面模式，打开终端：

```sh
install_root="$HOME/.local/share/uu-remote-steamos"
mkdir -p "$install_root"
git clone https://github.com/NEORUAA/UU-Remote-SteamOS.git "$install_root/project"
cd "$install_root/project"
./scripts/uu-steamos doctor
./install.sh
./scripts/uu-steamos open
```

也可以将 `install_root` 换成内置存储或 SD 卡上的其他真实目录。仓库放在安装目录的 `project` 子目录中时，启动器会自动识别位置。若仓库另行存放，使用 `./install.sh --root "/path/to/UURemote"` 安装，运行命令也传入同一个 `--root`。

安装包、工具链、Proton 环境、缓存和日志都保存在安装目录中。Steam 已安装的 Proton 运行时直接复用，项目不会修改其文件或安装系统软件包。

安装完成后，打开安装目录中的 `UU Remote.desktop`，登录 UU 账号即可使用。安装在 SD 卡上时，启动前需要先挂载该卡。

## 在游戏模式中使用

将安装目录中的 `UU Remote.desktop` 添加为非 Steam 应用，并检查快捷方式：

- **目标**：安装目录内的 `project/scripts/uu-steamos`，填写完整路径。
- **起始位置**：安装根目录。
- **启动选项**：`--root "/path/to/UURemote" open`，替换为实际路径。
- **兼容性**：不要勾选“强制使用特定 Steam Play 兼容性工具”。启动器会自行调用 Proton。

从 Steam 启动后，可以使用 UU 设备列表、完整远控窗口及菜单。关闭 UU 窗口后，快捷方式恢复为可启动状态，后台服务继续运行。再次启动即可重新打开界面。

Steam 的“停止”按钮结束前台快捷方式。要同时停止远程后台，请运行 `./scripts/uu-steamos stop`。

## 日常使用

在仓库目录中运行：

| 命令 | 用途 |
| --- | --- |
| `./scripts/uu-steamos open` | 启动后台并打开管理窗口 |
| `./scripts/uu-steamos start` | 仅启动后台 |
| `./scripts/uu-steamos status` | 查看运行状态 |
| `./scripts/uu-steamos stop` | 停止后台 |
| `./scripts/uu-steamos prune` | 停止后清理下载、编译器、缓存和诊断文件 |

`prune` 会保留账号、配置和运行所需组件，清理后仍可直接启动。卸载时，先停止后台，再删除安装目录。项目不会添加开机自启或持久系统服务。

## 更新与启动问题

更新本项目时，先停止后台，再更新源码：

```sh
./scripts/uu-steamos stop
git pull --ff-only
./scripts/uu-steamos open
```

当前适配的 UU 版本为 **4.42.0.2770**。UU 应用内自更新不会自动迁移本项目的兼容补丁，升级 UU 前请先查看本项目支持的版本。

Steam 更新 Proton 后，如果启动提示 `Unreviewed Proton ...`，先更新本项目，让启动器重新生成兼容文件。若仍提示不支持，请在 [Issues](https://github.com/NEORUAA/UU-Remote-SteamOS/issues) 中提供 SteamOS、Proton 和 UU 版本，以及安装目录 `logs/session.log` 中的错误信息。提交日志前请去掉账号和设备标识。

## 功能范围

- H.264 硬解和 60 fps 串流；实际帧率还取决于远端设备和网络。启动器会读取主机刷新率，修正 Wine 显示模式报告 0 Hz 时的 30 帧限制。
- 桌面模式转发当前 Plasma 桌面，游戏模式转发 gamescope 合成后的画面，包括 Steam 界面和当前获得焦点的游戏。
- 支持鼠标、键盘、光标形状和大小、滚轮方向，以及 Steam Input 手柄输入。手柄震动暂不作为支持功能。
- 音频转发已关闭，剪贴板、文件传输、远程终端和多显示器暂不支持。

配置和运行架构见 [SteamOS 适配说明](docs/steamos-proton.md)，开发与测试方法见 [贡献指南](CONTRIBUTING.md)。

本项目采用 MIT 许可证。UU 远程软件本身遵循网易的许可条款。
