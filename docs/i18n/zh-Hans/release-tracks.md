[English](../../release-tracks.md) · [中文（简体）](../zh-Hans/release-tracks.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 输入路径与维护标签

输入路径按已经验证的主机行为选择，`rdp`、`x11` 是保存的运行配置。Plus 的独立发布历史从 `v0.1.0` 开始。发布标签决定已知可用的重装源码，不会选择或改变保存的键盘路径；普通安装不需要行为轨道标签。

## 上游轨道历史

| 上游标签 | 历史用途 |
| --- | --- |
| `track-rdp-broker-20260724` | 已经流畅的 Wine broker/嵌套 RDP 输入 |
| `track-direct-x11-20260724` | X11/XRDP 上嵌套转换丢键时使用认证 XTEST |

带日期的两个轨道，以及较早的 `track-rdp-broker-v1`、`track-direct-x11-v1`、`v0.1.0`、`v0.2.0` 都属于[上游仓库](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)的历史。独立 Plus 仓库没有保留这些 refs。Plus 的 `v0.1.0` 是首次 Plus 发布，与同名上游版本不同。

## RDP broker

主机已有稳定画面/指针、电脑快速键盘、手机 `abcXYZ123,.!?` 一次准确送达且无需 X11 helper 时保持该轨道。迁移时未设置的 `UURB_TEXT_KEY_DELAY_MS` 保留原不 pacing 行为，`UURB_KEYBOARD_ROUTE=rdp` 不改变。上游历史源码在上游仓库中标记为 `v0.1.0`。

## 直接 X11

仅确认 X11/XRDP 且 broker 报已接收但真实快速键遗漏时选：

```text
UURB_KEYBOARD_ROUTE=x11
UURB_PHYSICAL_KEY_DELAY_MS=0
```

该轨道关注物理键/规范手机文字，视频和 UU transport 仍由中继承担；当前 helper 的键鼠能力见[架构](architecture.md)。helper 使用认证回环，完整请求 preflight，不在部分执行后的不明失败中重放。

## 选择 Plus 重装标签

配置器仍按保存的 route 推导旧上游轨道名称，缺失标签会被拒绝。首次发布后，显式选择本地确实存在的 Plus 标签：

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable --track v0.1.0 --branch main
```

维护源码来自 `origin/main`，`v0.1.0` 是已知可用的重装点。同用户 Codex 安装和登录要求见[自动更新](automatic-updates.md)。普通安装先运行 `install.sh`，再用明确标签配置维护；`install.sh --automatic-updates` 快捷入口使用旧默认，不能自行选择 Plus 标签。

检出发布标签后，先切回 `main` 再执行通常会拉取源码的升级；只有明确保留固定检出时才用 `--no-pull`。daily checker 不自动改变键盘节奏或开启 X11。修改保存的路径需要明确配置和真实输入检查。

## 本机记录

```text
Plus reinstall tag: v0.1.0
Maintenance branch: main
Desktop type: Wayland / Xorg / XRDP
Saved keyboard route: rdp / x11 / auto
Phone keyboard abcXYZ123,.!?: pass / fail
Computer-keyboard rapid alphabet: pass / fail
Quick verifier: pass / fail
```

记录留在本机，不提交 hostname、账户、控制端身份、raw logs。不同主机表现不同时见[手机键盘检查](mobile-keyboard-parity-handoff.md)。
