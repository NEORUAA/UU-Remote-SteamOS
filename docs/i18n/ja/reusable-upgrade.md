[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [简体中文](../zh-Hans/reusable-upgrade.md) · [繁體中文](../zh-Hant/reusable-upgrade.md)

[日本語ホームに戻る](../../../i18n/README.ja.md)

# ログインを保つ再利用可能な更新

uu-remote-upgrade はリポジトリ、受け入れ済み UU、ブリッジ更新と確認を一つの処理にし、アカウント、入力設定、XRDP を保持します。


リリースタグをチェックアウトした後、通常のソース取得付き更新を行う前に `git switch main` を実行します。保守用ブランチは `origin/main`、再インストール用の明示的なタグは `v0.1.0` です。更新中も固定タグのソースを保持する場合は `--no-pull` を指定します。

## コマンド

```bash
uu-remote-upgrade status
uu-remote upgrade status
uu-remote upgrade check
uu-remote upgrade apply
uu-remote upgrade apply --now
```

check は確認のみ、apply は保守のアイドル時間を待ちます。--now は短い UU 切断を選び、活動待ちだけを省略します。exact hash、approved manifest、acceptance、全 prefix コピー、byte 単位のアカウント比較、二回の runtime 確認と復元は維持します。未インストール時はソースから：

```bash
./scripts/upgrade-uu-remote.sh apply --now
```

## 実行順序

1. clean な非 detached checkout を要求し、fetch 後は fast-forward のみ。ソース更新後は新しい版から再実行します。
2. 閉じたバイナリー不要の unit suite と shell parse、現在の製品・中継・入力・タイミング・アカウント marker を確認します。
3. official endpoint と完全 hash に一致し、commit 済み acceptance のある版だけを選びます。
4. Wine 全体をコピーしてその場で受け入れ済み installer を実行し、patch を復元、login registry と二つのアカウントツリーを byte 比較して二回確認します。失敗は全体を戻します。
5. 現製品の manifest を選び runtime を別保存、helper/service を更新し environment 設定を保持します。
6. 保守ツールの track/Codex 設定を変えず更新し、uu-agent・ブリッジ・XRDP を確認します。

XRDP は状態照会だけです。PID 変化は報告し、active 状態変化は失敗として扱います。

## 入力設定を保つ

直接 X11 を別途確認したホストの保存例：

```text
UURB_TEXT_KEY_DELAY_MS=8
UURB_PHYSICAL_KEY_DELAY_MS=0
UURB_KEYBOARD_ROUTE=x11
UURB_NETWORK_INTERFACE=default
```

別の機械の推奨既定値ではありません。RDP ホストは自分の track を保持します。quick check は利用者のアプリへ入力しません。更新後に電話の abcXYZ123,.!?、速い物理キー/Enter/Ctrl+A、マウスの移動・クリック・ドラッグ・wheel を確認します。[キーボード中継](adaptive-keyboard-relays.md) を参照してください。

## 復元記録

```text
~/.local/state/uu-remote-updater/tasks/*/promotion/snapshot-prefix
~/.local/state/uu-remote-upgrader/transactions/TIMESTAMP/
~/.local/state/uu-remote-upgrader/latest
```

失敗・中断は promotion-blocked で自動再試行しません。--now は永続終端状態も確認します。同じ版を明示的に再適用できるのは promotion ツールの source commit が変わった場合だけで、古い task は tasks/retired/ に丸ごと移します。

製品更新後にソース runtime 更新が失敗したら UU だけを停止し保存 runtime を戻して起動します。snapshot は操作者用に保持し、timer は消しません。私有設定や閉じたファイルを含むため Git 外に置きます。

## 永続ユーザーバス

ネストした shell の DBUS_SESSION_BUS_ADDRESS と独立して、upgrader/uu-agent は以下を使います。

```text
unix:path=/run/user/UID/bus
```

物理画面、XRDP、VNC、SSH、無人 manager が同じユーザーサービスを照会します。

## 過去の修正と別ホスト

2026 年 7 月の上流 4.34 acceptance 撤回は現在の Plus 4.42 とは別の履歴です。[記録（English）](../../releases/4.34.0.8979-acceptance.md) に冷起動、signaling、実機入力、ログイン、安定性があります。欠けた verifier artifact、GNU PE timestamp/checksum、Type=simple と RDP ready の競合を修正しました。現在は実 daemon listener と選択 helper を最大 45 秒待ちます。旧 PE 比較は指定 timestamp/checksum だけを正規化し、他 byte と更新後 runtime digest は正確に比較します。

別機にはソースだけを移し、その機械の prefix、keyring、updater を保ちます。

```bash
git status --short
git switch main
git pull --ff-only origin main
./install.sh --skip-packages --skip-account-login
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/upgrade-uu-remote.sh check
```

~/.local/bin を PATH に入れます。[入力トラック（English）](../../release-tracks.md) と [自動更新](automatic-updates.md) を読み、そのホストの設定を選びます。
