[English](../../architecture.md) · [العربية](../ar/architecture.md) · [Español](../es/architecture.md) · [Français](../fr/architecture.md) · [日本語](../ja/architecture.md) · [한국어](../ko/architecture.md) · [Tiếng Việt](../vi/architecture.md) · [中文（简体）](../zh-Hans/architecture.md) · [中文（繁體）](../zh-Hant/architecture.md) · [Deutsch](../de/architecture.md) · [Русский](../ru/architecture.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 架构

![桌面画面通过 SDL 和 UU 到达控制端；键鼠和文字经输入桥返回 Ubuntu。管理窗口使用独立分支。](../../images/architecture-premium-v2-zh-Hans.png)

紫色箭头把 Ubuntu 的画面送往控制端，橙色箭头把键盘、鼠标和文字送回 Ubuntu。底部管理分支在本机显示 UU 自己的窗口，操作返回这些窗口。RDP 服务、输入插件和文字辅助路径见下文。

## 两个桌面，两个方向

UU 的 Windows 主机端运行在独立 Wine 前缀中，Windows 内核输入驱动不能直接控制原生 GNOME。桥接器在私有 X11 显示中提供桌面中继窗口，把 UU 的用户态输入送入选定的 Ubuntu 会话。

已登录的真实桌面与 Wine 画布相互独立。画面从 Ubuntu 经中继传到手机、Mac 或 Windows 控制端；键鼠和已提交的文字沿反方向返回。管理查看器只是 UU 账户与设置的本机窗口，不串联在远程桌面流中。当前源采用 UU 4.42 清单和固定来源的 FreeRDP/SDL 构建；更新保留原有配置。

## 默认设置与可选分支

| 设置 | 新安装默认 | 可选配置 |
| --- | --- | --- |
| 桌面中继 | `rdp` | X11/XRDP 桌面可显式选择 `vnc` |
| 输入路径 | RDP 对应 `rdp-public` | `legacy`；VNC 必须使用它 |
| 目标桌面 | `auto` | `physical`、`xrdp` 或准确的 X display |
| 私有画布 | 1920 × 1080 | 四档 720p、1080p、1440p、4K |
| 跟随桌面分辨率 | `off` | 显式开启 `on` |
| 旧输入分支的物理键路由 | 经中继的 `rdp` | X11 上的 `x11` 或 `auto` |
| 手机文字 | `auto` | `keys` 或 `clipboard` |

[安装器](../../../install.sh#L358)负责新安装默认值。没有已安装输入配置而直接调用[启动器](../../../scripts/uu-remote-bridge#L6)时，回退值是 `legacy`。`rdp-public` 要求 RDP 中继；VNC 要求可访问的 X11/XRDP 桌面，不能代替 Wayland。

[runtime-settings.sh](../../../scripts/runtime-settings.sh)区分新安装与升级时的手机按键节奏。中继选择不改变控制端的编码质量、FPS 或码率上限。

## 画面：Ubuntu 到控制端

![GNOME 画面向 UU 控制端传输，键鼠经 broker 与 FreeRDP 输入插件返回。](../../images/uu-plus-data-flow-zh-Hans.gif)

[静态 PNG](../../images/uu-plus-data-paths-zh-Hans.png) · [可编辑 SVG](../../images/uu-plus-data-paths-zh-Hans.svg) · [矢量动画](../../images/uu-plus-data-paths-animated-zh-Hans.svg) · [中文动图](../../images/uu-plus-data-flow-zh-Hans.gif)

```text
已登录并选定的 GNOME 桌面
  → 对应会话 D-Bus 上的 GNOME Remote Desktop
  → 本机回环 RDP
  → 固定源码构建的 Windows SDL FreeRDP：Ubuntu-Desktop-Relay
  → 私有 X11 画布（rdp-public 只合成绑定的 SDL 窗口）
  → UU GameViewerServer 捕获、编码和传输
  → 手机、macOS 或 Windows UU 控制端
```

启动器发现 GNOME Shell 的 display、会话和 D-Bus；显式指定目标时等待该目标，不替换成其他会话。GNOME RDP 在选定总线上启动，包括 XRDP 的私有总线。FreeRDP 默认连接 `127.0.0.1:3390`，固定 TLS 证书指纹，从标准输入读取 GNOME 凭据。这不是 UU 账户密码。源码见[桌面中继](../../../scripts/uu-remote-bridge#L1010)和[SDL 启动](../../../scripts/uu-remote-bridge#L1758)。

Xvfb 与 Openbox 提供私有画布。Xvfb 使用 Xauthority 和 `-nolisten tcp`，从 `:20` 开始选择空闲 display，或使用经过检查的指定 display。标准 RDP 模式最高 4K，在 Wine 启动前注册四个真实模式，见[显示配置](../../../scripts/uu-remote-bridge#L1437)。

`rdp-public` 下，[uu-manual-plane.py](../../../scripts/uu-manual-plane.py#L155)拥有 XComposite 重定向，只将绑定 SDL 的 pixmap 绘制到私有 root。管理窗口保持 mapped，但不进入这张 root 图像。

可选 VNC 分支为：

```text
选定的 X11 桌面 → 回环 x11vnc → 私有全屏 VNC 查看器
  → UU 捕获和传输 → UU 控制端
```

它使用已独立管理且经过检查的回环 x11vnc，或由桥接器启动自己的服务。查看器适配桌面画面，不改变物理显示器。该分支使用 `legacy` 输入，见[VNC 服务](../../../scripts/uu-remote-bridge#L1040)和[查看器](../../../scripts/uu-remote-bridge#L1844)。

## 普通输入：控制端到 Ubuntu

经过审阅、按版本匹配的 UU 补丁选择已有用户态 `SendInput`，替代 Windows 内核 HID 驱动。[4.42 清单](../../../patches/uu-remote-4.42.0.2770.json)只对应该版本。

```text
控制端键盘、指针、按钮和滚轮
  → GameViewerServer 的 SendInput 导入钩子
  → 本机 broker 命名管道
  → uu-input-broker.exe / uurb_rdp_backend
  → SDL 内 uurb-full-input 的本机命名管道
  → FreeRDP 公共键鼠接口
  → 既有 RDP 连接 → GNOME Remote Desktop → 选定桌面
```

`/dvc:uurb-full-input` 加载插件，但 broker 与插件间使用本机命名管道，不要求新增服务器输入通道。后端绑定会话和几何尺寸，插件在 FreeRDP 事件循环定时器上派发。此路径不靠抢 Wine 窗口焦点，也不会在部分或不明确的投递之后回退重放。源码：[输入钩子](../../../src/uu_input_bridge.c#L688)、[broker](../../../src/uu_input_broker.c#L1081)、[插件](../../../src/plugin.c#L200)、[适配器](../../../src/freerdp-adapter.c#L48)。

`legacy` 对普通数组先尝试 Wine `SendInput`，将未接收的余项交给 broker；Unicode 直接交给 broker。broker 聚焦私有中继，再通过 RDP/VNC 到达 Ubuntu。X11 桌面可选 `--keyboard-route x11` 或 `auto`，经带认证的原生 XTEST 辅助程序注入。注入前辅助程序不可用时可保留中继路径；注入后的不明确失败不会重放。见[旧钩子](../../../src/uu_input_bridge_legacy.c#L595)及[路由选择](../../../src/uu_input_broker.c#L1101)。

## Unicode 文字与复制粘贴

物理键与 IME 已提交文字不是同一种输入。手机 IME 提供 `KEYEVENTF_UNICODE`。`legacy/auto` 将键盘布局可表达的文字转成按键组合；中文、换行、制表符等使用原生文字辅助程序。`rdp-public/auto` 对所有 Unicode 提交采用字面文字，包括 ASCII，避免 Caps Lock 或布局改写内容。显式 `keys` 模式选择按键翻译，见[文字选择](../../../src/uu_input_broker.c#L454)。

语义文字协调两件事：

1. broker 通过认证回环连接发送有上限的文字。`uu-x11-input` 转为 UTF-8，由 `xclip` 在目标 X11/Xwayland 上拥有 `CLIPBOARD` 和 `PRIMARY`，并核实新 owner。
2. `rdp-public` 经插件/RDP 发送 `Shift+Insert`，再检查 owner/selection-request 屏障。旧 RDP 分离路径在源桌面设置选区，只在私有 SDL display 发粘贴组合键；直接 X11 在目标 display 完成两步。

屏障确认有限的选区事务；应用仍须支持粘贴并拥有焦点。见[send_semantic_segment](../../../src/uu_input_broker.c#L641)、[display 选择](../../../scripts/uu-remote-bridge#L1182)、[选区事务](../../../src/uu_x11_input.c#L1000)及[文字和剪贴板](semantic-text-and-clipboard.md)。

普通复制粘贴使用 RDP 的 `cliprdr`，与手机 IME 独立。固定 FreeRDP/SDL 补丁处理远端缓存及 sequence/owner，构建方式见[源码构建](source-build.md)。VNC 另有单向文字辅助路径：

```text
控制端 UU 剪贴板 → GameViewer CF_UNICODETEXT
  → uu-wine-clipboard-bridge → 认证回环辅助程序
  → 目标桌面 CLIPBOARD 和 PRIMARY
```

它以启动 sequence 为基线，读取前后都要求 owner 为 GameViewer；不读取主机剪贴板回传，也不发粘贴键，只在显式 VNC/X11 分支启动。见[启动](../../../scripts/uu-remote-bridge#L1266)、[owner 检查](../../../src/uu_wine_clipboard_bridge.c#L195)、[原生 owner](../../../src/uu_x11_clipboard.c#L329)。

## 本机管理与控制窗口

![私有 UU 管理窗口和关联弹窗通过独立捕获路径进入 GNOME 本机查看器。](../../images/manager-premium-zh-Hans.png)

`uu-remote open` 通过本机 TigerVNC 显示 GameViewer 管理界面。Wine 窗口仍在专用前缀和私有 display 中。

```text
管理窗口及同 owner 的弹窗/模态窗口
  → XComposite pixmap / uu-manager-capture.so
  → 限定窗口的回环 x11vnc → 本机 TigerVNC
本机查看器键鼠 → x11vnc → owner 命中与焦点处理 → 对应 UU 窗口
```

辅助程序合成关联弹窗、重新核实 owner 与几何尺寸。override-redirect 菜单保留焦点/grab，管理窗口内移动指针不会持续抢焦。见[捕获绑定](../../../scripts/uu-remote-console#L1121)、[弹窗关联](../../../src/uu_manager_capture.c#L464)、[输入路由](../../../src/uu_manager_capture.c#L1090)。

`rdp-public` 由合成 owner 将管理窗口排除 root；`legacy` 只重定向自己管理的帧，中继监督继续运行。查看器关闭剪贴板交换和远端改尺寸。session lock 复用已有查看器；关闭后回收 sidecar、移除 session、释放管理焦点标记并恢复中继焦点。UU 窗口保持 mapped，不在 layered-window 替换期间最小化。见[查看器选项](../../../scripts/uu-remote-console#L1193)、[清理](../../../scripts/uu-remote-console#L622)、[焦点释放](../../../scripts/uu-remote-console#L299)。

Ubuntu 控制其他机器时，独立绑定的控制窗口可使用相同捕获方式，属于另一条 UU 控制会话。全 root noVNC 是显式诊断入口，不是常规管理窗口。

## 分辨率、兼容性与生命周期

画布控制改变私有中继，不改变物理显示器。质量选择器保留四档，检查保存值与实际画布，在变更前安排独立恢复。试用失败时恢复配置并按需重启；恢复无法确认时报告失败。固定画布要求关闭分辨率跟随。见[恢复](../../../scripts/uu-quality.py#L329)、[模式注册](../../../scripts/uu-display-modes.py#L166)和[画质指南](quality-guide.md)。

GNOME Remote Desktop 负责 GNOME 集成。Wayland 输入由其系统合成器路径承担；本项目适配器调用 FreeRDP，不直接调用 libei。可配置的旧版 libei keymap-FD 补丁仅作用于受监督的 GNOME RDP 子进程；26.04 已含系统修复，不替换系统库。见[补丁选择](../../../scripts/uu-remote-bridge#L199)、[GNOME 环境](../../../scripts/uu-remote-bridge#L1121)。

SDL 来自固定源码。`winpr-sspi-shim.dll` 转发 SSPI 并规范 Wine/WinPR 私有句柄以完成认证；UU 辅助程序补齐活动会话 token 来源与事件日志 API 失败形态，不增加 Unix 权限。

systemd 用户服务拥有进程组。关键子进程退出会触发整体中继重启；内部监督在 UU 重启后重新绑定输入钩子。清理仅停止自有辅助程序和专用前缀 Wine 进程，回收选区 owner、捕获和 session 标记，恢复之前活动的原生 GNOME 分享服务；不清理其他 Wine 前缀或桌面应用。见[子进程监督](../../../scripts/uu-remote-bridge#L2207)、[清理](../../../scripts/uu-remote-bridge#L478)、[用户 unit](../../../systemd/uu-remote-bridge.service)。

无活动显示器的 Wayland 会话可临时使用 GNOME 虚拟显示器；物理显示器返回或桥接停止后恢复分享模式。终端通道则由 Windows stdio 代理和认证回环 `forkpty` 辅助程序运行当前用户登录 shell，不依赖 SSH listener。见[原生终端](native-ubuntu-terminal.md)和[无人值守启动](unattended-startup.md)。
