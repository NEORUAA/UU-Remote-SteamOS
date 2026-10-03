[English](../../clean-exit-recovery.md) · [简体中文](clean-exit-recovery.md)

[简体中文 · UU Remote Ubuntu Plus](../../../i18n/README.zh-Hans.md)

# 桥接器退出后的恢复

用户服务使用 `Restart=always` 和重启间隔，意外的正常退出也会恢复。显式 `uu-remote stop` 会保持停止；内存、swap、任务数量与清理限制继续生效。

## 查看服务状态

```bash
uu-remote status
journalctl --user -u uu-remote-bridge.service -n 60 --no-pager
```

结合可见桌面、输入与控制端连接判断恢复情况。原始日志保持私有。主动停止过服务时，只需重新启动，无需清空账号或重装：

```bash
systemctl --user start uu-remote-bridge.service
./scripts/verify.sh --quick
```

保留已保存的桌面、键盘和账号设置。恢复桥接器不需要重启 GNOME、XRDP、SSH 或其他 Wine 应用。若运行文件身份检查失败，按正常安装或 [仅刷新运行组件](runtime-only-refresh.md) 更新。

修改用户服务单元前保存副本，执行 `systemctl --user daemon-reload`，在可接受的断线时间重新启动；避免原地编辑正运行的启动器。相关操作见 [故障排查](troubleshooting.md) 与 [管理升级](reusable-upgrade.md)。
