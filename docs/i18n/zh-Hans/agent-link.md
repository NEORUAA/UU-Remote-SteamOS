[English](../../agent-link.md) · [简体中文](agent-link.md)

[简体中文 · UU Remote Ubuntu Plus](../../../i18n/README.zh-Hans.md)

# 通过 SSH 传递私有代理消息

`uu-link` 在有授权的 Linux 主机之间提供持久消息通道，使用现有 `uu-ssh` 别名与原生 OpenSSH。它不新增端口或后台服务，也不接管 UU 终端、图形界面或重启桌面桥接器。

## 独立安装

两台主机都在源码目录执行：

```bash
install -d -m 0755 "$HOME/.local/bin"
install -m 0755 scripts/uu-link "$HOME/.local/bin/uu-link"
```

正常安装器也会安装该辅助程序，升级回退包含它；卸载移除脚本但保留私有消息历史。只复制这一脚本不会部署其他源码改动。需要 Python 3 与 OpenSSH。

按 [SSH 指南](ssh-and-port-mapping.md) 配置自己的别名，经对方核对主机指纹。工具使用已知主机密钥与公钥认证。

## 发送、查看、回复

`lab` 与 `workstation` 是示例别名，先换成自己的授权配置：

```bash
# Workstation: one message, one bounded delivery attempt.
printf '%s\n' 'Ready for your test. 中文 / 日本語 / "quotes"' | uu-link send lab

# Lab: list message IDs, then read a specific message.
uu-link inbox
uu-link read MESSAGE_UUID

# Lab: send a correlated reply to the workstation.
printf '%s\n' 'Accepted; my test is complete.' |
  uu-link send workstation --reply-to MESSAGE_UUID

# Workstation: check replies and its delivery receipts.
uu-link inbox
uu-link outbox
```

UTF-8 Markdown 也可直接发送：

```bash
uu-link send lab --file /path/to/private-handoff.md
```

消息最多为 64 KiB UTF-8，保留中文、日文、表情、引号和换行。终端输出采用 JSON 转义，`\u4e2d\u6587` 表示已存储的中文。消息内容只作为数据保存；接收方需主动查看收件箱，发送不会唤醒已停止的代理，也不表示任务已被接手。

## 断线与重试

消息在启动 SSH 前先保存本地，首次输出给出 UUID。成功收据表示对端已持久保存同一消息 ID 和 SHA-256，不表示任务完成。

```bash
uu-link outbox
uu-link retry MESSAGE_UUID

# Prepare a message while offline without attempting any connection.
printf '%s\n' 'Next action after recovery...' | uu-link send lab --queue-only
```

每次尝试最多 20 秒。重试保留原 ID；对端存入但确认丢失时，重复发送返回同一收据，只保存一份。相同 ID 的冲突内容会拒绝。已有本地收据时 retry 只显示原收据，不重新检测网络。没有自动重连循环。

消息位于 `~/.local/state/uu-link/`：inbox 收到的不可变信封、outbox 原发送消息及目标、receipts 精确投递收据。目录权限 0700、文件 0600，写入原子化且落盘后才确认，拒绝符号链接目标。并发发送使用 UUID 去重；历史无自动清理，定期查看占用，私有内容不要提交。
