[English](../../runtime-only-refresh.md) · [简体中文](runtime-only-refresh.md)

[首页](../../../i18n/README.zh-Hans.md)

# 保留 UU 版本，只更新辅助组件

已安装的审核 UU 版本可用、仓库新增键盘、语音、启动或终端辅助组件时，可只更新运行时。产品升级与辅助组件更新分开执行。

```bash
./scripts/upgrade-uu-remote.sh apply --runtime-only --no-pull --now
```

`--now` 明确允许一次短暂 UU 重连；GNOME、SSH 和登录应用不重启。通过独立终端或 SSH 执行，避免只依赖 UU Terminal 管理。

该模式运行仓库测试和实时预检，要求已安装产品有批准清单，保存现有运行时，调用跳过账号登录的安装器并检查结果。安装／检查失败时进入已有回退流程。保存的输入、桌面、音频、登录状态保留。

它不查询厂商更新接口、不晋升待审版本、不运行 Codex、不修改维护定时器启用状态。共享 X11 VNC 后端仍需主动选择，Wayland 保留已工作的 RDP 中继。

关机或断电不能靠 shell trap 恢复，私有回退目录保留在 `~/.local/state/uu-remote-upgrader`。重启和真实手机操作需要各自检查。
