[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [中文（简体）](../zh-Hans/reusable-upgrade.md) · [中文（繁體）](../zh-Hant/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md)

[← Zur deutschen Startseite](../../../i18n/README.de.md)

# Wiederholbare Updates mit erhaltener Anmeldung

`uu-remote-upgrade` und `uu-remote upgrade` verbinden Repository-Update, akzeptierte UU-Promotion, Bridge-Erneuerung und Prüfung. `status` zeigt den Stand, `check` untersucht ohne Produktänderung, `apply` wartet auf Wartungsruhe. `apply --now` überspringt nur diese Aktivitätswartezeit; es erzwingt keine unbekannten oder nicht akzeptierten Binärdateien.


Nach dem Auschecken des Release-Tags führen Sie vor den üblichen Upgrades mit Quellenabruf `git switch main` aus. Die gepflegten Quellen liegen auf `origin/main`; das ausdrücklich gewählte Neuinstallations-Tag bleibt `v0.1.0`. Um die ausgecheckten Quellen beim Upgrade bewusst auf dem festen Tag zu belassen, verwenden Sie `--no-pull`.

## Transaktion

Der Checkout muss sauber und nicht detached sein. Fetch/fast-forward führt keine divergente Historie zusammen; nach Quellenänderung startet das neue Skript erneut. Tests und Shellparser laufen vor der Änderung. Laufendes Produkt, Relay, Eingaberoute, Timing und Kontomarker werden geprüft. Nur das offizielle exakte Installer-Hash mit genehmigtem Manifest und gebundener Acceptance darf weiterlaufen.

Die Promotion kopiert das ganze Wine-Präfix, installiert im selben Präfix, patcht und vergleicht Registry-Anmeldung sowie beide Kontobäume bytegenau. Zwei Runtimeprüfungen und der Stabilitätsabstand folgen. Anschließend wird die passende Produktdefinition gewählt, die Bridge separat gesichert und unter Erhalt der Environment-Datei erneuert. Wartungstrack und Codex-Einstellungen bleiben erhalten. XRDP wird ausschließlich abgefragt; eine Änderung seines Aktivzustands lässt die Operation scheitern.

## Wiederherstellung und Eingabe

Fehler oder Unterbrechung stellen das vollständige Präfix wieder her und markieren `promotion-blocked`. Keine automatische Wiederholung. Eine ausdrückliche Wiederaufnahme desselben akzeptierten Releases benötigt geänderten Promotion-Quellcommit; alte Aufgaben bleiben unter `tasks/retired/`. Scheitert erst die Quell-Erneuerung, wird der gesicherte Runtimezustand nach der Produktpromotion zurückgespielt. Snapshots werden nicht durch Timer gelöscht.

Die Beispielwerte für direktes X11 unten sind kein Profil zum Kopieren auf andere Rechner. Die gespeicherte Route ist maßgeblich. Der Quick-Verifier tippt nicht in Ihre Anwendung; prüfen Sie nach einem Produktwechsel sichtbare Telefontastatur, schnelle physische Tasten und Mausbewegung/Klick/Drag/Rad.

Der persistente Bus `/run/user/UID/bus` vermeidet die falsche Benutzer-Serviceinstanz aus verschachtelten Desktop-Terminals. Die historischen Juli-2026-Aufzeichnungen zu 4.34 beschreiben nicht den heutigen Plus-4.42-Stand. Damalige Korrekturen betrafen fehlende Verifier, PE-Zeitstempel und einen Readiness-Wettlauf; aktuelle Prüfungen warten bis zu 45 Sekunden auf den echten Listener und gewählten Helfer. Auf einen anderen Rechner gehören nur Quellen, nicht Präfix, Keyring oder private Updaterdaten. Installierte Befehle benötigen `~/.local/bin` im `PATH`.

[Automatische Updates](automatic-updates.md) · [Tastatur-Relays](adaptive-keyboard-relays.md)

## Befehle und technische Werte

```bash
uu-remote-upgrade status
uu-remote upgrade status
uu-remote upgrade check
uu-remote upgrade apply
uu-remote upgrade apply --now
./scripts/upgrade-uu-remote.sh apply --now
```

```text
UURB_TEXT_KEY_DELAY_MS=8
UURB_PHYSICAL_KEY_DELAY_MS=0
UURB_KEYBOARD_ROUTE=x11
UURB_NETWORK_INTERFACE=default
unix:path=/run/user/UID/bus
~/.local/state/uu-remote-updater/tasks/*/promotion/snapshot-prefix
~/.local/state/uu-remote-upgrader/transactions/TIMESTAMP/
~/.local/state/uu-remote-upgrader/latest
```

```bash
git status --short
git switch main
git pull --ff-only origin main
./install.sh --skip-packages --skip-account-login
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/upgrade-uu-remote.sh check
```

## Quellcode und verwandte Themen


Technische Details sind auf Englisch und vereinfachtem Chinesisch verfügbar:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
