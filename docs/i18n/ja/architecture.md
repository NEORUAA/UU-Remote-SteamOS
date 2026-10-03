[English](../../architecture.md) · [العربية](../ar/architecture.md) · [Deutsch](../de/architecture.md) · [Español](../es/architecture.md) · [Français](../fr/architecture.md) · [日本語](../ja/architecture.md) · [한국어](../ko/architecture.md) · [Русский](../ru/architecture.md) · [Tiếng Việt](../vi/architecture.md) · [简体中文](../zh-Hans/architecture.md) · [繁體中文](../zh-Hant/architecture.md)

[日本語ホームに戻る](../../../i18n/README.ja.md)

# アーキテクチャ

![Ubuntu の映像を操作側へ、キーボード・マウス・文字を Ubuntu へ。管理画面は別の経路。](../../images/architecture-premium-v2-en.png)

紫の経路は Ubuntu の映像、オレンジの経路は戻りの入力です。管理画面はローカルに表示し、そのウィンドウへ操作を返します。

## 実際のデスクトップと Wine キャンバス

Windows 版 UU は専用 Wine 環境で動作します。Windows のカーネル入力ドライバーは GNOME を直接操作できないため、私有 X11 画面に中継ウィンドウを置き、ユーザー空間の入力を選択した Ubuntu セッションへ渡します。アプリが動く元のデスクトップと中継用キャンバスは別です。UU アカウントの管理画面は遠隔デスクトップの映像経路に直列接続しません。現在は UU 4.42 のマニフェストと固定ソースの FreeRDP/SDL を使い、更新時は保存済み設定を維持します。

## 新規インストールの設定

| 項目 | 既定 | 選択肢 |
| --- | --- | --- |
| デスクトップ中継 | `rdp` | X11/XRDP の `vnc` |
| 入力バックエンド | RDP の `rdp-public` | `legacy`、VNC では必須 |
| 対象 | `auto` | `physical`、`xrdp`、明示的 X display |
| キャンバス | 1920 × 1080 | 720p、1080p、1440p、4K |
| 元画面サイズへの追従 | `off` | `on` |
| 旧経路の物理キー | 中継の `rdp` | X11 の `x11` / `auto` |
| スマートフォンの文字 | `auto` | `keys` / `clipboard` |

