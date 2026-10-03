[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[ホーム](../../../i18n/README.ja.md)

# Plus の変更点

![上流の基盤、Plus の変更と設計上の見込み](../../images/uu-plus-evolution-en.png)

[編集可能な SVG](../../images/uu-plus-evolution-en.svg)

[Lachlan Chen のブリッジ](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)の [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a) を参考とします。Wine 分離、GNOME 中継、入力、管理、サービスは上流から継承します。

## 日常の使い方から見る変更

| 項目 | 上流の基盤 | Plus の変更 | 使い方 |
| --- | --- | --- | --- |
| ホスト | Ubuntu 24.04 と分離 libei バックポート | Ubuntu 26.04/GNOME 50 対応と libei の選択。24.04 も対象 | ホストに合うプラットフォーム・ビルドガイドを読む |
| Windows UU | 既定 4.33.0.8907 と確認済みマニフェスト | 確認済み 4.42.0.2770 を既定に | UU の版に合うマニフェストを選ぶ |
| 画面サイズ | 保存済み解像度と RDP サイズ変更 | 最大 4K の 4 設定、全体表示、サイズ復元 | 720p、1080p、1440p、4K を選び現在の画面サイズを確認 |
| スマホ文字 | IME 正規化と Unicode 貼り付け | Plus 入力経路の改善と公開 FreeRDP 文字経路 | 中国語、コード、複数行の文字を入力 |
| クリップボード | RDP クリップボードと Unicode 処理 | SDL ソースで背景確認、所有者変更、形式キャッシュを修正 | 中継が背後でも現在の文字をコピー＆ペースト |
| 管理 | 専用ウィンドウ表示とフォーカス復帰 | 管理・ポップアップの独立キャプチャとビューア再利用 | UU アカウントや設定を開き、デスクトップに戻る |
| カーソル | 任意の固定サイズ保護 | テーマの代替と起動修正。既定は無効 | 必要に応じてカーソル保護を有効に |
| 操作 | マウス・キーボードによるデスクトップ操作 | GNOME デスクトップ・一覧操作を接続 | 操作端のデスクトップ操作を GNOME 側へつなぐ |
| ツール | 中継の依存関係と UU コマンド | 画質/VNC/FreeRDP/Openbox、個別フォント・DPI・認証 | 目的に合うツールを専用設定で開く |
| ビルド・復元 | 固定 nightly SDL/WinPR とサービス再接続 | 固定修正ソース、実行時確認、画面設定とビューアの復元 | 対応する中継を準備し、保守時も設定を保持 |

## 実装の分類

- スマホ文字：Plus 入力経路の改善 — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- クリップボード：SDL ソース修正 — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- 管理：独立キャプチャとビューア処理 — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- ツール：新しいデスクトップ統合 — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## 入力経路

新規 RDP インストールは `rdp-public` を選び、broker から FreeRDP 公開 API へ入力を渡します。自動モードの Unicode は ASCII も含めて原文貼り付け、物理キーは別経路です。更新は経路を保持します。`legacy` は表現できる文字をキー、CJK と改行を貼り付けで送り、未設定起動も `legacy` です。

FPS と遅延を比較するときは、版、元解像度、画質/FPS、ビットレート、ネットワーク、負荷を固定し、測定方法を記録します。[測定ガイド](performance-evidence.md)を参照してください。
