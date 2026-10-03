[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[Deutsch · UU Remote Ubuntu Plus](../../../i18n/README.de.md)

# Fehler beheben

## Zuerst den Zustand prüfen

Führe die Befehle im Quellordner aus. Protokolle liegen unter `~/.local/state/uu-remote-bridge`, Einstellungen unter `~/.config/uu-remote-bridge/environment`. Berichte Versionen und Fehler ohne Kontodaten oder eingegebenen Text. Nach Quelländerungen erneut installieren.

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

## Offline oder nach dem Neustart nicht erreichbar

Einmal im offiziellen Manager anmelden und das Fenster normal schließen. Prüfe Benutzerdienste und Schlüsselbund. Nach Passwortänderungen erneuert `./scripts/configure-unattended.sh enable --replace-credential` die verschlüsselte Anmeldeinformation. Bei beendetem Server die Wiederherstellung prüfen.

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

## Die Verbindung sucht dauerhaft nach Routen

Prüfe zuerst den Hoststart. Alte virtuelle Eingabe- und Bluetooth-Einträge können Wine bremsen. Die Reparatur sichert die Registry, entfernt bekannte Einträge im UU-Präfix und startet die Brücke neu; Ubuntu-Bluetooth bleibt erhalten.

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

## Schwarzes, weißes oder falsches Desktopbild

Prüfe die angemeldete GNOME-Sitzung, den RDP-Listener und SDL-Protokolle. Bei mehreren Sitzungen die Quelle bestimmen. Für XRDP `--desktop-target xrdp`, für den lokalen Sitz `physical` wählen. VNC ist mit `--desktop-relay vnc` nur für X11 gedacht; Wayland nutzt RDP.

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

## Leere Ränder, abgeschnittenes Bild oder zu viel 4K

Vergleiche Quellgröße und Canvas. Die Oberfläche bietet 720p, 1080p, 1440p und 4K. Canvas, Controller-FPS und Bitrate sind getrennt. Änderungen verbinden kurz neu und rollen bei Fehlern zurück; dynamische XRDP-Größen separat prüfen.

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

## Bild funktioniert, Eingabe nicht

Öffne den Manager mit uu-remote open statt dasselbe Wine-Präfix auf einem zweiten X-Display zu starten. Nach Schließen des Viewers kehrt der Fokus zurück. Handytext und mehrzeilige Eingabe benötigen den Clipboard-/RDP-Paste-Pfad; physische Tasten bleiben Ereignisse. Nach Updates den Injector prüfen. Bricht die erste Mausaktion ab, prüfe UU SendInput bridge active, UU Wine event-log compatibility active und den Broker; `uu-remote restart` stellt die Komponenten wieder her.

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

## Tasten verzögern sich oder fallen aus

Vergleiche VPN, Proxy und UU-Transport; stale kennzeichnet historische Sitzungen. Bei bestätigter falscher Schnittstelle `--network-interface default` testen, mit `all` zurücksetzen. Physisches Pacing kann mit `--physical-key-delay-ms 8` geprüft werden, Standard ist `0`. Symbole folgen Ubuntus Tastaturlayout. Langzeitfehler mit GRD/libei und Deskriptorprüfung eingrenzen.

```bash
uu-remote network
ip -4 route show default
```

## Cursor fehlt oder ist zu klein

Der optionale Cursor-Guard ist standardmäßig aus. auto folgt der Desktopgröße, feste Werte reichen von 24 bis 128. `--cursor-guard off` schaltet ihn ab, ohne die Desktopauflösung oder globale Wine-DPI zu ändern.

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

## UU-Terminal endet sofort oder zeichnet falsch

Installiere die aktuelle Brücke und prüfe den Terminalkanal. In UU PowerShell wählen; dahinter läuft die Ubuntu-Login-Shell. Bei Positionsfehlern eine neue Sitzung öffnen. Metadaten in terminal-bridge.log prüfen, keine beliebige powershell.exe einsetzen.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

## RDP-Anmeldung, NLA oder SSPI scheitert

Die Abfrage prüft das Vorhandensein ohne Passwortausgabe. Bei Bedarf nur den Brückeneintrag im Schlüsselbund entfernen und neu installieren. FreeRDP, WinPR und DLLs aus derselben festgelegten Version bauen; keine Hauptversionen mischen.

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

## Mac RDP/VNC oder Windows App hängt

Die interne FreeRDP-Verbindung nutzt bereits Desktop-Sharing; Remote Login erzeugt eine andere Sitzung. Den tatsächlichen Loopback-VNC-Port abfragen und über SSH weiterleiten. Bei Configuring zunächst Windows App am Mac schließen und neu öffnen, dann XRDP prüfen.

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

## Periodische Neustarts, Ton und Entfernen

Der vollständige Verifier prüft die Stabilität. UU-Audio, Wine-PulseAudio und VNC-Klingel getrennt nur im dedizierten Umfeld untersuchen. Deinstallation zuerst ansehen; normal bleibt das Präfix erhalten, `./uninstall.sh --purge` entfernt auch den Kontozustand. Mit `wpctl status` den tatsächlichen Audiostream identifizieren. `UURB_UU_AUDIO=system` ist der Kompatibilitätsstandard; die eigene stille ALSA-Konfiguration und Rücknahme sind im englischen Detailleitfaden beschrieben.

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

Weiter: [Bildqualität](quality-guide.md), [Quellbuild](source-build.md), [Architektur](architecture.md), [Eingabe](adaptive-keyboard-relays.md), [Updates](reusable-upgrade.md). [Ausführliche Technik und historische Fälle (English)](../../troubleshooting.md) behandeln Registry, Treiber, Audio, XRDP und Terminalkanäle.

## Weiterführende Anleitungen

- XRDP und Tastaturwiederherstellung · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- Tastaturkompatibilität · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- Aktueller Desktop am Mac · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- Gemeinsamer physischer Desktop · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- Wiederherstellung nach Ende · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- Controller-Agent · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- Agent-Nachrichten über SSH · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)
