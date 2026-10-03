[English](../../security.md) · [العربية](../ar/security.md) · [Deutsch](../de/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Русский](../ru/security.md) · [Tiếng Việt](../vi/security.md) · [简体中文](../zh-Hans/security.md) · [繁體中文](../zh-Hant/security.md)

[日本語ホームに戻る](../../../i18n/README.ja.md)

# セキュリティ

## 権限と隔離

許可されたコンピューターと UU アカウントで使います。通常の UU ログインと GNOME RDP 認証を保ち、無人起動は元に戻せる GDM/systemd 設定として扱います。

- ログイン済み Unix ユーザーとユーザー unit で動作し、専用環境は `~/.local/share/wineprefixes/uu-remote` です。
- Xvfb は Xauthority を使い TCP を待ち受けません。broker pipe は同じ Wine wineserver 名前空間に限定します。
- 任意の X11/端末 helper は一時 IPv4 loopback と起動ごとの 256-bit token を使います。runtime 0700、端末引継ぎ 0600、shell は最大四つです。
- 管理 VNC は単独パスワードなしの IPv4 loopback で、一つの UU 窓と関連 popup だけを共有し、viewer 終了時に閉じます。
- Mac の現デスクトップは認証済み loopback VNC を SSH 転送します。古典 VNC 認証ファイルは難読化で、0600 と SSH 境界を保ちます。
- FreeRDP は 127.0.0.1 だけに接続し GNOME 証明書の SHA-256 を固定します。GNOME の LAN 待受は別設定なので、ファイアウォールと別の強いパスワードで管理します。
- sudo は依存パッケージ、GDM、グループ、root の復元記録に使用します。

起動器は GNOME RDP を選択セッションのバスへ一時移し、終了時に以前のサービス状態を戻します。既存 socket/lock の固定 display は使いません。

## 認証情報と私有データ

インストーラーはパスワードを表示せず secret-tool で login keyring に保存します。FreeRDP は標準入力で受け取り、変数を消去し、引数や unit に保存しません。VNC の認証は最初の八バイトというプロトコル制約があり、Mac keychain には対応する値を保存できます。

無人起動では keyring パスワードを systemd-creds --with-key=tpm2 で暗号化します。保存するのは暗号文だけで、runtime credential を oneshot が D-Bus に渡します。tss と一時 TPM ACL は撤回時に追加分を戻します。Ubuntu 24.04/GNOME 46 で確認した私有インターフェースなので、更新後に unlock unit を確認します。

UU の token とアカウント状態は専用環境に残ります。入力ログは件数・型・flags・route・結果・error、端末ログは readiness・session/size・拒否・終了を記録し、キー値、Unicode、座標、clipboard、コマンドや出力を保存しません。

意味的文字は最大 2,048 records で UTF-16/UTF-8 をメモリー変換し、対象 xclip の owner を確認して貼り付けます。成功後の文字は対象 clipboard に残ります。legacy/auto は表現可能な文字をキー化し、rdp-public/auto は原文を保持します。RDP cliprdr は通常 clipboard、VNC helper は対象への一方向です。[入力設計](architecture.md) と [文字経路（English）](../../semantic-text-and-clipboard.md) を参照します。

## バイナリーと更新

[UU 4.42](../../../patches/uu-remote-4.42.0.2770.json) は原本/変更後の完全 SHA-256、size、unique signature、offset、等長置換を記録します。patch-gameviewer.py は approved のみ受け付け、原本を GameViewerServer.exe.uu-original に保存します。旧 manifest は旧版専用で、draft は独立の意味レビュー後に承認します。Healthd も身元を検査します。

FreeRDP/SDL は [固定 profile](../../../patches/freerdp-sdl-product.json) とソース・recipe・pins・provenance を一致させます。[ソース構築](source-build.md) を参照してください。旧 libei 修正は監督下 GRD のみで、26.04 のシステムライブラリを置換しません。

stage-uu-release.sh は静的展開を優先します。明示的 --sandbox-install はネットワークなし Bubblewrap または指定した root-managed systemd を使い、実 home を隠して書込先を制限します。さらに隔離するなら VM を使います。[上流保守（English）](../../upstream-maintenance.md) に手順があります。

## 運用上の境界

Wine は同じ Unix ユーザー内の強い sandbox ではありません。UU は閉じた遠隔入力ソフトで、自動更新やクラウドの挙動も変わります。強い分離には別 Unix アカウントを使い、OS/Wine/UU/GNOME を更新します。

[自動更新](automatic-updates.md) は正常な中継を再起動しません。修復は私有 clone の draft で、承認や配置を自分でしません。自動適用は明示的選択、exact installer/server hash、commit 済み acceptance、操作側/ログイン保持、270 秒以上の安定確認が一致した後です。全 Wine をコピーしてアカウントを byte 比較し、失敗や中断は復元して自動再試行を止めます。XRDP は変更しません。

GDM 自動ログイン後は物理アクセス者もアカウントを使えます。TPM は暗号文の他機への持ち出しを防ぎ、ログイン済み画面は保護しません。LUKS 等は起動前入力が必要です。公開するのはソース、説明、hash と必要な分析結論です。実行ファイル、prefix、registry、秘密情報、device ID、現場ログや私有画面は含めません。
