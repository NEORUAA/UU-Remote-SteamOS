[English](../../quality-guide.md) · [العربية](../ar/quality-guide.md) · [Deutsch](../de/quality-guide.md) · [Español](../es/quality-guide.md) · [Français](../fr/quality-guide.md) · [日本語](../ja/quality-guide.md) · [한국어](../ko/quality-guide.md) · [Русский](../ru/quality-guide.md) · [Tiếng Việt](../vi/quality-guide.md) · [简体中文](../zh-Hans/quality-guide.md) · [繁體中文](../zh-Hant/quality-guide.md)

[Startseite](../../../i18n/README.de.md)

# Qualität, Auflösung und Bildrate

Wählen Sie die Zeichenfläche auf Ubuntu und die Übertragungsqualität am steuernden Rechner oder Telefon. Größe, Kompression, angeforderte FPS und Bitratenlimit sind getrennte Einstellungen.

## Zeichenfläche auswählen

Öffnen Sie **UU Remote 画质与分辨率** in GNOME oder verwenden Sie:

```bash
uu-remote quality gui
uu-remote quality list
uu-remote quality status
uu-remote quality apply 2160p
uu-remote quality guide
```

![Auswahl der vier Auflösungen](../../images/quality-presets.png)

| Profil | Größe | Einsatz |
| --- | --- | --- |
| `720p` | 1280 × 720 | Kleine Bildschirme oder knappe Verbindung |
| `1080p` | 1920 × 1080 | Alltag; Standard bei Neuinstallation |
| `1440p` | 2560 × 1440 | Mehr Platz mit weniger Pixeln als 4K |
| `2160p` | 3840 × 2160 | Feine Schrift und vollständiger 4K-Arbeitsbereich |

Neuinstallation erhält die gespeicherte Auswahl. Smart Sizing passt den gesamten Quelldesktop ein und rechnet Zeigerkoordinaten mit derselben Geometrie um. Quellauflösung und Seitenverhältnis beeinflussen das Bild. Die Zeichenfläche ändert nicht den physischen GNOME-Bildschirm; die Aufnahme kann weiterhin die ganze Quelle verarbeiten.

Die Auswahl unterscheidet gespeicherte Start-/RDP-Größe und aktuelle Zeichenfläche. Eine neue gespeicherte Größe verbindet UU kurz neu. Erneutes Anwenden des gespeicherten Profils stellt die laufende Fläche im unterstützten RDP-Pfad ohne Relay-Neustart wieder her und prüft die Größe. Ein vorher gestarteter Rücksetztimer stellt alte Einstellungen wieder her, wenn die Bridge nicht bereit wird. Warten Sie die Wiederherstellung ab.

Feste Profile verwenden standardmäßig `--follow-desktop-resolution off`. Schalten Sie eine zuvor aktivierte Auflösungsnachführung zuerst ab. Siehe [Installation](../../../i18n/README.de.md) und `./install.sh --help`. Die getestete 4K-Quelle sah auf 5K vergrößert am Mac schlechter aus, ohne mehr Details. Daher enden normale Optionen bei 4K. Nominelle 60 Hz bezeichnen virtuelle Anzeigemodi; tatsächliche FPS hängen von der gesamten Verbindung ab.

## Qualität am Controller

Rechner: **控制中心 → 画质**. Telefon: **操作 → 显示**. True Color wird ebenfalls am Controller gewählt, soweit verfügbar.

![Natives UU-Menü](../../images/uu-native-quality-menu.png)

Das Beispiel stammt von Ubuntu als Mac-Controller. Geräte und Codec bestimmen Optionen. Qualität steuert Kompression/Details, FPS die gewünschte Aktualisierung. True Color verbessert farbige Schrift/Kanten. Meldet UU eine Leistungsgrenze, wählen Sie eine verfügbare Stufe. Vergleichen Sie dieselbe Schrift und Bewegung.

NetEase-Dokumentation: [FPS / Super Screen](https://uuyc.163.com/help/superscreen.html) · [True Color](https://uuyc.163.com/features/color/) · [UU](https://uuyc.163.com/help/20241216/40221_1200122.html). Super Screen/virtueller Treiber unter Wine und 144 FPS sind noch zu testen. Siehe [Messungen](performance-evidence.md).

## Bitratenlimit

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` fordert maximal **20 Mbps**, `0` entfernt das Limit. Das ist weder Zielbitrate noch FPS-/Größeneinstellung. Profile erhalten das Limit. Ein enger Wert kann Bewegungsdetails verschlechtern.

## Zeiger und Desktop

Der optionale Cursor Guard ist bei Neuinstallation aus. Bei zu großem Zeiger:

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size 24
```

`--cursor-size auto` folgt der Desktopgröße; feste Werte: 24–128 Pixel. GNOME-/App-Einstellungen bleiben unabhängig. Das Dock folgt GNOME. Android-Desktop-/Alle-Fenster-Aktionen sind auf Desktop/Übersicht abgebildet; echte Tastenprüfungen stehen aus.

## Verwaltung und Wiederherstellung

`uu-remote open` öffnet den getrennten Viewer. Vergrößern:

```bash
UURB_WINDOW_SCALE=2 ./install.sh --skip-packages --skip-account-login
```

Skalen: `1` (Standard), `1.5`, `2`, `3`; nur Viewer, nicht Wine-DPI oder Desktopauflösung. Verwaltungs-Zwischenablage ist isoliert; Desktop-Kopieren verwendet das Relay.

```bash
uu-remote status
uu-remote quality status
uu-remote network
uu-remote logs
```

Der Benutzerdienst startet fehlerhafte Komponenten neu, eventuell mit kurzer Neuverbindung. Profilrücksetzung betrifft Einstellungen; Deployment hat einen eigenen Ablauf. [Fehlersuche](troubleshooting.md), [Build](source-build.md). Ausgehende Wine-Steuerung hat andere Qualitätsgrenzen. Physischer Monitor und virtuelle Ausgänge: [Ubuntu 26.04](ubuntu-26.04-port.md), Tests offen. Telefon → ToDesk → Mac → UU wiederholt weiterhin Text; direkte Eingabe funktioniert.
