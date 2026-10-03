[English](../../source-build.md) · [العربية](../ar/source-build.md) · [Deutsch](../de/source-build.md) · [Español](../es/source-build.md) · [Français](../fr/source-build.md) · [日本語](../ja/source-build.md) · [한국어](../ko/source-build.md) · [Русский](../ru/source-build.md) · [Tiếng Việt](../vi/source-build.md) · [简体中文](../zh-Hans/source-build.md) · [繁體中文](../zh-Hant/source-build.md)

[ホーム](../../../i18n/README.ja.md)

# 中継のビルドと再利用

インストーラーは固定された FreeRDP SDL と Plus のクリップボード／サイズ修正をビルドします。[レシピ](../../../vendor/freerdp-sdl-build/)、[ソース固定情報](../../../vendor/freerdp-sdl-build/source-lock.json)、[製品プロファイル](../../../patches/freerdp-sdl-product.json)にリビジョン、アーカイブ、ツールと Windows 実行ファイル 13 個を記録しています。

<a id="reference-toolchain"></a>

## Ubuntu 26.04 の参照ツールを準備する

Ubuntu 26.04 amd64 では、[準備スクリプト](../../../scripts/prepare-build-toolchain.py)が固定された公式 Ubuntu パッケージ 17 個をダウンロードし、コンパイラー／ビルドツールの 14 ファイルを `source-lock.json` と照合します。[パッケージ一覧](../../../patches/reference-build-packages.json)にはバージョン、サイズ、ハッシュが記録されています。スクリプトは取得、専用ディレクトリへの展開、検証を行い、システムへのインストールは行いません。リポジトリのルートで実行します。

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root"
```

`--packages-dir` はパッケージのキャッシュ、`--root` は新規または空の専用ディレクトリを指定します。キャッシュだけで再展開・検証するには、別の空ディレクトリを選んで `--verify-only` を付けます。ネットワークには接続しません。

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root-offline" \
  --verify-only
```

スクリプトはローカルの `.deb` 17 個すべてを含む `sudo apt install` コマンドを表示します。Ubuntu 26.04 でそのコマンドを手動実行し、参照ツールをシステムにインストールします。既存のレシピは固定の `/usr` パスを使います。専用展開先はツール検証用で、ビルド環境の切り替え先ではありません。

続いて通常のインストーラーを実行します。残りのホスト用ビルド依存、WineHQ、GNOME 実行時パッケージを準備し、既存の中継ビルドと配置前の実行環境検証を行います。準備時の検証対象は参照ツールの 14 ファイルです。完全なソースビルドと実行ファイル 13 個は次のフローで確認します。

```bash
./install.sh
./scripts/verify.sh --quick
```

Ubuntu 24.04 では、下の再利用フローで現在の製品プロファイルに一致する検証済み出力を使います。上記の Ubuntu 26.04 パッケージは 26.04 専用です。

## ビルドとキャッシュ

新しいソースからのビルドには、`source-lock.json` に記録されたレビュー済みコンパイラーとビルドツールの、バイト単位で一致するファイルが必要です。通常のディストリビューションの APT パッケージでは、このツールチェーンは自動的に揃いません。

`./install.sh` は依存パッケージを準備し、検証してから中継を置き換えます。`build/freerdp` は現在のプロファイル、レシピ、固定バイナリと来歴が一致するときだけ再利用します。それ以外は `scripts/build-winpr.sh` が新しいソースを 2 ジョブ・900 秒制限でビルドして検証します。

確認済みツールをレシピ指定の `/usr` パスにインストールし、ホストのビルド依存を揃えた後は、中継キャッシュを個別にビルドすることもできます。

```bash
UURB_BUILD_DIR=/absolute/path/to/build-work   ./scripts/build-winpr.sh /absolute/path/to/fresh-output
```

新しい出力ディレクトリを指定してください。作業ディレクトリに固有ソースジョブを作り、稼働中の Wine prefix は使用しません。検証済み出力の再利用：

リポジトリのルートから、既存の出力を現在のプロファイルと照合します。通常のインストーラーがホスト依存を準備します。`--skip-packages` はホスト互換コンポーネントのビルドツール、WineHQ、GNOME 実行時パッケージがインストール済みの場合だけ使います。アカウント設定済みなら `--skip-account-login` も選べます。

```bash
python3 scripts/verify-freerdp-runtime.py --mode build /absolute/path/to/verified/output
```

続いて既存のインストール入口からその出力を再利用します。

```bash
UURB_FREERDP_PREBUILT_DIR=/absolute/path/to/verified/output   ./install.sh
```

レシピ、固定値、現在のプロファイル来歴が必要です。プロファイル変更時はビルド／検証入口を再実行します。生成された記録やチェックサムの書換えでは別バイナリを承認できません。サービス開始前にもコピー結果を検証します。

## 固定入力と結果

FreeRDP/WinPR、SDL 3.2.28、SDL_ttf、OpenH264、FreeType、HarfBuzz と OpenSSL/cJSON/uriparser を固定しています。コンパイル前にパッチ、MinGW／コンパイラー／ツールのハッシュを確認し、変更時はレシピを見直します。

ファイル・マクロ・デバッグの prefix map がパスを正規化します。FreeRDP opaque は初回から OFF、互換 DLL は相対出力名を使い、ローカルのソースパスを埋め込みません。

異なる 2 組のソース／出力ディレクトリで全 13 個のバイトが一致しました。初回／再度の CMake メタデータも一致。事前ビルドなしの完全ビルドは約 700 秒で、900 秒以内に実行環境・来歴検証を完了しました。[画質](quality-guide.md)、[コスト](performance-evidence.md)を参照してください。
