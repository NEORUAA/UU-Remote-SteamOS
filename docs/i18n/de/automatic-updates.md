[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [中文（简体）](../zh-Hans/automatic-updates.md) · [中文（繁體）](../zh-Hant/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Русский](../ru/automatic-updates.md)

[← Zur deutschen Startseite](../../../i18n/README.de.md)

# Automatische Prüfungen und fortsetzbare Reparatur

Die Wartung trennt Beobachtung, privaten Quellcode-Repair und ausdrücklich akzeptierte Live-Promotion. Normale Prüfungen unterbrechen kein funktionierendes Relay.

## Konfiguration und Timer

Plus beginnt seine eigene Versionsgeschichte mit `v0.1.0`. Die datierten Eingabe-Track-Tags gehören zur Upstream-Historie und sind nicht Teil dieses unabhängigen Repositorys. Eine normale Installation benötigt sie nicht. Sobald das Plus-Release-Tag lokal vorhanden ist, wählen Sie es ausdrücklich mit `--track v0.1.0 --branch main`; die Konfiguration verwendet sonst weiterhin alte Track-Namen und lehnt fehlende Tags ab.

Nach dem Auschecken des Release-Tags führen Sie vor den üblichen Upgrades mit Quellenabruf `git switch main` aus. Die gepflegten Quellen liegen auf `origin/main`; das ausdrücklich gewählte Neuinstallations-Tag bleibt `v0.1.0`. Um die ausgecheckten Quellen beim Upgrade bewusst auf dem festen Tag zu belassen, verwenden Sie `--no-pull`.

`--auto-promote-accepted` erlaubt nur später maintainer-akzeptierte, hashgebundene Versionen, nicht den eigenen Codex-Entwurf. Modell, Reasoning und der absolute Codex-Pfad stehen in `updater.json`; derselbe Unix-Benutzer muss angemeldet sein. Vor jedem Repair müssen alle gemeldeten Inklusivnutzungsfenster unter dem Standardlimit 20 Prozent liegen; nicht prüfbare Nutzung verschiebt um mindestens eine Stunde.

`uu-remote-update-check.timer` läuft täglich etwa 04:20 mit Zufallsverzögerung und zwölf Minuten nach Boot. `Persistent=true` holt einen verpassten Check nach. Der Repairmonitor startet nach sieben Minuten und dann 15 Minuten nach dem letzten Lauf.

## Beobachtung und Reparatur

Der Checker verfolgt die offizielle HEAD-Weiterleitung, entfernt temporäre Query-Schlüssel und vergleicht volle Versionsnummern. ETag, Größe und Hash-Sidecar vermeiden unveränderte Downloads. Ältere Endpoint-Versionen gelten nicht als Update. Zwei Gesundheitsfehler mit 20 Sekunden Abstand erzeugen Belege und eine Aufgabe, ohne Wine/RDP/UU zu stoppen. Nur separat aktiviertes `--auto-reinstall` gestattet Wiederherstellung.

Downloads sind auf 1 GiB begrenzt. Unbekannte Hashes werden statisch entpackt und in einem privaten Repairclone untersucht. Die Wartungsvereinbarung wird als `0600`-Kontext kopiert. Nicht extrahierbare Installer laufen nur nach ausdrücklichem netzlosem Sandbox-Staging. Codex darf weder sudo, Live-Präfixänderung, Push noch eigene Binärfreigabe ausführen.

## Akzeptierte Promotion

Offizielles Installer-Hash, `approved`-Manifest, schema-1 Acceptance und Evidence müssen im selben gefetchten `origin/main`-Commit übereinstimmen. Installer- und patched-server-Hashes sind gebunden. Tests umfassen Wegwerfpräfix, Controller, Reconnect, Cold Start, Service-Neustart, frisches Signaling und erhaltene Anmeldung; Stabilität beträgt 270–1800 Sekunden. Automatische Promotion muss aktiv sein, UU normalerweise 45 Minuten ruhig.

Nur der Bridge-Service stoppt. Das ganze Präfix wird mit zusätzlich 1 GiB Reserve kopiert, im selben Präfix installiert, Kontodaten bytegenau verglichen, ein neuer Room und zwei Runtimeprüfungen abgewartet. XRDP bleibt unverändert. State und Präfix müssen auf demselben Dateisystem liegen. Fehler, Reboot oder Unterbrechung stellen das alte Präfix her, behalten den Snapshot und blockieren automatische Wiederholung. `--now` überspringt ausschließlich die Ruhewartezeit.

## Aufgaben, Datenschutz und Sandbox

Thread-UUID wird bei `thread.started` gespeichert und mit `codex exec resume` weitergeführt. Ohne UUID beginnt ein neuer Thread aus demselben Kontext. Retry wächst von 15 Minuten bis 24 Stunden. Ergebnisse nach Schema werden separat getestet: `ready-for-review`, `no-change`, `blocked`; Promotionphasen sind `promotion-waiting-idle`, `promotion-running`, `promoted`, `promotion-blocked`.

Private Stateverzeichnisse sind `0700`, Dateien `0600`. Repairclone-Push ist deaktiviert, Codex nutzt workspace-write/never, der Service `NoNewPrivileges=yes`; Authentifizierung braucht weiterhin Netzwerk. Unter Ubuntu 24.04 darf die Benutzer-Service-Mountnamespace nicht die verschachtelte Bubblewrap-Sandbox verhindern. Installieren Sie bei `codex-sandbox-deferred` nur das distro-AppArmor-Profil mit den Befehlen unten, nicht eine globale Lockerung. `retry` behält Belege und Checkout, ersetzt den unbrauchbaren Thread und importiert Staging nur mit passenden Installer/server/healthd-Hashes.

`disable` erhält Belege; `disable --purge-state` entfernt auch die private Wartungskonfiguration. Übertragen Sie auf andere Rechner nur Quellen und wählen Sie deren eigenes Eingabeprofil.

[Upgrade](reusable-upgrade.md) · [Sicherheit](security.md)

## Befehle und technische Werte

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
uu-remote upgrade apply --now
```

```bash
sudo apt install apparmor-profiles
sudo install -o root -g root -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
uu-remote update retry
systemd-run --user --wait --pipe --collect \
  --property=NoNewPrivileges=yes \
  /usr/bin/bwrap --die-with-parent --unshare-user --uid 0 --gid 0 \
  --ro-bind / / /bin/true
systemctl --user cat uu-remote-repair-monitor.service
./scripts/configure-updater.sh status
./scripts/configure-updater.sh disable
./scripts/configure-updater.sh disable --purge-state
```

## Quellcode und verwandte Themen


Technische Details sind auf Englisch und vereinfachtem Chinesisch verfügbar:

- [automated-repair-agent-handoff](../../automated-repair-agent-handoff.md) · [简体中文](../zh-Hans/automated-repair-agent-handoff.md)
- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
