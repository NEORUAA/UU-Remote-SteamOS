[English](../../update-handoff.md) · [简体中文](update-handoff.md)

[首页](../../../i18n/README.zh-Hans.md)

# 更新现有安装

更新前保留本地源码修改与账号状态，不丢弃有改动的工作区。受管更新见[升级流程](reusable-upgrade.md)，UU 版本不变时见[仅更新运行时](runtime-only-refresh.md)。

## 源码更新

在源码目录检查 `git status --short`，保存本地修改，只更新到审核过的提交，然后执行：

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

安装会短暂重连 UU。远程使用时，从本地终端或独立管理连接执行。保存设置与独立账号状态保留。

## 安装后

确认目标桌面、指针、键盘及一次主控重连。手机文字、语音和粘贴见[键盘兼容检查](mobile-keyboard-parity-handoff.md)。样例 `abcXYZ123,.!?` 足够，无需把真实输入内容写入公开报告。

失败时保留回退文件与私有诊断，使用[故障排查](troubleshooting.md)。服务检查失败时，先查原因再决定是否调整账号或输入路径。

未知 UU 二进制需要[上游维护](upstream-maintenance.md)和独立审核。可选自动维护遵守[维护约定](automated-repair-agent-handoff.md)。

原版发布说明属于 [Lachlan Chen 的 MIT 桥接](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)；本项目变化见 [Plus 更新记录](../../../i18n/CHANGELOG.zh-Hans.md)。
