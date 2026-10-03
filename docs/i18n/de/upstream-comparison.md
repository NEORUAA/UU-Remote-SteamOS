[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[Startseite](../../../i18n/README.de.md)

# Änderungen durch Plus

![Upstream-Grundlage, Plus-Änderungen und Erwartungen aus dem Design](../../images/uu-plus-evolution-en.png)

[Bearbeitbare SVG](../../images/uu-plus-evolution-en.svg)

Basis: [Lachlan Chens Projekt](https://github.com/lachlanchen/uu-remote-ubuntu-bridge), [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a). Wine-Isolation, GNOME-Relay, Eingabe, Verwaltung/Dienst stammen von dort.

## Änderungen im Alltag

| Bereich | Upstream-Grundlage | Änderung in Plus | Im Alltag |
| --- | --- | --- | --- |
| Host | Ubuntu 24.04 und isolierter libei-Backport | Anpassung an Ubuntu 26.04/GNOME 50, System-libei oder Backport; Ziel 24.04 bleibt | Plattform- und Build-Anleitung für den Host lesen |
| Windows UU | Standard 4.33.0.8907 und geprüfte Manifeste | Geprüfte 4.42.0.2770 als Standard | Passendes Manifest zur UU-Version wählen |
| Bildfläche | Gespeicherte Auflösung und RDP-Größenwechsel | Vier Profile bis 4K, vollständiger Desktop und Größenwiederherstellung | 720p, 1080p, 1440p oder 4K wählen und aktuelle Größe prüfen |
| Telefontext | IME-Normalisierung und Unicode-Einfügung | Überarbeitete Plus-Eingabepfade und öffentlicher FreeRDP-Textpfad | Chinesisch, Code und mehrzeiligen Text eingeben |
| Zwischenablage | RDP-Clipboard und Unicode-Transaktionen | SDL-Quellpatch für Hintergrundprüfung, Besitzerwechsel und Formatcache | Aktuellen Text auch bei Relay im Hintergrund kopieren und einfügen |
| Verwaltung | Eigene Fensteransicht und Fokusrückgabe | Unabhängige Fenster-/Popup-Aufnahme und wiederverwendbarer Viewer | UU-Konto und Einstellungen öffnen, danach zum Desktop zurückkehren |
| Cursor | Optionale feste Cursorgröße | Theme-Fallback und Startkorrekturen; Standard aus | Cursorschutz bei Bedarf aktivieren |
| Desktopaktionen | Maus- und Tastatursteuerung | GNOME-Desktop-/Übersichtsaktionen angebunden | Controlleraktionen mit dem GNOME-Backend verbinden |
| Werkzeuge | Relay-Abhängigkeiten und UU-Befehle | Qualität/VNC/FreeRDP/Openbox mit lokalen Schriften, DPI und Zugangsdaten | Das benötigte Werkzeug mit seinen eigenen Einstellungen öffnen |
| Build und Wiederherstellung | Festes Nightly SDL/WinPR und Dienst-Neuverbindung | Feste Patchquellen, Laufzeitprüfung sowie Profil-/Viewer-Wiederherstellung | Passendes Relay vorbereiten und gespeicherte Einstellungen erhalten |

## Implementierung

- Telefontext: Weiterentwicklung der Plus-Eingabepfade — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- Zwischenablage: SDL-Quellpatch — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- Verwaltung: unabhängige Aufnahme und Viewer — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- Werkzeuge: neue Desktopintegration — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## Eingabepfade

Neue RDP-Installationen wählen `rdp-public` und leiten Broker-Eingaben an die öffentlichen FreeRDP-APIs. Unicode-Text einschließlich ASCII wird im Automatikmodus wörtlich eingefügt; physische Tasten bleiben getrennt. Upgrades erhalten die Route. `legacy` nutzt Tasten für darstellbare Zeichen und Einfügung für CJK/Zeilenwechsel; ohne Konfiguration gilt ebenfalls `legacy`.

Für vergleichbare FPS und Latenz Host-/Controllerversionen, Quellauflösung, Qualität/FPS, Bitrate, Netz und Last festhalten und die Messmethode dokumentieren; siehe [Messanleitung](performance-evidence.md).
