[English](../../source-build.md) · [العربية](../ar/source-build.md) · [Deutsch](../de/source-build.md) · [Español](../es/source-build.md) · [Français](../fr/source-build.md) · [日本語](../ja/source-build.md) · [한국어](../ko/source-build.md) · [Русский](../ru/source-build.md) · [Tiếng Việt](../vi/source-build.md) · [简体中文](../zh-Hans/source-build.md) · [繁體中文](../zh-Hant/source-build.md)

[首頁](../../../i18n/README.zh-Hant.md)

# 建置與重用桌面中繼

安裝器從固定版本原始碼建置 FreeRDP SDL，套用 Plus 剪貼簿與桌面尺寸修補。[建置配方](../../../vendor/freerdp-sdl-build/)、[來源鎖定](../../../vendor/freerdp-sdl-build/source-lock.json)、[產品設定](../../../patches/freerdp-sdl-product.json)記錄版本、封存檔、工具鏈與 13 個 Windows 執行檔。

<a id="reference-toolchain"></a>

## 準備 Ubuntu 26.04 參考工具

在 Ubuntu 26.04 amd64 上，[工具鏈準備腳本](../../../scripts/prepare-build-toolchain.py)會下載 17 個固定版本的 Ubuntu 官方套件，並依 `source-lock.json` 校驗 14 個編譯器／建置工具檔案。[套件清單](../../../patches/reference-build-packages.json)記錄套件版本、大小與雜湊。腳本負責下載、私有解包與校驗，不安裝系統套件。從儲存庫根目錄執行：

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root"
```

`--packages-dir` 指定套件快取；`--root` 必須是新建或空的私有目錄。使用已有快取重新解包並校驗工具時，換一個空目錄，加上 `--verify-only`，過程不會存取網路：

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root-offline" \
  --verify-only
```

腳本會印出含全部 17 個本地 `.deb` 路徑的 `sudo apt install` 命令。在 Ubuntu 26.04 手動執行這條命令，將參考工具安裝到系統。現有建置配方讀取固定的 `/usr` 路徑；私有解包目錄用於校驗工具，不用於切換建置環境。

接著執行一般安裝程式。它會準備其餘主機建置依賴、WineHQ 和 GNOME 執行套件，進入現有中繼建置流程，並在部署前驗證執行環境。工具準備校驗的是 14 個參考檔案；完整原始碼建置及其 13 個執行檔由這條流程檢查：

```bash
./install.sh
./scripts/verify.sh --quick
```

Ubuntu 24.04 可依下方重用流程，使用符合目前產品設定的已有驗證輸出。上述 Ubuntu 26.04 套件僅適用於 26.04。

## 建置與快取

冷原始碼建置需要 `source-lock.json` 中記錄的已審核編譯器和建置工具檔案，位元組身分須一致。一般發行版 APT 套件不會自動提供這套工具鏈。

`./install.sh` 準備套件，替換中繼前驗證執行環境。來源紀錄符合目前設定、配方與固定值才重用 `build/freerdp`。否則 `scripts/build-winpr.sh` 用新來源執行雙工作建置，限時 900 秒，再檢查結果。

已審核工具安裝在配方指定的 `/usr` 路徑，且主機建置依賴齊備後，也可單獨建置中繼快取：

```bash
UURB_BUILD_DIR=/absolute/path/to/build-work   ./scripts/build-winpr.sh /absolute/path/to/fresh-output
```

使用新輸出目錄。腳本在工作目錄建立唯一來源工作，不使用執行中的 Wine 前綴。更新時重用驗證輸出：

從儲存庫根目錄先依目前設定驗證已有輸出。一般安裝程式會準備主機依賴；只有主機相容元件建置工具、WineHQ 和 GNOME 執行套件已安裝時，才使用 `--skip-packages`。已有帳號設定時可選 `--skip-account-login`。

```bash
python3 scripts/verify-freerdp-runtime.py --mode build /absolute/path/to/verified/output
```

再透過現有安裝入口重用該輸出：

```bash
UURB_FREERDP_PREBUILT_DIR=/absolute/path/to/verified/output   ./install.sh
```

快取須符合目前配方、固定執行檔與產品設定來源。設定變更後要重跑建置／驗證入口；編輯產生的收據或校驗檔不能批准其他二進位。服務啟動前也會檢查複製結果。

## 固定輸入與結果

FreeRDP/WinPR、SDL 3.2.28、SDL_ttf、OpenH264、FreeType、HarfBuzz，及 OpenSSL/cJSON/uriparser 套件皆固定。編譯前檢查修補與 MinGW／編譯器／工具雜湊；變更需要審核配方。

檔案、巨集、偵錯前綴映射規範路徑。FreeRDP opaque 自首次設定起 OFF，相容 DLL 使用相對輸出名稱，避免嵌入本機來源路徑。

兩組不同來源／輸出根目錄產生全部 13 個檔案的相同位元組。首次／重複 CMake 中繼資料一致。無預建輸出的完整冷建置約 700 秒，在 900 秒內通過執行環境與來源檢查。見[畫質](quality-guide.md)、[成本](performance-evidence.md)。
