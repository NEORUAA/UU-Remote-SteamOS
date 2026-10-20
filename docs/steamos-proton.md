# SteamOS Proton 适配说明

本分支面向 SteamOS 的 Plasma 桌面模式和 gamescope 游戏模式，支持远程控制 SteamDeck，也支持在 SteamDeck 上控制其他设备。运行环境为 SteamOS 3.8.28、KRDP/Plasma 6.4.3、Proton 11.0 和 UU 远程 4.42.0.2770。

兼容补丁按完整文件 SHA-256 匹配。目前支持清单中的两种 Proton 11.0 构建，包括仅更新时间戳与 PE 校验和的重建版本；仅有相同的 Proton 版本号还不足以匹配。具体哈希见 [视频兼容清单](../patches/steamos-video.json)，KRDP 输入修正仅适用于 6.4.3。

请勿在 UU 内直接自更新。新版 UU 或未列入清单的 Proton 文件需要对应的兼容补丁，启动器会拒绝修改未知文件。升级 Steam 的 Proton 后，若出现 `Unreviewed Proton`，请使用支持当前构建的项目版本。

## 配置

将仓库放在 `<installation>/project`，启动器即可推断安装根目录；也可以在操作前传入 `--root /absolute/path`。根目录必须是真实目录，不能是符号链接。源码没有固定用户名、Steam 位置、SD 卡标签或设备地址。

启动器从当前用户的主目录查找 Steam，包括常见的 `.local/share/Steam` 和 `.steam` 路径。Proton 发现逻辑读取 `steamapps/libraryfolders.vdf`，包含外部库，并选择已安装的最新稳定版官方 Proton。使用 `--proton` 可以固定到受支持的 Proton 11.0 路径。

```sh
./scripts/uu-steamos --root "/storage/UURemote" \
  --steam "/home/current-user/.local/share/Steam" \
  --proton "/storage/SteamLibrary/steamapps/common/Proton 11.0/proton" \
  --resolution 1280x800 --monitor 0 --rdp-port 3399 --private-display 20 setup
```

设置保存在安装目录内的 `config/settings.json`，后续启动会复用。修改桌面或画布设置时，先停止会话，再向 `start` 传入新选项，最后执行 `open`。默认使用 1280x800 单显示器配置；命令行也提供 1280x720、1920x1080、2560x1440 和 3840x2160 画布预设，其他尺寸暂不纳入支持范围。

RDP 始终仅监听回环地址，其端口和私有 X 显示编号均可配置，以避免与其他软件冲突。

Proton 启动器元数据复制到 `tools/proton-*`；大型 `files` 目录仍通过只读符号链接指向 Steam。prefix、安装包、下载文件、构建工具、缓存和临时文件都位于安装根目录内。

Bubblewrap 将宿主文件系统挂载为只读，同时开放 GPU、现有输入设备目录（包括 Steam Input 热插拔的虚拟手柄）和现有桌面套接字。Wine 客户端共享宿主 PID 命名空间，因为同一个 wineserver 会在客户端间传递 Unix PID。子进程禁用核心转储。

本项目不会安装独立 Wine 或 pacman 软件包，不会解锁系统镜像，也不会创建持久服务、自动启动项或安装目录外的应用菜单文件。桌面启动器保存在安装根目录内。启动时创建临时 systemd 用户单元，让后台服务在 SSH 断开后继续运行；日志保存在安装目录内，不安装单元文件。运行期间请保持所选桌面或 gamescope 会话处于活动状态。

## 运行架构

```text
Plasma -> KRDP (loopback TLS) -> FreeRDP in private Xvfb -> Proton UU -> controller
controller -> UU input broker -> native XTEST -> FreeRDP -> Plasma
local user -> native Proton UU manager on host Xwayland
native RDP cursor -> CUR image -> UU cursor reader in Proton

gamescope -> PipeWire BGRx -> GStreamer in private Xvfb -> Proton UU -> controller
controller -> UU input broker -> native XTEST -> XInput2 -> libei -> gamescope
Steam shortcut -> native launcher -> manager window tagged with its Steam AppId
```

图中的 `controller` 指手机或电脑上的 UU 控制端。

游戏模式读取生成的 `gamescope-environment` 会话元数据，复用现有 Wayland、PipeWire、EIS 和 Xwayland 套接字。它不会启动嵌套 gamescope，运行时不需要 KRDP、额外 Wine 发行版或编译器。

GStreamer 强制使用共享内存 BGRx 帧，并将注册表缓存保存在安装目录内。采集画布无窗口装饰，铺满私有显示。输入使用 gamescope 现有的虚拟输入席位，对带黑边的窗口进行居中坐标映射，并采用与桌面模式相同的 UU 滚轮方向。原生光标形状跟随获得焦点的 Xwayland 显示，同时兼容保留旧热点的微小透明光标。

原生 Steam 快捷方式无需指定兼容性工具。`open` 将 Steam AppId 和分配的显示传给独立运行的会话管理进程，由其为 UU 显示窗口设置 `STEAM_GAME` 标记。

游戏模式使用 SteamOS 自带的 KWin 和 Xwayland 管理 UU 的原生 X 窗口，支持通过 DRI3 使用显卡硬件加速。管理界面、完整的远端设备桌面窗口及其菜单共用一个宿主 Xwayland 显示窗口，保留正常的工具包窗口层级、透明度渲染和输入坐标。启动器根据 KWin 子进程实际分配的显示编号连接，不固定额外的 X 显示地址。显示尺寸与配置的采集分辨率一致，私有 D-Bus 套接字、配置、缓存、日志和运行文件均位于安装根目录内。

