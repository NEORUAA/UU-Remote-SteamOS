[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [中文（简体）](../zh-Hans/adaptive-keyboard-relays.md) · [中文（繁體）](../zh-Hant/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 自适应键盘中继

同一个 Ubuntu X11 桌面可接收不同协议的键盘输入。全部按硬件扫描码处理，会丢失符号原意。

| 路径 | 协议提供的信息 | 主机处理 |
| --- | --- | --- |
| XRDP | 键盘元数据与扫描码 | 使用客户端报告的布局 |
| RealVNC/x11vnc | X11/RFB keysym | 保留 `modtweak`、XKB 和临时 keysym |
| UU 电脑键盘 | Windows 物理键事件 | 使用选定的 `rdp` 或 `x11` 行为 |
| UU 手机输入法 | Unicode 提交 | 与物理键路径分开 |

优先保留协议中的 keysym/Unicode；真正物理键才依赖布局。不要用全局 `setxkbmap` 循环追踪最近连接的客户端。`~/.xsessionrc` 中无条件 `setxkbmap ... -layout jp` 会覆盖 XRDP 的客户端布局。日文 Mac 专用修复可作为显式命令保留，不要每次登录都执行。IBus、语义文字和原生终端不应依赖当前物理 XKB。

直接 X11 的可表达文字使用组合键；中文、换行、tab、emoji 等通过同步 `CLIPBOARD`/`PRIMARY` 和一次粘贴，避免把口述换行当成终端 Enter。`rdp-public` 的 Unicode 提交则默认保持字面文本。见[架构](architecture.md)与[语义文字](semantic-text-and-clipboard.md)。

## 专用嵌套 VNC 查看器

只用于把目标桌面放进 UU 画布的全屏查看器默认：

```text
UURB_VNC_GRAB_KEYBOARD=on
```

查看器收到 `-GrabKeyboard=1`，避免中间 X 桌面消耗 Shift/Ctrl/Alt/Super，只把基础键传下去。典型现象是 `(` 变 `8`、`?` 变 `/`、`@` 变 `2`，Ctrl 快捷键失效。

回环 x11vnc 使用：

```text
-repeat -nobell -modtweak -xkb -add_keysyms
```

`modtweak` 重建目标布局所需组合键，`-xkb` 查询完整 XKB，`-add_keysyms` 允许原本没有的 keysym。只监听 IPv4 回环。非专用中继窗口才考虑关闭 grab：

```bash
./install.sh --skip-packages --skip-account-login \
  --vnc-grab-keyboard off
```

## 测试与选择

```bash
./scripts/test-vnc-keyboard-relay.sh
```

该独立 RFB/Xvfb 测试针对日文 XKB，检查 21 个 shift 符号和 `你好`：

```text
vnc-symbols=23/23 order=exact target-layout=jp
isolated VNC keyboard acceptance passed
```

真实控制端使用临时文本框，分别检查普通数字/标点、`()` 等 Shift 符号、Ctrl+A/C/V/Enter/Backspace，以及实际 IME 中文或日文。不要在密码框测试。

这项配置不改变桌面 XKB、不重启 XRDP、不注销 GNOME。UU 物理键协议没有可靠的每连接布局标识；直接 X11 使用目标会话布局。XRDP/RFB 可依赖元数据/keysym，手机依赖 Unicode。缺少源布局时，桥接器无法猜测 `Shift+7` 原意是 `&` 还是 `'`。需要不同布局时明确选择客户端配置或行为轨道，见[输入轨道](release-tracks.md)。
