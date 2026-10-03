[English](../../security.md) · [العربية](../ar/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Tiếng Việt](../vi/security.md) · [中文（简体）](../zh-Hans/security.md) · [中文（繁體）](../zh-Hant/security.md) · [Deutsch](../de/security.md) · [Русский](../ru/security.md)

[← Zur deutschen Startseite](../../../i18n/README.de.md)

# Sicherheit

## Berechtigungen und Grenzen

Verwenden Sie die Bridge nur mit autorisiertem Rechner und UU-Konto. Sie läuft als angemeldeter Unix-Benutzer in einem eigenen Wine-Präfix; sie umgeht weder die Anmeldung noch das Unix-Passwort. Xvfb benutzt Xauthority ohne TCP. Broker-Pipes gehören zum Wineserver dieses Präfixes.

Native X11- und Terminalhelfer binden kurzlebige IPv4-Loopback-Ports und erhalten jeweils ein neues 256-Bit-Token. Verzeichnisse sind `0700`, die Terminalübergabe `0600`, höchstens vier Shells sind erlaubt. Das lokale Verwaltungs-VNC hat keinen eigenen Passwortschutz, lauscht jedoch nur auf Loopback und exportiert ein UU-Fenster, nicht den privaten Root. Das optionale Mac-VNC bleibt authentifiziert hinter SSH. FreeRDP verbindet nur mit `127.0.0.1` und prüft GNOMEs TLS-Fingerabdruck. GNOMEs eigener LAN-Listener erfordert normale Firewall- und Passwortpflege.

## Zugangsdaten und Inhalt

`secret-tool` speichert das Relay-Passwort im Login-Keyring; FreeRDP liest es über stdin. Klassisches VNC verwendet nur die ersten acht Bytes, die Passwortdatei bleibt `0600`. Unbeaufsichtigter Start verschlüsselt das zusätzliche Keyring-Passwort mit TPM2 und `systemd-creds`; entschlüsselt wird es nur im geschützten Runtime-Verzeichnis. GDM-Autologin öffnet den lokalen Zugang nach dem Booten. TPM schützt gegen Offline-Übertragung, nicht gegen Programme des angemeldeten Benutzers; LUKS bleibt ein interaktives Boot-Hindernis.

Eingabeprotokolle enthalten Anzahl, Typ, Flags, Route, Ergebnis und Fehler, keine Zeichen, Koordinaten oder Zwischenablage. Terminalbefehle und Ausgabe werden nicht protokolliert. Semantische Texte sind auf 2.048 Datensätze begrenzt und verbleiben nach erfolgreichem Einfügen bewusst in der Zwischenablage. UU-Tokens, Registry, Präfixe und rohe Logs bleiben privat.

## Binärdateien und Wartung

Der Patcher akzeptiert nur ein `approved`-Manifest mit vollständigen Hashes, Größe, eindeutigen Signaturen und gleichlangen Änderungen. Originale bleiben als `.uu-original` erhalten. Das 4.42-Manifest gilt nur für diese Version; neue Entwürfe benötigen unabhängige Prüfung. Auch Relay-Build und Wiederverwendung benötigen passende Quellen, Recipe, Profile, Pins und Provenance.

Unbekannte Installer werden zunächst statisch entpackt. `--sandbox-install` ist ausdrücklich und verwendet einen netzlosen Bubblewrap- oder systemd-Stagingbereich. Wine ist keine starke Sandbox zwischen Prozessen desselben Benutzers. Reparaturausgaben dürfen sich nicht selbst freigeben: Promotion braucht exakte Hashes, committed Acceptance, echte Controller-/Loginprüfungen und mindestens 270 stabile Sekunden. Die Transaktion sichert das ganze Präfix und stellt es bei Fehlern wieder her, ohne XRDP zu verändern.

[Quellbuild](source-build.md) · [Automatische Updates](automatic-updates.md)

## Befehle und technische Werte

```text
~/.local/share/wineprefixes/uu-remote
~/.config/uu-remote-bridge/environment
CLIPBOARD / PRIMARY
KEYEVENTF_UNICODE / cliprdr
```

## Quellcode und verwandte Themen

- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [patches/freerdp-sdl-product.json](../../../patches/freerdp-sdl-product.json)

Technische Details sind auf Englisch und vereinfachtem Chinesisch verfügbar:

- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
