[English](../../ubuntu-26.04-port.md) · [العربية](../ar/ubuntu-26.04-port.md) · [Deutsch](../de/ubuntu-26.04-port.md) · [Español](../es/ubuntu-26.04-port.md) · [Français](../fr/ubuntu-26.04-port.md) · [日本語](../ja/ubuntu-26.04-port.md) · [한국어](../ko/ubuntu-26.04-port.md) · [Русский](../ru/ubuntu-26.04-port.md) · [Tiếng Việt](../vi/ubuntu-26.04-port.md) · [简体中文](../zh-Hans/ubuntu-26.04-port.md) · [繁體中文](../zh-Hant/ubuntu-26.04-port.md)

[首頁](../../../i18n/README.zh-Hant.md)

# Ubuntu 26.04 與 GNOME 50

Plus 將 [Lachlan Chen 的 MIT 橋接](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)擴展到 x86-64 Ubuntu 26.04／GNOME 50，保留24.04／GNOME 46。Wine 隔離、審核 UU 清單、輸入代理、中繼與使用者服務是基礎。

安裝中繼需要精確相符的已審核工具鏈，或已有驗證輸出／快取；一般 APT 套件不會自動提供這套工具鏈。見[建置前提與快取重用](source-build.md)。

| 元件 | 上游參考 | Plus |
| --- | --- | --- |
| Ubuntu |24.04|24.04／26.04；其他須 `UURB_ALLOW_UNVALIDATED_UBUNTU=1`|
| Windows UU |4.33.0.8907|批准4.42.0.2770，仍可選舊清單|
| libei |隔離1.2.1回移|系統庫含修正時採用，否則回移|
| 中繼 |固定nightly SDL/WinPR|固定修補原始碼；[建置](source-build.md)|
| CI |24.04|24.04／26.04；各次執行結果|

觀察環境使用 GRD 50.2、libei 1.5.0。舊庫可用 `ee27dd5c92e4e9496a36ca2d4112049fe02d2269`。`UURB_LIBEI_MODE=system|backport` 儲存選擇，`verify.sh` 檢查載入的庫。使用 WineHQ stable。

## 桌面行為

四檔、完整適配與滑鼠映射。新裝1080p，升級保留設定；儲存尺寸變更在還原保護下重連，再套用可恢復即時畫布。使用者確認正常重連與原生選單最高4K。新裝 RDP 用 `rdp-public`，升級保留路徑。Unicode 與實體按鍵分開。管理／彈窗獨立擷取，關閉檢視器恢復中繼焦點、管理視窗保持映射。桌面剪貼簿可用，管理交換隔離。

| 功能 | 結果 |
| --- | --- |
| 手機／Mac直連中文 |使用者在整合中確認|
| 一般電腦文字貼上 |使用者確認正常|
| Mac UU更新 |重連／中文／貼上正常，4K相近|
| 管理覆蓋／焦點 |使用者回報解決，部分檢查正常|
| Android動作 |後端雙向正常，實按鈕待測|
| 游標 |主題／部分正常，全形狀待測|
| 實體／虛擬輸出 |本機待測|
| 手機→ToDesk→Mac→UU |重複`a`未解決|

VNC/FreeRDP/Openbox 提供個別中文字型、DPI、憑證資訊。Dock 屬 GNOME；外連畫質與實體解析度與入站畫布分開。[畫質](quality-guide.md)、[架構](architecture.md)、[比較](upstream-comparison.md)。

## 更新

保留 Plus 為 `origin`：

```bash
git remote add upstream https://github.com/lachlanchen/uu-remote-ubuntu-bridge.git
git fetch upstream
```

開發分支審核上游；執行環境變更後：

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

安裝短暫中斷，來源摘要在更新前報差異。[可重用升級](reusable-upgrade.md)處理執行環境，檔位還原處理畫布。未知 UU 雜湊阻止自動修補；新版本須語意審核、批准清單與執行檢查。[維護](../../upstream-maintenance.md)。分發 MIT 原始碼／清單，UU 與相依保留各自授權。
