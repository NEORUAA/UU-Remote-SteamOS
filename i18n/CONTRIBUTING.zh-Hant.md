[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[繁體中文 · UU Remote Ubuntu Plus](README.zh-Hant.md)

# 參與 UU Remote Ubuntu Plus

歡迎回報問題、改進翻譯、文件或程式碼。以 [Lachlan Chen 的 MIT 橋接器](https://github.com/lachlanchen/uu-remote-ubuntu-bridge) 為基礎，保留上游署名、技術歷史和許可。

## 說明路徑與問題

提供 Ubuntu、GNOME、Wine、UU 版本、畫布、輸入路由和重現步驟。分清遠端控制 Ubuntu、本機管理、Ubuntu 控制別台裝置。改動小而明確，實測延遲與 FPS 記錄方法。可在[相容性回報表](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml)回報。

## 準備依賴

使用 Ubuntu 和系統 Python。套件供建置及隔離測試，正式安裝由 install.sh 管理。其他編譯器透過 WINEGCC、MINGW_CC、HOST_CC 選擇，不寫入私人路徑。測試使用暫存 Wine 前綴與 Xvfb。

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

## 檢查原始碼

修改的 shell 先執行 bash -n，再做下列檢查。保留嚴格 C 警告。有些測試需要 Wine、Xvfb、systemd 使用者匯流排；如實報告跳過項目，UURB_TEST_SYSTEMD=1 僅在環境具備能力時使用。

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

## 修改文件插畫

文件改動執行現有文件測試。資料流與移植圖的英文、簡中 SVG 共用布局；需要重繪時才執行 Node/Sharp 的後兩行。檢查完整畫面和元資料，收款碼原檔保持不變。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

## 驗證安裝後行為

在授權測試主機安裝，短暫斷線前準備復原途徑。完整驗證含 270 秒穩定階段，畫面、輸入與重連還需實際控制端操作。只停止專用前綴，不執行全域 pkill wine。

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

## 新版 UU

新可執行檔需新審查與獲准清單，核對完整 SHA-256 和每項等長修改，附補丁、還原、冷啟動、輸入與解除安裝結果。不要提交專有二進位、帳號狀態或原始私密日誌。見 [上游維護（English）](../docs/upstream-maintenance.md)。

## 整理公開內容

查看檔案清單與暫存差異。排除建置結果、Wine 前綴、快取、.omc 記錄、憑證、裝置識別和輸入內容；保留認證、TLS、清單檢查和可逆移除。

```bash
git status --short
git diff --cached
```

## 提交協作

交代問題、結果和實際檢查，邀請獨立審閱。設定 FPS 不是實測數字。閱讀 [畫質指南](../docs/i18n/zh-Hant/quality-guide.md)、[Ubuntu 適配](../docs/i18n/zh-Hant/ubuntu-26.04-port.md)、[安全](../docs/i18n/zh-Hant/security.md)，保留 MIT 與原版權。
