# SteamOS Proton 适配说明

## 配置

将仓库放在 `<installation>/project`，启动器即可推断安装根目录；也可以在操作前传入 `--root /absolute/path`。根目录必须是真实目录，不能是符号链接。源码没有固定用户名、Steam 位置、SD 卡标签或设备地址。

启动器从当前用户的主目录查找 Steam，包括常见的 `.local/share/Steam` 和 `.steam` 路径。Proton 发现逻辑读取 `steamapps/libraryfolders.vdf`，包含外部库，并选择已安装的最新稳定版官方 Proton。使用自定义工具时，请明确指定路径。

```sh
./scripts/uu-steamos --root "/storage/UURemote" \
  --steam "/home/current-user/.local/share/Steam" \
  --proton "/storage/SteamLibrary/steamapps/common/Proton 11.0/proton" \
  --resolution 1280x800 --monitor 0 --rdp-port 3399 --private-display 20 setup
```

设置保存在安装目录内的 `config/settings.json`，后续启动会复用。修改桌面或画布设置时，先停止会话，再向 `start` 传入新选项，最后执行 `open`。支持的画布预设为 1280x800、1280x720、1920x1080、2560x1440 和 3840x2160，目前仅默认的 1280x800 单显示器配置经过实际验收。

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

GStreamer 强制使用共享内存 BGRx 帧，并将注册表缓存保存在安装目录内。采集画布无窗口装饰，铺满私有显示。输入使用 gamescope 现有的虚拟输入席位，对带黑边的窗口进行居中坐标映射，并采用与桌面模式相同、已经验收的 UU 滚轮方向。原生光标形状跟随获得焦点的 Xwayland 显示，同时兼容保留旧热点的微小透明光标。

原生 Steam 快捷方式无需指定兼容性工具。`open` 将 Steam AppId 和分配的显示传给独立运行的会话管理进程，由其为 UU 显示窗口设置 `STEAM_GAME` 标记。

游戏模式使用安装根目录内的 Xephyr、Openbox 和 xcompmgr 管理 UU 的原生 X 窗口。管理界面、完整的远端设备桌面窗口及其菜单共用一个宿主 Xwayland 显示窗口，保留正常的工具包窗口层级、透明度渲染和输入坐标。这是直接显示的嵌套 X 环境，不使用 VNC 服务端、VNC 客户端或额外 Wine 运行时。显示尺寸与配置的采集分辨率一致，认证文件、套接字、日志和运行文件均位于安装根目录内。

UU 中缺少归属信息的 Qt 工具菜单，会关联到同一个已验证 UU 进程中可见的全屏远控窗口，让 Openbox 正确排列悬浮菜单和子菜单的层级。已有窗口归属、普通窗口、坐标和透明度渲染保持原样；远控窗口退出全屏或关闭后，移除补充的归属关系。

真实客户端和管理窗口存在时，前台快捷方式继续运行；窗口关闭后，快捷方式退出。真实管理窗口关闭时，嵌套显示也会隐藏，避免 Steam 留下空白应用窗口；再次打开时重新显示。

残留的 Wine 桌面窗口不能代替真实 UU 客户端。由于 UU 会修改进程标题，启动器通过已映射的 PE 文件和安装 prefix 识别客户端。后台服务属于独立的临时 systemd 用户单元。重新打开快捷方式时，调用 UU 的单实例入口恢复真实界面或重新创建窗口，保留账号和后台服务。若切换了会话类型，后续 `open` 会自动替换旧会话的后台服务。

