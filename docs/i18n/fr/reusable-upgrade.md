[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [中文（简体）](../zh-Hans/reusable-upgrade.md) · [中文（繁體）](../zh-Hant/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md)

[← Retour à l’accueil français](../../../i18n/README.fr.md)

# Mise à jour réutilisable conservant la connexion

`uu-remote-upgrade` et `uu-remote upgrade` combinent mise à jour du dépôt, promotion UU acceptée, renouvellement du pont et vérification. `status` affiche l’état, `check` ne modifie pas le produit, `apply` attend l’inactivité. `apply --now` saute seulement cette attente, sans forcer de binaire inconnu ou non accepté.


Après avoir extrait le tag de version, lancez `git switch main` avant les mises à jour habituelles qui récupèrent les sources. La branche maintenue est `origin/main` ; le tag explicite de réinstallation reste `v0.1.0`. Pour conserver volontairement les sources extraites du tag pendant une mise à jour, utilisez `--no-pull`.

## Transaction

Le checkout doit être propre et non detached. Fetch et fast-forward ne fusionnent pas une histoire divergente ; le script repart des nouvelles sources si nécessaire. Tests et analyse shell précèdent l’opération. Produit approuvé, relais, route, temporisations et marqueurs de compte sont vérifiés. Seul l’installateur officiel dont hash et acceptance correspondent au manifeste continue.

La promotion copie le préfixe Wine complet, installe dans ce même préfixe, applique les patches et compare octet par octet le login registry et les deux arbres de compte. Deux contrôles runtime encadrent la période de stabilité. Ensuite le runtime du pont est sauvegardé séparément et les helpers/services renouvelés en préservant environment. Track et paramètres Codex restent inchangés. XRDP est seulement interrogé ; changer son état actif fait échouer l’opération.

## Restauration et entrée

Échec ou interruption restaure tout le préfixe et produit `promotion-blocked`, sans nouvel essai automatique. Réenfiler explicitement la même version acceptée exige un autre commit du code de promotion ; les anciennes tâches vont dans `tasks/retired/`. Un échec de renouvellement des sources restaure le runtime après promotion. Aucun timer n’efface les snapshots.

Les valeurs X11 d’exemple ne sont pas à recopier sur un autre hôte : sa route sauvegardée prime. Le vérificateur rapide ne tape pas dans votre application ; testez ensuite téléphone, touches physiques rapides et souris/déplacement/clic/glisser/molette.

Le bus persistant `/run/user/UID/bus` évite d’interroger le mauvais user manager depuis un terminal imbriqué. L’incident historique 4.34 de juillet 2026 ne décrit pas Plus 4.42 actuel. Ses correctifs concernaient un verifier absent, les timestamps PE et une course de readiness ; les contrôles actuels attendent jusqu’à 45 secondes le vrai listener et l’auxiliaire choisi. Ne transportez vers un autre hôte que les sources, pas préfixe, keyring ou état privé. `~/.local/bin` doit être dans `PATH`.

[Mises à jour automatiques](automatic-updates.md) · [Clavier](adaptive-keyboard-relays.md)

## Commandes et valeurs techniques

```bash
uu-remote-upgrade status
uu-remote upgrade status
uu-remote upgrade check
uu-remote upgrade apply
uu-remote upgrade apply --now
./scripts/upgrade-uu-remote.sh apply --now
```

```text
UURB_TEXT_KEY_DELAY_MS=8
UURB_PHYSICAL_KEY_DELAY_MS=0
UURB_KEYBOARD_ROUTE=x11
UURB_NETWORK_INTERFACE=default
unix:path=/run/user/UID/bus
~/.local/state/uu-remote-updater/tasks/*/promotion/snapshot-prefix
~/.local/state/uu-remote-upgrader/transactions/TIMESTAMP/
~/.local/state/uu-remote-upgrader/latest
```

```bash
git status --short
git switch main
git pull --ff-only origin main
./install.sh --skip-packages --skip-account-login
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/upgrade-uu-remote.sh check
```

## Code source et sujets associés


Les détails techniques sont disponibles en anglais et en chinois simplifié:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
