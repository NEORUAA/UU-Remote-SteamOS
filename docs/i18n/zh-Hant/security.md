[English](../../security.md) · [العربية](../ar/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Tiếng Việt](../vi/security.md) · [中文（简体）](../zh-Hans/security.md) · [中文（繁體）](../zh-Hant/security.md) · [Deutsch](../de/security.md) · [Русский](../ru/security.md)

[← 返回繁體中文首頁](../../../i18n/README.zh-Hant.md)

# 安全

## 許可權與隔離邊界

僅在獲授權的電腦和 UU 賬戶上使用。橋接器保留正常 UU 登入和 GNOME RDP 憑據；無人值守模式是可撤銷的 GDM/systemd 配置。

- 全棧以已登入 Unix 使用者執行，專用 Wine 字首為 `~/.local/share/wineprefixes/uu-remote`，systemd 使用使用者 unit。
- Xvfb 使用 Xauthority 且不監聽 TCP；broker 管道限於這個 Wine wineserver 名稱空間。
- 可選 X11 與原生終端輔助程式各繫結臨時 IPv4 迴環埠，各有每次啟動新建的 256-bit token。執行目錄 `0700`，終端交接檔案 `0600`，最多四個 shell 會話。
- 管理視窗 VNC 不設定獨立密碼，但只監聽 IPv4 迴環，只匯出一個 UU 視窗及關聯彈窗，隨本機檢視器退出而結束。
- 可選 Mac 當前桌面中繼在 Ubuntu 迴環使用認證 VNC，透過 SSH 到達 Mac。經典 VNC 密碼檔案只是混淆而非加密，因此保持 `0600`，不能代替 SSH 邊界。
- FreeRDP 只連線 `127.0.0.1`，按 SHA-256 固定 GNOME TLS 證書。GNOME 自己是否對 LAN 監聽取決於其配置，應使用防火牆和獨立強密碼。
- 安裝依賴、無人值守 GDM 配置、組成員及 root 回滾記錄才使用 `sudo`。

啟動器可能臨時停止原生 GNOME RDP 服務，將 daemon 繫結到選定會話的匯流排；退出時恢復之前活動的服務。已有 socket/lock 的固定 X display 不會被搶用。

## 憑據和私有內容

安裝器不回顯密碼，以 `secret-tool` 存入登入 keyring。FreeRDP 從標準輸入接收憑據，隨後清除 shell 變數，不放入程序引數、unit 或倉庫。VNC 認證只使用憑據前八位元組，這是經典 VNC 的限制；Mac keychain 可儲存對應字首。

無人值守啟動另需 keyring 密碼，用 `systemd-creds --with-key=tpm2` 加密。持久化只儲存密文；systemd 在受保護 runtime credential 中解密，oneshot 經 D-Bus 解鎖登入集合。`tss` 成員和臨時 TPM ACL 使當前登入與下次啟動都能訪問 TPM；撤銷會移除指令碼新增的許可權。該 keyring 私有介面原在 Ubuntu 24.04/GNOME 46 檢查，升級後應檢查解鎖 unit。

UU 的 token 與賬戶狀態留在專用字首。不要釋出該字首、日誌、registry 或桌面截圖。輸入日誌只記錄數量、型別、flags、route、結果、error，不記錄按鍵值、Unicode、座標或剪貼簿。終端日誌只記錄 readiness、session/尺寸、拒絕和關閉，不儲存命令和輸出。

語義文字每次最多 2,048 records，在記憶體中轉換 UTF-16/UTF-8，交由目標 `xclip` 擁有選區。先核實 owner，再貼上；成功後文字保留在桌面剪貼簿。`legacy/auto` 可將可表達文字轉成組合鍵；`rdp-public/auto` 對 Unicode 提交使用字面文字。RDP `cliprdr` 可在 Wine 中繼與 GNOME 間交換正常剪貼簿；VNC 文字輔助只向目標桌面傳送，不反饋回私有 display。細節見[文字與剪貼簿（英文／簡體中文）](../zh-Hans/semantic-text-and-clipboard.md)。

## 二進位制與更新

[4.42 清單](../../../patches/uu-remote-4.42.0.2770.json)記錄原件和補丁結果完整 SHA-256、size、唯一簽名、offset 與等長替換。`patch-gameviewer.py` 只接受 `approved`，未知位元組拒絕；原件保留為 `GameViewerServer.exe.uu-original`。舊清單隻批准對應舊版本，draft 必須先獨立審閱指令語義。

GameViewerHealthd 同樣按身份檢查。FreeRDP/SDL 使用[固定產品 profile](../../../patches/freerdp-sdl-product.json)，複用 runtime 要使原始碼、recipe、profile、輸出 pins 與 provenance 一致，見[原始碼構建](source-build.md)。舊 libei keymap-FD backport 僅在配置存在時用於受監督 GNOME 子程序；26.04 使用包含修復的系統庫，不覆蓋系統 libei。

`stage-uu-release.sh` 先靜態解包。顯式 `--sandbox-install` 使用無網路 Bubblewrap，或顯式 root-managed systemd 後端，隱藏真實 home、只讀主機、限定可寫暫存目錄；更強隔離可使用 VM。見[上游維護（英文／簡體中文）](../zh-Hans/upstream-maintenance.md)。

## 剩餘風險與維護策略

Wine 不是同 Unix 使用者間的強安全沙箱；UU 是閉源遠端輸入軟體，雲端與自更新行為可能改變。需要更強隔離時用獨立 Unix 賬戶，並更新 OS、Wine、UU、GNOME。

自動檢查不重啟健康中繼。修復在私有 clone 中生成 draft，不能自行批准或部署。自動上線需要顯式開啟，且精確 installer/server hash、已提交 acceptance、控制端與登入保留測試及至少 270 秒穩定期全部匹配。事務複製完整 Wine 字首，賬戶狀態必須逐字相等；失敗、打斷或重啟恢復舊字首並停止自動重試，不改 XRDP。見[自動更新](automatic-updates.md)。

GDM 自動登入使啟動後有物理訪問的人可使用賬戶；TPM 防止密文離線搬到另一臺機器解密，不能保護已經登入的桌面。LUKS 等開機前密碼仍需本地輸入。

倉庫僅儲存原始碼、說明、hash 和必要反彙編結論。不要提交 UU/FreeRDP 編譯產物、Wine 字首、registry、憑據、token、裝置標識、現場日誌或私有截圖。
