[English](../../quality-guide.md) · [العربية](../ar/quality-guide.md) · [Deutsch](../de/quality-guide.md) · [Español](../es/quality-guide.md) · [Français](../fr/quality-guide.md) · [日本語](../ja/quality-guide.md) · [한국어](../ko/quality-guide.md) · [Русский](../ru/quality-guide.md) · [Tiếng Việt](../vi/quality-guide.md) · [简体中文](../zh-Hans/quality-guide.md) · [繁體中文](../zh-Hant/quality-guide.md)

[Accueil](../../../i18n/README.fr.md)

# Qualité, résolution et fréquence d’images

Choisissez le canevas sur Ubuntu, puis la qualité de transmission sur l’ordinateur ou le téléphone de contrôle. Taille, compression, FPS demandés et plafond de débit sont indépendants.

## Choisir le canevas

Ouvrez **UU Remote 画质与分辨率** dans GNOME ou utilisez :

```bash
uu-remote quality gui
uu-remote quality list
uu-remote quality status
uu-remote quality apply 2160p
uu-remote quality guide
```

![Sélecteur de quatre résolutions](../../images/quality-presets.png)

| Profil | Canevas | Usage |
| --- | --- | --- |
| `720p` | 1280 × 720 | Petit écran ou connexion limitée |
| `1080p` | 1920 × 1080 | Usage courant ; défaut initial |
| `1440p` | 2560 × 1440 | Plus d’espace avec moins de pixels que 4K |
| `2160p` | 3840 × 2160 | Texte fin et espace 4K complet |

Une réinstallation conserve le choix enregistré. Le redimensionnement intelligent affiche tout le bureau et transforme les coordonnées du pointeur avec la même géométrie. Résolution et proportions de la source influencent l’image ; le canevas ne change pas l’écran physique et la capture peut traiter toute la source.

Le sélecteur distingue taille enregistrée au démarrage/RDP et canevas actuel. Modifier la première reconnecte brièvement UU. Réappliquer le profil enregistré restaure le canevas en direct sur la voie RDP compatible sans redémarrer le relais, avec vérification de la taille. Un minuteur armé avant modification restaure la configuration précédente si le pont ne devient pas prêt. Attendez la fin de la récupération.

Les profils fixes utilisent `--follow-desktop-resolution off`, valeur initiale. Désactivez le suivi s’il était actif. Voir [installation](../../../i18n/README.fr.md) et `./install.sh --help`. L’agrandissement de la source 4K testée en 5K paraissait moins net sur Mac sans détail supplémentaire ; les choix courants s’arrêtent à 4K. Les 60 Hz nominaux concernent l’écran virtuel ; les FPS dépendent de toute la connexion.

## Qualité du contrôleur

Ordinateur : **控制中心 → 画质**. Téléphone : **操作 → 显示**. True Color se règle aussi côté contrôleur lorsque disponible.

![Menu natif de qualité UU](../../images/uu-native-quality-menu.png)

Cet exemple montre Ubuntu contrôlant un Mac. Appareils et codec déterminent les choix. La qualité règle compression/détails ; FPS indique la fréquence demandée. True Color améliore texte coloré et contours. Si UU signale une limite matérielle, choisissez un niveau disponible. Comparez le même texte et mouvement.

Documentation NetEase : [FPS / Super Screen](https://uuyc.163.com/help/superscreen.html) · [True Color](https://uuyc.163.com/features/color/) · [UU](https://uuyc.163.com/help/20241216/40221_1200122.html). Super Screen/pilote virtuel sous Wine et 144 FPS restent à tester. Voir [mesures](performance-evidence.md).

## Plafond de débit

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` demande un plafond de **20 Mbps**, `0` le supprime. Ce n’est ni un débit cible, ni un réglage FPS/taille. Les profils conservent ce paramètre. Un plafond bas peut dégrader les détails en mouvement.

## Curseur et bureau

La protection facultative du curseur est désactivée à l’installation. Pour un pointeur trop grand :

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size 24
```

`--cursor-size auto` suit le bureau ; tailles fixes : 24–128 pixels. Les réglages GNOME/applications sont séparés. Le Dock suit GNOME. Les actions Android bureau/toutes les fenêtres sont reliées au bureau/aperçu GNOME ; les boutons réels restent à tester.

## Gestion et récupération

`uu-remote open` ouvre le visualiseur séparé. Pour l’agrandir :

```bash
UURB_WINDOW_SCALE=2 ./install.sh --skip-packages --skip-account-login
```

Échelles : `1` par défaut, `1.5`, `2`, `3`. Elles concernent le visualiseur, pas les DPI Wine ou la résolution. Son presse-papiers est isolé ; le copier/coller du bureau utilise le relais.

```bash
uu-remote status
uu-remote quality status
uu-remote network
uu-remote logs
```

Le service utilisateur redémarre les composants défaillants, avec possible reconnexion. Le retour de profil récupère les paramètres ; le déploiement possède son propre mécanisme. Voir [dépannage](troubleshooting.md), [compilation](source-build.md). Le contrôle sortant depuis Wine a d’autres limites. Moniteur physique et sorties virtuelles : [Ubuntu 26.04](ubuntu-26.04-port.md), tests à réaliser. Téléphone → ToDesk → Mac → UU répète encore du texte ; les connexions directes fonctionnent.
