[English](../../source-build.md) · [العربية](../ar/source-build.md) · [Deutsch](../de/source-build.md) · [Español](../es/source-build.md) · [Français](../fr/source-build.md) · [日本語](../ja/source-build.md) · [한국어](../ko/source-build.md) · [Русский](../ru/source-build.md) · [Tiếng Việt](../vi/source-build.md) · [简体中文](../zh-Hans/source-build.md) · [繁體中文](../zh-Hant/source-build.md)

[Startseite](../../../i18n/README.de.md)

# Relay bauen und wiederverwenden

Der Installer baut einen festgelegten FreeRDP-SDL-Client mit Plus-Zwischenablage-/Größenpatches. [Rezept](../../../vendor/freerdp-sdl-build/), [Quell-Lock](../../../vendor/freerdp-sdl-build/source-lock.json) und [Produktprofil](../../../patches/freerdp-sdl-product.json) enthalten Revisionen, Archive, Tools und 13 Windows-Dateien.

<a id="reference-toolchain"></a>

## Referenzwerkzeuge für Ubuntu 26.04 vorbereiten

Unter Ubuntu 26.04 amd64 lädt das [Vorbereitungsskript](../../../scripts/prepare-build-toolchain.py) 17 festgelegte offizielle Ubuntu-Pakete herunter und prüft 14 Compiler-/Buildtool-Dateien gegen `source-lock.json`. Das [Paketmanifest](../../../patches/reference-build-packages.json) enthält Versionen, Größen und Prüfsummen. Das Skript lädt, entpackt in ein privates Verzeichnis und prüft die Dateien; es installiert keine Systempakete. Im Repository-Stamm ausführen:

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root"
```

`--packages-dir` wählt den Paketcache; `--root` muss ein neues oder leeres privates Verzeichnis sein. Zum erneuten Entpacken und Prüfen ausschließlich aus dem Cache ein anderes leeres Verzeichnis mit `--verify-only` wählen; dabei erfolgt kein Netzwerkzugriff:

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root-offline" \
  --verify-only
```

Das Skript gibt einen `sudo apt install`-Befehl mit allen 17 lokalen `.deb`-Pfaden aus. Diesen Befehl unter Ubuntu 26.04 manuell ausführen, um die Referenzwerkzeuge zu installieren. Das bestehende Rezept liest feste `/usr`-Pfade. Das private Entpackverzeichnis dient der Prüfung, nicht der Auswahl einer Buildumgebung.

Danach den normalen Installer ausführen. Er richtet die übrigen Buildabhängigkeiten des Hosts sowie WineHQ und GNOME-Laufzeitpakete ein, baut das Relay über den bestehenden Ablauf und prüft vor der Bereitstellung. Die Vorbereitung prüft 14 Referenzdateien; der vollständige Quellbuild und seine 13 Laufzeitdateien werden in diesem Ablauf geprüft:

```bash
./install.sh
./scripts/verify.sh --quick
```

Unter Ubuntu 24.04 über den folgenden Wiederverwendungsablauf eine vorhandene geprüfte Ausgabe passend zum aktuellen Produktprofil nutzen. Die obigen Ubuntu-26.04-Pakete sind für 26.04 bestimmt.

## Build und Cache

Ein Build aus frischen Quellen benötigt genau die überprüften Compiler- und Buildtool-Dateien aus `source-lock.json`, mit identischen Bytes. Gewöhnliche APT-Pakete der Distribution stellen diese Toolchain nicht automatisch bereit.

`./install.sh` installiert Pakete und validiert vor dem Austausch. `build/freerdp` wird nur bei passender Provenienz zu Profil/Rezept/Pins wiederverwendet. Sonst baut `scripts/build-winpr.sh` frische Quellen mit zwei Jobs und 900 Sekunden Zeitlimit und prüft das Ergebnis.

Sind die geprüften Werkzeuge an den `/usr`-Pfaden des Rezepts installiert und die Buildabhängigkeiten vorhanden, lässt sich auch ein separater Relaycache bauen:

```bash
UURB_BUILD_DIR=/absolute/path/to/build-work   ./scripts/build-winpr.sh /absolute/path/to/fresh-output
```

Neues Ausgabeverzeichnis verwenden. Ein eindeutiger Quelljob entsteht im Arbeitsverzeichnis, unabhängig von laufenden Wine-Präfixen. Validierte Ausgabe wiederverwenden:

Im Repository-Stamm zuerst eine vorhandene Ausgabe gegen das aktuelle Profil prüfen. Der normale Installer richtet Hostabhängigkeiten ein. `--skip-packages` nur verwenden, wenn die Buildtools der Host-Kompatibilitätskomponenten, WineHQ und GNOME-Laufzeitpakete schon installiert sind; `--skip-account-login` ist bei eingerichtetem Konto optional.

```bash
python3 scripts/verify-freerdp-runtime.py --mode build /absolute/path/to/verified/output
```

Verwenden Sie diese Ausgabe anschließend über den bestehenden Installer-Einstieg:

```bash
UURB_FREERDP_PREBUILT_DIR=/absolute/path/to/verified/output   ./install.sh
```

Cache, Pins und Provenienz müssen zum aktuellen Profil passen. Ein neues Profil erfordert erneuten Build-/Validierungseinstieg; bearbeitete Belege/Prüfsummen genehmigen keine anderen Binärdateien. Vor Dienststart wird auch die Kopie geprüft.

## Eingaben und Ergebnisse

FreeRDP/WinPR, SDL 3.2.28, SDL_ttf, OpenH264, FreeType, HarfBuzz sowie OpenSSL/cJSON/uriparser sind festgelegt. Patch und MinGW-/Compiler-/Tool-Hashes werden vor dem Build geprüft; Änderungen brauchen ein überprüftes Rezept.

Datei-/Makro-/Debug-Präfixabbildungen normalisieren Pfade. FreeRDP opaque bleibt schon bei Erstkonfiguration OFF, die Kompatibilitäts-DLL nutzt einen relativen Ausgabenamen. Lokale Checkoutpfade bleiben damit aus dem Runtime-Inhalt.

Zwei Quell-/Ausgaberoots erzeugten identische Bytes aller 13 Dateien. Erstes/wiederholtes CMake lieferte gleiche Metadaten. Der vollständige Kaltbuild ohne vorgefertigte Ausgabe dauerte rund 700 Sekunden innerhalb 900 und bestand Runtime-/Provenienzprüfungen. Siehe [Qualität](quality-guide.md), [Kosten](performance-evidence.md).