参考：[gamescope PipeWire 实现](https://github.com/ValveSoftware/gamescope/blob/3.16.23/src/pipewire.cpp)、[gamescope 输入模拟](https://github.com/ValveSoftware/gamescope/blob/3.16.23/src/InputEmulation.cpp)、[libei 发送端 API](https://libinput.pages.freedesktop.org/libei/api/group__libei-sender.html)、[gamescope 窗口选择逻辑](https://github.com/ValveSoftware/gamescope/blob/3.16.23/src/steamcompmgr.cpp)。

管理界面通过 `explorer /desktop=root` 启动，使其 X 窗口 ID 与后台私有桌面分离，同时在同一个 prefix 内共享账号数据。不使用 TigerVNC 客户端。光标桥接保留原生图像尺寸、形状、透明度和热点，并在形状更新时保留近期光标句柄。

KRDP 6.4.3 的进程内兼容补丁负责模拟输入代理认证，并修正缺失的鼠标和滚轮 24.8 定点数编码。一个标准滚轮刻度转换为 15 个轴单位，保留已验收的 UU/FreeRDP 滚动方向。补丁只影响 KRDP；启动器会拒绝未经审核的 KRDP 版本，避免未来上游修复后再次重复放大坐标。

协议参考：[KRDP Plasma 会话实现](https://github.com/KDE/krdp/blob/Plasma/6.4/src/PlasmaScreencastV1Session.cpp)、[KWin 模拟输入后端](https://github.com/KDE/kwin/blob/Plasma/6.4/src/backends/fakeinput/fakeinputbackend.cpp)。

## 清理和重新构建

运行 `prune` 前先停止会话。清理会保留 prefix 和账号、配置、证书、源码、必要的兼容程序、精简 Xvfb/Openbox 等运行工具，以及选定的 Proton 元数据；删除安装包归档、本机和交叉编译器、废弃 VNC 工具、诊断图片和日志、缓存及临时状态。应用无需重新构建即可再次启动。需要重建时，`setup` 会重新下载经过审核的构建工具。

安装过程和运行中的会话管理进程持有当前 prefix 专属的锁。启动第二个管理进程不会终止已有 prefix；停止操作通过控制套接字或经过验证的 PID 和进程启动时间记录执行。`open` 在使用控制套接字前检查实时 ping，失效的会话会重新启动。控制客户端断开不会终止转发服务。

桌面启动器将日志写入 `logs/launcher.log`，启动失败时显示错误对话框。其他日志位于 `logs`；`screenshot` 将图片保存为 `logs/relay.png`。常规启动器不会启用详细跟踪日志。

## 验收记录和限制

2026-10-08，用户验证了登录、手机端桌面画面、UU 管理窗口内外的点击、悬停、键盘，以及与本机一致的光标尺寸和形状。KRDP 修正后，也验证了 Mac 控制端的滚动，以及关闭自然滚动时对应的滚动方向。

这些结果对应被测 SteamDeck 上的 SteamOS 3.8.28、Plasma/KRDP 6.4.3、Proton 11.0 和 UU 4.42.0.2770，其他设备和版本仍需各自验收。

`status: ready` 仅证明本机启动和注入成功，不代表真实远程连接可用。游戏模式在 gamescope 3.16.23.6、PipeWire 1.6.8 和 libei 1.4.1 下进行了本机验证，包括实际合成画面、通过 Steam 快捷方式启动、关闭管理窗口后保持同一后台进程，以及重新创建管理窗口。

随后用户验证了游戏模式的远程画面和输入、Mac 关闭自然滚动时修正后的滚动方向，以及关闭并重新打开 Steam 快捷方式时不再黑屏。管理窗口关闭和重开期间，后台服务保持运行。这些结果仅适用于被测 SteamDeck。

用户还验证了游戏模式下嵌套 X 显示中的完整“进入桌面”远控窗口，以及关闭并重开后显示的网络状态浮窗。实际抓图中能同时看到设备桌面和控制中心菜单。直接改变 Qt 工具窗口父窗口的方案已弃用，因为它破坏了点击坐标和透明度更新。

Steam Input 的虚拟 Xbox 手柄通过现有 `/dev/input` 目录开放给 Proton。Proton 11.0 使用 evdev HID 总线处理该设备；本分支不会接管物理手柄，也不会创建额外虚拟手柄驱动。修正后，Windows 手柄面板识别到 `Controller (XBOX 360 For Windows)`，用户随后验证了摇杆、十字键和按键能够传入远端设备。

远端浏览器中的震动仍未验证：测试网页未从接收端 Windows 设备获取到 `vibrationActuator`，不能据此确认 UU 震动回传链路是否可用。本机小型 XInput 诊断程序调用 `XInputGetCapabilities` 和 `XInputSetState` 均返回成功，电机能力值非零；实际震动仍需用户确认，API 调用成功不能证明 SteamDeck 已经震动。

原生 Wayland 游戏和锁定鼠标指针的游戏仍需验证，绝对坐标式桌面鼠标控制无法表达所有游戏的相对输入。音频已禁用。剪贴板、文件传输、远程终端、多显示器和其他画布尺寸尚未完成验证，也不属于本分支已支持的产品功能。
