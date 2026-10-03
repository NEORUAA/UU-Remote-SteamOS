[English](../../ubuntu-26.04-port.md) · [العربية](../ar/ubuntu-26.04-port.md) · [Deutsch](../de/ubuntu-26.04-port.md) · [Español](../es/ubuntu-26.04-port.md) · [Français](../fr/ubuntu-26.04-port.md) · [日本語](../ja/ubuntu-26.04-port.md) · [한국어](../ko/ubuntu-26.04-port.md) · [Русский](../ru/ubuntu-26.04-port.md) · [Tiếng Việt](../vi/ubuntu-26.04-port.md) · [简体中文](../zh-Hans/ubuntu-26.04-port.md) · [繁體中文](../zh-Hant/ubuntu-26.04-port.md)

[Accueil](../../../i18n/README.fr.md)

# Ubuntu 26.04 et GNOME 50

Plus étend le [pont MIT de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge) à Ubuntu 26.04/GNOME 50 x86-64 et conserve 24.04/GNOME 46. Isolation Wine, manifestes audités, courtier, relais et service supervisé restent la base.

L’installation du relais exige la chaîne vérifiée exacte ou une sortie validée existante ; les paquets APT ordinaires ne fournissent pas automatiquement cette chaîne. Voir [prérequis de compilation et réutilisation du cache](source-build.md).

| Composant | Référence amont | Plus |
| --- | --- | --- |
| Ubuntu | 24.04 | 24.04/26.04 ; autres : `UURB_ALLOW_UNVALIDATED_UBUNTU=1` |
| Windows UU | 4.33.0.8907 | 4.42.0.2770 approuvé ; anciens manifestes disponibles |
| libei | Backport isolé 1.2.1 | Système si corrigé, sinon backport |
| Relais | SDL nightly fixé/WinPR | Source FreeRDP/SDL fixée et corrigée ; [compilation](source-build.md) |
| CI | 24.04 | Cibles 24.04/26.04, résultats selon exécution |

L’installation observée utilise GRD 50.2 et libei 1.5.0. Les anciennes bibliothèques peuvent utiliser `ee27dd5c92e4e9496a36ca2d4112049fe02d2269`. `UURB_LIBEI_MODE=system|backport` enregistre le choix ; `verify.sh` vérifie la bibliothèque chargée. Wine vient de WineHQ stable.

## Bureau

Quatre profils, ajustement complet et pointeur ; première installation 1080p, mises à jour conservées. Le changement enregistré reconnecte avec retour automatique ; réappliquer restaure le canevas vivant. L’utilisateur confirme reconnexion et menu jusqu’à 4K. RDP neuf utilise `rdp-public`, les mises à jour gardent leur voie. Unicode et touches physiques sont séparés. Gestionnaire/popups capturés à part ; fermer rend le focus au relais, gestionnaire toujours mappé. Presse-papiers bureau actif, gestionnaire isolé.

| Fonction | Résultat |
| --- | --- |
| Chinois direct téléphone/Mac | Confirmé durant l’intégration |
| Copier/coller texte | Normal selon utilisateur |
| Mise à jour Mac UU | Reconnexion/chinois/collage normaux ; 4K similaire |
| Superposition/focus | Résolus selon utilisateur ; contrôles sélectionnés normaux |
| Android | Backend bidirectionnel normal ; boutons à tester |
| Curseur | Thème/tests partiels normaux ; formes complètes à tester |
| Moniteur/sortie virtuelle | À tester sur cet hôte |
| Téléphone → ToDesk → Mac → UU | `a` répété non résolu |

Lanceurs VNC/FreeRDP/Openbox : polices CJK, DPI et identifiants limités aux outils. Dock réglé par GNOME. Contrôle sortant et résolution physique sont distincts du canevas entrant. [Qualité](quality-guide.md), [architecture](architecture.md), [comparaison](upstream-comparison.md).

## Mises à jour

Gardez Plus comme `origin` :

```bash
git remote add upstream https://github.com/lachlanchen/uu-remote-ubuntu-bridge.git
git fetch upstream
```

Examinez l’amont en branche de développement. Après modification :

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

L’installation interrompt brièvement la connexion ; le digest signale les changements jusqu’à réinstallation. [Mise à jour réutilisable](reusable-upgrade.md) décrit le runtime, le retour de profils les paramètres. Un hash UU inconnu bloque le correctif automatique ; nouvelle version : examen sémantique, manifeste approuvé et contrôles, voir [maintenance](../../upstream-maintenance.md). Source MIT et manifestes sont distribués ; UU/dépendances conservent leurs licences.
