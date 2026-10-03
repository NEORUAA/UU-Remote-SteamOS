[English](../../porting.md) · [العربية](../ar/porting.md) · [Deutsch](../de/porting.md) · [Español](../es/porting.md) · [Français](../fr/porting.md) · [日本語](../ja/porting.md) · [한국어](../ko/porting.md) · [Русский](../ru/porting.md) · [Tiếng Việt](../vi/porting.md) · [简体中文](../zh-Hans/porting.md) · [繁體中文](../zh-Hant/porting.md)

[ホーム](../../../i18n/README.ja.md)

# 他の Linux デスクトップへの移植

x86-64 GNOME が近い出発点で、RDP を維持してインストールを適応できます。KDE／Xfce は独自デスクトップアダプターが必要です。現在は Ubuntu 24.04／26.04、それ以外は移植候補です。

中継のインストールには、正確に一致するレビュー済みツールチェーン、または既存の検証済み出力が必要です。通常の APT パッケージでは、このツールチェーンは自動的に揃いません。[ビルドの前提とキャッシュ再利用](source-build.md)を参照してください。

![移植の3層](../../images/uu-plus-porting.png)

[編集可能 SVG](../../images/uu-plus-porting.svg)

| 層 | 再利用 | 適応／ソース |
| --- | --- | --- |
| 核心 | Wine/UU 分離、マニフェスト、SDL/FreeRDP、ブローカー／プラグイン、画面／管理 | 境界維持、Unicode／キー分離；[入力](../../../src/uu_input_broker.c)、[RDP](../../../src/freerdp-adapter.c)、[プラグイン](../../../src/plugin.c)、[捕捉](../../../src/uu_manager_capture.c) |
| 配布環境 | レシピ、検証、設定、サービス | パッケージ／パス／ライブラリ／起動；[インストール](../../../install.sh)、[build](../../../scripts/build-winpr.sh)、[検証](../../../scripts/verify-freerdp-runtime.py)、[サービス](../../../systemd/uu-remote-bridge.service) |
| デスクトップ | RDP イベント、文字／操作プロトコル | セッション、捕捉入力、クリップボード、元座標、操作；[起動](../../../scripts/uu-remote-bridge)、[文字](../../../src/uu_x11_input.c)、[モード](../../../scripts/uu-display-modes.py) |

FreeRDP 公開 API は既存接続を使い、サーバーは UU Windows hook と別に変更できます。Unicode は元デスクトップのクリップボード／貼付が必要で現在 X11/Xwayland。管理画面は Wine 私有 X11 に残ります。[構成](architecture.md)。

| 環境 | 再利用と作業 |
| --- | --- |
| Ubuntu 24.04/GNOME 46 | 既存インストール／後端、libei backport 可 |
| Ubuntu 26.04/GNOME 50 | Plus 統合、system libei、UU 4.42 |
| Debian/GNOME | 核心／画面／RDP、Debian パッケージ／Wine、事前検査／daemon／検出；[APT/dpkg](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html) |
| Fedora/GNOME | 核心／後端、RPM/DNF／パス／権限；[GRD](https://packages.fedoraproject.org/pkgs/gnome-remote-desktop/gnome-remote-desktop/) |
| Arch/GNOME | 核心／後端、pacman／パス／固定ツール／更新追従；[GRD](https://archlinux.org/packages/extra/x86_64/gnome-remote-desktop/) |
| KDE | 核心／画面／管理、KDE セッション／捕捉入力／出力／文字／操作；[KRDP](https://github.com/KDE/krdp) は認証／codec／文字統合が必要 |
| Xfce/X11 | 核心／画面／管理／X11、セッション／元座標／操作、VNC `legacy` が出発点 |

パッケージ管理変更はインストールだけです。捕捉、入力、元座標、デスクトップ操作をすべて接続します。

| 接点 | 現在の実装と変更 |
| --- | --- |
| アーキテクチャ | `x86_64`、AMD64 PE；他は AMD64 実行／検証 |
| パッケージ | Ubuntu、`apt-get`、`dpkg`、i386、WineHQ Ubuntu；対象へ置換 |
| Wine | `/opt/wine-stable/bin/wine`、`wineserver`、`winepath`；起動／清理で統一 |
| ビルド | MinGW/CMake/Meson/Ninja／固定依存；一致または新プロファイル；[説明](source-build.md) |
| セッション | `gnome-shell`、D-Bus、`/usr/libexec/gnome-remote-desktop-daemon`；探索または交換 |
| 資格情報 | Keyring、`secret-tool`、`grdctl`、`org.gnome.desktop.remote-desktop.rdp`；UU アカウントと分離した TLS／サービス |
| 出力 | `org.gnome.Mutter.DisplayConfig`、仮想画面；対象 compositor／X11 XRandR |
| 文字 | `uu-x11-input`/`xclip`、`CLIPBOARD`/`PRIMARY`；正しい display、Wayland 専用 API |
| 操作 | `_NET_SHOWING_DESKTOP`、`org.gnome.Shell.OverviewActive`；対象 WM と状態確認 |
| サービス | `systemctl --user`、GUI D-Bus；対象 session/init |
| ツール | `/usr/bin/xfreerdp`、`xtigervncviewer`、`obconf`、`zenity`；パス／フォント／DPI／対話認証／中継保護 |

私有 Wine/Xvfb 画面と物理／仮想出力は別。4 設定を保持できれば保持し、KDE/Xfce は Mutter ロジックを置換します。

1. x86-64 OS／session を1つ選び OS／desktop／Wine／UU を記録。
2. パッケージ、パス、ライブラリ、サービス、起動を適応し中継を検証。
3. 捕捉入力、bus、display、資格情報、座標、clipboard を接続。
4. 実操作端で移動／クリック／ホイール／ドラッグ／ショートカット／Unicode／貼付／再接続／管理とポップアップ確認。
5. 4 設定、保存復元、失敗回復、終了清理、デスクトップ／概要を確認。

UU バイナリやアカウントを含めず、対応表・パス・版・操作結果を提供してください。[比較](upstream-comparison.md)、[画質](quality-guide.md)。
