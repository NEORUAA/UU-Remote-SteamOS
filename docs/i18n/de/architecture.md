[English](../../architecture.md) · [العربية](../ar/architecture.md) · [Español](../es/architecture.md) · [Français](../fr/architecture.md) · [日本語](../ja/architecture.md) · [한국어](../ko/architecture.md) · [Tiếng Việt](../vi/architecture.md) · [中文（简体）](../zh-Hans/architecture.md) · [中文（繁體）](../zh-Hant/architecture.md) · [Deutsch](../de/architecture.md) · [Русский](../ru/architecture.md)

[← Zur deutschen Startseite](../../../i18n/README.de.md)

# Architektur

## Zwei Bildflächen und zwei Richtungen

Die offizielle Windows-Anwendung von UU läuft in einem eigenen Wine-Präfix. Der Windows-Kerneltreiber steuert GNOME nicht direkt. Eine private X11-Bildfläche enthält das Relay-Fenster: Bilddaten laufen von Ubuntu zum UU-Controller; Tastatur, Maus und übernommener Text laufen zurück. Das lokale Verwaltungsfenster ist ein eigener Zweig. Die Quellen verwenden das UU-4.42-Manifest und einen festgelegten FreeRDP/SDL-Build.

## Standard und Alternativen

Eine neue Installation verwendet `rdp`, dazu `rdp-public`, Ziel `auto`, 1920 × 1080, `--follow-desktop-resolution off` und Telefontext `auto`. Updates erhalten gespeicherte Werte. Ohne installierte Routenkonfiguration fällt der Launcher auf `legacy` zurück. Vier reguläre Größen sind 720p, 1080p, 1440p und 4K. VNC ist eine ausdrückliche Alternative für X11/XRDP und benötigt `legacy`; es ersetzt keine Wayland-Sitzung.

GNOME Remote Desktop startet am D-Bus der ausgewählten Sitzung. FreeRDP verbindet sich über Loopback, standardmäßig `127.0.0.1:3390`, prüft den TLS-Fingerabdruck und erhält das GNOME-Passwort über Standardeingabe. Xvfb verwendet Xauthority und `-nolisten tcp`. Bei `rdp-public` komponiert XComposite nur das gebundene SDL-Fenster auf den privaten Root; UU erfasst und überträgt dieses Bild.

## Eingabe und Text

Ein versionsgebundener Patch wählt UUs vorhandenen `SendInput`-Pfad. Der öffentliche Broker sendet an die lokale Pipe des Plugins `uurb-full-input`; FreeRDPs Eingabefunktionen liefern die Ereignisse über die bestehende RDP-Verbindung. `/dvc:uurb-full-input` lädt das Plugin, ohne einen neuen serverseitigen Eingabekanal zu verlangen. `legacy` versucht gewöhnliche Eingaben zunächst über Wine und leitet den nicht angenommenen Rest zum Broker. Direkte XTEST-Eingabe ist für X11 optional; unklar zugestellte Ereignisse werden nicht wiederholt.

Physische Tasten bleiben von `KEYEVENTF_UNICODE` getrennt. `rdp-public/auto` überträgt alle Unicode-Übernahmen als wörtlichen Text, auch ASCII. `legacy/auto` verwendet Tastenkombinationen für darstellbaren Text, sonst semantisches Einfügen. Der native Helfer setzt `CLIPBOARD` und `PRIMARY`, prüft neue Eigentümer und liefert `Shift+Insert` über den gewählten Pfad. Die Selektionsbarriere bestätigt die Transaktion; die Zielanwendung braucht weiterhin Fokus und Einfügeunterstützung. Gewöhnliches Kopieren nutzt RDP `cliprdr`. Der VNC-Begleiter sendet nur GameViewer-Text zur Ubuntu-Zwischenablage, ohne Rücklesen oder Einfügetaste.

## Verwaltung und Lebenszyklus

`uu-remote open` erfasst das GameViewer-Fenster und zugehörige Popups per XComposite in einem lokalen TigerVNC-Fenster. Viewer-Eingaben gehen an das jeweilige eigene Fenster. Schließen beendet Sidecars und gibt den Relay-Fokus frei; das UU-Fenster bleibt mapped. Diese Ansicht ist kein Zwischenschritt des Desktopstreams.

Die Qualitätseinstellung verändert nur die private Bildfläche, nicht den physischen Monitor. Vor Änderungen wird Wiederherstellung vorbereitet; Fehler bei der Wiederherstellung werden gemeldet. Der Benutzer-Service beaufsichtigt eigene Kinder und bereinigt nur das eigene Präfix. GNOME übernimmt Wayland-Eingabe; der Adapter ruft FreeRDP, nicht libei direkt auf. Ein älterer libei-Backport ist optional, Ubuntu 26.04 enthält die Systemkorrektur. Terminal und unbeaufsichtigter Start sind eigenständige Pfade.

[Qualität](quality-guide.md) · [Quellbuild](source-build.md) · [Sicherheit](security.md)

![UU / GNOME](../../images/architecture-premium-v2-en.png)

![Video / Input](../../images/uu-plus-data-flow-en.gif)

[PNG](../../images/uu-plus-data-paths-en.png) · [SVG](../../images/uu-plus-data-paths-en.svg)

![UU manager](../../images/manager-premium-en.png)

## Befehle und technische Werte

```text
GNOME -> GNOME Remote Desktop -> loopback RDP -> SDL FreeRDP
  -> private X11 / UU capture -> UU controller
UU controller -> SendInput hook -> broker -> uurb-full-input
  -> FreeRDP input -> GNOME Remote Desktop -> GNOME
GameViewer + popups -> XComposite -> loopback x11vnc -> local TigerVNC
```

## Quellcode und verwandte Themen

- [install.sh](../../../install.sh#L358)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L6)
- [scripts/runtime-settings.sh](../../../scripts/runtime-settings.sh)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1010)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1758)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1437)
- [scripts/uu-manual-plane.py](../../../scripts/uu-manual-plane.py#L155)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1040)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1844)
- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [src/uu_input_bridge.c](../../../src/uu_input_bridge.c#L688)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L1081)
- [src/plugin.c](../../../src/plugin.c#L200)
- [src/freerdp-adapter.c](../../../src/freerdp-adapter.c#L48)
- [src/uu_input_bridge_legacy.c](../../../src/uu_input_bridge_legacy.c#L595)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L1101)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L454)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L641)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1182)
- [src/uu_x11_input.c](../../../src/uu_x11_input.c#L1000)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1266)
- [src/uu_wine_clipboard_bridge.c](../../../src/uu_wine_clipboard_bridge.c#L195)
- [src/uu_x11_clipboard.c](../../../src/uu_x11_clipboard.c#L329)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L1121)
- [src/uu_manager_capture.c](../../../src/uu_manager_capture.c#L464)
- [src/uu_manager_capture.c](../../../src/uu_manager_capture.c#L1090)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L1193)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L622)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L299)
- [scripts/uu-quality.py](../../../scripts/uu-quality.py#L329)
- [scripts/uu-display-modes.py](../../../scripts/uu-display-modes.py#L166)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L199)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1121)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L2207)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L478)
- [systemd/uu-remote-bridge.service](../../../systemd/uu-remote-bridge.service)

Technische Details sind auf Englisch und vereinfachtem Chinesisch verfügbar:

- [native-ubuntu-terminal](../../native-ubuntu-terminal.md) · [简体中文](../zh-Hans/native-ubuntu-terminal.md)
- [unattended-startup](../../unattended-startup.md) · [简体中文](../zh-Hans/unattended-startup.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
