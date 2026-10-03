[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[首页](../../../i18n/README.zh-Hans.md)

# Plus 改了什么

![上游基础、Plus 变化与设计预期](../../images/uu-plus-evolution-zh-Hans.png)

[可编辑 SVG](../../images/uu-plus-evolution-zh-Hans.svg)

Plus 基于 [Lachlan Chen 的 UU Remote Ubuntu Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)，参考提交为 [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a)。Wine 隔离、GNOME 中继、鼠标键盘桥、本地管理和用户服务均来自上游。

## 日常使用中的变化

| 领域 | 上游已有 | Plus 改动 | 日常用途 |
| --- | --- | --- | --- |
| 主机兼容 | Ubuntu 24.04 与隔离 libei 回移库 | 适配 Ubuntu 26.04／GNOME 50，选择系统或回移 libei；保留 24.04 目标 | 按主机环境阅读平台与源码构建指南 |
| Windows UU | 默认 4.33.0.8907 与已审核版本清单 | 默认采用已审核的 4.42.0.2770 | 选择与 UU 版本匹配的清单 |
| 桌面尺寸 | 保存分辨率与 RDP 尺寸调整 | 最高 4K 的四档选择、完整桌面适配与保存尺寸恢复 | 选择 720p、1080p、1440p 或 4K，并查看实时画布 |
| 手机文字 | 输入法规范化与 Unicode 粘贴 | Plus 输入路径迭代与公开 FreeRDP 文本路径 | 从控制端输入中文、代码和多行文字 |
| 剪贴板 | RDP 剪贴板与 Unicode 文本事务 | SDL 源码补丁处理后台刷新、剪贴板归属变化与格式缓存 | 中继在后台时也能复制粘贴当前文字 |
| 管理窗口 | 独立窗口视图与焦点返回 | 管理窗口／弹窗独立捕获，复用查看器会话 | 在本机打开 UU 账号或设置，再回到桌面 |
| 光标 | 可选固定尺寸保护 | 主题光标回退与启动修正，默认保持关闭 | 需要时启用可选光标保护 |
| 桌面动作 | 鼠标键盘控制桌面 | 接入 GNOME 桌面／概览动作 | 将控制端桌面动作连接到 GNOME 后端 |
| 桌面工具 | 中继依赖与 UU 命令 | 集成画质／VNC／FreeRDP／Openbox 入口，局部字体、DPI 与凭据输入 | 按工具需求打开对应设置与连接窗口 |
| 构建与恢复 | 固定 nightly SDL／WinPR 与用户服务重连 | 固定补丁源码构建、运行时检查和档位／查看器恢复 | 准备匹配的中继，维护时保留已有设置 |

## 实现分类

- 手机文字：Plus 输入路径迭代 — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- 剪贴板：SDL 源码补丁 — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- 管理窗口：独立捕获与查看器处理 — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- 桌面工具：新增集成 — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## 输入路径

新装 RDP 选择 `rdp-public`，代理输入通过 FreeRDP 公开 API。自动模式下，包含 ASCII 的 Unicode 提交使用原文粘贴，实体按键独立处理。升级保留已保存路径；`legacy` 对可表示字符使用按键，对中文和换行使用粘贴。未配置的启动器也回退为 `legacy`。

比较 FPS 与延迟时，固定主机／控制端版本、源尺寸、画质／帧率、码率、网络和负载，并记录量测方法，见[测量说明](performance-evidence.md)。
