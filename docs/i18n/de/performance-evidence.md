[English](../../performance-evidence.md) · [العربية](../ar/performance-evidence.md) · [Deutsch](../de/performance-evidence.md) · [Español](../es/performance-evidence.md) · [Français](../fr/performance-evidence.md) · [日本語](../ja/performance-evidence.md) · [한국어](../ko/performance-evidence.md) · [Русский](../ru/performance-evidence.md) · [Tiếng Việt](../vi/performance-evidence.md) · [简体中文](../zh-Hans/performance-evidence.md) · [繁體中文](../zh-Hant/performance-evidence.md)

[Startseite](../../../i18n/README.de.md)

# Nutzungserlebnis und Leistung

![Verbesserungen bei chinesischer Eingabe, Zwischenablage und Verwaltung](../../images/experience-refinements-en.png)

[Bearbeitbare SVG](../../images/experience-refinements-en.svg)

![Pixelflächen und Auswahl der vier Zeichenflächen](../../images/canvas-pixel-scale-en.png)

[Bearbeitbare SVG](../../images/canvas-pixel-scale-en.svg)

720p/1080p/1440p/4K nach Bildschirm/Verbindung wählen. Qualität, angeforderte FPS und Limit bleiben getrennt.

## Alltag

Die jüngsten Verbesserungen betreffen chinesische Eingabe, das Einfügen von Text und die Fensterbedienung.

| Szene | Kontext | Frühere Bedienung | Verbesserte Bedienung |
| --- | --- | --- | --- |
| Chinesisch am Telefon | Frühere Telefoneingabe in Plus | Ein Teil des übermittelten Textes kam nicht richtig auf dem Desktop an | Chinesischer Text über die direkte Telefonverbindung erreicht den Ubuntu-Desktop korrekt |
| Kopieren und Einfügen | Früherer Textrelay in Plus | Trotz neu kopiertem Text konnte noch der alte Inhalt eingefügt werden | Neu kopierter Text steht aktuell zum Einfügen bereit; gewöhnliches Kopieren und Einfügen am Computer funktioniert |
| UU-Einstellungen und Popups | Frühere Verwaltungsansicht in Plus | Verwaltungsfenster konnten das Desktopbild überlagern oder den Fokus falsch hinterlassen | Einstellungen bleiben vom Desktopbild getrennt; nach dem Schließen der Verwaltungsansicht liegt der Eingabefokus wieder auf dem Desktop |
| Schärfe und Größe | Plus-Versuch mit größerer Zeichenfläche | Eine Vergrößerung der getesteten 4K-Quelle brachte keine Details und sah schlechter aus | Vier Profile zeigen den ganzen Desktop und stellen die gespeicherte Größe wieder her; für die getestete Quelle genügt 4K |
| Neuverbindung | Update des Mac-UU-Clients | Nach dem Mac-UU-Update mussten alltägliche Funktionen geprüft werden | Neuverbindung, direkte chinesische Eingabe und Textpaste funktionieren weiter; die 4K-Nutzung fühlt sich ähnlich an |

Der [Vergleich](upstream-comparison.md) trennt die Upstream-Grundlage, die Kompatibilität mit neueren Versionen, Plus-Erweiterungen und Korrekturen während der Plus-Nutzung.

![Upstream-Grundlage, Plus-Änderungen und Erwartungen aus dem Design](../../images/uu-plus-evolution-en.png)

[Bearbeitbare SVG](../../images/uu-plus-evolution-en.svg)

**Erwartung aus dem Design:** aktuelle Texte und eine verlässliche Fokusrückgabe sollten wiederholte Einfügeversuche und Unterbrechungen zwischen Einstellungen und Desktop verringern. Eine kleinere Zeichenfläche liefert weniger Pixel pro Bild; die sichtbare Reaktion hängt auch von Aufnahme, Kodierung, Netz und Controlleranzeige ab.

| Zeichenfläche | Pixel je Bild | Gegenüber1080p |
| --- | ---: | ---: |
| 1280 × 720 | 921,600 | 0.44× |
| 1920 × 1080 | 2,073,600 | 1.00× |
| 2560 × 1440 | 3,686,400 | 1.78× |
| 3840 × 2160 | 8,294,400 | 4.00× |

Das sind Flächenverhältnisse. Capture kann ganze Quelle verwenden; Kompression/Bewegung/Netz beeinflussen Last. Fit ändert keine physische Auflösung.

| Einstellung | Zweck |
| --- | --- |
| Ubuntu-Fläche |Relaybild;1080p Start,4K für Text/Platz |
| Qualität/FPS/True Color |Kompression, gewünschte Updates, verfügbare Farbe |
| `uu-remote quality bitrate 20` |20 Mbps-Limit; `0` entfernt. Niedrig kann Bewegung verwischen |

[Qualität](quality-guide.md): Menüs/Befehle/Recovery.

## Buildkosten

Vollständiger Kaltbuild einschließlich Vorbereitung/Checks:

| Wert | Beobachtung |
| --- | --- |
| Zeit |699.851 s (~11min40s) |
| Limits |CPU entsprechend2 Kernen;4 GiB RAM |
| Gemeldetes Maximum |~1.8 GB, gerundete Dienstanzeige |
| Swap |0 Bytes |
| Ausgabe |13 Windows-Binärdateien |
| Reproduzierbarkeit |Gleiche Bytes bei festen Eingaben in anderen Verzeichnissen |

Normaler Einstieg mit normalisierten Pfaden/expliziter Konfiguration. Downloads/Compiler beeinflussen andere Rechner; geprüfte Ausgabe wiederverwendbar: [Build](source-build.md).

| Umgebung | Ubuntu | GNOME | Windows UU |
| --- | --- | --- | --- |
| Upstream |24.04|46|4.33.0.8907|
| Plus lokal |26.04|50|4.42.0.2770|

## Vergleichsmessung

Die vorhandenen Aufzeichnungen enthalten keine Messung von Controller-FPS oder Eingabe-bis-Bild-Latenz unter gleichen Bedingungen für den festen Upstream-Stand und Plus. Relay-Zeiten und CPU-Quota-Versuche messen einzelne Komponenten.


Host/Controller, Auflösung, App, Netz, Qualität/FPS/Bitrate fixieren. Getrennte Umgebungen, feste Versionen, Upstream24.04-Grenze berücksichtigen. Aktion bis sichtbare Antwort messen, sichtbare Updates in wiederholbarer Bewegung zählen. Wiederholen, Streuung/Schriftklarheit und Methode festhalten.
