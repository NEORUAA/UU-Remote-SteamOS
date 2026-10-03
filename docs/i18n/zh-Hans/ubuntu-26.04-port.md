[English](../../ubuntu-26.04-port.md) · [العربية](../ar/ubuntu-26.04-port.md) · [Deutsch](../de/ubuntu-26.04-port.md) · [Español](../es/ubuntu-26.04-port.md) · [Français](../fr/ubuntu-26.04-port.md) · [日本語](../ja/ubuntu-26.04-port.md) · [한국어](../ko/ubuntu-26.04-port.md) · [Русский](../ru/ubuntu-26.04-port.md) · [Tiếng Việt](../vi/ubuntu-26.04-port.md) · [简体中文](../zh-Hans/ubuntu-26.04-port.md) · [繁體中文](../zh-Hant/ubuntu-26.04-port.md)

[首页](../../../i18n/README.zh-Hans.md)

# Ubuntu 26.04 与 GNOME 50

Plus 将 [Lachlan Chen 的 MIT 桥接项目](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)扩展到 x86-64 Ubuntu 26.04／GNOME 50，同时保留 Ubuntu 24.04／GNOME 46。Wine 隔离、已审核 UU 清单、输入代理、桌面中继和用户服务仍是基础。

安装中继需要精确匹配的已审核工具链，或已有验证输出／缓存；普通 APT 软件包不会自动提供这套工具链。见[构建前提与缓存复用](source-build.md)。

## 平台选择

| 组件 | 上游参考 | Plus |
| --- | --- | --- |
| Ubuntu 安装器 | 24.04 | 24.04、26.04；其他版本须显式设置 `UURB_ALLOW_UNVALIDATED_UBUNTU=1` |
| 默认 Windows UU | 4.33.0.8907 | 已审核 4.42.0.2770；仍可选择已有审核清单 |
| libei | 隔离的 1.2.1 回移补丁 | 系统库含修正时使用系统库，否则保留回移方案 |
| Windows 中继 | 固定 nightly SDL 客户端及匹配 WinPR | 固定源码构建的补丁版 FreeRDP/SDL；见[源码构建](source-build.md) |
| 源码 CI | Ubuntu 24.04 | 工作流面向 24.04、26.04；托管结果按每次运行检查 |

已观察的 26.04 安装使用 GNOME Remote Desktop 50.2 和系统 libei 1.5.0。旧库可使用回移提交 `ee27dd5c92e4e9496a36ca2d4112049fe02d2269`。`UURB_LIBEI_MODE=system|backport` 记录选择，`verify.sh` 检查 RDP 进程实际加载的库。Wine 使用 WineHQ stable。

## 桌面行为

GUI 和 CLI 提供四档画布、完整桌面适配与鼠标映射。首次安装选 1080p，升级保留设置。保存尺寸变化时，中继在回退保护下重连；重新应用已保存档位可恢复实时 RDP 画布。用户确认普通重连正常，原生分辨率菜单最高为 4K。

全新 RDP 安装使用 `rdp-public`，通过 FreeRDP 公开 API 传送输入；升级保留已保存路径。Unicode 提交文本与物理按键使用独立操作。管理窗口和其弹窗独立捕获；关闭查看器后恢复中继焦点，管理窗口保持映射。桌面剪贴板继续可用，管理窗口剪贴板交换关闭。

| 功能 | 当前结果 |
| --- | --- |
| 手机、Mac 直连中文输入 | 用户在 Plus 联调中确认正常 |
| 普通电脑文本复制粘贴 | 用户确认正常 |
| Mac UU 更新与重连 | 输入、粘贴、重连正常，4K 体验相近 |
| 管理窗口覆盖与焦点 | 用户反馈已解决；部分窗口／弹窗检查通过 |
| Android 桌面／概览动作 | 后端双向切换正常；手机按钮待测 |
| 可选光标保护 | 主题回退与部分光标检查正常；完整控制端形状待测 |
| 物理显示器开关、虚拟输出 | 本机待测 |
| 手机 → ToDesk → Mac → UU 文本 | 重复小写 `a` 问题仍未解决 |

桌面工具启动器为 VNC、FreeRDP、Openbox 提供局部中文字体、DPI 和凭据处理。Dock 设置属于 GNOME。Ubuntu 外连 Wine 主控的画质限制与入站桌面串流分开；请求画布尺寸也不会强制改变物理源桌面分辨率。见[画质](quality-guide.md)、[架构](architecture.md)和[对比](upstream-comparison.md)。

## 更新与上游变化

保留 Plus 为 `origin`，原项目设为独立远端：

```bash
git remote add upstream https://github.com/lachlanchen/uu-remote-ubuntu-bridge.git
git fetch upstream
```

在开发分支审核上游变化。修改运行脚本或原生组件后，重装并检查：

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

安装会短暂中断连接。源码变化后、安装更新前，运行时摘要会报告差异。[可复用升级](reusable-upgrade.md)介绍运行时恢复；档位回退负责画布设置。

未知 UU 安装包哈希会阻止自动补丁。新版本须进行语义审核、批准清单与运行时检查，再进入产品；见[上游维护](upstream-maintenance.md)。仓库分发 MIT 桥接源码与清单，UU 和依赖保留各自许可。
