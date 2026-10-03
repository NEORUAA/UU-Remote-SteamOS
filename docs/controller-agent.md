[English](controller-agent.md) · [简体中文](i18n/zh-Hans/controller-agent.md)

[English · UU Remote Ubuntu Plus](../README.md)

# UU Controller CLI and Remote Agent

## Scope

UU Remote 4.34.0.8979 includes `uuyc-cli.exe` beside the official controller.
It talks to the already authenticated UU GUI/server through local IPC. The
bridge installs `uu-agent`, a small launcher that discovers the live private
X display, Xauthority file, Wine prefix, and controller executable from the
systemd service. It does not implement or emulate UU's network protocol.

The observed command surface is:

```text
version
user info|wallet
device list|connect|disconnect|status
cloudpc list|launch|shutdown|connect|disconnect
echo
term
```

This is an observed vendor interface, not a stability promise. Run
`uu-agent cli --help` after every upstream UU update and keep automation
bounded to the commands that the installed version reports.

## Local Wrapper

```bash
uu-agent version
uu-agent list
uu-agent status
uu-agent runtime
```

`runtime` prints paths and a display number, but no account or device
identifier. `list` can print private device names and IDs; do not paste it
into issues, CI logs, or a public repository.

The wrapper also provides private-display diagnostics:

```bash
uu-agent windows
uu-agent focus '网易UU远程'
capture="$(uu-agent snapshot)"
printf '%s\n' "$capture"
```

Captures default to `~/.local/state/uu-remote-agent/captures`, use mode `0600`,
and must stay outside Git.

## Mac Terminal Agent

For an authorized Mac with terminal support, open a shell:

```bash
uu-agent term 'Mac device name' --shell zsh --new-session
```

Non-interactive input is supported by the tested CLI:

```bash
printf '%s\n' \
  'sw_vers' \
  'xcodebuild -version' \
  'xcrun simctl list devices available' \
  'exit' |
  uu-agent term 'Mac device name' --shell zsh --new-session
```

Select an exact device name from the live list. Never hard-code a controller
device ID in a script or document. A terminal session has the authority of the
logged-in remote user; do not send passwords, signing secrets, recovery keys,
or destructive disk commands through reusable scripts.

The current CLI advertises `powershell`, `cmd`, `zsh`, and `bash`. Actual
support depends on the controlled platform and UU host version.

## Terminal into this Ubuntu bridge host

The same UU terminal panel can now control the Ubuntu machine that hosts this
Wine bridge. Select `PowerShell`: the name is the vendor compatibility entry
point, but the installed proxy opens the Ubuntu user's native interactive
login shell. It does not run Wine PowerShell and does not use SSH.

The old immediate `exit 0` was caused by Wine's placeholder
`powershell.exe`, not by UU networking. Installation, security boundaries,
tests, and rollback are documented in
[Native Ubuntu terminal through UU Remote](native-ubuntu-terminal.md).

## GUI Fallback

Use GUI control only when the task inherently needs Xcode, Simulator, System
Settings, keychain approval, or another visual surface:

```bash
uu-agent connect 'Mac device name'
uu-agent windows
uu-agent snapshot
```

Controller success means only that a request reached the local UU process.
Confirm that a remote window appeared before sending input. Coordinates are
resolution- and version-dependent, so scripts must rediscover the current
window and inspect a fresh private screenshot. Never automate account
publication, a purchase, firmware flashing, credential entry, or a destructive
confirmation dialog.
