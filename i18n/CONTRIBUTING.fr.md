[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[Français · UU Remote Ubuntu Plus](README.fr.md)

# Contribuer à UU Remote Ubuntu Plus

Retours, traductions, documentation et code sont bienvenus. Préservez l’attribution et la licence MIT du [pont de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge).

## Décrire problème et parcours

Indiquez Ubuntu, GNOME, Wine, UU, canevas, route d’entrée et reproduction. Distinguez Ubuntu comme hôte, gestionnaire local et Ubuntu comme contrôleur. Privilégiez petites modifications et méthodes de mesure explicites. Utilisez le [formulaire de compatibilité](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

## Environnement de développement

Utilisez Ubuntu et Python système. Ces paquets servent à compiler et aux tests isolés ; install.sh gère l’exécution. Choisissez WINEGCC, MINGW_CC ou HOST_CC sans chemins personnels. Utilisez des préfixes Wine et affichages Xvfb temporaires.

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

## Vérifier les sources

Passez bash -n sur les scripts modifiés, puis ces contrôles. Gardez les avertissements C stricts. Wine, Xvfb ou systemd peuvent être nécessaires : indiquez les tests omis. UURB_TEST_SYSTEMD=1 exige un bus utilisateur utilisable.

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

## Documents et illustrations

Exécutez les tests existants. Les SVG anglais/chinois des flux et du portage partagent leur disposition ; les deux dernières commandes servent seulement au rendu facultatif Node/Sharp. Vérifiez images entières et métadonnées, conservez les codes originaux.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

## Valider l’installation

Installez sur un hôte autorisé et préparez une reconnexion de secours. Le vérificateur complet comprend 270 secondes de stabilité ; image, saisie et reconnexion nécessitent un contrôleur réel. Arrêtez seulement le préfixe UU, jamais pkill wine global.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

## Nouvelles versions UU

Un nouvel exécutable exige examen et manifeste approuvé, SHA-256 complets et justification des changements de même longueur. Documentez restauration identique, démarrage, saisie et retrait. Aucun binaire propriétaire ou journal privé. Voir [maintenance upstream (English)](../docs/upstream-maintenance.md).

## Préparer la publication

Vérifiez liste et différence indexée. Écartez builds, préfixes, caches, état .omc, secrets, identifiants et texte saisi. Préservez authentification, TLS, manifests et suppression réversible.

```bash
git status --short
git diff --cached
```

## Soumettre à la revue

Décrivez problème, résultat et contrôles exécutés ; demandez une revue indépendante. Les FPS réglés ne sont pas une mesure. Voir [qualité](../docs/i18n/fr/quality-guide.md), [Ubuntu](../docs/i18n/fr/ubuntu-26.04-port.md), [sécurité](../docs/i18n/fr/security.md), en gardant MIT et copyright.
