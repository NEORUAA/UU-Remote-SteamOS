[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[日本語 · UU Remote Ubuntu Plus](../../../i18n/README.ja.md)

# トラブルシューティング

## 最初に状態を確認

ソースディレクトリで実行します。ログは `~/.local/state/uu-remote-bridge`、設定は `~/.config/uu-remote-bridge/environment`。報告にはバージョンと症状を添え、アカウントや入力内容は除きます。ソース変更後は再インストールします。

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

## オフライン・再起動後につながらない

公式管理画面で一度ログインし、通常の方法で閉じます。ユーザーサービスとキーリングを確認します。パスワード変更時は `./scripts/configure-unattended.sh enable --replace-credential` で暗号化認証情報を更新します。サーバー終了時の復旧記録も確認します。

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

## 経路を検索したまま

ホストの起動完了を確認します。Wine の古い入力・Bluetooth デバイス記録が起動を遅らせることがあります。修復はレジストリを保存し、専用プレフィックス内の認識済み記録を整理して UU を再起動します。Ubuntu の Bluetooth は保持されます。

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

## 黒画面・白画面・別のデスクトップ

ログイン済み GNOME、RDP リスナー、SDL を順に確認します。XRDP は `--desktop-target xrdp`、物理画面は `physical` を選びます。`--desktop-relay vnc` は X11 用、Wayland は RDP を使います。

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

## 余白・画面切れ・4K が重い

元の画面とキャンバスを比較し、720p、1080p、1440p、4K を選びます。キャンバス、操作側 FPS、ビットレートは別設定です。切り替えは短時間再接続し、失敗時は戻ります。XRDP の動的サイズも確認します。

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

## 映像はあるが入力できない

uu-remote open で管理画面を開き、同じ Wine 環境を別 X 画面に直接起動しません。ビューアを閉じると中継にフォーカスが戻ります。スマートフォンの文字はクリップボード/RDP 貼り付け、物理キーはキーイベントです。更新後は入力注入器を確認します。 最初のクリックで切断する場合は UU SendInput bridge active、UU Wine event-log compatibility active と broker を確認し、`uu-remote restart` で復旧します。

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

## キーが遅い・記号が違う・長時間で悪化

VPN、プロキシ、UU 経路を比較します。stale は過去の接続です。誤った NIC を確認した場合 `--network-interface default` を試し、`all` で戻します。物理キーは `--physical-key-delay-ms 8` を試せますが既定は `0`。記号は Ubuntu 配列に従い、長期悪化は GRD/libei と FD を確認します。

```bash
uu-remote network
ip -4 route show default
```

## カーソルが消える・小さい

保護機能は任意で、既定では無効です。auto はデスクトップサイズに追従し、固定値は 24〜128。`--cursor-guard off` で無効化します。画面全体や Wine DPI の変更は不要です。

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

## UU ターミナルが終了・文字位置がずれる

現在のブリッジを再インストールして確認します。UU では PowerShell を選び、実際は Ubuntu ログイン shell が開きます。位置異常時は新しいセッションを作り、terminal-bridge.log のメタデータを確認します。任意の powershell.exe に置き換えません。

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

## RDP 認証・NLA・SSPI エラー

この検索はパスワードを表示しません。必要ならブリッジ専用キーリング項目だけ消し、再インストールします。FreeRDP、WinPR、DLL は同じ固定バージョンから構築します。

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

## Mac RDP/VNC・Windows App の Configuring

内部 FreeRDP が共有ポートを使用中で、リモートログインは別デスクトップです。実際のループバック VNC ポートを調べ、SSH 転送します。Configuring ではまず Mac の Windows App を開き直し、次に XRDP を確認します。

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

## 定期再起動・音・削除

完全検証は安定性も調べます。UU 音声、Wine PulseAudio、VNC ベルを専用環境内で別々に確認します。削除は先にプレビュー。通常はプレフィックスを保持し、`./uninstall.sh --purge` はアカウント状態も削除します。 `wpctl status` で実際の音声ストリームを特定します。`UURB_UU_AUDIO=system` が互換性の既定値です。専用の無音 ALSA と復元は英語の詳細ガイドにあります。

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

詳しくは [画質](quality-guide.md)、[構築](source-build.md)、[構成](architecture.md)、[入力](adaptive-keyboard-relays.md)、[更新](reusable-upgrade.md)。[工程詳細・履歴（English）](../../troubleshooting.md) にレジストリ、ドライバー、音声、XRDP、ターミナルの説明があります。

## 詳しいガイド

- XRDP とキーボード復旧 · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- 入力の互換性確認 · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- Mac から現在のデスクトップ · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- 物理デスクトップ共有 · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- 終了後の復旧 · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- 操作側エージェント · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- SSH のエージェントメッセージ · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)
