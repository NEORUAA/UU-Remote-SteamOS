<div align="center">

[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

<a href="README.de.md"><img src="../docs/images/uu-plus-logo.png" alt="UU Remote Ubuntu Plus" width="140"></a>

# UU Remote Ubuntu Plus

**Deine Ideen sind überall dabei. Deine Entwicklungsumgebung bleibt auf Ubuntu.**

Editor, Terminals und App-Sitzungen bleiben auf Ubuntu. Verbinde dich vom Smartphone, Mac oder Windows-PC aus, lass deinen Ideen mit Vibe Coding freien Lauf und schreib auf dem nächsten Bildschirm einfach weiter.

[![Ubuntu 24.04 / 26.04](https://img.shields.io/badge/Ubuntu-24.04%20%7C%2026.04-E95420?logo=ubuntu&logoColor=white)](../docs/i18n/de/ubuntu-26.04-port.md)
[![GNOME 46 / 50](https://img.shields.io/badge/GNOME-46%20%7C%2050-4A86CF?logo=gnome&logoColor=white)](../docs/i18n/de/architecture.md)
[![UU Remote 4.42](https://img.shields.io/badge/UU_Remote-4.42.0.2770-00A870)](../patches/uu-remote-4.42.0.2770.json)
[![MIT](https://img.shields.io/badge/License-MIT-2F81F7)](../LICENSE)

<img src="../docs/images/vibe-coding-cross-device-en.png" alt="UU Remote Ubuntu Plus" width="1120">

</div>

Plus verbindet NetEase UU Remote mit deiner angemeldeten Ubuntu-GNOME-Sitzung.
Die offizielle Windows-Anwendung von UU läuft in einer eigenen Wine-Umgebung.
Ein lokales Relay zeigt den tatsächlichen Desktop; ein separates Fenster dient
für UU-Konto und Einstellungen. Anwendungen und Dateien bleiben beim Wechsel
zwischen lokaler und entfernter Nutzung in derselben Sitzung.

Das Projekt basiert auf **[UU Remote Ubuntu Bridge von Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
Plus erweitert die Ubuntu- und UU-Kompatibilität, ergänzt vier Bildflächen und
verbessert Eingabe, Zwischenablage sowie Verwaltung.

Der Installer richtet sich an x86-64 Ubuntu 24.04 / GNOME 46 und Ubuntu 26.04 / GNOME 50 mit UU 4.42.0.2770. Neue Installationen wählen 1080p und lassen den optionalen Cursorschutz ausgeschaltet.

Alle elf Sprachseiten und die technischen Anleitungen beschreiben Plus in der jeweiligen Sprache. Englisch ist die kanonische Referenz.

## Von der Einrichtung zur Fernnutzung

1. Installiere die Bridge auf deinem Ubuntu-Desktop.
2. Starte `uu-remote open` und melde dich im Verwaltungsfenster bei UU an.
3. Verbinde dich über UU auf dem Smartphone, Mac oder Windows-PC mit diesem Rechner.
4. Wähle eine Bildfläche und nutze deine gewohnten Anwendungen.

## Funktionen und Verbesserungen

Das ursprüngliche Projekt liefert Desktop-Relay, Tastatur und Maus, Smartphone-IME-Verarbeitung und Dienstwiederherstellung. Plus erweitert diese Grundlage mit neuerer Kompatibilität, übersichtlichen Qualitätseinstellungen und Verbesserungen für den Alltag.

| Alltag | Ergänzungen von Plus |
| --- | --- |
| Neueres Ubuntu und UU | Ubuntu 26.04 / GNOME 50 und UU 4.42; der Installationsweg für Ubuntu 24.04 bleibt erhalten. |
| Passende Bildfläche wählen | 720p, 1080p, 1440p und 4K grafisch auswählen. Der gesamte Desktop passt in die Bildfläche; gespeicherte Einstellungen lassen sich wiederherstellen. |
| Chinesisch, Code und Kopieren/Einfügen | Korrigiert Smartphone-Texteingaben und die Aktualisierung der Zwischenablage. Neuer Text erreicht den Desktop; Code und mehrzeiliger Text behalten ihren Inhalt. |
| Einstellungen öffnen, verbunden bleiben | Erfasst UU-Verwaltung und Menüs getrennt. Beim Schließen des Viewers kehrt der Eingabefokus zum Desktop-Relay zurück. |
| Praktischere lokale Werkzeuge | Zugriff auf Qualität, VNC, FreeRDP und Openbox mit Verbesserungen bei Schriften, DPI und Start. |
| Installation und Wartung | Baut das Relay aus festgelegten Quellen und prüft Komponenten vor der Installation. Stellt fehlgeschlagene Bildflächenänderungen wieder her und zeigt eine Vorschau vor dem Entfernen. |

Der [Vergleich mit dem ursprünglichen Projekt](../docs/i18n/de/upstream-comparison.md) beschreibt Änderungen und Versionskontext.

<img src="../docs/images/experience-refinements-en.png" alt="Erlebnis und Messungen" width="1120">

[Erlebnis und Messungen](../docs/i18n/de/performance-evidence.md)

## Schnellinstallation

Nutze einen x86-64-Ubuntu-Host mit angemeldeter GNOME-Sitzung und klone das Projekt:

```bash
git clone https://github.com/llmir/uu-remote-ubuntu-plus.git
cd uu-remote-ubuntu-plus
```

Die Installation benötigt die geprüfte Toolchain zum Bauen des Relays oder ein vorhandenes geprüftes Ergebnis passend zum Produktprofil; Relay-Binärdateien sind nicht enthalten. Ubuntu 26.04 bietet den Weg zur Vorbereitung der Referenzwerkzeuge; unter Ubuntu 24.04 wird eine geprüfte Ausgabe wiederverwendet. [Toolchain vorbereiten und Relay wiederverwenden](../docs/i18n/de/source-build.md#reference-toolchain)

Sobald die Werkzeuge oder die passende Ausgabe bereitstehen, den normalen Installer ausführen:

```bash
./install.sh
./scripts/verify.sh --quick
uu-remote open
```

Der Installer richtet Abhängigkeiten ein, baut Komponenten, konfiguriert GNOME
Remote Desktop und startet Benutzerdienste. Das Relay-Passwort wird im GNOME
Keyring gespeichert; UU öffnet sich für die Kontoanmeldung.
Eine erneute Installation behält Einstellungen und Kontostatus bei.
Für einen Start mit 4K:

```bash
./install.sh --resolution 3840x2160
```

Melde deine Umgebung und reproduzierbares Verhalten über das [Kompatibilitätsformular](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

Die erste Installation kann Abhängigkeiten herunterladen und kompilieren.
Siehe [Quellcode-Build](../docs/i18n/de/source-build.md) und [Sicherheit](../docs/i18n/de/security.md).
Lade den Windows-UU-Client von NetEases offizieller Seite [uuyc.163.com](https://uuyc.163.com/). Die Bridge führt ihn in einer eigenen Wine-Umgebung aus. UU behält seine eigene Lizenz.

## Technischer Überblick

<img src="../docs/images/architecture-premium-v2-en.png" alt="Bilderfassung, Eingabe und lokale UU-Verwaltung auf Ubuntu." width="1120">

Der Ubuntu-Desktop gelangt über GNOME RDP zum SDL-/FreeRDP-Relay und über UU zum Controller. Tastatur und Maus kehren über die Eingabebrücke in dieselbe Sitzung zurück. UU-Konto und Einstellungen haben ein eigenes lokales Verwaltungsfenster.

`uu-remote open` öffnet die Verwaltung; die Bridge läuft nach dem Schließen des Viewers weiter. `uu-remote console` bietet eine optionale lokale Browseransicht. Module und Eingabewege stehen in [Architektur](../docs/i18n/de/architecture.md).

## Auflösung und Qualität

<img src="../docs/images/quality-controls-cartoon-v2-en.png" alt="Ubuntu canvas and UU controller quality controls" width="1120">

Öffne **UU Remote 画质与分辨率** in GNOME oder starte:

```bash
uu-remote quality gui
```

Der ganze Quelldesktop passt in die Bildfläche; die physische Monitorauflösung
bleibt erhalten. Ein Wechsel verbindet die Bridge kurz neu.
Bei einem Fehler wird die vorherige Einstellung wiederhergestellt.

```bash
uu-remote quality list
uu-remote quality apply 2160p
uu-remote quality status
uu-remote quality guide
```

Kodierungsqualität, FPS und True Color werden im **UU-Controller** eingestellt:
**Kontrollzentrum → Qualität** am Computer, **Aktionen → Anzeige** am Smartphone.

Die Bitratenobergrenze wird getrennt eingestellt:

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` fordert höchstens 20 Mbps an, `0` entfernt die Obergrenze.
Bildfläche, Qualität, angeforderte FPS und Bitrate sind eigene Einstellungen.
Siehe [Qualitätsleitfaden](../docs/i18n/de/quality-guide.md).

## Eingabe und Cursor

Smartphone-IME-Eingaben, Codeausschnitte und mehrzeiliger Text gelangen über den Textweg zu Ubuntu. Physische Tasten und Tastenkombinationen behalten ihre Tastenereignisse. Plus korrigiert Textübermittlung und Zwischenablageaktualisierung für tägliches Schreiben und Kopieren/Einfügen. Die [Tastatur-Relays](../docs/i18n/de/adaptive-keyboard-relays.md) erklären die Eingabemodi.

Der optionale Cursorschutz stammt aus dem ursprünglichen Projekt.
Plus verbessert Cursorressourcen und deren Verarbeitung. Aktivieren mit:

```bash
./install.sh --skip-packages --skip-account-login \
  --cursor-guard on --cursor-size auto
```

`auto` folgt der Desktop-Cursorgröße; ein Wert wie `24` setzt die Größe des
Ersatzcursors. `--cursor-guard off` schaltet den Schutz aus.
Die Neuinstallation verbindet UU kurz neu.

## Alltag und Wartung

```bash
uu-remote status
uu-remote network
uu-remote logs
uu-remote restart
uu-remote stop
```

`uu-remote open` öffnet die Verwaltung, `uu-remote login` die Anmeldung oder
Kontowiederherstellung. Neustart, Anmeldung und Neuinstallation unterbrechen
die Fernverbindung kurz.

Sichere lokale Änderungen, aktualisiere den Quellcode und installiere erneut:

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

Änderungen am Laufzeitcode werden durch die Neuinstallation wirksam.
Siehe [Upgrade](../docs/i18n/de/reusable-upgrade.md) für `uu-remote upgrade` und
[Automatische Updates](../docs/i18n/de/automatic-updates.md) für optionale Wartung.

Bridge entfernen und den UU-Kontostatus behalten:

```bash
./uninstall.sh --dry-run
./uninstall.sh
```

`./uninstall.sh --purge` entfernt zusätzlich das eigene Wine-Präfix, die
Relay-Zugangsdaten und die GNOME-RDP-Aktivierung.

## Weitere Linux-Systeme

Der aktuelle Installer richtet sich an Ubuntu 24.04 und 26.04 auf x86-64. Der [Linux-Portierungsleitfaden](../docs/i18n/de/porting.md) teilt zukünftige Ports in drei Ebenen:

- UU-Kompatibilitätskern, Relay und Eingabe wiederverwenden.
- Pakete, Wine-Pfade und Dienste der Distribution anpassen.
- Desktop-spezifische Erfassung, Eingabe, Anzeigemodi und Aktionen anbinden.

Andere GNOME-Distributionen können mehr bestehende Integration übernehmen. KDE und Xfce benötigen eigene Desktop-Backends.

## Dokumentation und Mitarbeit

- [Qualität](../docs/i18n/de/quality-guide.md), [Quellcode-Build](../docs/i18n/de/source-build.md) und [Ubuntu 26.04](../docs/i18n/de/ubuntu-26.04-port.md)
- [Architektur](../docs/i18n/de/architecture.md), [Sicherheit](../docs/i18n/de/security.md) und [Fehlersuche](../docs/i18n/de/troubleshooting.md)
- [Vergleich](../docs/i18n/de/upstream-comparison.md) und [Messungen](../docs/i18n/de/performance-evidence.md)
- [Änderungen](CHANGELOG.de.md) und [Mitarbeit](CONTRIBUTING.de.md)

Nenne Versionen, Einstellungen und die Schritte zum Reproduzieren des Verhaltens.

## Projekt unterstützen

**Spendier mir einen Kaffee ☕**

UU und Ubuntu entwickeln sich weiter. Ich passe Plus an neue Versionen an und arbeite weiter an Texteingabe, Kopieren und Einfügen sowie Bildqualität. Ein Kaffee hilft bei den Kosten für Versionstests, Entwicklungswerkzeuge und Tokens.

| PayPal | Alipay · CNY | AlipayHK · HKD | WeChat · chinesischer QR | WeChat · HKD |
| :---: | :---: | :---: | :---: | :---: |
| <a href="https://paypal.me/mirmirlin"><img src="../docs/images/support-paypal-en.png" alt="PayPal" width="160"></a> | <a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support-alipay-cny-en.png" alt="Alipay · CNY" width="160"></a> | <a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support-alipay-hkd-en.png" alt="AlipayHK · HKD" width="160"></a> | <a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support-wechat-zh-en.png" alt="WeChat · chinesischer QR" width="160"></a> | <a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support-wechat-en-en.png" alt="WeChat · HKD" width="160"></a> |

<details>
<summary>Zahlungscodes für Alipay und WeChat</summary>

<p><a href="../docs/i18n/de/support.md#alipay-cny">Alipay CNY</a><br><a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support/alipay-cny.jpg" alt="Alipay CNY" width="240"></a></p>

<p><a href="../docs/i18n/de/support.md#alipay-hkd">AlipayHK HKD</a><br><a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support/alipay-hkd.png" alt="AlipayHK HKD" width="240"></a></p>

<p><a href="../docs/i18n/de/support.md#wechat-zh">WeChat Chinesisch</a><br><a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support/wechat-zh.png" alt="WeChat Chinesisch" width="240"></a></p>

<p><a href="../docs/i18n/de/support.md#wechat-en">WeChat · HKD</a><br><a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support/wechat-en.png" alt="WeChat · HKD" width="240"></a></p>

</details>

Reproduzierbare Fehlerberichte, Erfahrungen mit Linux-Portierungen und Pull Requests sind ebenfalls willkommen. Danke, dass du die nächste Version mitgestaltest.

[UU Remote Ubuntu Plus unterstützen](../docs/i18n/de/support.md)

## Dank und Lizenz

Basierend auf **[UU Remote Ubuntu Bridge von Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
Der ursprüngliche Copyright-Hinweis und die [MIT-Lizenz](../LICENSE) bleiben erhalten.
UU und die Abhängigkeiten behalten ihre eigenen Lizenzen und Marken.
Dies ist ein unabhängiges Community-Projekt.

Symbole der Zahlungsanbieter: [Simple Icons](https://simpleicons.org/) (CC0); die Marken bleiben Eigentum ihrer jeweiligen Inhaber.
