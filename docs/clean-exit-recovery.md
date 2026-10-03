[English](clean-exit-recovery.md) · [简体中文](i18n/zh-Hans/clean-exit-recovery.md)

[English · UU Remote Ubuntu Plus](../README.md)

# Recover after a bridge exit

The user service uses `Restart=always` and a restart delay so an unexpected
clean exit also recovers. An explicit `uu-remote stop` stays stopped.
Finite memory, swap, task and cleanup limits still apply.

## Check service state

```bash
uu-remote status
journalctl --user -u uu-remote-bridge.service -n 60 --no-pager
```

Keep raw journal output private. A running service alone does not establish
that the expected desktop or input path works. Confirm the visible desktop and
controller connection before reporting recovery.

If the service was deliberately stopped, start it without resetting the UU
account or reinstalling the product:

```bash
systemctl --user start uu-remote-bridge.service
./scripts/verify.sh --quick
```

Retain saved desktop, keyboard and account settings. Do not restart GNOME,
XRDP, SSH or unrelated Wine environments to fix an inactive bridge.
If a binary identity check fails, use the normal installation or
[runtime-only refresh](runtime-only-refresh.md); do not suppress validation.

When changing a user unit, keep a rollback copy, run `systemctl --user
daemon-reload` and restart at an agreed disconnect point. Avoid editing an
executing launcher in place. See [troubleshooting](troubleshooting.md) and
[managed upgrades](reusable-upgrade.md) for other failure cases.
