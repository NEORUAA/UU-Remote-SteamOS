[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[首頁](../../../i18n/README.zh-Hant.md)

# Plus 改了什麼

![上游基礎、Plus 變化與設計預期](../../images/uu-plus-evolution-zh-Hans.png)

[可編輯 SVG](../../images/uu-plus-evolution-zh-Hans.svg)

基於 [Lachlan Chen 的橋接](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)，參考 [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a)。Wine隔離、GNOME中繼、輸入、管理與服務繼承自上游。

## 日常使用中的變化

| 領域 | 上游已有 | Plus 改動 | 日常用途 |
| --- | --- | --- | --- |
| 主機相容 | Ubuntu 24.04 與隔離 libei 回移庫 | 適配 Ubuntu 26.04／GNOME 50，選擇系統或回移 libei；保留 24.04 目標 | 依主機環境閱讀平台與原始碼建置指南 |
| Windows UU | 預設 4.33.0.8907 與已審核版本清單 | 預設採用已審核的 4.42.0.2770 | 選擇與 UU 版本相符的清單 |
| 桌面尺寸 | 儲存解析度與 RDP 尺寸調整 | 最高 4K 的四檔選擇、完整桌面適配與儲存尺寸恢復 | 選擇 720p、1080p、1440p 或 4K，查看即時畫布 |
| 手機文字 | 輸入法正規化與 Unicode 貼上 | Plus 輸入路徑迭代與公開 FreeRDP 文字路徑 | 從控制端輸入中文、程式碼和多行文字 |
| 剪貼簿 | RDP 剪貼簿與 Unicode 文字交易 | SDL 原始碼修補背景更新、剪貼簿歸屬變更與格式快取 | 中繼在背景時也能複製貼上目前文字 |
| 管理視窗 | 獨立視窗檢視與焦點返回 | 管理視窗／彈窗獨立擷取，重用檢視器連線 | 在本機開啟 UU 帳號或設定，再回到桌面 |
| 游標 | 選用固定尺寸保護 | 主題游標回退與啟動修正，預設維持關閉 | 需要時啟用選用游標保護 |
| 桌面動作 | 滑鼠鍵盤控制桌面 | 接入 GNOME 桌面／概覽動作 | 將控制端桌面動作連到 GNOME 後端 |
| 桌面工具 | 中繼相依套件與 UU 指令 | 整合畫質／VNC／FreeRDP／Openbox 入口、局部字型、DPI 與認證輸入 | 依工具需求開啟設定與連線視窗 |
| 建置與恢復 | 固定 nightly SDL／WinPR 與使用者服務重連 | 固定修補原始碼建置、執行期檢查與檔位／檢視器恢復 | 準備相符的中繼，維護時保留既有設定 |

## 實作分類

- 手機文字：Plus 輸入路徑迭代 — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- 剪貼簿：SDL 原始碼修補 — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- 管理視窗：獨立擷取與檢視器處理 — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- 桌面工具：新增整合 — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## 輸入路徑

新裝 RDP 選擇 `rdp-public`，代理輸入經 FreeRDP 公開 API。自動模式下，含 ASCII 的 Unicode 提交使用原文貼上，實體按鍵分開處理。升級保留已儲存路徑；`legacy` 對可表示字元使用按鍵，對中文和換行使用貼上。未設定的啟動器也回退為 `legacy`。

比較 FPS 與延遲時，固定主機／控制端版本、來源尺寸、畫質／影格率、位元率、網路和負載，並記錄量測方法，見[量測說明](performance-evidence.md)。
