[English](../CHANGELOG.md) · [العربية](CHANGELOG.ar.md) · [Deutsch](CHANGELOG.de.md) · [Español](CHANGELOG.es.md) · [Français](CHANGELOG.fr.md) · [日本語](CHANGELOG.ja.md) · [한국어](CHANGELOG.ko.md) · [Русский](CHANGELOG.ru.md) · [Tiếng Việt](CHANGELOG.vi.md) · [简体中文](CHANGELOG.zh-Hans.md) · [繁體中文](CHANGELOG.zh-Hant.md)

[Startseite](README.de.md)

# Änderungsverlauf

Bridge-Tags und genehmigte Windows-UU-Version sind getrennt.

## Plus 0.2.0-work — 2026-10-06

- **Terminal fortsetzen:** optionaler Modus `persistent` behält Shell, Verzeichnis und Jobs beim Wiederverbinden; Standard bleibt `fresh`.

- **Mehrere Dateien empfangen:** reguläre Dateien am Controller kopieren, fertige Gruppe im Ubuntu-Dateimanager einfügen; Fortschritt in empfangenen Bytes.

- **Bildkompatibilität:** Original-PNG plus DIBV5/DIB; ein optionaler Mac-Helfer ergänzt TIFF für PNG.

- **Native Aufnahme erkunden:** optionale CPU/GPU-Prototypen, experimentell und außerhalb der Standardinstallation.

Nur eingehende reguläre Dateien. Aktuelle Ubuntu → Mac-Bildsynchronisierung und Fokusverlust zwischen zwei Controllern bleiben offen.

[CPU (MIT)](../vendor/uur-native-cpu/NOTICE) · [GPU (AGPL-3.0)](../vendor/uuway-gpu-component/README.md) · [Anleitung und Update auf Englisch](../docs/updates/2026-10-06.md)

## Plus 0.1.0 — 2026-10-03

Plus baut auf der MIT-lizenzierten Upstream-Bridge auf.

### Neu

- Bildfläche: Vier Profile bis 4K, vollständiger Desktop und Größenwiederherstellung.
- Telefontext: Überarbeitete Plus-Eingabepfade und öffentlicher FreeRDP-Textpfad.
- Verwaltung: Unabhängige Fenster-/Popup-Aufnahme und wiederverwendbarer Viewer.
- Cursor: Theme-Fallback und Startkorrekturen; Standard aus.
- Desktopaktionen: GNOME-Desktop-/Übersichtsaktionen angebunden.
- Werkzeuge: Qualität/VNC/FreeRDP/Openbox mit lokalen Schriften, DPI und Zugangsdaten.
- Build und Wiederherstellung: Feste Patchquellen, Laufzeitprüfung sowie Profil-/Viewer-Wiederherstellung.
- Startseiten und Kernanleitungen in elf Sprachen sowie bearbeitbare Architektur-, Portierungs- und Vergleichsgrafiken.

### Korrekturen

- Zwischenablage: SDL-Quellpatch für Hintergrundprüfung, Besitzerwechsel und Formatcache.
- Wiederöffnen des Managers, UTF-8-Titel, zugehörige Popups und Fokusrückgabe beim Schließen des Viewers.
- Telefontexte, Initialisierung des Eingabehooks, Teileingaben und zeitlich begrenztes Beenden des nativen Terminals.
- Zeigerabbildung auf die gesamte Bildfläche, getrennte Größe/Bitrate, Schutz manueller RDP-Sitzungen und wiederherstellbare Starter.

### Kompatibilität

- Ubuntu 24.04 / GNOME 46 · Ubuntu 26.04 / GNOME 50 · x86-64.
- Windows UU: Geprüfte 4.42.0.2770 als Standard.

## Geerbter Upstream — unveröffentlicht

Upstream liefert semantische Unicode-Clipboard-Transaktionen, Kompositionsbearbeitung und lange Diktate, physische Tastaturlayouts, authentifizierte Eingabe, Netz-/Laufzeitdiagnose, Wine-Bluetooth-Isolation und Wiederherstellung unbeaufsichtigter Sitzungen.

## Upstream0.2.0 — 2026-07-18

Netzdiagnose/Quelldigest, Default/fester Adapter; GNOME/libei-Descriptor-Recovery und Limits/Keyring/PythonGI; Telefontexttempo/physische Tasten ohne Verzögerung, originales `SendInput` vor Broker/Fokusprüfung; X11/XTEST/Telemetrie, Cleanup/Netz-Recovery; XRDP/unbeaufsichtigte Anleitung.

## Upstream0.1.0 — 2026-07-17

Erste unterstützte Wine/UU/Xvfb/SDLFreeRDP/GNOME-Bridge, Broker/Reinjection/Dienst; gespeicherte Einstellungen, Audit/Rollback/RDP-Clipboard; optional TPM2/GDM; Handy-Normalisierung, Wayland/Xorg/XRDP-D-Bus, Wine-Events/Präfixcleanup.

Originale Releases: [v0.1.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.1.0) · [v0.2.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.2.0). Vollständige ursprüngliche Historie und Prüfeinträge: [CHANGELOG.md — e2854e2b](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b/CHANGELOG.md).
