[English](../../source-build.md) · [العربية](../ar/source-build.md) · [Deutsch](../de/source-build.md) · [Español](../es/source-build.md) · [Français](../fr/source-build.md) · [日本語](../ja/source-build.md) · [한국어](../ko/source-build.md) · [Русский](../ru/source-build.md) · [Tiếng Việt](../vi/source-build.md) · [简体中文](../zh-Hans/source-build.md) · [繁體中文](../zh-Hant/source-build.md)

[Accueil](../../../i18n/README.fr.md)

# Compiler et réutiliser le relais

L’installateur compile un client FreeRDP SDL fixé avec les correctifs Plus du presse-papiers et de taille. [Recette](../../../vendor/freerdp-sdl-build/), [verrou source](../../../vendor/freerdp-sdl-build/source-lock.json), [profil produit](../../../patches/freerdp-sdl-product.json) décrivent révisions, archives, outils et 13 fichiers Windows.

<a id="reference-toolchain"></a>

## Préparer les outils de référence Ubuntu 26.04

Sous Ubuntu 26.04 amd64, le [script de préparation](../../../scripts/prepare-build-toolchain.py) télécharge 17 paquets officiels Ubuntu fixés et vérifie 14 fichiers de compilation par rapport à `source-lock.json`. Le [manifeste des paquets](../../../patches/reference-build-packages.json) contient les versions, tailles et empreintes. Le script télécharge, extrait dans un répertoire privé et vérifie les fichiers ; il n’installe pas de paquets système. Depuis la racine du dépôt :

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root"
```

`--packages-dir` choisit le cache ; `--root` doit être un répertoire privé nouveau ou vide. Pour refaire l’extraction et les vérifications depuis le cache sans réseau, choisissez une autre racine vide et ajoutez `--verify-only` :

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root-offline" \
  --verify-only
```

Le script affiche une commande `sudo apt install` contenant les 17 chemins `.deb` locaux. Exécutez-la manuellement sous Ubuntu 26.04 pour installer les outils de référence. La recette utilise des chemins `/usr` fixes ; le répertoire privé sert à vérifier les outils, pas à choisir un autre environnement de compilation.

Lancez ensuite l’installateur normal. Il prépare les autres dépendances de compilation de l’hôte, WineHQ et les paquets d’exécution GNOME, puis compile le relais et vérifie avant déploiement. La préparation contrôle 14 fichiers de référence ; la compilation complète et ses 13 fichiers d’exécution sont vérifiés par ce flux :

```bash
./install.sh
./scripts/verify.sh --quick
```

Sous Ubuntu 24.04, utilisez une sortie déjà validée correspondant au profil actuel via le parcours de réutilisation ci-dessous. Les paquets Ubuntu 26.04 ci-dessus sont propres à 26.04.

## Compilation et cache

Une compilation à partir de sources neuves exige les fichiers exacts du compilateur et des outils vérifiés inscrits dans `source-lock.json`, avec les mêmes octets. Les paquets APT ordinaires de la distribution ne fournissent pas automatiquement cette chaîne.

`./install.sh` prépare les paquets et valide avant remplacement. `build/freerdp` est réutilisé si la provenance correspond au profil, à la recette et aux binaires fixés. Sinon, `scripts/build-winpr.sh` utilise des sources neuves, deux tâches et un délai de 900 secondes, puis vérifie.

Une fois les outils vérifiés installés aux chemins `/usr` de la recette et les dépendances de compilation prêtes, vous pouvez aussi créer un cache de relais séparé :

```bash
UURB_BUILD_DIR=/absolute/path/to/build-work   ./scripts/build-winpr.sh /absolute/path/to/fresh-output
```

Choisissez une nouvelle sortie. Un travail source unique est créé sous le répertoire indiqué, sans utiliser de préfixe Wine actif. Pour réutiliser une sortie validée :

Depuis la racine du dépôt, validez d’abord une sortie existante par rapport au profil actuel. L’installateur normal prépare les dépendances de l’hôte. Réservez `--skip-packages` aux hôtes disposant déjà des outils de compatibilité, de WineHQ et des paquets d’exécution GNOME ; `--skip-account-login` est facultatif avec un compte déjà configuré.

```bash
python3 scripts/verify-freerdp-runtime.py --mode build /absolute/path/to/verified/output
```

Réutilisez ensuite cette sortie par l’entrée existante de l’installateur :

```bash
UURB_FREERDP_PREBUILT_DIR=/absolute/path/to/verified/output   ./install.sh
```

Le cache doit correspondre à la recette, aux binaires et à la provenance du profil actuel. Un profil modifié exige de relancer compilation/validation ; modifier un reçu ou une somme ne valide pas d’autres binaires. L’installateur vérifie la copie avant démarrage.

## Entrées et résultats

FreeRDP/WinPR, SDL 3.2.28, SDL_ttf, OpenH264, FreeType, HarfBuzz et paquets OpenSSL/cJSON/uriparser sont fixés. Correctif et empreintes MinGW/compilateur/outils sont vérifiés avant compilation. Un changement exige une recette révisée.

Les cartes de préfixes fichier/macro/débogage normalisent les chemins. Opaque reste OFF dès la première configuration FreeRDP ; la DLL utilise un nom de sortie relatif. Les chemins locaux ne sont donc pas inscrits.

Avec les outils fixés, deux racines distinctes ont produit les mêmes octets pour les 13 fichiers. Les configurations CMake initiale/répétée ont donné les mêmes métadonnées. Une compilation complète sans sortie précompilée a pris environ 700 secondes, dans les 900, avec vérifications runtime/provenance réussies. Voir [qualité](quality-guide.md) et [coûts](performance-evidence.md).
