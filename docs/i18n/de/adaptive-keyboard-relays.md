[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [中文（简体）](../zh-Hans/adaptive-keyboard-relays.md) · [中文（繁體）](../zh-Hant/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md)

[← Zur deutschen Startseite](../../../i18n/README.de.md)

# Adaptive Tastatur-Relays

XRDP liefert Layoutmetadaten und Scancodes, RFB/X11 liefert Keysyms, UU-Computertastaturen liefern physische Windows-Ereignisse, Telefon-IMEs liefern Unicode. Diese Bedeutungen dürfen nicht zu einer einzigen Roh-Tastaturroute vermischt werden.

XRDP soll das vom Client gemeldete Layout wählen. Ein bedingungsloses `setxkbmap ... -layout jp` in `~/.xsessionrc` überschreibt es für jeden späteren Client. Bewahren Sie eine japanische Mac-Korrektur als ausdrücklich aufgerufenen Helfer, nicht als globale Login-Schleife. Semantischer Text und IBus bleiben vom physischen XKB getrennt.

## Dediziertes VNC-Fenster

Das Vollbild-Relay verwendet standardmäßig `UURB_VNC_GRAB_KEYBOARD=on` und `-GrabKeyboard=1`. Sonst kann das Zwischen-Desktop Shift/Ctrl/Alt/Super abfangen: `(` wird `8`, `?` wird `/`, `@` wird `2`. x11vnc nutzt `-modtweak -xkb -add_keysyms`, um passende Modifikatoren und fehlende Keysyms zu liefern. Der Listener bleibt auf IPv4-Loopback.

Deaktivieren Sie den Grab nur für ein nicht dediziertes Viewer-Fenster. Der isolierte RFB/Xvfb-Test prüft 21 Shift-Symbole plus `你好` gegen japanisches XKB. Prüfen Sie anschließend in einem Wegwerftextfeld normale Zeichen, Shift-Symbole, Ctrl+A/C/V, Enter/Backspace und die gewünschte IME; niemals im Passwortfeld.

## Layoutgrenze

Direktes X11 folgt dem Layout der Zielsitzung. UU übermittelt keine verlässliche Layoutkennung pro Verbindung: aus `Shift+7` allein lässt sich `&` oder `'` nicht rekonstruieren. XRDP/RFB können Metadaten oder Keysyms nutzen, Telefontext Unicode. Ändern Sie ein Clientprofil bewusst, statt das gemeinsame Desktoplayout für alle umzuschalten. In `rdp-public/auto` bleibt übernommener Unicode wörtlich; gewöhnliche physische Tasten bleiben gewöhnliche Ereignisse.

[Architektur](architecture.md) · [Sicherheit](security.md)

## Befehle und technische Werte

```text
UURB_VNC_GRAB_KEYBOARD=on
-GrabKeyboard=1
-repeat -nobell -modtweak -xkb -add_keysyms
```

```bash
./install.sh --skip-packages --skip-account-login \
  --vnc-grab-keyboard off
./scripts/test-vnc-keyboard-relay.sh
```

```text
vnc-symbols=23/23 order=exact target-layout=jp
isolated VNC keyboard acceptance passed
```

## Quellcode und verwandte Themen


Technische Details sind auf Englisch und vereinfachtem Chinesisch verfügbar:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
