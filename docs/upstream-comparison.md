[English](upstream-comparison.md) · [العربية](i18n/ar/upstream-comparison.md) · [Deutsch](i18n/de/upstream-comparison.md) · [Español](i18n/es/upstream-comparison.md) · [Français](i18n/fr/upstream-comparison.md) · [日本語](i18n/ja/upstream-comparison.md) · [한국어](i18n/ko/upstream-comparison.md) · [Русский](i18n/ru/upstream-comparison.md) · [Tiếng Việt](i18n/vi/upstream-comparison.md) · [简体中文](i18n/zh-Hans/upstream-comparison.md) · [繁體中文](i18n/zh-Hant/upstream-comparison.md)

[Home](../README.md)

# What changes in Plus

![Upstream foundations, Plus changes and design expectations](images/uu-plus-evolution-en.png)

[Editable SVG](images/uu-plus-evolution-en.svg)

Plus extends [Lachlan Chen's UU Remote Ubuntu Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge). The reference is [commit `e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a). Wine isolation, GNOME relay, mouse/keyboard bridging, local management and the supervised service come from upstream.

## Features in everyday use

| Area | Upstream foundation | Plus change | What you can do |
| --- | --- | --- | --- |
| Host compatibility | Ubuntu 24.04 and an isolated libei backport | Ubuntu 26.04 / GNOME 50 adaptation with system/backport libei selection; the 24.04 target remains | Use the platform and source-build guide for your host |
| Windows UU | Default 4.33.0.8907 and approved version manifests | Approved 4.42.0.2770 as the default | Select the manifest matching your UU release |
| Desktop size | Saved resolution and RDP resizing | Four visible presets up to 4K, complete-desktop fitting and saved-size recovery | Choose 720p, 1080p, 1440p or 4K and check the live canvas |
| Phone text | IME normalization and Unicode paste | Plus input-path refinements and the public FreeRDP text route | Enter Chinese, code and multiline text from your controller |
| Clipboard | RDP clipboard and Unicode text transactions | SDL source patches for background checks, owner changes and cached formats | Copy and paste current text while the relay is in the background |
| Management | Private window view and focus return | Independent window/popup capture and reusable viewer sessions | Open UU account/settings locally, then return to the desktop |
| Cursor | Optional fixed-size guard | Theme-based fallback and startup fixes; default remains off | Enable the optional cursor guard when needed |
| Desktop actions | Mouse and keyboard desktop control | GNOME desktop/overview action mapping | Connect controller desktop actions to the GNOME backend |
| Desktop tools | Relay dependencies and UU commands | Quality/VNC/FreeRDP/Openbox launchers with scoped fonts, DPI and credentials | Open the relevant tool with its local settings |
| Build and recovery | Pinned nightly SDL/WinPR and supervised reconnect | Pinned patched source build, runtime checks and preset/viewer recovery | Prepare a matching relay and retain saved settings during maintenance |

## Implementation categories

- Phone text: Plus input-path iteration — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../src/uu_input_broker.c) · [freerdp-adapter.c](../src/freerdp-adapter.c)
- Clipboard: SDL source patch — [freerdp-sdl-owner-refresh.patch](../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- Management: independent capture and viewer handling — [uu_manager_capture.c](../src/uu_manager_capture.c) · [uu-remote-console](../scripts/uu-remote-console)
- Tools: new desktop integration — [uu-desktop-tool.py](../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../desktop/uu-tools-fonts.conf)

## Input paths

New RDP installations select `rdp-public`, sending broker input through FreeRDP's public APIs. Automatic Unicode commits, including ASCII, use literal-text paste; physical keys remain separate. Upgrades preserve the saved route. `legacy` sends representable characters as keys and CJK/newlines as paste; an unconfigured launcher also falls back to `legacy`.

For comparable FPS and latency results, keep the host/controller versions, source resolution, quality/FPS, bitrate, network and workload fixed and record the measurement method; see [measurement guidance](performance-evidence.md).
