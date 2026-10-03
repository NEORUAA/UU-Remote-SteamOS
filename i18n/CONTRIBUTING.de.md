[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[Deutsch · UU Remote Ubuntu Plus](README.de.md)

# Zu UU Remote Ubuntu Plus beitragen

Fehlerberichte, Übersetzungen, Dokumentation und Code sind willkommen. Bewahre den Copyright-Vermerk und die MIT-Lizenz von [Lachlan Chens Bridge](https://github.com/lachlanchen/uu-remote-ubuntu-bridge).

## Problem und Nutzungspfad beschreiben

Nenne Ubuntu, GNOME, Wine, UU, Canvas, Eingaberoute und Reproduktion. Unterscheide Ubuntu als Host, lokalen Manager und Ubuntu als Controller. Kleine nachvollziehbare Änderungen und Messmethoden erleichtern Review. Nutze das [Kompatibilitätsformular](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

## Entwicklungsumgebung

Ubuntu und System-Python verwenden. Die Pakete dienen Build und isolierten Tests; Laufzeitabhängigkeiten verwaltet install.sh. Alternative Compiler über WINEGCC, MINGW_CC oder HOST_CC wählen. Temporäre Wine-Präfixe/Xvfb statt des angemeldeten Desktops nutzen.

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

## Quellen prüfen

Geänderte Shell-Dateien mit bash -n prüfen und die folgenden Checks ausführen. Strikte C-Warnungen behalten. Wine-, Xvfb- oder systemd-Tests können Fähigkeiten benötigen; übersprungene Tests angeben. UURB_TEST_SYSTEMD=1 nur bei verfügbarem Benutzerbus setzen.

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

## Dokumentation und Grafiken

Bestehende Dokumentationstests ausführen. Englische und chinesische Datenfluss-/Portierungs-SVGs teilen ein Layout; die letzten zwei Befehle sind nur fürs optionale Rendern mit Node und Sharp. Ganze Bilder und Metadaten prüfen, originale Zahlungscodes erhalten.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

## Installierte Laufzeit prüfen

Auf einem autorisierten Testhost installieren, mit einer Wiederherstellungsverbindung für die kurze Unterbrechung. Der vollständige Verifier enthält 270 Sekunden Stabilität; Bild, Eingabe und Wiederverbindung am echten Controller testen. Nur das UU-Präfix beenden, kein globales pkill wine.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

## Neue UU-Versionen

Neue ausführbare Dateien benötigen geprüfte Manifeste mit vollständigen SHA-256 und Begründung gleicher Patchlängen. Patch, identische Wiederherstellung, Kaltstart, Eingabe und Entfernung dokumentieren. Keine proprietären Dateien oder privaten Rohlogs veröffentlichen. Siehe [Upstream-Wartung (English)](../docs/upstream-maintenance.md).

## Veröffentlichbare Dateien

Dateiliste und Staging-Diff prüfen. Builds, Wine-Präfixe, Caches, .omc-Laufzeitdaten, Zugangsdaten, Gerätekennungen und Eingaben ausschließen. Authentifizierung, TLS, Manifestprüfung und reversible Entfernung erhalten.

```bash
git status --short
git diff --cached
```

## Review vorbereiten

Problem, neues Verhalten und tatsächlich ausgeführte Checks nennen. Unabhängige Prüfung anfragen, FPS-Einstellungen nicht als Messwerte ausgeben. [Qualität](../docs/i18n/de/quality-guide.md), [Ubuntu-Port](../docs/i18n/de/ubuntu-26.04-port.md) und [Sicherheit](../docs/i18n/de/security.md) lesen; MIT und Copyright bewahren.
