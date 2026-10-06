[English](../CHANGELOG.md) · [العربية](CHANGELOG.ar.md) · [Deutsch](CHANGELOG.de.md) · [Español](CHANGELOG.es.md) · [Français](CHANGELOG.fr.md) · [日本語](CHANGELOG.ja.md) · [한국어](CHANGELOG.ko.md) · [Русский](CHANGELOG.ru.md) · [Tiếng Việt](CHANGELOG.vi.md) · [简体中文](CHANGELOG.zh-Hans.md) · [繁體中文](CHANGELOG.zh-Hant.md)

[首頁](README.zh-Hant.md)

# 更新紀錄

橋接發布標籤與批准的 Windows UU 版本分開管理。

## Plus 0.2.0-work — 2026-10-06

- **終端斷線後接著用：**可選 `persistent` 模式讓重連回到原 shell、目錄與工作，安裝預設仍為 `fresh`。

- **一次接收多個檔案：**在控制端複製普通檔案，接收完成後貼到 Ubuntu 檔案管理器；顯示實際位元組進度。

- **圖片格式相容：**保留原始 PNG 與 DIBV5／DIB，可選 Mac 助手為 PNG 補充 TIFF。

- **原生擷取探索：**可選 CPU／GPU 原型目前仍屬實驗，不包含在預設安裝。

僅支援普通檔案入站；目前 Ubuntu → Mac 圖片同步與雙控制端焦點仍待解決。

[CPU (MIT)](../vendor/uur-native-cpu/NOTICE) · [GPU (AGPL-3.0)](../vendor/uuway-gpu-component/README.md) · [使用與更新說明（英文）](../docs/updates/2026-10-06.md)

## Plus 0.1.0 — 2026-10-03

Plus 基於 MIT 許可的上游橋接。

### 新增

- 桌面尺寸：最高 4K 的四檔選擇、完整桌面適配與儲存尺寸恢復。
- 手機文字：Plus 輸入路徑迭代與公開 FreeRDP 文字路徑。
- 管理視窗：管理視窗／彈窗獨立擷取，重用檢視器連線。
- 游標：主題游標回退與啟動修正，預設維持關閉。
- 桌面動作：接入 GNOME 桌面／概覽動作。
- 桌面工具：整合畫質／VNC／FreeRDP／Openbox 入口、局部字型、DPI 與認證輸入。
- 建置與恢復：固定修補原始碼建置、執行期檢查與檔位／檢視器恢復。
- 十一種語言的首頁和核心指南，以及可編輯的架構、遷移和對比圖。

### 修復

- 剪貼簿：SDL 原始碼修補背景更新、剪貼簿歸屬變更與格式快取。
- 管理視窗重開、UTF-8 標題、所屬彈窗擷取與關閉檢視器後的焦點返回。
- 手機文字提交、輸入鉤子初始化、部分輸入處理與原生終端限時退出。
- 完整畫布滑鼠映射、獨立尺寸／位元率設定、手動 RDP 連線保護和可恢復工具啟動器。

### 相容

- Ubuntu 24.04 / GNOME 46 · Ubuntu 26.04 / GNOME 50 · x86-64。
- Windows UU：預設採用已審核的 4.42.0.2770。

## 繼承上游 — 未發布

上游提供 Unicode 語義剪貼簿交易、輸入法編輯與長語音批次、實體鍵盤配置、認證主機輸入、網路／執行期診斷、Wine 藍牙驅動隔離和無人值守連線恢復。

## 上游0.2.0 — 2026-07-18

網路診斷／來源摘要／適配器；GNOME/libei描述符恢復、限額／Keyring／PythonGI；手機文字節奏、實體按鍵無延遲、原始 `SendInput`優先／代理／焦點確認；X11/XTEST／分類遙測／清理／網路復原；XRDP與無人值守說明。

## 上游0.1.0 — 2026-07-17

首版Wine/UU/Xvfb/SDLFreeRDP/GNOME、代理／重注入／服務；保存設定／審核／還原／RDP剪貼簿；可選TPM2/GDM；手機規範、Wayland/Xorg/XRDP匯流排、Wine事件相容、前綴清理。

原版發布：[v0.1.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.1.0) · [v0.2.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.2.0)。完整上游歷史與原始驗證紀錄：[CHANGELOG.md — e2854e2b](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b/CHANGELOG.md)。
