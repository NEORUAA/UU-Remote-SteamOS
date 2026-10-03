[English](update-handoff.md) · [简体中文](i18n/zh-Hans/update-handoff.md)

[Home](../README.md)

# Updating an installation

Keep local source edits and account state before updating. Do not discard a dirty worktree. Read [the upgrade procedure](reusable-upgrade.md) when using
managed updates, or [runtime-only refresh](runtime-only-refresh.md) when the
approved UU release remains unchanged.

## Source update

From your source checkout, inspect `git status --short`, retain local changes
and update only to a reviewed revision. Then run:

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

Installation briefly reconnects UU. Use a local terminal or an independent
management connection if UU is your normal way into the desktop.
Saved settings and the dedicated account state are retained.

## After installation

Confirm the intended desktop, pointer, keyboard and a controller reconnect.
Use the [keyboard compatibility checks](mobile-keyboard-parity-handoff.md) for
phone text, dictation and paste. A nonsensitive sample such as `abcXYZ123,.!?`
is sufficient; do not put real typed content into a public report.

If an update fails, preserve the rollback files and private diagnostics.
Use [troubleshooting](troubleshooting.md); do not reset an account or switch
input tracks merely because a service check failed.

Unknown UU binaries require [upstream maintenance](upstream-maintenance.md)
and independent review before they can be installed. Optional automated
maintenance follows the [maintenance contract](automated-repair-agent-handoff.md).

The upstream release notes belong to
[Lachlan Chen's MIT-licensed bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge);
review the Plus changelog for changes in this project.
