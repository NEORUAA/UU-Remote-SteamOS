[English](porting.md) · [العربية](i18n/ar/porting.md) · [Deutsch](i18n/de/porting.md) · [Español](i18n/es/porting.md) · [Français](i18n/fr/porting.md) · [日本語](i18n/ja/porting.md) · [한국어](i18n/ko/porting.md) · [Русский](i18n/ru/porting.md) · [Tiếng Việt](i18n/vi/porting.md) · [简体中文](i18n/zh-Hans/porting.md) · [繁體中文](i18n/zh-Hant/porting.md)

[Home](../README.md)

# Porting to other Linux desktops

An x86-64 GNOME distribution is the closest starting point: keep the RDP desktop backend and adapt installation paths. KDE and Xfce need desktop adapters. The current installer targets Ubuntu 24.04 and 26.04; the other platforms below are migration targets.

Installing the relay requires the exact reviewed toolchain or an existing verified output/cache; ordinary APT packages do not automatically provide that toolchain. See [build prerequisites and cache reuse](source-build.md).

![Three layers of a Linux port](images/uu-plus-porting.png)

[Editable SVG](images/uu-plus-porting.svg) · [Chinese diagram](images/uu-plus-porting-zh-Hans.png)

## Three layers

| Layer | Reusable parts | Adaptation | Sources |
| --- | --- | --- | --- |
| Bridge core | Isolated Wine/UU prefix, approved manifest, SDL/FreeRDP relay, input broker, public RDP plugin, private canvas and manager capture | Preserve Windows runtime/protocol boundaries and separate literal Unicode text from physical keys | [broker](../src/uu_input_broker.c), [RDP adapter](../src/freerdp-adapter.c), [plugin](../src/plugin.c), [manager capture](../src/uu_manager_capture.c) |
| Distribution installation | Build recipe, runtime checks, configuration and supervised service | Map packages, Wine/native paths, system libraries, user service and launchers | [installer](../install.sh), [build](../scripts/build-winpr.sh), [runtime checks](../scripts/verify-freerdp-runtime.py), [service](../systemd/uu-remote-bridge.service) |
| Desktop backend | RDP events and text/action protocols | Session discovery, capture/input server, clipboard/paste, source geometry and desktop actions | [launcher](../scripts/uu-remote-bridge), [text/actions](../src/uu_x11_input.c), [canvas modes](../scripts/uu-display-modes.py) |

FreeRDP's public keyboard and pointer APIs use the existing RDP connection. Its server can be adapted independently of UU's Windows input hook. Unicode text also needs source-desktop clipboard ownership and paste; the current helper uses X11/Xwayland. Manager windows stay on the private Wine X11 display. See [architecture](architecture.md).

## Platform choices

| Platform / desktop | Reuse | Main adaptation |
| --- | --- | --- |
| Ubuntu 24.04 / GNOME 46 | Existing installer/backend | Retained path and optional libei backport |
| Ubuntu 26.04 / GNOME 50 | Existing installer/backend | Current Plus integration, system libei and approved UU 4.42 |
| Debian / GNOME | Core, canvas and GNOME RDP design | Debian packages/Wine source, preflight, daemon paths and library detection; [APT/dpkg guide](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html) |
| Fedora / GNOME | Core and GNOME backend design | RPM/DNF packages, Wine/helper paths and service permissions; [GRD package](https://packages.fedoraproject.org/pkgs/gnome-remote-desktop/gnome-remote-desktop/) |
| Arch / GNOME | Core and GNOME backend design | pacman packages, paths, pinned tools and rolling GNOME/libei updates; [GRD package](https://archlinux.org/packages/extra/x86_64/gnome-remote-desktop/) |
| KDE Plasma | Core, canvas and manager capture | KDE session, capture/input, output queries, clipboard and shell actions; [KRDP](https://github.com/KDE/krdp) is a candidate endpoint requiring authentication, codec and text integration |
| Xfce / X11 | Core, canvas, manager capture and X11 helpers | Session, source geometry and shell actions; the X11 VNC branch with `legacy` input is a starting point |

Changing package managers handles only installation. Every desktop adapter needs source capture, input delivery, source geometry and shell actions.

## Current platform interfaces

| Interface | Current implementation | Port requirement |
| --- | --- | --- |
| Architecture | Host `x86_64`, Windows AMD64 PE | Keep x86-64 initially; other hosts need AMD64 execution and runtime checks |
| Packages | Ubuntu check, `apt-get`, `dpkg`, i386 and Ubuntu WineHQ source | Target package mapping, Wine source and architectures |
| Wine paths | `/opt/wine-stable/bin/wine`, `wineserver`, `winepath` | Resolve paths consistently in launch, cleanup and checks |
| Build tools | Pinned MinGW, CMake, Meson, Ninja and dependency archives | Match pinned tools or review a changed profile; [build guide](source-build.md) |
| GNOME session/capture | `gnome-shell`, selected session D-Bus, `/usr/libexec/gnome-remote-desktop-daemon` | Find equivalent paths or another capture/input server |
| Credentials/settings | Keyring, `secret-tool`, `grdctl`, `org.gnome.desktop.remote-desktop.rdp` | Backend credential/TLS/service controls separate from the UU account |
| Source outputs | `org.gnome.Mutter.DisplayConfig` and GNOME virtual-monitor settings | Compositor output information and monitor lifecycle; X11 can use XRandR |
| Text clipboard | `uu-x11-input` / `xclip` own `CLIPBOARD` and `PRIMARY` | Correct display/clipboard bridge; native Wayland needs desktop clipboard interfaces |
| Desktop actions | `_NET_SHOWING_DESKTOP`, `org.gnome.Shell.OverviewActive` | Window-manager desktop/all-windows actions and resulting state |
| User service | `systemctl --user` and graphical-session D-Bus | Adapt startup to the distribution/session/init system |
| Tools | `/usr/bin/xfreerdp`, `xtigervncviewer`, `obconf`, `zenity`; scoped fonts/DPI | Tool paths and launchers, interactive credentials and local-relay protection |

Private Wine/Xvfb canvas modes are separate from physical and virtual source outputs. Keep the four canvas choices where supported; replace Mutter source-display logic for KDE or Xfce.

## First port checklist

1. Choose one x86-64 OS/session and record OS, desktop, Wine and UU versions. GNOME preserves the most interfaces.
2. Adapt packages, paths, libraries, user service and launchers; validate the pinned relay.
3. Connect capture/input, session bus, display, credentials, geometry and clipboard.
4. Test from a real controller: motion, clicks, wheel, drag, physical shortcuts, phone Unicode, paste, reconnect and manager popups/open/close.
5. Exercise all four canvases, saved-size restoration, failed-change rollback, helper cleanup and desktop/overview actions.

Contribute package mapping, interface paths, versions and controller results without UU binaries or account data. [Comparison](upstream-comparison.md) and [quality](quality-guide.md) describe behavior to preserve.
