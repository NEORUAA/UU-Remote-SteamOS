[English](../../automated-repair-agent-handoff.md) · [中文（简体）](../zh-Hans/automated-repair-agent-handoff.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 自动维护合同

这份可复用规则随 repair checkout 的同一源码版本复制到 `build/automated-repair/OPERATIONAL-HANDOFF.md`。它不包含主机历史、账户状态或已完成现场记录。

## 工作范围

只在指定 repair checkout 中工作。保留输入轨道、保存的按键节奏和工作桌面路径，先读生成的私有上下文，再改兼容源码或候选清单。允许源码检查、非执行二进制检查、针对测试、文档和 draft 清单；按 updater schema 报 `ready_for_review`、`no_change`、`blocked`。修复完成不自动授权部署。

## 需另行批准的动作

不改 live Wine prefix、账户、keyring、用户配置、systemd unit 或 live checkout，不 sudo/push/发布。未知 installer 只能按[上游维护](upstream-maintenance.md)的显式 staging sandbox 执行。

自动 task 不能批准自己的二进制解释或将清单标 `approved`。签名、指令语义与完整身份由独立审阅确认后维护者接受。不能绕过失败的身份检查。

## 输入与恢复

物理键、手机文字、鼠标、剪贴板是不同路径；只查故障路径，不一起改全路由或增加全局延迟。投递不明确时报告，不重复用户输入。

live update 前保留恢复材料。服务健康不能代替画面、重连和真实输入。新版本须覆盖键盘、手机、剪贴板、所选桌面路径及登录保留。

## 关联文档

- [上游维护](upstream-maintenance.md)
- [安全](security.md)
- [输入轨道](release-tracks.md)
- [自动更新](automatic-updates.md)
- [排查方法](debugging-journey.md)
- [键盘兼容](mobile-keyboard-parity-handoff.md)
- [XRDP 恢复](xrdp-and-keyboard-recovery.md)

installer、闭源二进制、原始日志、截图、凭据、标识和 task context 留在私有 Git 外目录。只发布可复用结论和清理过的示例。

原桥接源码与维护工具来自 [Lachlan Chen 的 MIT 项目](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)。
