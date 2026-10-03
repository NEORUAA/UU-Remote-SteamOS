[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [中文（简体）](../zh-Hans/automatic-updates.md) · [中文（繁體）](../zh-Hant/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Русский](../ru/automatic-updates.md)

[← 返回简体中文首页](../../../i18n/README.zh-Hans.md)

# 自动检查与可恢复修复

维护系统将不打断中继的上游观察、私有源码修复和显式上线事务分开。普通检查不会替换正在工作的桌面连接。

## 启用

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review \
  --reasoning-effort medium \
  --auto-promote-accepted
```

Plus 的独立发布历史从 `v0.1.0` 开始。带日期的输入轨道标签属于上游历史，不包含在这个独立仓库中；普通安装不需要它们。Plus 发布标签在本地实际存在后，用 `--track v0.1.0 --branch main` 显式选择。配置器默认仍选择旧轨道名称，缺失标签会被拒绝。

检出发布标签后，先执行 `git switch main`，再使用通常会拉取源码的升级命令。维护分支为 `origin/main`，显式重装标签仍是 `v0.1.0`。如明确要在升级中保持固定标签对应的源码检出，可使用 `--no-pull`。

`--auto-promote-accepted` 只允许后续已有完整 maintainer acceptance 的精确版本，不允许 Codex 部署自己的结果；不开启则只报告可升级。

model 和 reasoning 写入 `~/.config/uu-remote-bridge/updater.json`，不继承日后交互默认；同用户 Codex 必须已经登录。配置保存 `command -v codex` 的绝对可执行路径，适用于 NVM 等较小 systemd `PATH`。可显式用 `--codex /absolute/path/to/codex`。

每次修复前查询包含额度：所有报告窗口用量不超过 `codex_max_used_percent`（默认 20）才启动。不使用购买或 reset credits；不能验证时至少延后一小时，不消耗 attempt。

## 定时服务

| Timer | 时间 | 工作 |
| --- | --- | --- |
| `uu-remote-update-check.timer` | 每日约 04:20，加随机延迟；启动后 12 分钟 | endpoint 与元数据检查 |
| `uu-remote-repair-monitor.timer` | 启动后 7 分钟；前次完成后每 15 分钟 | 健康观察、恢复 task、显式接受事务 |

daily 的 `Persistent=true` 补做关机期间错过的一次检查。无需打开交互终端。

```bash
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
```

## 检查与修复

普通检查只 HEAD 官方跳转，保存前删除临时 query keys，比较完整版本；同版本下载一次核完整 SHA，后续凭 ETag、size、hash sidecar 避免重复。比基线旧的 endpoint 不当升级。

默认 monitor 两次异常相隔 20 秒后记录证据并排队分析，不停止 Wine/RDP/UU。`--auto-reinstall` 是另一个显式选择：确认异常才允许一次 systemd restart，失败再从固定轨道预构建、测试和重装；本页启用示例没打开它。

新版本下载到 `~/.local/state/uu-remote-updater/downloads`，上限 1 GiB。未知 hash 先静态解包，再在 `tasks` 私有 repair clone 中分析、生成 draft 和测试。每次复制[维护合同](automated-repair-agent-handoff.md)到 mode `0600` 上下文。不可自动解包的 wrapper 不会直接执行，显式 `--sandbox-install` 才使用无网络 Bubblewrap/systemd 沙箱。

Codex 不能改 live prefix、sudo、push、批准自己的二进制语义或部署未知文件。维护者依照[上游维护](upstream-maintenance.md)独立审阅并完成控制端检查。

## 已接受、保留登录的上线

必须同时满足：官方版本与 installer 完整 hash 匹配 fetched `origin/main` 的 approved 清单；同一 commit 含 schema-1 acceptance 和 evidence；acceptance 绑定 installer 与 patched server hash；记录 disposable prefix、控制端、重连、冷启动、service restart、新 signaling 和登录保留；稳定期 270–1800 秒；显式开启自动接受上线；本地 UU 活动安静达到维护期（默认 45 分钟）。

事务核当前 runtime 与账户 marker，只查询 XRDP，停止 UU 桥接，复制完整前缀并留额外 1 GiB 空间，在同一前缀就地安装，应用精确清单。启动前登录 registry 与账户状态树必须逐字相同。等待启动枚举和新 room，两次 runtime 检查间隔稳定期，XRDP 活动状态须保持。任何失败、打断或重启恢复旧前缀，标 `promotion-blocked` 不自动重试。state 与 prefix 要在同一文件系统，保留回滚快照。

操作者可明确选择短暂停机：

```bash
uu-remote upgrade apply --now
```

它只绕过活动等待，其他规则不变，见[可复用升级](reusable-upgrade.md)。

## 恢复任务与状态

task 以 `0600` 原子保存候选/轨道/base commit、上下文、thread UUID、attempt、phase、JSONL 和结构化结果。收到 `thread.started` 即保存 UUID；打断后 `codex exec resume` 同一个 thread，未建 UUID 才从同上下文新建。重试间隔从 15 分钟增至 24 小时。

输出须匹配 `scripts/codex-repair-result.schema.json`，monitor 另跑完整 unit suite：

| 状态 | 含义 |
| --- | --- |
| `ready-for-review` | 源码与测试就绪，仍需语义审阅和实际接受 |
| `no-change` | 没有可安全实施的改动 |
| `blocked` | 尚缺证据、暂存、测试或人类批准 |
| `promotion-waiting-idle` | 已接受但等待空闲 |
| `promotion-running` | 前缀事务进行中 |
| `promoted` | 登录与 runtime 检查通过 |
| `promotion-blocked` | 恢复旧前缀，停止自动重试 |

配置和 state 不含密码/token，目录 `0700`、文件 `0600`。installer、日志、账户及本机证据留在 Git 外。repair clone 禁用 push URL，Codex 用 workspace-write/never，service `NoNewPrivileges=yes`；其认证仍需网络，这不等价 VM 隔离。

## Ubuntu 24.04 沙箱与重试

用户服务不叠加 `PrivateTmp`、`ProtectSystem`、`ProtectKernelTunables`、`ProtectControlGroups` mount namespace，以免 AppArmor `unprivileged_userns` 阻止嵌套 Bubblewrap。遇 `codex-sandbox-deferred`，只安装发行版 bwrap profile，不全局关闭 namespace 限制：

```bash
sudo apt install apparmor-profiles
sudo install -o root -g root -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
uu-remote update retry
```

```bash
systemd-run --user --wait --pipe --collect \
  --property=NoNewPrivileges=yes \
  /usr/bin/bwrap --die-with-parent --unshare-user --uid 0 --gid 0 \
  --ro-bind / / /bin/true
systemctl --user cat uu-remote-repair-monitor.service
```

`retry` 保留私有证据与 checkout，清除不可用 thread，下一轮新建；非可重试 phase 拒绝。手动完成无网络 fallback 的暂存记录，须 installer/server/healthd 三 hash 与 backend 都匹配才能导入。`ready-for-review` 不自动变成可部署。

## 另一台机器与关闭

只迁移源码，不复制 updater、会话、前缀或凭据。确认干净工作树、同用户 Codex 登录与重启后 timer，按该机[输入轨道](release-tracks.md)配置。

```bash
git status --short
git switch main
git pull --ff-only origin main
git fetch --tags origin
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/configure-updater.sh status
./scripts/configure-updater.sh disable
# 同时删除维护配置和全部私有维护状态：
./scripts/configure-updater.sh disable --purge-state
```
