[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[日本語 · UU Remote Ubuntu Plus](README.ja.md)

# UU Remote Ubuntu Plus に貢献する

不具合報告、翻訳、文書、コードを歓迎します。[Lachlan Chen のブリッジ](https://github.com/lachlanchen/uu-remote-ubuntu-bridge) の著作権と MIT ライセンスを保持してください。

## 問題と経路を説明

Ubuntu/GNOME/Wine/UU、画面サイズ、入力経路、再現手順を記載します。Ubuntu の被操作、本機管理、Ubuntu から他機の操作を分けます。小さな変更と測定方法を添え、[互換性報告フォーム](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml)を利用します。

## 開発環境

Ubuntu とシステム Python を使います。以下は構築と隔離テスト用で、実行依存関係は install.sh が管理します。WINEGCC、MINGW_CC、HOST_CC でコンパイラーを選び、一時 Wine/Xvfb を使います。

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

## ソース確認

変更した shell を bash -n で確認し、以下を実行します。厳格な C 警告を維持します。Wine/Xvfb/systemd が必要なテストは実行・省略を記載し、UURB_TEST_SYSTEMD=1 は対応ユーザーバスでのみ使います。

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

## 文書と図

既存の文書テストを実行します。英語・簡体字 SVG は同じ配置です。後半の Node/Sharp コマンドは再描画時だけ使います。画像全体とメタデータを確認し、支払いコードの原本を保持します。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

## 実行環境の検証

許可されたホストにインストールし、短い切断に備えて復旧経路を用意します。完全検証は 270 秒の安定確認を含み、映像・入力・再接続は実機で確認します。専用プレフィックスだけ停止します。

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

## 新しい UU

新実行ファイルは承認済みマニフェスト、完全な SHA-256、同長パッチの説明を必要とします。復元、起動、入力、削除を確認し、専有バイナリや私的ログは含めません。[上流メンテナンス（English）](../docs/upstream-maintenance.md) を参照します。

## 公開ファイル

差分とファイル一覧を確認します。ビルド、プレフィックス、キャッシュ、.omc、認証情報、機器 ID、入力内容を除きます。認証、TLS、マニフェスト検証、復元可能な削除を維持します。

```bash
git status --short
git diff --cached
```

## レビュー

問題、結果、実行した確認を書き、独立レビューを依頼します。設定 FPS は実測ではありません。[画質](../docs/i18n/ja/quality-guide.md)、[Ubuntu](../docs/i18n/ja/ubuntu-26.04-port.md)、[安全](../docs/i18n/ja/security.md) を読み、MIT と著作権を保持します。
