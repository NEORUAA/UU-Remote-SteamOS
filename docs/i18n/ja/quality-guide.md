[English](../../quality-guide.md) · [العربية](../ar/quality-guide.md) · [Deutsch](../de/quality-guide.md) · [Español](../es/quality-guide.md) · [Français](../fr/quality-guide.md) · [日本語](../ja/quality-guide.md) · [한국어](../ko/quality-guide.md) · [Русский](../ru/quality-guide.md) · [Tiếng Việt](../vi/quality-guide.md) · [简体中文](../zh-Hans/quality-guide.md) · [繁體中文](../zh-Hant/quality-guide.md)

[ホーム](../../../i18n/README.ja.md)

# 画質・解像度・フレームレート

Ubuntu 側でキャンバスを選び、操作する PC やスマートフォンで配信画質を設定します。画面サイズ、圧縮画質、要求 FPS、ビットレート上限は独立した設定です。

## キャンバスの選択

GNOME の **UU Remote 画质与分辨率** を開くか、次を実行します。

```bash
uu-remote quality gui
uu-remote quality list
uu-remote quality status
uu-remote quality apply 2160p
uu-remote quality guide
```

![4種類の解像度を選択](../../images/quality-presets.png)

| 設定 | サイズ | 用途 |
| --- | --- | --- |
| `720p` | 1280 × 720 | 小画面・帯域の少ない接続 |
| `1080p` | 1920 × 1080 | 日常利用・新規インストールの既定値 |
| `1440p` | 2560 × 1440 | 4K より少ない画素で広い作業領域 |
| `2160p` | 3840 × 2160 | 細かな文字と 4K 作業領域 |

再インストールでも保存した選択を維持します。スマートサイズ調整は元デスクトップ全体を収め、同じ幾何関係でポインター座標を変換します。元解像度と縦横比が画質に影響します。物理 GNOME 画面の解像度は変えず、キャプチャは元画像全体を処理する場合があります。

選択画面は保存済み起動／要求 RDP サイズと現在のキャンバスを分けて表示します。保存サイズを変更すると短時間再接続します。同じ保存設定の再適用は対応 RDP 経路で中継を再起動せずキャンバスを復元し、実サイズを確認します。変更前に復旧タイマーを起動し、準備できなければ旧設定に戻します。復旧完了を待って次の変更を行ってください。

固定設定は既定の `--follow-desktop-resolution off` を使います。追従を有効にした場合は先に解除します。[インストール](../../../i18n/README.ja.md)、`./install.sh --help` を参照してください。試した 4K 元画像を 5K に拡大しても細部は増えず Mac では悪化したため、通常は 4K が最大です。公称 60 Hz は仮想表示モードの値で、配信 FPS は接続全体に依存します。

## 操作端の画質

PC は **控制中心 → 画质**、スマートフォンは **操作 → 显示**。True Color も対応する操作端で選択します。

![UU 標準メニュー](../../images/uu-native-quality-menu.png)

この例は Ubuntu から Mac を操作したものです。選択肢は機器とコーデックに依存します。画質は圧縮と細部、FPS は要求更新率を設定します。True Color は色付き文字や輪郭を改善できます。性能制限が表示される場合は利用可能な段階を選び、同じ文字と動きで比較します。

NetEase の資料：[FPS / Super Screen](https://uuyc.163.com/help/superscreen.html) · [True Color](https://uuyc.163.com/features/color/) · [UU](https://uuyc.163.com/help/20241216/40221_1200122.html)。Wine 上の Super Screen／仮想表示ドライバーと 144 FPS は未テストです。[測定方法](performance-evidence.md)も参照してください。

## ビットレート上限

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` は **20 Mbps 上限**を要求し、`0` は解除します。目標ビットレート、FPS、サイズは変更しません。解像度変更でもこの値を保持します。厳しい上限は動く画像の細部を減らす場合があります。

## カーソルとデスクトップ操作

任意のカーソル保護は新規インストールで無効です。大きすぎるポインターには次を使います。

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size 24
```

`--cursor-size auto` はデスクトップに追従し、固定値は 24–128 ピクセルです。GNOME／アプリの設定は独立します。Dock は GNOME 設定を使用します。Android のデスクトップ表示／全ウィンドウ表示は GNOME デスクトップ／概要に対応し、実ボタンの確認は今後行います。

## 管理画面と復旧

`uu-remote open` で独立した管理ビューアを開きます。拡大するには：

```bash
UURB_WINDOW_SCALE=2 ./install.sh --skip-packages --skip-account-login
```

倍率は `1`（既定）、`1.5`、`2`、`3`。ビューアのみ変更し、Wine DPI やデスクトップ解像度は変えません。管理画面のクリップボードは分離され、通常のコピーは中継を使います。

```bash
uu-remote status
uu-remote quality status
uu-remote network
uu-remote logs
```

ユーザーサービスが失敗した構成要素を再起動し、短時間再接続することがあります。設定の復旧と実行環境の更新復旧は別です。[トラブル対処](troubleshooting.md)、[ビルド](source-build.md)。Ubuntu Wine から別 PC を操作する場合は別の画質制限があります。物理モニターの切替と仮想出力は[Ubuntu 26.04](ubuntu-26.04-port.md)で今後確認します。スマートフォン → ToDesk → Mac → UU は文字重複が残り、直接接続の入力は正常です。
