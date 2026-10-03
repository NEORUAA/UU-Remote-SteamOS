[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[繁體中文 · UU Remote Ubuntu Plus](../../../i18n/README.zh-Hant.md)

# 故障排查

## 先查看狀態

在原始碼目錄執行以下命令。日誌在 `~/.local/state/uu-remote-bridge`，設定在 `~/.config/uu-remote-bridge/environment`。回報提供版本、症狀和錯誤訊息，移除帳號、裝置和輸入內容。原始碼更新後需重新安裝。

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

## 離線、開機後未上線

先透過官方管理視窗登入一次，正常關閉後中繼恢復。檢查使用者服務與鑰匙圈解鎖；密碼變更後用 `./scripts/configure-unattended.sh enable --replace-credential` 更新加密憑證。伺服器退出時查看復原與重新注入紀錄。

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

## 持續尋找線路

先確認主機啟動完成。Wine 中累積的輸入與藍牙裝置紀錄可能拖慢啟動；修復命令會備份並清理專用前綴的已識別紀錄，重啟 UU 中繼，保留 Ubuntu 藍牙。

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

## 黑屏、白屏或錯誤桌面

檢查已登入的 GNOME 工作階段、RDP 監聽和 SDL 日誌。有多個階段時查清來源。既有 XRDP 桌面可選 `--desktop-target xrdp`，實體桌面用 `physical`。X11 可選 `--desktop-relay vnc`，Wayland 使用 RDP。

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

## 留白、裁切或 4K 太吃力

比較來源桌面與畫布，透過圖形設定選擇 720p、1080p、1440p、4K。畫布、UU 控制端 FPS 與位元率分別設定。切換會短暫重連，失敗會回退；XRDP 動態改變尺寸時也要核對來源。

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

## 畫面正常但輸入失效

使用 uu-remote open 開啟管理，不要把同一 Wine 前綴直接啟動在另一 X 顯示上。正常關閉管理查看器會恢復中繼焦點。手機文字、中文和多行貼上需要剪貼簿路徑；實體鍵維持鍵事件，重新安裝後檢查注入器。 首次點擊就斷線時，檢查 UU SendInput bridge active、UU Wine event-log compatibility active 與輸入代理，再以 `uu-remote restart` 恢復。

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

## 按鍵延遲、符號錯誤、長期退化

先比較 VPN、代理和 UU 線路，stale 是歷史會話。確認網卡錯選後可用 `--network-interface default`，恢復用 `all`。實體鍵節奏可測 `--physical-key-delay-ms 8`，預設 `0`。符號依 Ubuntu 鍵盤配置；長期退化需驗證 GRD/libei 與檔案描述符。

```bash
uu-remote network
ip -4 route show default
```

## 游標消失或太小

選用游標保護預設關閉。auto 跟隨桌面大小，固定值支援 24 至 128，停用用 `--cursor-guard off`。不必改整個桌面解析度或 Wine DPI。

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

## UU 終端結束或顯示位置不對

安裝目前中繼並檢查終端通道；在 UU 選 PowerShell，實際使用 Ubuntu 登入 shell。關閉舊會話再開新終端，查 terminal-bridge.log 元資料，保留原 powershell.exe 的受控替換流程。

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

## RDP 認證、NLA 或 SSPI 錯誤

查詢憑證是否存在而不顯示內容。需要更換時清除專用鑰匙圈項目，再重新安裝。FreeRDP、WinPR 和 DLL 必須來自同一固定版本，詳細步驟見原始碼建置。

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

## Mac RDP/VNC 與 Windows App

內部 FreeRDP 已使用桌面共享連接埠；遠端登入會開另一桌面。查實際回環 VNC 連接埠再用 SSH 轉送，不依賴舊顯示號。Windows App 停在 Configuring 時先重開 Mac 客戶端，再檢查 XRDP。

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

## 週期重啟、聲音與移除

完整驗證器檢查穩定性。聲音問題分別檢查 UU 音訊、Wine PulseAudio 與 VNC 鈴聲，只改專用環境。先預覽解除安裝；普通移除保留前綴，`./uninstall.sh --purge` 會刪除帳號狀態。 先用 `wpctl status` 確認音訊流。`UURB_UU_AUDIO=system` 為相容預設，專用靜音 ALSA 的設定與回復見英文詳細排查。

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

繼續閱讀：[畫質](quality-guide.md)、[建置](source-build.md)、[架構](architecture.md)、[輸入](adaptive-keyboard-relays.md)、[升級](reusable-upgrade.md)。[詳細工程與歷史（English）](../../troubleshooting.md) 提供驅動、登錄檔、音訊、XRDP 與終端的深入說明。

## 深入閱讀

- XRDP 與鍵盤恢復 · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- 鍵盤相容檢查 · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- Mac 目前桌面 · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- 共用實體桌面 · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- 退出恢復 · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- 控制端代理 · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- SSH 代理訊息 · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)
