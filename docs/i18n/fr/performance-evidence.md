[English](../../performance-evidence.md) · [العربية](../ar/performance-evidence.md) · [Deutsch](../de/performance-evidence.md) · [Español](../es/performance-evidence.md) · [Français](../fr/performance-evidence.md) · [日本語](../ja/performance-evidence.md) · [한국어](../ko/performance-evidence.md) · [Русский](../ru/performance-evidence.md) · [Tiếng Việt](../vi/performance-evidence.md) · [简体中文](../zh-Hans/performance-evidence.md) · [繁體中文](../zh-Hant/performance-evidence.md)

[Accueil](../../../i18n/README.fr.md)

# Expérience et performance

![Améliorations du chinois, du presse-papiers et de la gestion](../../images/experience-refinements-en.png)

[SVG modifiable](../../images/experience-refinements-en.svg)

![Aire des pixels et choix des quatre canevas](../../images/canvas-pixel-scale-en.png)

[SVG modifiable](../../images/canvas-pixel-scale-en.svg)

Choisissez 720p/1080p/1440p/4K selon écran/connexion ; qualité, FPS demandés et plafond restent séparés.

## Usage courant

Les améliorations récentes portent sur la saisie du chinois, le collage de texte et la gestion des fenêtres.

| Scène | Contexte | Expérience précédente | Expérience améliorée |
| --- | --- | --- | --- |
| Chinois sur téléphone | Ancienne saisie mobile dans Plus | Une partie du texte envoyé n’arrivait pas correctement au bureau | Le chinois envoyé par connexion directe du téléphone arrive correctement sur le bureau Ubuntu |
| Copier et coller | Ancien relais de texte dans Plus | Un nouveau copier pouvait encore être suivi du collage d’un ancien texte | Le texte nouvellement copié est actualisé pour le collage sur le bureau ; le copier/coller courant depuis un ordinateur fonctionne |
| Réglages et fenêtres UU | Ancienne vue de gestion dans Plus | La gestion pouvait recouvrir l’image du bureau ou laisser le focus ailleurs | Les réglages restent séparés du bureau ; fermer la vue de gestion rend le focus au bureau |
| Netteté et taille | Essai d’agrandissement du canevas de Plus | Agrandir la source 4K testée n’ajoutait aucun détail et dégradait l’image | Quatre profils affichent le bureau entier et restaurent la taille enregistrée ; 4K suffit pour la source testée |
| Reconnexion | Mise à jour du client Mac UU | La mise à jour Mac UU demandait de revoir les usages courants | Reconnexion, chinois direct et collage restent fonctionnels ; la sensation en 4K est similaire |

La [comparaison](upstream-comparison.md) distingue la base amont, la compatibilité avec les nouvelles versions, les ajouts et les corrections au cours de l’usage de Plus.

![Base amont, changements de Plus et effets attendus de la conception](../../images/uu-plus-evolution-en.png)

[SVG modifiable](../../images/uu-plus-evolution-en.svg)

**Effet attendu de la conception :** un texte actualisé à temps et un retour de focus prévisible devraient réduire les tentatives de collage répétées et les interruptions entre réglages et bureau. Un canevas plus petit fournit moins de pixels par image ; la réponse visible dépend aussi de la capture, de l’encodage, du réseau et de l’affichage du contrôleur.

| Canevas | Pixels par image | Rapport à1080p |
| --- | ---: | ---: |
| 1280 × 720 | 921,600 | 0.44× |
| 1920 × 1080 | 2,073,600 | 1.00× |
| 2560 × 1440 | 3,686,400 | 1.78× |
| 3840 × 2160 | 8,294,400 | 4.00× |

Ce sont des rapports d’aire. Capture complète possible ; compression, mouvement/réseau affectent la charge. L’ajustement ne change pas l’écran physique.

| Réglage | Usage |
| --- | --- |
| Canevas Ubuntu | Taille relais ; départ1080p,4K pour texte/espace |
| Qualité/FPS/True Color | Compression, fréquence demandée, couleur compatible |
| `uu-remote quality bitrate 20` | Plafond20 Mbps ; `0` supprime, trop bas réduit détail mobile |

[Qualité](quality-guide.md) décrit menus, commandes, récupération.

## Coût de compilation

Construction complète depuis sources propres, préparation et checks :

| Élément | Observation |
| --- | --- |
| Durée | 699.851 s (~11min40s) |
| Limites | CPU équivalent2 cœurs ; mémoire4 GiB |
| Pic déclaré | ~1.8 GB, lecture service arrondie |
| Swap | 0 octet |
| Sortie | 13 binaires Windows |
| Reproductibilité | Octets identiques à entrées fixes dans d’autres répertoires |

Entrée normale : chemins normalisés/configuration explicite. Téléchargements/compilateur influencent une autre machine ; sortie validée réutilisable : [build](source-build.md).

| Environnement | Ubuntu | GNOME | Windows UU |
| --- | --- | --- | --- |
| Référence amont | 24.04 | 46 | 4.33.0.8907 |
| Plus local | 26.04 | 50 | 4.42.0.2770 |

## Mesure comparable

Les relevés existants ne contiennent aucune mesure comparable des FPS du contrôleur ou de la latence entre saisie et image visible pour l’amont fixé et Plus. Les temps du relais et les essais de quota CPU mesurent des composants.


Fixez hôte/contrôleur, résolution, application, réseau, qualité/FPS/débit. Environnements séparés et versions fixées, frontière amont24.04 prise en compte. Chronométrez une action jusqu’à réponse visible ; comptez les mises à jour visibles sur une scène reproductible. Répétez, indiquez dispersion/netteté et méthode.
