[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Русский](../ru/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [简体中文](../zh-Hans/automatic-updates.md) · [繁體中文](../zh-Hant/automatic-updates.md)

[日本語ホームに戻る](../../../i18n/README.ja.md)

# 自動チェックと再開できる修復

保守システムは中継を止めない上流チェック、私有ソース修復、明示的な適用を分けます。通常のチェックは動作中のデスクトップを置き換えません。

## 有効にする

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review \
  --reasoning-effort medium \
  --auto-promote-accepted
```

Plus 独自のリリース履歴は `v0.1.0` から始まります。日付付きの入力トラックタグは上流プロジェクトの履歴であり、この独立リポジトリには含まれません。通常のインストールには不要です。Plus のタグがローカルに存在してから、`--track v0.1.0 --branch main` で明示的に選びます。設定ツールの既定値は今も古いトラック名なので、存在しないタグは拒否されます。

リリースタグをチェックアウトした後、通常のソース取得付き更新を行う前に `git switch main` を実行します。保守用ブランチは `origin/main`、再インストール用の明示的なタグは `v0.1.0` です。更新中も固定タグのソースを保持する場合は `--no-pull` を指定します。

--auto-promote-accepted は完全な maintainer acceptance のある exact version を後から適用可能にし、Codex の自作 draft は配置しません。無効なら準備状況の報告のみです。

model/reasoning は ~/.config/uu-remote-bridge/updater.json に明示保存します。同じユーザーで Codex にログインしておきます。command -v codex の絶対パスを保存し NVM/systemd PATH に対応します。変更は --codex /absolute/path/to/codex です。修復前に含まれる使用枠を照会し、全 window が codex_max_used_percent（既定 20）以下の時だけ実行します。購入枠/reset credits は使わず、不明なら一時間以上延期します。

## タイマー

| timer | 時間 | 処理 |
| --- | --- | --- |
| uu-remote-update-check.timer | 毎日 04:20 前後＋ランダム、起動 12 分後 | endpoint と metadata |
| uu-remote-repair-monitor.timer | 起動 7 分後、終了から 15 分ごと | 状態、task 再開、明示的受入処理 |

Persistent=true の daily は停止中に逃した一回を次回起動で行います。対話端末は不要です。

```bash
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
```

## チェックと修復

通常は official redirect を HEAD し、一時 query key を除去して完全な版を比較します。同版は一度 SHA を確定し ETag/size/sidecar を再利用、古い endpoint を更新扱いしません。monitor は 20 秒間隔で二度異常を確認して記録し分析を予約します。既定では Wine/RDP/UU を停止しません。

--auto-reinstall は別の選択で、確認済み不調で一度 restart、その後既知 track を build/test して再インストールできます。この有効化例では選びません。未知版は downloads に最大 1 GiB、静的展開後 tasks の私有 clone で draft/test を作ります。[保守契約（English）](../../automated-repair-agent-handoff.md) を 0600 context に保存します。展開不能 wrapper は自動実行せず、明示的 --sandbox-install の無通信 Bubblewrap/systemd を使います。Codex は live prefix、sudo、push、自身の binary approval を扱いません。[上流保守（English）](../../upstream-maintenance.md) の独立確認を行います。

## 受け入れ済み版のログイン保持

公式 version と完全 installer hash が fetched origin/main の approved manifest に一致し、同 commit の schema-1 acceptance と evidence が installer/server hash に結び付くことが条件です。disposable prefix、実機入力、再接続、冷起動、service restart、新 signaling、ログインを記録し、安定期は 270〜1800 秒。自動適用を明示選択し、活動の静穏時間は既定 45 分です。

runtime と account marker、XRDP 状態を確認し UU だけ停止、全 prefix をコピーし追加 1 GiB の空きを確保します。同 prefix を更新して exact patch を適用し、起動前の registry/アカウントツリーを byte 比較します。driver 初期処理と新 room を待ち、安定期を挟む二回の検査後に確定します。失敗・中断・再起動は旧 prefix を戻して promotion-blocked にし自動再試行を止めます。state/prefix は同じ filesystem、snapshot は保持します。XRDP の開始・停止・再起動はしません。

活動待ちだけを省略する操作：

```bash
uu-remote upgrade apply --now
```

詳細は [再利用できる更新](reusable-upgrade.md)。

## task の再開と状態

0600 の atomic task に候補、track、base commit、context、thread UUID、attempt、phase、JSONL と結果を保存します。thread.started で UUID を保存し、次回は codex exec resume で同じ thread を再開します。UUID がなければ同 context から新規開始。間隔は 15 分から最大 24 時間へ延ばします。schema は [codex-repair-result.schema.json](../../../scripts/codex-repair-result.schema.json)、monitor は別途 full unit suite を実行します。

| 状態 | 意味 |
| --- | --- |
| ready-for-review | ソースとテスト準備、意味レビューと実機受入待ち |
| no-change | 変更なし |
| blocked | 証拠・staging・test・人の判断待ち |
| promotion-waiting-idle | 空き時間待ち |
| promotion-running | prefix 処理中 |
| promoted | ログイン/runtime 検査済み |
| promotion-blocked | 旧 prefix 復元、自動再試行停止 |

設定はパスワード/token を含まず、dir 0700/file 0600。私有 artifact は Git 外です。clone は push URL を無効化し Codex は workspace-write/never、service は NoNewPrivileges=yes。認証にネット接続が必要で VM 相当の隔離ではありません。

## Ubuntu 24.04 sandbox

PrivateTmp/ProtectSystem/ProtectKernelTunables/ProtectControlGroups の namespace を重ねると AppArmor unprivileged_userns が nested bwrap を妨げるため、ユーザーサービスには使いません。codex-sandbox-deferred では distro の bwrap profile を設定します。

```bash
sudo apt install apparmor-profiles
sudo install -o root -g root -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
uu-remote update retry
```

両レイヤーの確認：

```bash
systemd-run --user --wait --pipe --collect \
  --property=NoNewPrivileges=yes \
  /usr/bin/bwrap --die-with-parent --unshare-user --uid 0 --gid 0 \
  --ro-bind / / /bin/true
systemctl --user cat uu-remote-repair-monitor.service
```

probe が成功し、上記の mount namespace が unit にないことを確認します。retry は証拠と checkout を保ち、使えない thread を外して次回新規開始。対応外 phase は拒否します。手動 fallback は installer/server/healthd と backend の記録一致後に取り込みます。ready-for-review から直接配置しません。

## 別の機械と停止

[入力トラック（English）](../../release-tracks.md) を選び、clean tree、同ユーザーの codex login status、再起動後 timer を確認します。updater 状態、session、Wine、keyring やログはコピーしません。以下の末尾二行は無効化の選択肢です。

```bash
git status --short
git switch main
git pull --ff-only origin main
git fetch --tags origin
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/configure-updater.sh status
./scripts/configure-updater.sh disable
# 保守設定と全ての私有状態も削除する場合：
./scripts/configure-updater.sh disable --purge-state
```
