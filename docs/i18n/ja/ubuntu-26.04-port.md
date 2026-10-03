[English](../../ubuntu-26.04-port.md) · [العربية](../ar/ubuntu-26.04-port.md) · [Deutsch](../de/ubuntu-26.04-port.md) · [Español](../es/ubuntu-26.04-port.md) · [Français](../fr/ubuntu-26.04-port.md) · [日本語](../ja/ubuntu-26.04-port.md) · [한국어](../ko/ubuntu-26.04-port.md) · [Русский](../ru/ubuntu-26.04-port.md) · [Tiếng Việt](../vi/ubuntu-26.04-port.md) · [简体中文](../zh-Hans/ubuntu-26.04-port.md) · [繁體中文](../zh-Hant/ubuntu-26.04-port.md)

[ホーム](../../../i18n/README.ja.md)

# Ubuntu 26.04 と GNOME 50

Plus は [Lachlan Chen の MIT ブリッジ](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)を x86-64 Ubuntu 26.04／GNOME 50 に拡張し、24.04／GNOME 46 も維持します。Wine 分離、監査済み UU、入力ブローカー、中継、監視サービスを基盤とします。

中継のインストールには、正確に一致するレビュー済みツールチェーン、または既存の検証済み出力が必要です。通常の APT パッケージでは、このツールチェーンは自動的に揃いません。[ビルドの前提とキャッシュ再利用](source-build.md)を参照してください。

| 構成 | 上流参考版 | Plus |
| --- | --- | --- |
| Ubuntu | 24.04 | 24.04／26.04、他は `UURB_ALLOW_UNVALIDATED_UBUNTU=1` |
| Windows UU | 4.33.0.8907 | 承認済み 4.42.0.2770、既存の旧マニフェストも選択可 |
| libei | 分離 1.2.1 backport | 修正済みシステムライブラリ、他は backport |
| 中継 | 固定 nightly SDL／WinPR | 固定ソースとパッチ、[ビルド](source-build.md) |
| CI | 24.04 | 24.04／26.04 を対象、実行ごとに結果確認 |

観察した環境は GRD 50.2／libei 1.5.0。旧ライブラリには `ee27dd5c92e4e9496a36ca2d4112049fe02d2269` を使用できます。`UURB_LIBEI_MODE=system|backport` が選択を保存し、`verify.sh` が読み込みを確認します。WineHQ stable を使います。

## 動作

4 サイズと全体表示、座標対応を提供。新規は 1080p、更新は設定保持。保存サイズ変更は復旧保護付き再接続、同じ設定を再適用すると実キャンバスを復元します。通常再接続と標準メニュー最大 4K はユーザー確認済み。新規 RDP は `rdp-public`、更新は保存経路を維持します。Unicode と物理キーは別操作。管理／ポップアップは別捕捉し、閉じると中継へフォーカスを戻し管理ウィンドウはマップ状態を維持します。デスクトップのクリップボードは有効、管理画面は分離。

| 機能 | 結果 |
| --- | --- |
| スマートフォン／Mac 直接中国語 | 統合作業中にユーザー確認 |
| 通常の文字コピー | 正常とユーザー確認 |
| Mac UU 更新 | 再接続・中国語・貼付正常、4K 感覚は同等 |
| 管理画面の重なり／フォーカス | 解消と報告、一部確認済み |
| Android 操作 | バックエンド双方向正常、実ボタンは今後確認 |
| カーソル | テーマと一部正常、全形状は今後確認 |
| 物理／仮想出力 | この環境では今後確認 |
| スマートフォン → ToDesk → Mac → UU | 小文字 `a` 重複が残る |

VNC／FreeRDP／Openbox は個別の CJK フォント、DPI、資格情報で起動。Dock は GNOME 管理。外向き操作の画質や物理解像度は入向きキャンバスと別です。[画質](quality-guide.md)、[構成](architecture.md)、[比較](upstream-comparison.md)。

## 更新

Plus を `origin` に維持します。

```bash
git remote add upstream https://github.com/lachlanchen/uu-remote-ubuntu-bridge.git
git fetch upstream
```

開発ブランチで上流変更を確認。実行スクリプト／ネイティブ変更後：

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

インストール中は短時間切断し、ソース摘要は更新まで差分を示します。[再利用可能な更新](reusable-upgrade.md)が実行環境復旧、設定ロールバックがキャンバスを担当します。未知 UU ハッシュは自動パッチを停止。新バージョンは意味の確認・マニフェスト・実行検証が必要です。[保守](../../upstream-maintenance.md)。MIT ソースとマニフェストを配布し、UU／依存のライセンスを維持します。
