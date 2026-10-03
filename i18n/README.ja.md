<div align="center">

[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

<a href="README.ja.md"><img src="../docs/images/uu-plus-logo.png" alt="UU Remote Ubuntu Plus" width="140"></a>

# UU Remote Ubuntu Plus

**ひらめいたときに接続。開発環境は Ubuntu に。**

エディタ、ターミナル、アプリのセッションは Ubuntu に置いたまま。スマートフォン、Mac、Windows からつないで、好きなときに Vibe Coding。画面を変えても、続きをすぐに書き始められます。

[![Ubuntu 24.04 / 26.04](https://img.shields.io/badge/Ubuntu-24.04%20%7C%2026.04-E95420?logo=ubuntu&logoColor=white)](../docs/i18n/ja/ubuntu-26.04-port.md)
[![GNOME 46 / 50](https://img.shields.io/badge/GNOME-46%20%7C%2050-4A86CF?logo=gnome&logoColor=white)](../docs/i18n/ja/architecture.md)
[![UU Remote 4.42](https://img.shields.io/badge/UU_Remote-4.42.0.2770-00A870)](../patches/uu-remote-4.42.0.2770.json)
[![MIT](https://img.shields.io/badge/License-MIT-2F81F7)](../LICENSE)

<img src="../docs/images/vibe-coding-cross-device-en.png" alt="UU Remote Ubuntu Plus" width="1120">

</div>

Plus は NetEase UU Remote を、ログイン済みの Ubuntu GNOME セッションにつなぎます。
公式 Windows 版 UU は専用の Wine 環境で動作し、ローカル中継が実際のデスクトップを表示します。
UU のアカウントや設定は別の管理ウィンドウから操作できます。
ローカルでも遠隔でも、同じアプリ、ファイル、デスクトップセッションを使えます。

**[Lachlan Chen の UU Remote Ubuntu Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)** を基盤としています。
Plus は新しい Ubuntu と UU への対応、4 段階の画面サイズ、入力・クリップボードの修正、
管理とデスクトップ操作の改善を加えています。

インストーラは x86-64 Ubuntu 24.04 / GNOME 46 と Ubuntu 26.04 / GNOME 50 を対象とし、UU 4.42.0.2770 を使います。新規インストールは 1080p を選択し、任意のカーソル保護は無効です。

11 言語のホームページと技術ガイドから、同じ言語で読み進められます。英語版が原本です。

## セットアップから遠隔操作まで

1. Ubuntu デスクトップにブリッジをインストールします。
2. `uu-remote open` を実行し、管理ウィンドウで UU にログインします。
3. スマートフォン、Mac、Windows の UU からこの Ubuntu に接続します。
4. 画面サイズを選び、いつものデスクトップアプリを使います。

## 機能と改善点

上流はデスクトップ中継、キーボードとマウス、スマートフォン IME の処理、サービス復旧を提供しています。Plus はこの基盤に新しい環境への対応、分かりやすい画質設定、日常操作の改善を加えます。

| 日常の場面 | Plus の改善 |
| --- | --- |
| 新しい Ubuntu と UU | Ubuntu 26.04 / GNOME 50 と UU 4.42 に対応し、Ubuntu 24.04 のインストール経路も維持。 |
| 画面サイズを選ぶ | 720p、1080p、1440p、4K を GUI で切り替え。デスクトップ全体を画面内に収め、保存した設定を復元。 |
| 中国語、コード、コピー＆ペースト | スマートフォンの文字送信とクリップボード更新を修正。新しい文字がデスクトップに届き、コードや複数行テキストの内容を維持。 |
| 接続したまま設定を開く | UU 管理画面とメニューを独立して取得。ビューアを閉じると入力フォーカスが中継に戻る。 |
| 使いやすいローカルツール | 画質、VNC、FreeRDP、Openbox にアクセスし、フォント、DPI、起動処理を改善。 |
| インストールと管理 | 固定したソースから中継をビルドし、インストール前に構成要素を確認。失敗した画面変更を復旧し、削除前に変更をプレビュー。 |

変更内容とバージョンの背景は[上流との比較](../docs/i18n/ja/upstream-comparison.md)にあります。

<img src="../docs/images/experience-refinements-en.png" alt="使い心地と測定" width="1120">

[使い心地と測定](../docs/i18n/ja/performance-evidence.md)

## クイックインストール

GNOME にログインした x86-64 Ubuntu で、まずプロジェクトを取得します。

```bash
git clone https://github.com/llmir/uu-remote-ubuntu-plus.git
cd uu-remote-ubuntu-plus
```

インストールには、確認済みツールチェーンで中継をビルドするか、製品プロファイルに一致する検証済み出力が必要です。中継バイナリは含まれていません。Ubuntu 26.04 には参照ツールの準備手順があり、Ubuntu 24.04 では検証済み出力を再利用します。 [ツールチェーンの準備と中継の再利用](../docs/i18n/ja/source-build.md#reference-toolchain)

ツールまたは対応する出力を準備したら、通常のインストーラーを実行します。

```bash
./install.sh
./scripts/verify.sh --quick
uu-remote open
```

依存関係と互換コンポーネントを準備し、GNOME Remote Desktop とユーザーサービスを設定します。
中継パスワードは GNOME Keyring に保存され、UU のログイン画面が開きます。
再インストールでは保存済み設定とアカウント状態を引き継ぎます。最初から 4K にする場合：

```bash
./install.sh --resolution 3840x2160
```

環境と再現手順は[互換性報告フォーム](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml)から報告できます。

初回は依存ソースのダウンロードとコンパイルが行われることがあります。
[ソースビルド](../docs/i18n/ja/source-build.md)と[セキュリティ](../docs/i18n/ja/security.md)に詳細があります。
NetEase 公式の [uuyc.163.com](https://uuyc.163.com/) から Windows 版 UU を取得します。ブリッジは専用 Wine 環境で実行します。UU には本来のライセンスが適用されます。

## 技術概要

<img src="../docs/images/architecture-premium-v2-en.png" alt="Ubuntu の画面、入力、ローカル UU 管理の経路。" width="1120">

Ubuntu の画面は GNOME RDP から SDL / FreeRDP 中継に入り、UU を通じてコントローラへ届きます。キーボードとマウスは入力ブリッジを通り、同じセッションに戻ります。UU のアカウントと設定は専用のローカル管理画面で操作します。

`uu-remote open` で管理画面を開きます。ビューアを閉じてもブリッジは動き続けます。任意の `uu-remote console` はローカルブラウザ表示を提供します。モジュールと入力経路は[構成](../docs/i18n/ja/architecture.md)をご覧ください。

## 解像度と画質

<img src="../docs/images/quality-controls-cartoon-v2-en.png" alt="Ubuntu canvas and UU controller quality controls" width="1120">

GNOME の **UU Remote 画质与分辨率** を開くか、次を実行します。

```bash
uu-remote quality gui
```

元のデスクトップ全体が画面内に収まり、物理モニターの解像度は維持されます。
別の設定を適用すると短時間再接続し、変更に失敗すると前の設定を復元します。

```bash
uu-remote quality list
uu-remote quality apply 2160p
uu-remote quality status
uu-remote quality guide
```

エンコード品質、FPS、True Color は **UU コントローラ**で設定します。
コンピュータは**コントロールセンター → 画質**、スマートフォンは**操作 → 表示**です。

ビットレート上限は別に設定します。

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` は 20 Mbps の上限、`0` は上限解除です。
画面サイズ、品質、要求 FPS、ビットレートはそれぞれの設定です。
[画質ガイド](../docs/i18n/ja/quality-guide.md)に選び方があります。

## 入力とカーソル

スマートフォン IME の文字送信、コード、複数行テキストはテキスト経路で Ubuntu に届きます。物理キーやショートカットはキーイベントを保持します。Plus は文字送信とクリップボード更新を修正し、日常の入力とコピー＆ペーストを整えます。入力モードは[キーボード中継](../docs/i18n/ja/adaptive-keyboard-relays.md)をご覧ください。

任意のカーソル保護は上流由来です。Plus はカーソル素材とその扱いを改善しています。
有効にするには：

```bash
./install.sh --skip-packages --skip-account-login \
  --cursor-guard on --cursor-size auto
```

`auto` はデスクトップのカーソルサイズに従います。`24` などの固定値は代替カーソルのサイズです。
`--cursor-guard off` で無効にできます。再インストール時は UU が短時間再接続します。

## 日常操作とメンテナンス

```bash
uu-remote status
uu-remote network
uu-remote logs
uu-remote restart
uu-remote stop
```

管理画面は `uu-remote open`、ログインや復旧は `uu-remote login` を使います。
再起動、ログイン、再インストールでは遠隔接続が短時間切れます。

ローカル変更を保存し、ソースを更新して再インストールします。

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

実行コードの変更は再インストール後に反映されます。
`uu-remote upgrade` は[アップグレード](../docs/i18n/ja/reusable-upgrade.md)、
任意の自動メンテナンスは[自動更新](../docs/i18n/ja/automatic-updates.md)を参照してください。

UU アカウント状態を残して削除する場合：

```bash
./uninstall.sh --dry-run
./uninstall.sh
```

`./uninstall.sh --purge` は専用 Wine prefix、中継認証情報、GNOME RDP の有効化も削除します。

## Ubuntu 以外への移植

現在のインストーラは x86-64 の Ubuntu 24.04 と 26.04 を対象としています。[Linux 移植ガイド](../docs/i18n/ja/porting.md)は、今後の移植を 3 層に分けています。

- UU 互換処理、中継、入力のコアを再利用する。
- ディストリビューションのパッケージ、Wine パス、サービスを調整する。
- デスクトップ固有のキャプチャ、入力、表示モード、操作を接続する。

他の GNOME ディストリビューションは既存の連携を多く再利用できます。KDE や Xfce には専用のデスクトップバックエンドが必要です。

## 文書と貢献

- [画質](../docs/i18n/ja/quality-guide.md)、[ビルド](../docs/i18n/ja/source-build.md)、[Ubuntu 26.04](../docs/i18n/ja/ubuntu-26.04-port.md)
- [構成](../docs/i18n/ja/architecture.md)、[セキュリティ](../docs/i18n/ja/security.md)、[トラブルシューティング](../docs/i18n/ja/troubleshooting.md)
- [上流比較](../docs/i18n/ja/upstream-comparison.md)、[測定](../docs/i18n/ja/performance-evidence.md)
- [変更履歴](CHANGELOG.ja.md)、[貢献ガイド](CONTRIBUTING.ja.md)

バージョン、設定、動作を再現する手順を記載してください。

## プロジェクトを支援

**コーヒー一杯で応援していただけるとうれしいです ☕**

UU と Ubuntu の更新に合わせて、Plus の対応も続けていきます。応援は新バージョンの検証、開発ツールやトークンの費用を支え、文字入力、コピー＆ペースト、画質をさらに磨く力になります。

| PayPal | Alipay · CNY | AlipayHK · HKD | WeChat · 中国語 QR | WeChat · HKD |
| :---: | :---: | :---: | :---: | :---: |
| <a href="https://paypal.me/mirmirlin"><img src="../docs/images/support-paypal-en.png" alt="PayPal" width="160"></a> | <a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support-alipay-cny-en.png" alt="Alipay · CNY" width="160"></a> | <a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support-alipay-hkd-en.png" alt="AlipayHK · HKD" width="160"></a> | <a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support-wechat-zh-en.png" alt="WeChat · 中国語 QR" width="160"></a> | <a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support-wechat-en-en.png" alt="WeChat · HKD" width="160"></a> |

<details>
<summary>Alipay・WeChat の支払いコード</summary>

<p><a href="../docs/i18n/ja/support.md#alipay-cny">Alipay CNY</a><br><a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support/alipay-cny.jpg" alt="Alipay CNY" width="240"></a></p>

<p><a href="../docs/i18n/ja/support.md#alipay-hkd">AlipayHK HKD</a><br><a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support/alipay-hkd.png" alt="AlipayHK HKD" width="240"></a></p>

<p><a href="../docs/i18n/ja/support.md#wechat-zh">WeChat 中国語版</a><br><a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support/wechat-zh.png" alt="WeChat 中国語版" width="240"></a></p>

<p><a href="../docs/i18n/ja/support.md#wechat-en">WeChat · HKD</a><br><a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support/wechat-en.png" alt="WeChat · HKD" width="240"></a></p>

</details>

再現手順のある不具合報告、Linux への移植経験、プルリクエストも歓迎します。次のバージョンを一緒に使いやすくしていきましょう。

[UU Remote Ubuntu Plus を応援する](../docs/i18n/ja/support.md)

## 謝辞とライセンス

**[Lachlan Chen の UU Remote Ubuntu Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)** が基盤です。
元の著作権表示と [MIT ライセンス](../LICENSE)を保持しています。
UU と依存ソフトウェアには各自のライセンスと商標が適用されます。
独立したコミュニティプロジェクトです。

決済ブランドのアイコン：[Simple Icons](https://simpleicons.org/)（CC0）。各商標の権利はそれぞれの所有者に帰属します。
