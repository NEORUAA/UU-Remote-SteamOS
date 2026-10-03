[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[Français · UU Remote Ubuntu Plus](../../../i18n/README.fr.md)

# Résoudre les problèmes

## Premières vérifications

Exécutez les commandes depuis les sources. Journaux dans `~/.local/state/uu-remote-bridge`, réglages dans `~/.config/uu-remote-bridge/environment`. Fournissez versions et erreurs sans compte ni texte saisi. Réinstallez après modification des sources.

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

## Hors ligne après démarrage

Connectez-vous une fois au gestionnaire officiel puis fermez-le normalement. Vérifiez services utilisateur et trousseau. Après changement de mot de passe, `./scripts/configure-unattended.sh enable --replace-credential` renouvelle le secret chiffré. Vérifiez la récupération si le serveur s’arrête.

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

## Recherche de routes sans fin

Vérifiez d’abord le démarrage local. Les anciennes entrées de périphériques d’entrée et Bluetooth ralentissent parfois Wine. La réparation sauvegarde le registre, nettoie les entrées reconnues du préfixe UU et redémarre le pont, sans modifier le Bluetooth Ubuntu.

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

## Écran noir, blanc ou mauvaise session

Vérifiez session GNOME ouverte, écoute RDP et journaux SDL. Identifiez les sessions multiples. Choisissez `--desktop-target xrdp` pour XRDP, `physical` pour le bureau local. `--desktop-relay vnc` concerne X11 ; Wayland utilise RDP.

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

## Marges vides, image coupée ou 4K trop lourde

Comparez bureau source et canevas. Choisissez 720p, 1080p, 1440p ou 4K dans l’interface. Canevas, FPS du contrôleur et débit sont distincts. Le changement reconnecte brièvement et revient en arrière en cas d’échec ; vérifiez le redimensionnement XRDP.

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

## Image présente, saisie absente

Ouvrez le gestionnaire avec uu-remote open, sans lancer le même préfixe sur un autre affichage X. Fermer le visualiseur rend le focus au relais. Le texte du téléphone utilise presse-papiers/RDP, les touches physiques gardent leurs événements. Vérifiez l’injecteur après réinstallation. Si le premier clic ferme la session, vérifiez UU SendInput bridge active, UU Wine event-log compatibility active et le broker ; `uu-remote restart` restaure les composants.

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

## Touches lentes, symboles erronés ou dégradation

Comparez VPN, proxy et transport UU ; stale signale une ancienne session. Si l’interface est incorrecte, testez `--network-interface default`, rétablissez `all`. Le rythme physique se teste avec `--physical-key-delay-ms 8`, défaut `0`. Les symboles suivent le clavier Ubuntu ; pour les longues sessions vérifiez GRD/libei et les descripteurs.

```bash
uu-remote network
ip -4 route show default
```

## Curseur absent ou trop petit

La protection facultative est désactivée par défaut. auto suit le bureau ; taille fixe entre 24 et 128. Désactivez avec `--cursor-guard off`, sans changer résolution ou DPI global Wine.

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

## Terminal UU fermé ou texte mal placé

Réinstallez le pont actuel et testez le canal. Choisissez PowerShell dans UU : il ouvre le shell de connexion Ubuntu. Créez une nouvelle session si le curseur est décalé. Consultez les métadonnées de terminal-bridge.log, sans remplacer arbitrairement powershell.exe.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

## Échec RDP, NLA ou SSPI

La requête vérifie le secret sans afficher le mot de passe. Au besoin, effacez seulement l’entrée du pont puis réinstallez. Compilez FreeRDP, WinPR et DLL depuis la même version fixée ; ne mélangez pas les versions majeures.

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

## Mac RDP/VNC ou Windows App bloquée

Le FreeRDP interne occupe déjà le partage de bureau ; la connexion distante ouvre un autre bureau. Relevez le vrai port VNC local et utilisez un tunnel SSH. Si Windows App reste sur Configuring, relancez d’abord le client Mac puis vérifiez XRDP.

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

## Redémarrages, son et suppression

Le vérificateur complet contrôle la stabilité. Examinez séparément audio UU, PulseAudio Wine et cloche VNC dans l’environnement dédié. Prévisualisez la désinstallation ; le mode normal garde le préfixe, `./uninstall.sh --purge` retire aussi l’état du compte. Identifiez le flux réel avec `wpctl status`. `UURB_UU_AUDIO=system` est le réglage compatible ; la configuration ALSA silencieuse dédiée et son retrait figurent dans le guide détaillé anglais.

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

Lire aussi : [qualité](quality-guide.md), [compilation](source-build.md), [architecture](architecture.md), [saisie](adaptive-keyboard-relays.md), [mise à jour](reusable-upgrade.md). [Détails techniques et historique (English)](../../troubleshooting.md) développent registre, pilotes, audio, XRDP et terminal.

## Guides détaillés

- Récupération XRDP et clavier · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- Compatibilité clavier · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- Bureau actuel sur Mac · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- Bureau physique partagé · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- Récupération après arrêt · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- Agent de contrôle · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- Messages d’agents par SSH · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)
