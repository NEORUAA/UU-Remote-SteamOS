[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [中文（简体）](../zh-Hans/reusable-upgrade.md) · [中文（繁體）](../zh-Hant/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 可复用、保留登录的升级

`uu-remote-upgrade` 把仓库更新、已接受 UU 产品升级、桥接刷新和检查组合成事务，保留账户登录、输入配置与 XRDP 可用性。


检出发布标签后，先执行 `git switch main`，再使用通常会拉取源码的升级命令。维护分支为 `origin/main`，显式重装标签仍是 `v0.1.0`。如明确要在升级中保持固定标签对应的源码检出，可使用 `--no-pull`。

## 命令

```bash
uu-remote-upgrade status
uu-remote upgrade status
uu-remote upgrade check
uu-remote upgrade apply
uu-remote upgrade apply --now
```

`check` 只检查；`apply` 等待维护空闲期；`--now` 表示操作者愿意短暂中断 UU，只跳过活动等待，不跳过精确 hash、批准清单、acceptance、完整前缀快照、账户逐字比较、两次 runtime 检查或恢复规则。未安装命令时可在提供的源码目录运行：

```bash
./scripts/upgrade-uu-remote.sh apply --now
```

## 事务顺序

1. 要求干净、非 detached checkout，fetch 后只 fast-forward，不合并分叉历史；源码变化时从新版本重新执行。
2. 运行无闭源二进制的完整 unit suite 和 shell parser，检查当前批准产品、中继、输入路径、时序、账户 marker。
3. 只选择官方 endpoint 与完整 hash 都匹配、并有已提交 acceptance 的版本。
4. 复制整个 Wine 前缀，就地运行接受的 installer，恢复补丁，逐字检查登录 registry 和两棵账户状态树，再启动并检查两次；失败恢复整个旧前缀。
5. 选择已安装版本对应清单，另存桥接 runtime，刷新 helper/service，保留 `~/.config/uu-remote-bridge/environment`。
6. 刷新已配置维护工具，不改其轨道或 Codex 配置，最后检查 `uu-agent`、桥接与 XRDP 状态。

只查询 XRDP，不启停或重新配置它。PID 变化会报告，活动状态变化使事务失败。

## 输入配置与人工检查

例如已经验过的直接 X11 配置可能保存：

```text
UURB_TEXT_KEY_DELAY_MS=8
UURB_PHYSICAL_KEY_DELAY_MS=0
UURB_KEYBOARD_ROUTE=x11
UURB_NETWORK_INTERFACE=default
```

这些值不是跨机器推荐默认，RDP 主机保留自己的轨道。快速检查不向用户应用输入文字；更新后仍需实际检查手机 `abcXYZ123,.!?`、电脑快速字母/Enter/Ctrl+A、鼠标移动/点击/拖动/滚轮，见[键盘中继](adaptive-keyboard-relays.md)。

## 回滚记录

```text
~/.local/state/uu-remote-updater/tasks/*/promotion/snapshot-prefix
~/.local/state/uu-remote-upgrader/transactions/TIMESTAMP/
~/.local/state/uu-remote-upgrader/latest
```

产品失败或打断后标为 `promotion-blocked`，不会自动重试。`--now` 还检查持久化终态，不能仅因 pending 文件消失就说完成。只有 promotion 工具源码 commit 已变化，显式再次 apply 才能重新排队同一精确版本；原 task 完整移入 `tasks/retired/`。

产品升级成功后的源码刷新若失败，只停止 UU 桥接、恢复刚保存的 runtime 并启动。快照保留供操作者检查，timer 不自行删除；其中可能有闭源文件和配置，不能提交。

## 持久用户总线

嵌套终端可能导出不同 `DBUS_SESSION_BUS_ADDRESS`。upgrader 与 `uu-agent` 明确使用：

```text
unix:path=/run/user/UID/bus
```

因此物理桌面、XRDP、VNC、SSH 和无人值守 manager 查询同一个持久用户服务。

## 历史经验与新主机

2026 年 7 月上游 4.34 升级曾撤回 acceptance；这是历史记录，不是当前 Plus 4.42 状态。恢复需要冷启动、新 signaling、真实控制端、登录保留和稳定期，见[历史验收记录](releases/4.34.0.8979-acceptance.md)。

当时修复了三类维护工具问题：缺少 verifier artifact；GNU PE 时间戳/校验和破坏同源 hash；`Type=simple` 已 active 但 GNOME RDP 尚未监听的 readiness 竞态。当前检查等待真实 daemon listener 和所选 X11 helper，时限 45 秒；PE 比较只规范明确的旧 timestamp/checksum 字段，代码等其他字节仍严格比较。源码刷新后要求准确 runtime digest。

新电脑只拉源码，保留该机自己的前缀、keyring 与 updater 状态：

```bash
git status --short
git switch main
git pull --ff-only origin main
./install.sh --skip-packages --skip-account-login
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/upgrade-uu-remote.sh check
```

命令安装在 `~/.local/bin`，需在 `PATH`。轨道选择见[输入行为轨道](release-tracks.md)，自动接受规则见[自动更新](automatic-updates.md)。
