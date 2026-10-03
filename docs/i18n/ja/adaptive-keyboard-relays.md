[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [简体中文](../zh-Hans/adaptive-keyboard-relays.md) · [繁體中文](../zh-Hant/adaptive-keyboard-relays.md)

[日本語ホームに戻る](../../../i18n/README.ja.md)

# 入力に応じたキーボード中継

同じ Ubuntu X11 に複数プロトコルの入力が届きます。全てをハードウェア scancode にすると記号の意味を失います。

| 経路 | 受け取る情報 | 処理 |
| --- | --- | --- |
| XRDP | 配列メタデータと scancode | クライアントの配列 |
| RealVNC/x11vnc | X11/RFB keysym | modtweak、XKB、一時 keysym |
| UU 物理キーボード | Windows キーイベント | 選択した rdp/x11 |
| UU 電話 IME | Unicode 確定文字 | 物理キーとは別 |

keysym/Unicode の意味を優先し、物理キーだけ配列に依存させます。最近接続した端末を追う全体 setxkbmap ループは使いません。~/.xsessionrc の常時 -layout jp は XRDP の報告配列を上書きします。日本語 Mac 用の変更は明示的操作として残し、毎回ログインで実行しません。IBus、意味的文字、端末は物理 XKB に依存させません。

直接 X11 は表現できる文字をキー組合せにし、中国語・改行・tab・emoji は CLIPBOARD/PRIMARY の同期と一回の貼り付けを使います。口述改行を terminal Enter にしません。rdp-public は Unicode を原文どおり送ります。[構成](architecture.md)、[文字と clipboard（English）](../../semantic-text-and-clipboard.md) を参照します。

## 専用 VNC viewer

対象画面を UU キャンバスへ置く全画面 viewer の既定値：

```text
UURB_VNC_GRAB_KEYBOARD=on
```

-GrabKeyboard=1 で中間 X デスクトップが Shift/Ctrl/Alt/Super を消費するのを防ぎます。典型的には ( が 8、? が /、@ が 2 になったり、Ctrl が効かなくなります。loopback x11vnc のオプション：

```text
-repeat -nobell -modtweak -xkb -add_keysyms
```

modtweak は対象配列の修飾キーを再構成し、-xkb は完全な XKB を調べ、-add_keysyms は未登録の keysym を許可します。IPv4 loopback のみです。専用中継でない窓なら grab を無効化できます。

```bash
./install.sh --skip-packages --skip-account-login \
  --vnc-grab-keyboard off
```

## 比較とテスト

```bash
./scripts/test-vnc-keyboard-relay.sh
```

隔離 RFB/Xvfb で日本語 XKB の 21 個の Shift 記号と「你好」を確認します。

```text
vnc-symbols=23/23 order=exact target-layout=jp
isolated VNC keyboard acceptance passed
```

実際の操作側では一時テキスト欄を使い、数字・句読点、()、Ctrl+A/C/V、Enter、Backspace、IME 日本語/中国語を別々に試します。パスワード欄は使いません。

この設定は XKB を変更せず、XRDP 再起動や GNOME ログアウトもしません。UU 物理入力には接続ごとの信頼できる配列識別がなく、直接 X11 は対象の配列を使います。XRDP/RFB はメタデータ/keysym、電話は Unicode を使います。源配列がなければ Shift+7 の意図を & と ' のどちらか推測できません。[入力トラック（English）](../../release-tracks.md) またはクライアントで明示的に選びます。
