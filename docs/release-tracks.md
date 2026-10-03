[English](release-tracks.md) · [中文（简体）](i18n/zh-Hans/release-tracks.md)

[← English home](../README.md)

# Input Routes and Reinstall Tags

The bridge has two useful keyboard paths, `rdp` and `x11`, selected by the
saved runtime profile. Plus starts its independent release history at `v0.1.0`.
A release tag names the source used for a known-good reinstall; it does not
select or change the saved keyboard route. Ordinary installation needs no
behavior-track tag.

## Upstream behavior-track history

| Upstream tag | Historical source point | Intended host behavior |
| --- | --- | --- |
| `track-rdp-broker-20260724` | Upstream hardened source with the saved `rdp` profile | Keep the original Wine broker and nested RDP keyboard path on a host where phone text and physical keys are already smooth |
| `track-direct-x11-20260724` | Same hardened source with the saved `x11` profile | Use the authenticated X11/XTEST helper for physical keys and normalized phone text on an X11/XRDP host where accepted keys are lost by the nested RDP conversion |

These dated aliases and the older `track-rdp-broker-v1`,
`track-direct-x11-v1`, `v0.1.0`, and `v0.2.0` belong to the
[upstream repository](https://github.com/lachlanchen/uu-remote-ubuntu-bridge).
They are not retained refs in the independent Plus repository. In particular,
Plus `v0.1.0` names the first Plus release, not the upstream release with the
same version number.

## RDP broker track

Keep the saved `rdp` route when the host already passes all of these checks:

- UU video and pointer input remain stable
- the computer-keyboard panel handles rapid physical keys
- the phone's normal keyboard produces `abcXYZ123,.!?` exactly once
- no direct-X11 helper is needed

This is the known-good profile for the original smooth host. Migrating its
absent `UURB_TEXT_KEY_DELAY_MS` value intentionally preserves the original
unpaced behavior, and its keyboard route remains `rdp`. The upstream
historical source was tagged `v0.1.0` in the upstream repository.

## Direct X11 track

Use the `x11` route only on a confirmed X11 or XRDP desktop after the
broker reports successful input but visible fast keys are still omitted. Its
runtime profile is:

```text
UURB_KEYBOARD_ROUTE=x11
UURB_PHYSICAL_KEY_DELAY_MS=0
```

The helper accepts authenticated loopback requests for supported X11 keyboard,
pointer and semantic-text input. The saved profile selects the physical-key route;
video and UU transport stay on the relay. See [architecture](architecture.md)
for the current input branches. An unavailable helper before injection can
retain the relay route; an ambiguous partial delivery is not replayed.

## Select a Plus reinstall tag

The configurator still derives its default from the saved route using the old
upstream track names. A missing tag is rejected, so explicitly select a Plus
release tag that exists in the local checkout. After the first release:

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable --track v0.1.0 --branch main
```

The configured branch `main` supplies maintenance and repair source from
`origin/main`; the tag `v0.1.0` is the known-good reinstall point. Codex must
be installed and logged in as described in [automatic updates](automatic-updates.md).
For ordinary installation, run `install.sh` first and enable maintenance
separately with the explicit tag. The shortcut `install.sh --automatic-updates`
uses the historical default and cannot select the Plus tag itself.

After a release-tag checkout, switch to `main` before a usual pulling upgrade.
Use `--no-pull` only when deliberately keeping the fixed checkout. The daily
checker does not change keyboard timing or enable X11 routing. Changing the
saved route requires an explicit configuration change and visible input checks.

## Handoff record

Keep this record locally on each computer:

```text
Plus reinstall tag: v0.1.0
Maintenance branch: main
Desktop type: Wayland / Xorg / XRDP
Saved keyboard route: rdp / x11 / auto
Phone keyboard abcXYZ123,.!?: pass / fail
Computer-keyboard rapid alphabet: pass / fail
Quick verifier: pass / fail
```

Do not commit the hostname, UU account, controller identity, raw logs, or other
machine-specific data. Use the
[mobile keyboard parity handoff](mobile-keyboard-parity-handoff.md) when the
same controller behaves differently on two computers.
