[English](../../debugging-journey.md) · [中文（简体）](../zh-Hans/debugging-journey.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 排查方法

从对应症状的组件入手。详细 incident、私有截图与 raw logs 留在公开源码外，本页给可复用检查。

## 分开看画面

桌面中继与本机 UU 管理窗口是不同视图。诊断黑帧前确认截图来自哪个窗口和 desktop，按[架构](architecture.md)定位路径，再用[故障排查](troubleshooting.md)的对应命令。

## 检查输入到达

UU 接受请求、broker 接受 events、应用收到文字是三层。确认焦点和目标应用；物理键、手机文字、粘贴分开检查，见[键盘兼容](mobile-keyboard-parity-handoff.md)。一次只改一个设置，保存旧值，不用反复注入或全局延迟掩盖丢输入。XRDP 会话按[恢复指南](xrdp-and-keyboard-recovery.md)处理。

## 分清源码与已安装文件

改源码或编译成功不等于 helper 已更新。通过 installer 或[仅 runtime 刷新](runtime-only-refresh.md)部署，再运行 `./scripts/verify.sh --quick`。身份检查失败要检查安装，不关闭校验。

## 先恢复服务

用 `uu-remote status` 和私有 service logs 分清服务未运行、桌面不可用或连接失败，生命周期见[正常退出恢复](clean-exit-recovery.md)。保留工作账户、route 和 rollback 材料。

公开结论描述组件、版本和修复，不带主机、账户/设备 IDs、原始输入、网络拓扑或完整聊天事件记录。
