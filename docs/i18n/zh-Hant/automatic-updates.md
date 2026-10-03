[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [中文（简体）](../zh-Hans/automatic-updates.md) · [中文（繁體）](../zh-Hant/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Русский](../ru/automatic-updates.md)

[← 返回繁體中文首頁](../../../i18n/README.zh-Hant.md)

# 自動檢查與可恢復修復

維護系統將不打斷中繼的上游觀察、私有原始碼修復和顯式上線事務分開。普通檢查不會替換正在工作的桌面連線。

## 啟用

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review \
  --reasoning-effort medium \
  --auto-promote-accepted
```

Plus 的獨立發布歷史從 `v0.1.0` 開始。帶日期的輸入軌道標籤屬於上游歷史，不包含在這個獨立儲存庫中；一般安裝不需要它們。Plus 發布標籤在本機實際存在後，用 `--track v0.1.0 --branch main` 明確選擇。設定工具預設仍選擇舊軌道名稱，缺少標籤會被拒絕。

取出發布標籤後，先執行 `git switch main`，再使用一般會取得原始碼的升級命令。維護分支為 `origin/main`，明確的重裝標籤仍是 `v0.1.0`。如確定要在升級中保持固定標籤對應的原始碼取出版本，可使用 `--no-pull`。

`--auto-promote-accepted` 只允許後續已有完整 maintainer acceptance 的精確版本，不允許 Codex 部署自己的結果；不開啟則只報告可升級。

model 和 reasoning 寫入 `~/.config/uu-remote-bridge/updater.json`，不繼承日後互動預設；同用戶 Codex 必須已經登入。配置儲存 `command -v codex` 的絕對可執行路徑，適用於 NVM 等較小 systemd `PATH`。可顯式用 `--codex /absolute/path/to/codex`。

每次修復前查詢包含額度：所有報告視窗用量不超過 `codex_max_used_percent`（預設 20）才啟動。不使用購買或 reset credits；不能驗證時至少延後一小時，不消耗 attempt。

## 定時服務

| Timer | 時間 | 工作 |
| --- | --- | --- |
| `uu-remote-update-check.timer` | 每日約 04:20，加隨機延遲；啟動後 12 分鐘 | endpoint 與元資料檢查 |
| `uu-remote-repair-monitor.timer` | 啟動後 7 分鐘；前次完成後每 15 分鐘 | 健康觀察、恢復 task、顯式接受事務 |

daily 的 `Persistent=true` 補做關機期間錯過的一次檢查。無需開啟互動終端。

```bash
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
```

## 檢查與修復

普通檢查只 HEAD 官方跳轉，儲存前刪除臨時 query keys，比較完整版本；同版本下載一次核完整 SHA，後續憑 ETag、size、hash sidecar 避免重複。比基線舊的 endpoint 不當升級。

預設 monitor 兩次異常相隔 20 秒後記錄證據並排隊分析，不停止 Wine/RDP/UU。`--auto-reinstall` 是另一個顯式選擇：確認異常才允許一次 systemd restart，失敗再從固定軌道預構建、測試和重灌；本頁啟用示例沒開啟它。

新版本下載到 `~/.local/state/uu-remote-updater/downloads`，上限 1 GiB。未知 hash 先靜態解包，再在 `tasks` 私有 repair clone 中分析、生成 draft 和測試。每次複製[維護合同（英文／簡體中文）](../zh-Hans/automated-repair-agent-handoff.md)到 mode `0600` 上下文。不可自動解包的 wrapper 不會直接執行，顯式 `--sandbox-install` 才使用無網路 Bubblewrap/systemd 沙箱。

Codex 不能改 live prefix、sudo、push、批准自己的二進位制語義或部署未知檔案。維護者依照[上游維護（英文／簡體中文）](../zh-Hans/upstream-maintenance.md)獨立審閱並完成控制端檢查。

## 已接受、保留登入的上線

必須同時滿足：官方版本與 installer 完整 hash 匹配 fetched `origin/main` 的 approved 清單；同一 commit 含 schema-1 acceptance 和 evidence；acceptance 繫結 installer 與 patched server hash；記錄 disposable prefix、控制端、重連、冷啟動、service restart、新 signaling 和登入保留；穩定期 270–1800 秒；顯式開啟自動接受上線；本地 UU 活動安靜達到維護期（預設 45 分鐘）。

事務核當前 runtime 與賬戶 marker，只查詢 XRDP，停止 UU 橋接，複製完整字首並留額外 1 GiB 空間，在同一字首就地安裝，應用精確清單。啟動前登入 registry 與賬戶狀態樹必須逐字相同。等待啟動列舉和新 room，兩次 runtime 檢查間隔穩定期，XRDP 活動狀態須保持。任何失敗、打斷或重啟恢復舊字首，標 `promotion-blocked` 不自動重試。state 與 prefix 要在同一檔案系統，保留回滾快照。

操作者可明確選擇短暫停機：

```bash
uu-remote upgrade apply --now
```

它只繞過活動等待，其他規則不變，見[可複用升級](reusable-upgrade.md)。

## 恢復任務與狀態

task 以 `0600` 原子儲存候選/軌道/base commit、上下文、thread UUID、attempt、phase、JSONL 和結構化結果。收到 `thread.started` 即儲存 UUID；打斷後 `codex exec resume` 同一個 thread，未建 UUID 才從同上下文新建。重試間隔從 15 分鐘增至 24 小時。

輸出須匹配 `scripts/codex-repair-result.schema.json`，monitor 另跑完整 unit suite：

| 狀態 | 含義 |
| --- | --- |
| `ready-for-review` | 原始碼與測試就緒，仍需語義審閱和實際接受 |
| `no-change` | 沒有可安全實施的改動 |
| `blocked` | 尚缺證據、暫存、測試或人類批准 |
| `promotion-waiting-idle` | 已接受但等待空閒 |
| `promotion-running` | 字首事務進行中 |
| `promoted` | 登入與 runtime 檢查透過 |
| `promotion-blocked` | 恢復舊字首，停止自動重試 |

配置和 state 不含密碼/token，目錄 `0700`、檔案 `0600`。installer、日誌、賬戶及本機證據留在 Git 外。repair clone 停用 push URL，Codex 用 workspace-write/never，service `NoNewPrivileges=yes`；其認證仍需網路，這不等價 VM 隔離。

## Ubuntu 24.04 沙箱與重試

使用者服務不疊加 `PrivateTmp`、`ProtectSystem`、`ProtectKernelTunables`、`ProtectControlGroups` mount namespace，以免 AppArmor `unprivileged_userns` 阻止巢狀 Bubblewrap。遇 `codex-sandbox-deferred`，只安裝發行版 bwrap profile，不全域性關閉 namespace 限制：

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

`retry` 保留私有證據與 checkout，清除不可用 thread，下一輪新建；非可重試 phase 拒絕。手動完成無網路 fallback 的暫存記錄，須 installer/server/healthd 三 hash 與 backend 都匹配才能匯入。`ready-for-review` 不自動變成可部署。

## 另一臺機器與關閉

只遷移原始碼，不復制 updater、會話、字首或憑據。確認乾淨工作樹、同用戶 Codex 登入與重啟後 timer，按該機[輸入軌道（英文／簡體中文）](../zh-Hans/release-tracks.md)配置。

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
# 同時刪除維護配置和全部私有維護狀態：
./scripts/configure-updater.sh disable --purge-state
```
