[English](../../porting.md) · [العربية](../ar/porting.md) · [Deutsch](../de/porting.md) · [Español](../es/porting.md) · [Français](../fr/porting.md) · [日本語](../ja/porting.md) · [한국어](../ko/porting.md) · [Русский](../ru/porting.md) · [Tiếng Việt](../vi/porting.md) · [简体中文](../zh-Hans/porting.md) · [繁體中文](../zh-Hant/porting.md)

[首页](../../../i18n/README.zh-Hans.md)

# 迁移到其他 Linux 桌面

x86-64 GNOME 发行版是最接近的起点：保留 RDP 桌面后端，适配安装路径。KDE、Xfce 需要自己的桌面适配层。当前安装器面向 Ubuntu 24.04 和 26.04，下表其他平台是迁移目标。

安装中继需要精确匹配的已审核工具链，或已有验证输出／缓存；普通 APT 软件包不会自动提供这套工具链。见[构建前提与缓存复用](source-build.md)。

![Linux 迁移的三个层次](../../images/uu-plus-porting-zh-Hans.png)

[可编辑 SVG](../../images/uu-plus-porting-zh-Hans.svg) · [中文图](../../images/uu-plus-porting-zh-Hans.png)

## 三个层次

| 层次 | 可复用内容 | 适配内容 | 源码 |
| --- | --- | --- | --- |
| 桥接核心 | 独立 Wine/UU 前缀、批准清单、SDL/FreeRDP 中继、输入代理、公开 RDP 插件、私有画布、管理窗口捕获 | 保持 Windows 运行时和协议边界，将 Unicode 字面文本与物理按键分开 | [代理](../../../src/uu_input_broker.c)、[RDP 适配](../../../src/freerdp-adapter.c)、[插件](../../../src/plugin.c)、[管理捕获](../../../src/uu_manager_capture.c) |
| 发行版安装 | 构建配方、运行时检查、配置、监督服务 | 软件包、Wine／原生路径、系统库、用户服务及启动器 | [安装器](../../../install.sh)、[构建](../../../scripts/build-winpr.sh)、[运行检查](../../../scripts/verify-freerdp-runtime.py)、[服务](../../../systemd/uu-remote-bridge.service) |
| 桌面后端 | RDP 事件及文本／动作协议 | 会话发现、捕获输入服务、剪贴板粘贴、源几何与桌面动作 | [启动器](../../../scripts/uu-remote-bridge)、[文本／动作](../../../src/uu_x11_input.c)、[画布模式](../../../scripts/uu-display-modes.py) |

FreeRDP 公开键盘、指针 API 使用已有 RDP 连接，其服务端可独立于 UU 的 Windows 输入钩子适配。Unicode 文本还需要源桌面剪贴板所有权与粘贴，目前使用 X11/Xwayland。管理窗口位于私有 Wine X11 显示。见[架构](architecture.md)。

## 平台选择

| 平台／桌面 | 复用 | 主要适配 |
| --- | --- | --- |
| Ubuntu 24.04／GNOME 46 | 现有安装器、后端 | 保留路径及可选 libei 回移 |
| Ubuntu 26.04／GNOME 50 | 现有安装器、后端 | 当前 Plus 集成、系统 libei、批准 UU 4.42 |
| Debian／GNOME | 核心、画布、GNOME RDP 设计 | Debian 软件包和 Wine 源、预检、守护进程路径、库检测；[APT/dpkg 指南](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html) |
| Fedora／GNOME | 核心、GNOME 后端设计 | RPM/DNF、Wine／辅助程序路径、服务权限；[GRD 软件包](https://packages.fedoraproject.org/pkgs/gnome-remote-desktop/gnome-remote-desktop/) |
| Arch／GNOME | 核心、GNOME 后端设计 | pacman、路径、固定工具、滚动 GNOME/libei 更新；[GRD 软件包](https://archlinux.org/packages/extra/x86_64/gnome-remote-desktop/) |
| KDE Plasma | 核心、画布、管理捕获 | KDE 会话、捕获输入、输出查询、剪贴板、桌面动作；[KRDP](https://github.com/KDE/krdp) 可作候选端点，认证、编解码及文本需要集成 |
| Xfce／X11 | 核心、画布、管理捕获、X11 辅助程序 | 会话、源几何与桌面动作；已有 `legacy` 输入的 X11 VNC 分支可作起点 |

更换包管理器只解决安装层。每种桌面适配都须接通源捕获、输入传送、源几何与桌面动作。

## 当前平台接口

| 接口 | 当前实现 | 迁移要求 |
| --- | --- | --- |
| 架构 | 主机 `x86_64`、Windows AMD64 PE | 首轮保持 x86-64；其他架构需 AMD64 执行及运行时检查 |
| 软件包 | Ubuntu 预检、`apt-get`、`dpkg`、i386、Ubuntu WineHQ 源 | 目标包映射、Wine 源与架构设置 |
| Wine 路径 | `/opt/wine-stable/bin/wine`、`wineserver`、`winepath` | 启动、清理、检查统一解析路径 |
| 构建工具 | 固定 MinGW、CMake、Meson、Ninja、依赖归档 | 匹配固定工具，或审核新配置；见[构建指南](source-build.md) |
| GNOME 会话／捕获 | `gnome-shell`、所选会话 D-Bus、`/usr/libexec/gnome-remote-desktop-daemon` | 对应路径或其他捕获输入服务 |
| 凭据／设置 | Keyring、`secret-tool`、`grdctl`、`org.gnome.desktop.remote-desktop.rdp` | 后端凭据、TLS、服务控制独立于 UU 账号 |
| 源输出 | `org.gnome.Mutter.DisplayConfig`、GNOME 虚拟显示器设置 | 合成器输出信息和显示器生命周期；X11 可用 XRandR |
| 文本剪贴板 | `uu-x11-input`／`xclip` 持有 `CLIPBOARD`、`PRIMARY` | 正确显示与剪贴板桥；原生 Wayland 使用桌面剪贴板接口 |
| 桌面动作 | `_NET_SHOWING_DESKTOP`、`org.gnome.Shell.OverviewActive` | 映射窗口管理器的桌面／全部窗口动作并确认状态 |
| 用户服务 | `systemctl --user`、图形会话 D-Bus | 适配发行版、会话及初始化系统 |
| 工具 | `/usr/bin/xfreerdp`、`xtigervncviewer`、`obconf`、`zenity`；局部字体／DPI | 工具路径、启动器、交互凭据与本地中继保护 |

私有 Wine/Xvfb 画布模式与物理、虚拟源输出分开。支持时保留四档画布；KDE、Xfce 替换面向 Mutter 的源显示逻辑。

## 首次迁移清单

1. 选择一种 x86-64 系统／会话，记录系统、桌面、Wine、UU 版本。GNOME 可保留最多接口。
2. 适配包、路径、库、用户服务和启动器，验证固定中继。
3. 接通捕获输入、会话总线、显示、凭据、几何和剪贴板。
4. 用真实主控检查鼠标、点击、滚轮、拖动、物理快捷键、手机 Unicode、粘贴、重连、管理弹窗和开关。
5. 检查四档画布、保存尺寸恢复、失败回退、辅助进程清理、桌面和概览动作。

提交包映射、接口路径、版本和主控结果，不带 UU 二进制或账号数据。[对比](upstream-comparison.md)和[画质](quality-guide.md)说明应保留的行为。
