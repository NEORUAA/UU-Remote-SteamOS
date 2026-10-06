[English](../CHANGELOG.md) · [العربية](CHANGELOG.ar.md) · [Deutsch](CHANGELOG.de.md) · [Español](CHANGELOG.es.md) · [Français](CHANGELOG.fr.md) · [日本語](CHANGELOG.ja.md) · [한국어](CHANGELOG.ko.md) · [Русский](CHANGELOG.ru.md) · [Tiếng Việt](CHANGELOG.vi.md) · [简体中文](CHANGELOG.zh-Hans.md) · [繁體中文](CHANGELOG.zh-Hant.md)

[ホーム](README.ja.md)

# 更新履歴

ブリッジのリリースタグと承認した Windows UU は別に管理します。

## Plus 0.2.0-work — 2026-10-06

- **端末を続ける：**任意の `persistent` モードで再接続時も shell・ディレクトリ・ジョブを維持。既定は `fresh`。

- **複数ファイルを受信：**操作端で通常ファイルをコピーし、受信完了後に Ubuntu のファイル管理へ貼り付け。実受信バイトで進捗表示。

- **画像互換性：**元の PNG と DIBV5/DIB を保持。任意の Mac 補助アプリが PNG に TIFF を追加。

- **ネイティブ取得を探索：**任意の CPU/GPU 原型は実験段階で、既定のインストールには含まれません。

通常ファイルの受信のみ対応。現在の Ubuntu → Mac 画像同期と二つの操作端間のフォーカスは未解決です。

[CPU (MIT)](../vendor/uur-native-cpu/NOTICE) · [GPU (AGPL-3.0)](../vendor/uuway-gpu-component/README.md) · [使い方と更新詳細（英語）](../docs/updates/2026-10-06.md)

## Plus 0.1.0 — 2026-10-03

Plus は MIT ライセンスの上流ブリッジを基盤としています。

### 追加

- 画面サイズ: 最大 4K の 4 設定、全体表示、サイズ復元。
- スマホ文字: Plus 入力経路の改善と公開 FreeRDP 文字経路。
- 管理: 管理・ポップアップの独立キャプチャとビューア再利用。
- カーソル: テーマの代替と起動修正。既定は無効。
- 操作: GNOME デスクトップ・一覧操作を接続。
- ツール: 画質/VNC/FreeRDP/Openbox、個別フォント・DPI・認証。
- ビルド・復元: 固定修正ソース、実行時確認、画面設定とビューアの復元。
- 11 言語のホームページと主要ガイド、編集可能なアーキテクチャ・移植・比較図。

### 修正

- クリップボード: SDL ソースで背景確認、所有者変更、形式キャッシュを修正。
- 管理ウィンドウの再表示、UTF-8 タイトル、関連ポップアップのキャプチャ、ビューア終了後のフォーカス復帰。
- スマホ文字の送信、入力フックの初期化、部分入力の処理、ネイティブ端末の終了待ち時間。
- 画面全体のポインタ対応、解像度とビットレートの独立設定、手動 RDP 接続の保護、復元可能なランチャー。

### 互換性

- Ubuntu 24.04 / GNOME 46 · Ubuntu 26.04 / GNOME 50 · x86-64。
- Windows UU: 確認済み 4.42.0.2770 を既定に。

## 継承した上流 — 未公開

上流から Unicode クリップボード処理、変換中の編集と長い音声入力、物理キーボード配列、認証入力、ネットワーク・実行時診断、Wine Bluetooth 分離、無人接続の復元を継承しています。

## 上流0.2.0 — 2026-07-18

ネットワーク診断／導入ソース摘要と既定／固定アダプター選択、GNOME RDP／libeiの記述子復旧、上限／Keyring／システムPython GI。スマホ文字間隔、遅延なしの物理キー、元 `SendInput` 優先とブローカー／フォーカス確認。認証X11/XTEST、分類計測、旧セッション清理、ネットワーク復旧、XRDP／無人利用資料を追加しました。

## 上流0.1.0 — 2026-07-17

最初の対応Wine/UU/Xvfb/SDLFreeRDP/GNOME、ブローカー／再注入／監督サービス。保存設定、二進監査、ロールバック、RDPクリップボード、任意TPM2/GDM。スマホ入力正規化、Wayland/Xorg/XRDP探索、Wineイベント互換、旧プレフィックス清理。

元リリース：[v0.1.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.1.0) · [v0.2.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.2.0)。完全な上流変更と元の確認記録：[CHANGELOG.md — e2854e2b](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b/CHANGELOG.md)。
