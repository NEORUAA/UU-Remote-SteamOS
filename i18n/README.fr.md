<div align="center">

[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

<a href="README.fr.md"><img src="../docs/images/uu-plus-logo.png" alt="UU Remote Ubuntu Plus" width="140"></a>

# UU Remote Ubuntu Plus

**Les idées vous suivent ; votre environnement de développement reste sur Ubuntu.**

Votre éditeur, vos terminaux et vos sessions restent sur Ubuntu. Connectez-vous depuis votre téléphone, un Mac ou un PC Windows, faites du Vibe Coding à votre rythme, puis changez d’écran et continuez à coder.

[![Ubuntu 24.04 / 26.04](https://img.shields.io/badge/Ubuntu-24.04%20%7C%2026.04-E95420?logo=ubuntu&logoColor=white)](../docs/i18n/fr/ubuntu-26.04-port.md)
[![GNOME 46 / 50](https://img.shields.io/badge/GNOME-46%20%7C%2050-4A86CF?logo=gnome&logoColor=white)](../docs/i18n/fr/architecture.md)
[![UU Remote 4.42](https://img.shields.io/badge/UU_Remote-4.42.0.2770-00A870)](../patches/uu-remote-4.42.0.2770.json)
[![MIT](https://img.shields.io/badge/License-MIT-2F81F7)](../LICENSE)

<img src="../docs/images/vibe-coding-cross-device-en.png" alt="UU Remote Ubuntu Plus" width="1120">

</div>

Plus relie NetEase UU Remote à votre session Ubuntu GNOME ouverte. L'application
officielle Windows UU fonctionne dans un environnement Wine dédié. Un relais local
présente le vrai bureau, tandis qu'une fenêtre distincte donne accès au compte et
aux réglages UU. Vos applications et fichiers restent dans la même session.

Le projet s'appuie sur **[UU Remote Ubuntu Bridge de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
Plus étend la compatibilité Ubuntu et UU, ajoute quatre formats de canevas et
améliore la saisie, le presse-papiers et les commandes de gestion.

L’installateur vise Ubuntu 24.04 / GNOME 46 et Ubuntu 26.04 / GNOME 50 sur x86-64, avec UU 4.42.0.2770. Une nouvelle installation sélectionne 1080p et laisse la protection facultative du curseur désactivée.

Les onze pages de langue et leurs guides techniques décrivent Plus dans chaque langue ; l’anglais reste la référence canonique.

## De l'installation au travail à distance

1. Installez le pont sur votre bureau Ubuntu.
2. Lancez `uu-remote open` et connectez-vous à UU dans la fenêtre de gestion.
3. Connectez votre téléphone, Mac ou ordinateur Windows à cet hôte avec UU.
4. Choisissez un canevas et utilisez vos applications habituelles.

## Fonctionnalités et améliorations

Le projet amont fournit le relais de bureau, le clavier et la souris, le traitement de l’IME du téléphone et la récupération des services. Plus prolonge cette base avec une compatibilité plus récente, des réglages de qualité plus clairs et des améliorations au quotidien.

| Usage quotidien | Apports de Plus |
| --- | --- |
| Ubuntu et UU plus récents | Ubuntu 26.04 / GNOME 50 et UU 4.42, tout en conservant l’installation Ubuntu 24.04. |
| Choisir son canevas | Passez entre 720p, 1080p, 1440p et 4K dans le sélecteur graphique. Le bureau complet s’adapte au canevas et le réglage enregistré peut être restauré. |
| Chinois, code et copier-coller | Corrige la transmission du texte du téléphone et l’actualisation du presse-papiers. Le nouveau texte arrive sur le bureau ; code et texte multiligne conservent leur contenu. |
| Ouvrir les réglages, rester connecté | Capture séparément le gestionnaire UU et ses menus. Fermer la visionneuse rend le focus au relais du bureau. |
| Des outils locaux plus pratiques | Accès aux réglages de qualité, VNC, FreeRDP et Openbox, avec améliorations des polices, du DPI et du démarrage. |
| Installer et entretenir | Compile le relais depuis des sources fixées et contrôle les composants avant installation. Restaure les changements de canevas échoués et propose un aperçu de la désinstallation. |

Consultez la [comparaison avec l’amont](../docs/i18n/fr/upstream-comparison.md) pour les changements et leur contexte de version.

<img src="../docs/images/experience-refinements-en.png" alt="Expérience et mesures" width="1120">

[Expérience et mesures](../docs/i18n/fr/performance-evidence.md)

## Installation rapide

Sur un hôte Ubuntu x86-64 avec une session GNOME ouverte, clonez le projet :

```bash
git clone https://github.com/llmir/uu-remote-ubuntu-plus.git
cd uu-remote-ubuntu-plus
```

L’installation nécessite la chaîne de compilation vérifiée pour construire le relais, ou un résultat validé correspondant au profil du produit ; les binaires du relais ne sont pas inclus. Ubuntu 26.04 dispose d’un parcours de préparation des outils de référence ; Ubuntu 24.04 utilise la réutilisation d’une sortie validée. [Préparer la chaîne et réutiliser le relais](../docs/i18n/fr/source-build.md#reference-toolchain)

Une fois les outils ou la sortie correspondante prêts, lancez l’installateur normal :

```bash
./install.sh
./scripts/verify.sh --quick
uu-remote open
```

L'installateur prépare les dépendances, compile les composants, configure GNOME
Remote Desktop et lance les services utilisateur. Le mot de passe du relais est
enregistré dans GNOME Keyring, puis UU s'ouvre pour la connexion au compte.
Une réinstallation conserve les réglages et l'état du compte. Pour démarrer en 4K :

```bash
./install.sh --resolution 3840x2160
```

Décrivez votre environnement et les étapes de reproduction dans le [formulaire de compatibilité](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

La première installation peut télécharger et compiler des dépendances.
Consultez [Compilation](../docs/i18n/fr/source-build.md) et [Sécurité](../docs/i18n/fr/security.md).
Téléchargez le client UU pour Windows depuis le site officiel NetEase [uuyc.163.com](https://uuyc.163.com/). Le pont l’exécute dans un environnement Wine dédié. UU conserve sa propre licence.

## Vue technique

<img src="../docs/images/architecture-premium-v2-en.png" alt="Image Ubuntu, saisie et gestion locale UU." width="1120">

Le bureau Ubuntu traverse GNOME RDP vers le relais SDL / FreeRDP, puis UU vers le contrôleur. Clavier et souris reviennent par le pont de saisie à la même session. Le compte et les réglages UU disposent d’une fenêtre locale dédiée.

Lancez `uu-remote open` pour la gestion ; le pont reste actif après fermeture de la visionneuse. `uu-remote console` offre une vue facultative dans le navigateur local. Voir [Architecture](../docs/i18n/fr/architecture.md) pour les modules et chemins de saisie.

## Résolution et qualité

<img src="../docs/images/quality-controls-cartoon-v2-en.png" alt="Ubuntu canvas and UU controller quality controls" width="1120">

Ouvrez **UU Remote 画质与分辨率** dans GNOME, ou lancez :

```bash
uu-remote quality gui
```

Le bureau complet s'adapte au canevas, sans modifier la résolution du moniteur
physique. Le changement reconnecte brièvement le pont ; un échec restaure la
configuration précédente.

```bash
uu-remote quality list
uu-remote quality apply 2160p
uu-remote quality status
uu-remote quality guide
```

Réglez la qualité d'encodage, les FPS et True Color dans le **contrôleur UU** :
**Centre de contrôle → Qualité** sur ordinateur ; **Opérations → Affichage** sur téléphone.

Le plafond de débit se règle séparément :

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` demande un plafond de 20 Mbps ; `0` le retire. Format du canevas, qualité,
FPS demandés et débit sont des réglages distincts. Consultez le
[guide de qualité](../docs/i18n/fr/quality-guide.md).

## Saisie et curseur

Les saisies de l’IME du téléphone, les fragments de code et les textes multiligne empruntent le chemin de texte vers Ubuntu. Touches physiques et raccourcis conservent leurs événements clavier. Plus corrige la transmission du texte et le rafraîchissement du presse-papiers pour la saisie et le copier-coller au quotidien. Voir [Relais clavier](../docs/i18n/fr/adaptive-keyboard-relays.md) pour les modes de saisie.

La protection facultative du curseur vient de l'amont. Plus améliore ses ressources
et leur traitement. Pour l'activer :

```bash
./install.sh --skip-packages --skip-account-login \
  --cursor-guard on --cursor-size auto
```

`auto` suit la taille du curseur du bureau ; une valeur telle que `24` fixe celle du
curseur de secours. `--cursor-guard off` la désactive.
La réinstallation reconnecte brièvement UU.

## Utilisation et maintenance

```bash
uu-remote status
uu-remote network
uu-remote logs
uu-remote restart
uu-remote stop
```

`uu-remote open` ouvre la gestion et `uu-remote login` permet la connexion ou sa
récupération. Redémarrage, connexion et réinstallation interrompent brièvement
la session distante.

Enregistrez vos modifications locales, actualisez les sources et réinstallez :

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

Les changements du code d'exécution prennent effet après réinstallation.
Consultez [Mise à niveau](../docs/i18n/fr/reusable-upgrade.md) pour `uu-remote upgrade` et
[Mises à jour automatiques](../docs/i18n/fr/automatic-updates.md) pour la maintenance facultative.

Pour retirer le pont en conservant l'état du compte UU :

```bash
./uninstall.sh --dry-run
./uninstall.sh
```

`./uninstall.sh --purge` retire aussi le préfixe Wine dédié, les identifiants du relais
et l'activation de GNOME RDP.

## Au-delà d’Ubuntu

L’installateur actuel cible Ubuntu 24.04 et 26.04 sur x86-64. Le [guide de portage Linux](../docs/i18n/fr/porting.md) distingue trois couches pour de futurs portages :

- Réutiliser le cœur de compatibilité UU, le relais et la saisie.
- Adapter les paquets, chemins Wine et services de la distribution.
- Relier les mécanismes de capture, saisie, modes d’affichage et actions propres au bureau.

D’autres distributions GNOME peuvent reprendre davantage d’intégration existante. KDE et Xfce demandent leurs propres composants de bureau.

## Documentation et contributions

- [Qualité](../docs/i18n/fr/quality-guide.md), [Compilation](../docs/i18n/fr/source-build.md) et [Ubuntu 26.04](../docs/i18n/fr/ubuntu-26.04-port.md)
- [Architecture](../docs/i18n/fr/architecture.md), [Sécurité](../docs/i18n/fr/security.md) et [Dépannage](../docs/i18n/fr/troubleshooting.md)
- [Comparaison](../docs/i18n/fr/upstream-comparison.md) et [Mesures](../docs/i18n/fr/performance-evidence.md)
- [Historique](CHANGELOG.fr.md) et [Contribuer](CONTRIBUTING.fr.md)

Indiquez les versions, les réglages et les étapes permettant de reproduire le comportement.

## Soutenir le projet

**Offrez-moi un café ☕**

UU et Ubuntu continuent d’évoluer. Je poursuivrai l’adaptation de Plus aux nouvelles versions et l’amélioration de la saisie, du copier-coller et de l’image. Un café contribue aux essais de versions, aux outils de développement et aux tokens.

| PayPal | Alipay · CNY | AlipayHK · HKD | WeChat · CNY | WeChat · HKD |
| :---: | :---: | :---: | :---: | :---: |
| <a href="https://paypal.me/mirmirlin"><img src="../docs/images/support-paypal-en.png" alt="PayPal" width="160"></a> | <a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support-alipay-cny-en.png" alt="Alipay · CNY" width="160"></a> | <a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support-alipay-hkd-en.png" alt="AlipayHK · HKD" width="160"></a> | <a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support-wechat-zh-en.png" alt="WeChat · CNY" width="160"></a> | <a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support-wechat-en-en.png" alt="WeChat · HKD" width="160"></a> |

<details>
<summary>Codes de paiement Alipay et WeChat</summary>

<p><a href="../docs/i18n/fr/support.md#alipay-cny">Alipay CNY</a><br><a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support/alipay-cny.jpg" alt="Alipay CNY" width="240"></a></p>

<p><a href="../docs/i18n/fr/support.md#alipay-hkd">AlipayHK HKD</a><br><a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support/alipay-hkd.png" alt="AlipayHK HKD" width="240"></a></p>

<p><a href="../docs/i18n/fr/support.md#wechat-zh">WeChat · CNY</a><br><a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support/wechat-zh.png" alt="WeChat · CNY" width="240"></a></p>

<p><a href="../docs/i18n/fr/support.md#wechat-en">WeChat · HKD</a><br><a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support/wechat-en.png" alt="WeChat · HKD" width="240"></a></p>

</details>

Les signalements reproductibles, les retours de portage Linux et les pull requests sont aussi les bienvenus. Merci de contribuer à la prochaine version.

[Soutenir UU Remote Ubuntu Plus](../docs/i18n/fr/support.md)

## Remerciements et licence

Basé sur **[UU Remote Ubuntu Bridge de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
L'avis de copyright original et la [licence MIT](../LICENSE) sont conservés.
UU et les dépendances gardent leurs licences et marques.
Ce projet est maintenu par une communauté indépendante.

Icônes des moyens de paiement : [Simple Icons](https://simpleicons.org/) (CC0) ; les marques restent la propriété de leurs détenteurs.
