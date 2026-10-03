[English](../../quality-guide.md) · [العربية](../ar/quality-guide.md) · [Deutsch](../de/quality-guide.md) · [Español](../es/quality-guide.md) · [Français](../fr/quality-guide.md) · [日本語](../ja/quality-guide.md) · [한국어](../ko/quality-guide.md) · [Русский](../ru/quality-guide.md) · [Tiếng Việt](../vi/quality-guide.md) · [简体中文](../zh-Hans/quality-guide.md) · [繁體中文](../zh-Hant/quality-guide.md)

[首頁](../../../i18n/README.zh-Hant.md)

# 畫質、解析度與影格率

先在 Ubuntu 選擇畫布，再在控制電腦或手機上調整串流畫質。畫布大小、壓縮畫質、要求影格率與位元率上限是獨立設定。

## 選擇畫布

在 GNOME 應用程式列表開啟 **UU Remote 画质與分辨率**，或執行：

```bash
uu-remote quality gui
uu-remote quality list
uu-remote quality status
uu-remote quality apply 2160p
uu-remote quality guide
```

![Ubuntu 四檔畫布選擇器](../../images/quality-presets.png)

| 檔位 | 畫布 | 適合情境 |
| --- | --- | --- |
| `720p` | 1280 × 720 | 小螢幕或頻寬有限 |
| `1080p` | 1920 × 1080 | 日常使用；首次安裝預設值 |
| `1440p` | 2560 × 1440 | 增加工作空間，像素量低於 4K |
| `2160p` | 3840 × 2160 | 清晰文字與完整 4K 工作區 |

重新安裝保留已儲存的選擇。智慧縮放將整個來源桌面放入畫布，並依相同幾何關係映射滑鼠座標。來源解析度與比例影響結果；畫布不改變 GNOME 實體桌面的解析度，擷取仍可能處理完整來源影像。

選擇器分別顯示儲存的啟動／要求 RDP 尺寸與目前畫布。修改儲存尺寸會短暫重連。重新套用已儲存檔位，可在支援的 RDP 路徑上恢復即時畫布而不必重新啟動中繼；選擇器會核對實際尺寸。修改前啟動還原計時器，橋接無法就緒時恢復舊組態。等待恢復結束後再改下一項。

固定檔位使用安裝預設值 `--follow-desktop-resolution off`。曾開啟跟隨桌面解析度時，請先透過該安裝參數關閉。見[安裝說明](../../../i18n/README.zh-Hant.md)、`./install.sh --help`。測試的 4K 來源放大成 5K 沒有增加細節，在 Mac 上反而較模糊，因此常用選擇最高 4K。標稱 60 Hz 描述虛擬顯示模式，實際串流影格率取決於整條連線。

## 控制端畫質與影格率

電腦開啟**控制中心 → 画质**；手機開啟**操作 → 显示**。支援真彩時，也在控制端選擇。

![UU 原生畫質與影格率選單](../../images/uu-native-quality-menu.png)

此範例來自 Ubuntu 控制 Mac。可用畫質、影格率及色彩選项取決於裝置與編解碼器。畫質影響壓縮和細節，要求影格率設定 UU 的目標更新速率，真彩可改善彩色文字和邊緣。若提示裝置效能限制，選擇可用檔位，用同一段文字和移動場景比較清晰度與回應。

網易資料：[FPS / Super Screen](https://uuyc.163.com/help/superscreen.html) · [True Color](https://uuyc.163.com/features/color/) · [UU](https://uuyc.163.com/help/20241216/40221_1200122.html)。Wine 下超級螢幕／虛擬顯示驅動及 144 FPS 仍待測試。[效能說明](performance-evidence.md)介紹控制端測量。

## 位元率上限

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` 透過 UU CLI 要求 **20 Mbps 上限**，`0` 取消上限。它不設定目標位元率、影格率或畫布尺寸；切換檔位保留該設定。過低上限會減少運動畫面的細節，請在實際連線上比較。

## 游標與桌面動作

可選游標保護在首次安裝時預設關閉。指標過大時可啟用：

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size 24
```

`--cursor-size auto` 跟隨桌面游標大小，固定範圍 24–128 像素。GNOME 與應用程式設定獨立。Dock 使用你的 GNOME 設定。Android 顯示桌面／所有視窗已映射到 GNOME 桌面與概覽，手機按鈕實測待完成。

## 管理視窗與恢復

`uu-remote open` 開啟獨立管理檢視器。放大該視窗：

```bash
UURB_WINDOW_SCALE=2 ./install.sh --skip-packages --skip-account-login
```

支援 `1`（預設）、`1.5`、`2`、`3`，只改檢視器，不改 Wine DPI 或桌面解析度。管理視窗停用剪貼簿交換；桌面複製貼上走中繼。

```bash
uu-remote status
uu-remote quality status
uu-remote network
uu-remote logs
```

使用者服務會重啟故障中繼元件，可能短暫重連。檔位還原恢復設定，執行環境部署有自己的恢復流程。見[疑難排解](troubleshooting.md)、[原始碼建置](source-build.md)。Ubuntu Wine 控制其他電腦的畫質限制另行處理。本機實體螢幕開關與虛擬輸出待測，見[Ubuntu 26.04](ubuntu-26.04-port.md)。手機 → ToDesk → Mac → UU 仍有重複輸入；手機／Mac 直連正常。