既定値は [install.sh](../../../install.sh#L358) が設定します。設定なしで [起動スクリプト](../../../scripts/uu-remote-bridge#L6) を直接実行した場合は legacy に戻ります。rdp-public は RDP 中継用です。VNC はアクセス可能な X11/XRDP を必要とし、Wayland の代わりにはなりません。[runtime-settings.sh](../../../scripts/runtime-settings.sh) は新規と更新の文字入力の送信間隔を区別します。中継の選択と UU 操作側の画質・FPS・ビットレートは独立しています。

## 映像の経路

![デスクトップ映像と戻りの入力経路](../../images/uu-plus-data-flow-en.gif)

[静止 PNG](../../images/uu-plus-data-paths-en.png) · [編集用 SVG](../../images/uu-plus-data-paths-en.svg)

```text
選択したログイン済み GNOME デスクトップ
 → セッション D-Bus 上の GNOME Remote Desktop
 → localhost RDP
 → 固定ソースの Windows SDL FreeRDP / Ubuntu-Desktop-Relay
 → 私有 X11 キャンバス
 → UU GameViewerServer の取得・エンコード・転送
 → スマートフォン、Mac、Windows の UU 操作側
```

起動時に GNOME Shell の display、セッション、D-Bus を発見し、明示した対象がなければ待ちます。GNOME RDP はそのバスで起動し、XRDP の私有バスにも対応します。FreeRDP は既定で `127.0.0.1:3390` に接続し、TLS 証明書の指紋を固定、GNOME 用認証情報を標準入力から受け取ります。これは UU のアカウントパスワードとは別です。[中継の実装](../../../scripts/uu-remote-bridge#L1010) と [SDL 起動](../../../scripts/uu-remote-bridge#L1758) を参照できます。

Xvfb/Openbox が私有画面を用意します。Xauthority と -nolisten tcp を使用し、空いている :20 以降または検査済み display を選びます。Wine 起動前に四つの実モードを登録します。rdp-public の [uu-manual-plane.py](../../../scripts/uu-manual-plane.py#L155) が XComposite リダイレクトを所有し、結び付けた SDL pixmap だけを root に描きます。管理画面は mapped のままですが、その映像には入りません。

```text
選択した X11 デスクトップ → loopback x11vnc → 私有全画面 VNC viewer
 → UU の取得と転送 → UU 操作側
```

VNC は検査済みの独立サービスを再利用するか、自分のサービスを起動します。viewer は画面に合わせ、物理モニターを変更しません。この経路は legacy 入力を使います。

## キーボード・マウスの戻り

[4.42 マニフェスト](../../../patches/uu-remote-4.42.0.2770.json) の版限定パッチがカーネル HID の代わりに既存のユーザー空間 SendInput を選びます。

```text
操作側のキー、ポインター、ボタン、ホイール
 → GameViewerServer / SendInput hook
 → ローカル broker named pipe
 → uu-input-broker.exe / uurb_rdp_backend
 → SDL の uurb-full-input named pipe
 → FreeRDP 公開入力 API
 → 既存 RDP → GNOME Remote Desktop → 選択デスクトップ
```

/dvc:uurb-full-input はプラグインを読み込みます。broker との接続はローカル named pipe で、新たなサーバー入力チャネルは必要ありません。セッションと幾何サイズを結び付け、FreeRDP のイベントループ上で送信します。Wine の前景フォーカスを取り直す方式ではありません。部分送信や不明な結果の後に再送しません。[hook](../../../src/uu_input_bridge.c#L688)、[broker](../../../src/uu_input_broker.c#L1081)、[plugin](../../../src/plugin.c#L200)、[adapter](../../../src/freerdp-adapter.c#L48) が担当します。

legacy は通常の配列を Wine SendInput に渡し、未受理分を broker に渡します。Unicode は直接 broker へ進みます。broker は私有中継を前景にして RDP/VNC に送信します。X11 では --keyboard-route x11/auto を選び、認証済み XTEST helper を使えます。注入前に使用不能なら中継を使い、注入後の曖昧な失敗は再生しません。

## Unicode とコピー・貼り付け

物理キーと IME の確定文字は別です。電話の KEYEVENTF_UNICODE を legacy/auto は表現できるキー組合せへ変換し、中国語、改行、tab などは文字 helper に渡します。rdp-public/auto は ASCII を含む Unicode を原文どおり送り、Caps Lock や配列の影響を避けます。明示的 keys はキー変換です。

broker が有界文字列を認証 loopback へ送り、uu-x11-input が UTF-8 に変換します。xclip が許可された対象 X11/Xwayland の CLIPBOARD/PRIMARY を所有し、新 owner を確認します。rdp-public は plugin/RDP から Shift+Insert を送り、owner/selection-request の完了を確認します。旧 RDP 分離経路は元の選区と私有 SDL の貼り付けキーを使い、直接 X11 は対象側で両方を実行します。アプリのフォーカスと貼り付け対応も必要です。[文字とクリップボード（English）](../../semantic-text-and-clipboard.md) に詳細があります。

通常のコピーは RDP cliprdr を使い、スマートフォン IME とは独立です。固定 SDL パッチは remote cache と sequence/owner を修正します。[ソース構築](source-build.md) を参照してください。VNC の補助経路は一方向です。

```text
操作側 UU clipboard → GameViewer CF_UNICODETEXT
 → uu-wine-clipboard-bridge → 認証 loopback helper
 → 対象 CLIPBOARD / PRIMARY
```

開始時 sequence を基準にし、読み取り前後とも GameViewer owner を要求します。ホストから戻す読み取りや貼り付けキーは行わず、明示的 VNC/X11 でのみ起動します。

## ローカル管理画面

![UU 管理ウィンドウと関連ポップアップの独立取得](../../images/manager-premium-en.png)

uu-remote open は TigerVNC で管理画面を表示します。Wine ウィンドウは同じ専用環境・私有 display に置かれます。

```text
管理ウィンドウと同 owner のポップアップ/モーダル
 → XComposite pixmap / uu-manager-capture.so
 → ウィンドウ限定 loopback x11vnc → ローカル TigerVNC
viewer 入力 → x11vnc → owner/フォーカス確認 → 対応 UU ウィンドウ
```

helper は関連ポップアップを合成し、owner とサイズを再確認します。override-redirect メニューの grab を保持し、ポインター移動でフォーカスを奪い続けません。rdp-public の合成 owner が管理画面を root から除外し、legacy は自分が管理する frame だけをリダイレクトします。

viewer の clipboard と remote resize は無効です。session lock で既存 viewer を再利用し、閉じると sidecar/session/管理フォーカス印を回収して中継のフォーカスを戻します。UU は mapped のままで、layered-window 置換中に最小化しません。Ubuntu から他機を操作する窓は別の UU セッションです。全 root noVNC は明示的診断入口です。

## 解像度・互換性・ライフサイクル

キャンバス操作は私有中継を変えます。[画質ガイド](quality-guide.md) の四段階で保存値と実画面を確認し、変更前に復旧を予約します。失敗時は設定を戻し、固定キャンバスでは追従を切ります。Wayland 入力は GNOME RDP の compositor 経路、adapter は FreeRDP を呼び、libei を直接呼びません。旧 keymap-FD backport は設定された GRD 子プロセスだけに作用し、26.04 は修正済みシステムライブラリを使います。

winpr-sspi-shim.dll は SSPI を転送し Wine/WinPR の私有ハンドルを整えます。UU helper は session token と event-log API を補い、Unix 権限を追加しません。systemd ユーザーサービスがプロセス群を所有し、重要子プロセスの終了で中継全体を再起動、UU 更新後に入力 hook を再結合します。終了は自分の helper と専用 Wine、選区・取得・session 印だけを回収し、以前動いていた GNOME 共有サービスを戻します。

モニターのない Wayland は一時 GNOME 仮想ディスプレイを使い、物理画面復帰または停止後に共有モードを戻します。終端は Windows stdio proxy と認証 loopback forkpty で現ユーザーの shell を開きます。[端末（English）](../../native-ubuntu-terminal.md)、[無人起動（English）](../../unattended-startup.md)、[安全](security.md) を参照してください。
