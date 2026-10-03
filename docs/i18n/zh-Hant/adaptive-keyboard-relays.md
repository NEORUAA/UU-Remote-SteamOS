[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [中文（简体）](../zh-Hans/adaptive-keyboard-relays.md) · [中文（繁體）](../zh-Hant/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md)

[← 返回繁體中文首頁](../../../i18n/README.zh-Hant.md)

# 自適應鍵盤中繼

同一個 Ubuntu X11 桌面可接收不同協議的鍵盤輸入。全部按硬體掃描碼處理，會丟失符號原意。

| 路徑 | 協議提供的資訊 | 主機處理 |
| --- | --- | --- |
| XRDP | 鍵盤元資料與掃描碼 | 使用客戶端報告的佈局 |
| RealVNC/x11vnc | X11/RFB keysym | 保留 `modtweak`、XKB 和臨時 keysym |
| UU 電腦鍵盤 | Windows 物理鍵事件 | 使用選定的 `rdp` 或 `x11` 行為 |
| UU 手機輸入法 | Unicode 提交 | 與物理鍵路徑分開 |

優先保留協議中的 keysym/Unicode；真正物理鍵才依賴佈局。不要用全域性 `setxkbmap` 迴圈追蹤最近連線的客戶端。`~/.xsessionrc` 中無條件 `setxkbmap ... -layout jp` 會覆蓋 XRDP 的客戶端佈局。日文 Mac 專用修復可作為顯式命令保留，不要每次登入都執行。IBus、語義文字和原生終端不應依賴當前物理 XKB。

直接 X11 的可表達文字使用組合鍵；中文、換行、tab、emoji 等透過同步 `CLIPBOARD`/`PRIMARY` 和一次貼上，避免把口述換行當成終端 Enter。`rdp-public` 的 Unicode 提交則預設保持字面文字。見[架構](architecture.md)與[語義文字（英文／簡體中文）](../zh-Hans/semantic-text-and-clipboard.md)。

## 專用巢狀 VNC 檢視器

只用於把目標桌面放進 UU 畫布的全屏檢視器預設：

```text
UURB_VNC_GRAB_KEYBOARD=on
```

檢視器收到 `-GrabKeyboard=1`，避免中間 X 桌面消耗 Shift/Ctrl/Alt/Super，只把基礎鍵傳下去。典型現象是 `(` 變 `8`、`?` 變 `/`、`@` 變 `2`，Ctrl 快捷鍵失效。

迴環 x11vnc 使用：

```text
-repeat -nobell -modtweak -xkb -add_keysyms
```

`modtweak` 重建目標佈局所需組合鍵，`-xkb` 查詢完整 XKB，`-add_keysyms` 允許原本沒有的 keysym。只監聽 IPv4 迴環。非專用中繼窗口才考慮關閉 grab：

```bash
./install.sh --skip-packages --skip-account-login \
  --vnc-grab-keyboard off
```

## 測試與選擇

```bash
./scripts/test-vnc-keyboard-relay.sh
```

該獨立 RFB/Xvfb 測試針對日文 XKB，檢查 21 個 shift 符號和 `你好`：

```text
vnc-symbols=23/23 order=exact target-layout=jp
isolated VNC keyboard acceptance passed
```

真實控制端使用臨時文字框，分別檢查普通數字/標點、`()` 等 Shift 符號、Ctrl+A/C/V/Enter/Backspace，以及實際 IME 中文或日文。不要在密碼框測試。

這項配置不改變桌面 XKB、不重啟 XRDP、不登出 GNOME。UU 物理鍵協議沒有可靠的每連線佈局標識；直接 X11 使用目標會話佈局。XRDP/RFB 可依賴元資料/keysym，手機依賴 Unicode。缺少源佈局時，橋接器無法猜測 `Shift+7` 原意是 `&` 還是 `'`。需要不同佈局時明確選擇客戶端配置或行為軌道，見[輸入軌道（英文／簡體中文）](../zh-Hans/release-tracks.md)。