UU 中缺少归属信息的 Qt 工具菜单，会关联到同一个 UU 进程中可见的全屏远控窗口，让窗口管理器正确排列悬浮菜单和子菜单的层级。已有窗口归属、普通窗口、坐标和透明度渲染保持原样；远控窗口退出全屏或关闭后，移除补充的归属关系。

真实客户端和管理窗口存在时，前台快捷方式继续运行；窗口关闭后，快捷方式退出。真实管理窗口关闭时，嵌套显示也会隐藏，避免 Steam 留下空白应用窗口；再次打开时重新显示。

残留的 Wine 桌面窗口不能代替真实 UU 客户端。由于 UU 会修改进程标题，启动器通过已映射的 PE 文件和安装 prefix 识别客户端。后台服务属于独立的临时 systemd 用户单元。重新打开快捷方式时，调用 UU 的单实例入口恢复真实界面或重新创建窗口，保留账号和后台服务。若切换了会话类型，后续 `open` 会自动替换旧会话的后台服务。

参考：[gamescope PipeWire 实现](https://github.com/ValveSoftware/gamescope/blob/3.16.23/src/pipewire.cpp)、[gamescope 输入模拟](https://github.com/ValveSoftware/gamescope/blob/3.16.23/src/InputEmulation.cpp)、[libei 发送端 API](https://libinput.pages.freedesktop.org/libei/api/group__libei-sender.html)、[gamescope 窗口选择逻辑](https://github.com/ValveSoftware/gamescope/blob/3.16.23/src/steamcompmgr.cpp)。

管理界面通过 `explorer /desktop=root` 启动，使其 X 窗口 ID 与后台私有桌面分离，同时在同一个 prefix 内共享账号数据。不使用 TigerVNC 客户端。光标桥接保留原生图像尺寸、形状、透明度和热点，并在形状更新时保留近期光标句柄。

KRDP 6.4.3 的进程内兼容补丁负责模拟输入代理认证，并修正缺失的鼠标和滚轮 24.8 定点数编码。一个标准滚轮刻度转换为 15 个轴单位，保持 UU/FreeRDP 的滚动方向。补丁只影响 KRDP；启动器会拒绝未经审核的 KRDP 版本，避免未来上游修复后再次重复放大坐标。

协议参考：[KRDP Plasma 会话实现](https://github.com/KDE/krdp/blob/Plasma/6.4/src/PlasmaScreencastV1Session.cpp)、[KWin 模拟输入后端](https://github.com/KDE/kwin/blob/Plasma/6.4/src/backends/fakeinput/fakeinputbackend.cpp)。

## 清理和重新构建

运行 `prune` 前先停止会话。清理会保留 prefix 和账号、配置、证书、源码、必要的兼容程序、精简 Xvfb/Openbox 等运行工具，以及选定的 Proton 元数据；删除安装包归档、本机和交叉编译器、废弃 VNC 工具、诊断图片和日志、缓存及临时状态。应用无需重新构建即可再次启动。需要重建时，`setup` 会重新下载经过审核的构建工具。

安装过程和运行中的会话管理进程持有当前 prefix 专属的锁。启动第二个管理进程不会终止已有 prefix；停止操作通过控制套接字或经过验证的 PID 和进程启动时间记录执行。`open` 在使用控制套接字前检查实时 ping，失效的会话会重新启动。控制客户端断开不会终止转发服务。

桌面启动器将日志写入 `logs/launcher.log`，启动失败时显示错误对话框。其他日志位于 `logs`；`screenshot` 将图片保存为 `logs/relay.png`。常规启动器不会启用详细跟踪日志。

## 视频解码与帧率

桌面模式与 gamescope 模式均支持 60 fps 远端桌面串流。启动器从宿主 `xrandr --current` 的活动模式读取刷新率，四舍五入为 Windows 使用的整数值，修正 Wine 显示模式报告 0 Hz 时导致的默认 30 帧限制。UU 的显示枚举和用户帧率设置仍由原逻辑处理，不依赖固定的 60 Hz；实际接收帧率可在 UU 网络状态中查看。

H.264 硬件解码通过 DX11VA 使用系统 RADV 的 Vulkan 视频解码能力。UU 界面采用桌面 OpenGL，视频解码使用 Vulkan，避免两个后端互相影响。[视频准备程序](../scripts/uu_steamos_video.py) 按清单校验完整文件，在安装目录内生成两个兼容 DLL 副本，不修改 Steam 安装的 Proton。

兼容副本补齐 H.264/NV12 格式与配置查询，并将 NV12 平面元数据调整为 UU 使用的 UNORM 视图，修正绿屏。UU 的独立探测器与实际解码初始化代码使用非共享纹理路径，渲染器复用解码器的设备。补丁保留 PE 异常展开信息；未知版本或已有非本项目管理的应用 DLL 会被拒绝修改。当前硬解适配范围为 H.264/NV12，不包含 H.265、HDR 或 4:4:4。

## 手柄与功能范围

Steam Input 的虚拟 Xbox 手柄通过现有 `/dev/input` 目录开放给 Proton。Proton 11.0 使用 evdev HID 总线处理该设备，以 `Controller (XBOX 360 For Windows)` 提供摇杆、十字键和按键输入。本分支不接管物理手柄，也不创建额外虚拟手柄驱动。

手柄震动回传的可用性仍不确定，远端浏览器可能显示 `n/a`。当前不将震动列为支持功能。

默认鼠标控制使用绝对坐标。原生 Wayland 游戏，以及需要锁定指针或相对鼠标输入的游戏，暂不纳入支持范围。

音频转发已禁用。本分支不支持剪贴板、文件传输、远程终端和多显示器。`status` 中的 `ready` 表示后台服务和输入桥已启动，远程设备的连接状态可在 UU 界面查看。
