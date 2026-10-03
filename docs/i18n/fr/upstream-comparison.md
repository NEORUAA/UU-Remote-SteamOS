[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[Accueil](../../../i18n/README.fr.md)

# Ce que change Plus

![Base amont, changements de Plus et effets attendus de la conception](../../images/uu-plus-evolution-en.png)

[SVG modifiable](../../images/uu-plus-evolution-en.svg)

Plus reprend le [projet de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge), référence [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a). Wine isolé, relais GNOME, entrée, gestionnaire/service sont hérités.

## Les changements au quotidien

| Domaine | Base amont | Changement Plus | Usage |
| --- | --- | --- | --- |
| Hôte | Ubuntu 24.04 et libei rétroporté isolé | Adaptation Ubuntu 26.04/GNOME 50, libei système ou rétroportage ; cible 24.04 conservée | Consulter les guides de plateforme et de compilation |
| Windows UU | 4.33.0.8907 par défaut et manifestes vérifiés | 4.42.0.2770 vérifié par défaut | Choisir le manifeste de la version UU |
| Canevas | Résolution enregistrée et redimensionnement RDP | Quatre profils jusqu’à 4K, bureau entier et restauration de taille | Choisir 720p, 1080p, 1440p ou 4K et voir la taille actuelle |
| Texte mobile | Normalisation IME et collage Unicode | Évolution des voies Plus et voie texte publique FreeRDP | Saisir du chinois, du code et plusieurs lignes |
| Presse-papiers | Presse-papiers RDP et transactions Unicode | Patch SDL pour vérification en arrière-plan, propriétaire et cache | Copier-coller le texte courant avec le relais en arrière-plan |
| Gestion | Vue de fenêtre privée et retour du focus | Capture indépendante des fenêtres/dialogues et visualiseur réutilisable | Ouvrir le compte ou les réglages UU puis revenir au bureau |
| Curseur | Protection facultative de taille fixe | Repli du thème et corrections de démarrage ; désactivé par défaut | Activer la protection si nécessaire |
| Actions | Commande du bureau par clavier et souris | Actions GNOME bureau/vue d’ensemble | Relier les actions du contrôleur au backend GNOME |
| Outils | Dépendances du relais et commandes UU | Qualité/VNC/FreeRDP/Openbox avec polices, DPI et identifiants locaux | Ouvrir l’outil avec ses réglages propres |
| Compilation et reprise | Nightly SDL/WinPR fixe et reconnexion du service | Sources corrigées fixes, vérification et reprise des profils/visualiseur | Préparer le relais adapté et conserver les réglages |

## Implémentation

- Texte mobile : évolution des voies d’entrée Plus — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- Presse-papiers : patch des sources SDL — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- Gestion : capture indépendante et visualiseur — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- Outils : nouvelle intégration au bureau — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## Voies d’entrée

Les nouvelles installations RDP choisissent `rdp-public` : le courtier passe par les API publiques FreeRDP. Le texte Unicode, ASCII inclus, est collé littéralement en automatique ; les touches physiques restent séparées. Les mises à jour gardent la voie. `legacy` utilise des touches pour les caractères représentables et le collage CJK/sauts ; le lanceur non configuré utilise aussi `legacy`.

Pour comparer FPS et latence, fixez versions, résolution source, qualité/FPS, débit, réseau et charge, puis décrivez la méthode de mesure ; voir [le guide de mesure](performance-evidence.md).
