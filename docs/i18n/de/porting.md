[English](../../porting.md) · [العربية](../ar/porting.md) · [Deutsch](../de/porting.md) · [Español](../es/porting.md) · [Français](../fr/porting.md) · [日本語](../ja/porting.md) · [한국어](../ko/porting.md) · [Русский](../ru/porting.md) · [Tiếng Việt](../vi/porting.md) · [简体中文](../zh-Hans/porting.md) · [繁體中文](../zh-Hant/porting.md)

[Startseite](../../../i18n/README.de.md)

# Auf andere Linux-Desktops portieren

x86-64 GNOME ist der nächste Ausgangspunkt: RDP behalten, Installation anpassen. KDE/Xfce benötigen Desktopadapter. Aktueller Installer: Ubuntu 24.04/26.04; weitere Plattformen sind Portierungsziele.

Die Relay-Installation benötigt die exakt überprüfte Toolchain oder eine vorhandene validierte Ausgabe; gewöhnliche APT-Pakete stellen diese Toolchain nicht automatisch bereit. Siehe [Buildvoraussetzungen und Cache-Nutzung](source-build.md).

![Drei Portierungsebenen](../../images/uu-plus-porting.png)

[Bearbeitbare SVG](../../images/uu-plus-porting.svg)

| Ebene | Wiederverwendbar | Anpassung / Quellen |
| --- | --- | --- |
| Kern | Wine/UU-Präfix, Manifest, SDL/FreeRDP, Broker/Plugin, Canvas/Manager | Protokolle erhalten, Unicode/Tasten trennen; [Broker](../../../src/uu_input_broker.c), [RDP](../../../src/freerdp-adapter.c), [Plugin](../../../src/plugin.c), [Capture](../../../src/uu_manager_capture.c) |
| Distribution | Rezept, Checks, Konfiguration/Dienst | Pakete/Pfade/Bibliotheken/Launcher; [Installer](../../../install.sh), [Build](../../../scripts/build-winpr.sh), [Checks](../../../scripts/verify-freerdp-runtime.py), [Dienst](../../../systemd/uu-remote-bridge.service) |
| Desktop | RDP-Ereignisse, Text/Aktionen | Sitzung, Capture/Eingabe, Clipboard, Geometrie, Aktionen; [Start](../../../scripts/uu-remote-bridge), [Text](../../../src/uu_x11_input.c), [Modi](../../../scripts/uu-display-modes.py) |

Öffentliche FreeRDP-APIs nutzen die bestehende Verbindung. Serverwechsel ist vom UU-Windows-Hook unabhängig. Unicode braucht Quell-Clipboard und Einfügen, derzeit X11/Xwayland. Manager bleibt im privaten Wine-X11. [Architektur](architecture.md).

| Plattform | Wiederverwendung / Arbeit |
| --- | --- |
| Ubuntu 24.04/GNOME 46 | Bestehender Installer/Backend, optionaler libei-Backport |
| Ubuntu 26.04/GNOME 50 | Plus-Integration, System-libei, UU 4.42 |
| Debian/GNOME | Kern/Canvas/RDP; Debian-Pakete/Wine, Preflight, Daemon, Bibliotheken; [APT/dpkg](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html) |
| Fedora/GNOME | Kern/Backend; RPM/DNF, Pfade/Berechtigungen; [GRD](https://packages.fedoraproject.org/pkgs/gnome-remote-desktop/gnome-remote-desktop/) |
| Arch/GNOME | Kern/Backend; pacman, Pfade/feste Tools, rolling GNOME/libei; [GRD](https://archlinux.org/packages/extra/x86_64/gnome-remote-desktop/) |
| KDE | Kern/Canvas/Manager; Sitzung/Capture/Eingabe/Ausgänge/Clipboard/Aktionen; [KRDP](https://github.com/KDE/krdp) braucht Auth-/Codec-/Textintegration |
| Xfce/X11 | Kern/Canvas/Manager/X11-Helper; Sitzung/Geometrie/Aktionen; VNC `legacy` als Start |

Paketmanagerwechsel löst nur Installation. Capture, Eingabe, Quellgeometrie und Aktionen müssen verbunden sein.

| Schnittstelle | Aktueller Stand / Port |
| --- | --- |
| Architektur | `x86_64`, AMD64 PE; andere Hosts brauchen AMD64-Ausführung/Checks |
| Pakete | Ubuntu, `apt-get`, `dpkg`, i386, WineHQ Ubuntu; Zielmapping |
| Wine | `/opt/wine-stable/bin/wine`, `wineserver`, `winepath`; konsistente Pfade |
| Tools | MinGW/CMake/Meson/Ninja/Archive fest; übernehmen oder Profil prüfen; [Build](source-build.md) |
| Sitzung/Capture | `gnome-shell`, D-Bus, `/usr/libexec/gnome-remote-desktop-daemon`; auflösen/ersetzen |
| Zugang | Keyring, `secret-tool`, `grdctl`, `org.gnome.desktop.remote-desktop.rdp`; TLS/Dienst getrennt von UU |
| Ausgänge | `org.gnome.Mutter.DisplayConfig`, virtuelle Monitore; Compositor, XRandR unter X11 |
| Text | `uu-x11-input`/`xclip`, `CLIPBOARD`/`PRIMARY`; korrekter Display, natives Wayland-Clipboard |
| Aktionen | `_NET_SHOWING_DESKTOP`, `org.gnome.Shell.OverviewActive`; Ziel-Windowmanager/Status |
| Dienst | `systemctl --user`, grafischer D-Bus; Sitzung/init anpassen |
| Hilfsprogramme | `/usr/bin/xfreerdp`, `xtigervncviewer`, `obconf`, `zenity`; Pfade/Schriften/DPI, interaktive Anmeldung, Relayschutz |

Private Wine/Xvfb-Fläche und physische/virtuelle Ausgänge sind getrennt. Vier Profile beibehalten, Mutter-Quelllogik für KDE/Xfce ersetzen.

1. Eine x86-64-Distribution/Sitzung wählen; OS/Desktop/Wine/UU erfassen.
2. Pakete/Pfade/Bibliotheken/Dienst/Launcher anpassen, Relay prüfen.
3. Capture/Eingabe, Bus, Display, Zugang, Geometrie/Clipboard verbinden.
4. Realen Controller testen: Bewegung/Klick/Rad/Drag, Shortcuts, Unicode, Paste, Neuverbindung, Manager/Popups.
5. Vier Profile, Wiederherstellung, Rücksetzung, Cleanup und Aktionen prüfen.

Mapping/Pfade/Versionen/Ergebnisse beitragen, ohne UU-Binärdateien/Konten. [Vergleich](upstream-comparison.md), [Qualität](quality-guide.md).
