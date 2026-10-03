[English](../../ubuntu-26.04-port.md) · [العربية](../ar/ubuntu-26.04-port.md) · [Deutsch](../de/ubuntu-26.04-port.md) · [Español](../es/ubuntu-26.04-port.md) · [Français](../fr/ubuntu-26.04-port.md) · [日本語](../ja/ubuntu-26.04-port.md) · [한국어](../ko/ubuntu-26.04-port.md) · [Русский](../ru/ubuntu-26.04-port.md) · [Tiếng Việt](../vi/ubuntu-26.04-port.md) · [简体中文](../zh-Hans/ubuntu-26.04-port.md) · [繁體中文](../zh-Hant/ubuntu-26.04-port.md)

[Startseite](../../../i18n/README.de.md)

# Ubuntu 26.04 und GNOME 50

Plus erweitert [Lachlan Chens MIT-Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge) auf x86-64 Ubuntu 26.04/GNOME 50 und erhält24.04/GNOME 46. Wine-Isolation, geprüfte Manifeste, Broker, Relay und Dienst bleiben Grundlage.

Die Relay-Installation benötigt die exakt überprüfte Toolchain oder eine vorhandene validierte Ausgabe; gewöhnliche APT-Pakete stellen diese Toolchain nicht automatisch bereit. Siehe [Buildvoraussetzungen und Cache-Nutzung](source-build.md).

| Teil | Upstream | Plus |
| --- | --- | --- |
| Ubuntu | 24.04 | 24.04/26.04; andere: `UURB_ALLOW_UNVALIDATED_UBUNTU=1` |
| Windows UU | 4.33.0.8907 | Geprüft4.42.0.2770; ältere Manifeste auswählbar |
| libei | Isolierter1.2.1-Backport | Systembibliothek mit Fix, sonst Backport |
| Relay | Festgelegtes SDL nightly/WinPR | Gepatchte feste Quellen; [Build](source-build.md) |
| CI | 24.04 | Ziel24.04/26.04; Ergebnisse je Lauf |

Beobachtete Installation: GRD 50.2, libei 1.5.0. Alte Bibliotheken können `ee27dd5c92e4e9496a36ca2d4112049fe02d2269` verwenden. `UURB_LIBEI_MODE=system|backport` speichert Auswahl; `verify.sh` prüft geladenes libei. Wine kommt von WineHQ stable.

## Desktop

Vier Profile, vollständige Anpassung und Zeigermapping; Neuinstallation1080p, Upgrade erhält Einstellungen. Neue gespeicherte Größe verbindet mit Rücksetzungsschutz neu; erneutes Anwenden stellt die laufende Fläche wieder her. Nutzer bestätigt Verbindung und natives Menü bis4K. Neues RDP verwendet `rdp-public`; Upgrades behalten Route. Unicode und physische Tasten sind getrennt. Manager/Popups werden separat erfasst; Viewer-Schließen gibt Relay-Fokus zurück, Manager bleibt gemappt. Desktop-Zwischenablage bleibt aktiv, Manager isoliert.

| Funktion | Ergebnis |
| --- | --- |
| Direktes Chinesisch Telefon/Mac | Nutzer bestätigt während Integration |
| Text kopieren/einfügen | Nutzer bestätigt normal |
| Mac-UU-Update | Neuverbindung/Chinesisch/Einfügen normal;4K ähnlich |
| Manager-Überlagerung/Fokus | Laut Nutzer behoben; ausgewählte Checks normal |
| Android | Backend beide Richtungen; Tasten noch zu testen |
| Cursor | Theme/Teilprüfungen normal; gesamte Formen offen |
| Monitor/virtueller Ausgang | Auf diesem Host offen |
| Telefon → ToDesk → Mac → UU | Wiederholtes `a` offen |

VNC/FreeRDP/Openbox-Launcher haben lokale CJK-Schriften, DPI und Anmeldedaten. Dock ist GNOME-Einstellung. Ausgehende Qualität und physische Auflösung sind vom eingehenden Canvas getrennt. [Qualität](quality-guide.md), [Architektur](architecture.md), [Vergleich](upstream-comparison.md).

## Aktualisieren

Plus bleibt `origin`:

```bash
git remote add upstream https://github.com/lachlanchen/uu-remote-ubuntu-bridge.git
git fetch upstream
```

Upstream in Entwicklungsbranch prüfen. Nach Runtime-Änderungen:

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

Installation unterbricht kurz; der Digest meldet Quelländerungen bis Neuinstallation. [Wiederverwendbare Upgrades](reusable-upgrade.md) behandeln Runtime-Recovery, Profilrücksetzung die Fläche. Unbekannter UU-Hash blockiert automatische Patches; neue Version braucht semantische Prüfung, Manifest und Runtime-Checks: [Wartung](../../upstream-maintenance.md). MIT-Quellen/Manifeste werden verteilt; UU/Abhängigkeiten behalten Lizenzen.
