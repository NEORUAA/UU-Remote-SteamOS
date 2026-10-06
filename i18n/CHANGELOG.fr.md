[English](../CHANGELOG.md) · [العربية](CHANGELOG.ar.md) · [Deutsch](CHANGELOG.de.md) · [Español](CHANGELOG.es.md) · [Français](CHANGELOG.fr.md) · [日本語](CHANGELOG.ja.md) · [한국어](CHANGELOG.ko.md) · [Русский](CHANGELOG.ru.md) · [Tiếng Việt](CHANGELOG.vi.md) · [简体中文](CHANGELOG.zh-Hans.md) · [繁體中文](CHANGELOG.zh-Hant.md)

[Accueil](README.fr.md)

# Journal des changements

Versions du pont et Windows UU approuvé sont distinctes.

## Plus 0.2.0-work — 2026-10-06

- **Reprendre le terminal :** le mode optionnel `persistent` conserve shell, répertoire et tâches à la reconnexion ; défaut : `fresh`.

- **Recevoir plusieurs fichiers :** copiez des fichiers ordinaires côté contrôleur, puis collez le lot complet dans Ubuntu ; progression en octets reçus.

- **Compatibilité des images :** PNG original avec DIBV5/DIB ; un compagnon Mac optionnel ajoute TIFF pour PNG.

- **Explorer la capture native :** prototypes CPU/GPU optionnels et expérimentaux, hors installation par défaut.

Fichiers ordinaires entrants uniquement. La synchronisation actuelle Ubuntu → Mac et le focus entre deux contrôleurs restent ouverts.

[CPU (MIT)](../vendor/uur-native-cpu/NOTICE) · [GPU (AGPL-3.0)](../vendor/uuway-gpu-component/README.md) · [Utilisation et mise à jour en anglais](../docs/updates/2026-10-06.md)

## Plus 0.1.0 — 2026-10-03

Plus repose sur le pont amont sous licence MIT.

### Ajouts

- Canevas: Quatre profils jusqu’à 4K, bureau entier et restauration de taille.
- Texte mobile: Évolution des voies Plus et voie texte publique FreeRDP.
- Gestion: Capture indépendante des fenêtres/dialogues et visualiseur réutilisable.
- Curseur: Repli du thème et corrections de démarrage ; désactivé par défaut.
- Actions: Actions GNOME bureau/vue d’ensemble.
- Outils: Qualité/VNC/FreeRDP/Openbox avec polices, DPI et identifiants locaux.
- Compilation et reprise: Sources corrigées fixes, vérification et reprise des profils/visualiseur.
- Pages d’accueil et guides essentiels en onze langues, avec graphiques éditables d’architecture, de portage et de comparaison.

### Corrections

- Presse-papiers: Patch SDL pour vérification en arrière-plan, propriétaire et cache.
- Réouverture du gestionnaire, titres UTF-8, capture des dialogues associés et retour du focus à la fermeture du visualiseur.
- Envoi du texte mobile, initialisation du hook, saisies partielles et fermeture limitée du terminal natif.
- Pointeur sur tout le canevas, taille/débit indépendants, protection des sessions RDP manuelles et lanceurs réversibles.

### Compatibilité

- Ubuntu 24.04 / GNOME 46 · Ubuntu 26.04 / GNOME 50 · x86-64.
- Windows UU: 4.42.0.2770 vérifié par défaut.

## Amont hérité — non publié

L’amont apporte les transactions Unicode du presse-papiers, l’édition de composition et les longues dictées, les dispositions physiques du clavier, l’entrée authentifiée, les diagnostics réseau/runtime, l’isolation Bluetooth de Wine et la reprise des sessions sans surveillance.

## Amont0.2.0 — 2026-07-18

Diagnostic réseau/digest installé, adaptateur défaut/fixe ; récupération des descripteurs GNOME/libei, limites/Keyring/PythonGI ; cadence mobile configurable/touches sans délai, `SendInput` d’abord/fallback/focus confirmé ; X11/XTEST authentifié, télémétrie, nettoyage et réseau temporisé ; guides XRDP et sans surveillance.

## Amont0.1.0 — 2026-07-17

Premier pont Wine/UU/Xvfb/SDLFreeRDP/GNOME, courtier/réinjection/service ; paramètres enregistrés, audit/retour/clipboard RDP ; TPM2/GDM facultatif ; normalisation mobile, D-Bus Wayland/Xorg/XRDP, événements Wine et nettoyage préfixes.

Versions originales : [v0.1.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.1.0) · [v0.2.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.2.0). Historique détaillé et contrôles originaux : [CHANGELOG.md — e2854e2b](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b/CHANGELOG.md).
