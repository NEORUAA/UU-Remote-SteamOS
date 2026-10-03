[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [中文（简体）](../zh-Hans/reusable-upgrade.md) · [中文（繁體）](../zh-Hant/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md)

[← 返回繁體中文首頁](../../../i18n/README.zh-Hant.md)

# 可複用、保留登入的升級

`uu-remote-upgrade` 把倉庫更新、已接受 UU 產品升級、橋接重新整理和檢查組合成事務，保留賬戶登入、輸入配置與 XRDP 可用性。


取出發布標籤後，先執行 `git switch main`，再使用一般會取得原始碼的升級命令。維護分支為 `origin/main`，明確的重裝標籤仍是 `v0.1.0`。如確定要在升級中保持固定標籤對應的原始碼取出版本，可使用 `--no-pull`。

## 命令

```bash
uu-remote-upgrade status
uu-remote upgrade status
uu-remote upgrade check
uu-remote upgrade apply
uu-remote upgrade apply --now
```

`check` 只檢查；`apply` 等待維護空閒期；`--now` 表示操作者願意短暫中斷 UU，只跳過活動等待，不跳過精確 hash、批准清單、acceptance、完整字首快照、賬戶逐字比較、兩次 runtime 檢查或恢復規則。未安裝命令時可在提供的原始碼目錄執行：

```bash
./scripts/upgrade-uu-remote.sh apply --now
```

## 事務順序

1. 要求乾淨、非 detached checkout，fetch 後只 fast-forward，不合並分叉歷史；原始碼變化時從新版本重新執行。
2. 執行無閉源二進位制的完整 unit suite 和 shell parser，檢查當前批准產品、中繼、輸入路徑、時序、賬戶 marker。
3. 只選擇官方 endpoint 與完整 hash 都匹配、並有已提交 acceptance 的版本。
4. 複製整個 Wine 字首，就地執行接受的 installer，恢復補丁，逐字檢查登入 registry 和兩棵賬戶狀態樹，再啟動並檢查兩次；失敗恢復整個舊字首。
5. 選擇已安裝版本對應清單，另存橋接 runtime，重新整理 helper/service，保留 `~/.config/uu-remote-bridge/environment`。
6. 重新整理已配置維護工具，不改其軌道或 Codex 配置，最後檢查 `uu-agent`、橋接與 XRDP 狀態。

只查詢 XRDP，不啟停或重新配置它。PID 變化會報告，活動狀態變化使事務失敗。

## 輸入配置與人工檢查

例如已經驗過的直接 X11 配置可能儲存：

```text
UURB_TEXT_KEY_DELAY_MS=8
UURB_PHYSICAL_KEY_DELAY_MS=0
UURB_KEYBOARD_ROUTE=x11
UURB_NETWORK_INTERFACE=default
```

這些值不是跨機器推薦預設，RDP 主機保留自己的軌道。快速檢查不向使用者應用輸入文字；更新後仍需實際檢查手機 `abcXYZ123,.!?`、電腦快速字母/Enter/Ctrl+A、滑鼠移動/點選/拖動/滾輪，見[鍵盤中繼](adaptive-keyboard-relays.md)。

## 回滾記錄

```text
~/.local/state/uu-remote-updater/tasks/*/promotion/snapshot-prefix
~/.local/state/uu-remote-upgrader/transactions/TIMESTAMP/
~/.local/state/uu-remote-upgrader/latest
```

產品失敗或打斷後標為 `promotion-blocked`，不會自動重試。`--now` 還檢查持久化終態，不能僅因 pending 檔案消失就說完成。只有 promotion 工具原始碼 commit 已變化，顯式再次 apply 才能重新排隊同一精確版本；原 task 完整移入 `tasks/retired/`。

產品升級成功後的原始碼重新整理若失敗，只停止 UU 橋接、恢復剛儲存的 runtime 並啟動。快照保留供操作者檢查，timer 不自行刪除；其中可能有閉原始檔和配置，不能提交。

## 持久使用者匯流排

巢狀終端可能匯出不同 `DBUS_SESSION_BUS_ADDRESS`。upgrader 與 `uu-agent` 明確使用：

```text
unix:path=/run/user/UID/bus
```

因此物理桌面、XRDP、VNC、SSH 和無人值守 manager 查詢同一個持久使用者服務。

## 歷史經驗與新主機

2026 年 7 月上游 4.34 升級曾撤回 acceptance；這是歷史記錄，不是當前 Plus 4.42 狀態。恢復需要冷啟動、新 signaling、真實控制端、登入保留和穩定期，見[歷史接受記錄（英文）](../../releases/4.34.0.8979-acceptance.md)。

當時修復了三類維護工具問題：缺少 verifier artifact；GNU PE 時間戳/校驗和破壞同源 hash；`Type=simple` 已 active 但 GNOME RDP 尚未監聽的 readiness 競態。當前檢查等待真實 daemon listener 和所選 X11 helper，時限 45 秒；PE 比較只規範明確的舊 timestamp/checksum 欄位，程式碼等其他位元組仍嚴格比較。原始碼重新整理後要求準確 runtime digest。

新電腦只拉原始碼，保留該機自己的字首、keyring 與 updater 狀態：

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

命令安裝在 `~/.local/bin`，需在 `PATH`。軌道選擇見[輸入行為軌道（英文／簡體中文）](../zh-Hans/release-tracks.md)，自動接受規則見[自動更新](automatic-updates.md)。
