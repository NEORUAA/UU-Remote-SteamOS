[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [中文（简体）](../zh-Hans/automatic-updates.md) · [中文（繁體）](../zh-Hant/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Русский](../ru/automatic-updates.md)

[← Retour à l’accueil français](../../../i18n/README.fr.md)

# Vérifications automatiques et réparation reprenable

La maintenance sépare observation, réparation privée des sources et promotion active explicitement acceptée. Un contrôle normal n’interrompt pas un relais fonctionnel.

## Réglages et timers

Plus commence son propre historique de versions avec `v0.1.0`. Les tags datés des chemins de saisie appartiennent à l’histoire du projet d’origine et ne sont pas inclus dans ce dépôt indépendant. L’installation ordinaire n’en a pas besoin. Dès que le tag Plus existe localement, sélectionnez-le explicitement avec `--track v0.1.0 --branch main` ; le configurateur utilise encore les anciens noms par défaut et refuse un tag absent.

Après avoir extrait le tag de version, lancez `git switch main` avant les mises à jour habituelles qui récupèrent les sources. La branche maintenue est `origin/main` ; le tag explicite de réinstallation reste `v0.1.0`. Pour conserver volontairement les sources extraites du tag pendant une mise à jour, utilisez `--no-pull`.

`--auto-promote-accepted` autorise seulement de futures versions acceptées par mainteneur et liées aux hashes, pas un brouillon Codex. Modèle, reasoning et chemin absolu Codex sont dans `updater.json` ; le même utilisateur doit être connecté. Toutes les fenêtres d’usage inclus doivent rester sous le seuil par défaut de 20 % ; l’impossibilité de vérifier reporte d’au moins une heure.

`uu-remote-update-check.timer` passe chaque jour vers 04:20 avec délai aléatoire et douze minutes après boot ; `Persistent=true` rattrape un contrôle manqué. Le monitor démarre à sept minutes puis quinze minutes après chaque exécution.

## Observation et réparation

Le checker suit la redirection HEAD officielle, retire les clés query temporaires et compare les versions complètes. ETag, taille et sidecar hash évitent de télécharger à nouveau les mêmes octets. Un endpoint plus ancien n’est pas une mise à jour. Deux anomalies espacées de 20 secondes créent preuve et tâche sans arrêter Wine/RDP/UU. Seul l’opt-in distinct `--auto-reinstall` permet la récupération.

Les téléchargements sont plafonnés à 1 GiB. Les hashes inconnus sont extraits statiquement et analysés dans un clone privé, avec contrat copié en contexte `0600`. Un wrapper non extractible exige un staging explicite sans réseau. Codex ne peut ni sudo, modifier le préfixe actif, pousser ni approuver ses propres conclusions binaires.

## Promotion acceptée

Hash officiel, manifeste `approved`, acceptance schema-1 et preuves doivent coïncider dans le même commit récupéré d’`origin/main`, avec hashes installer/server patché liés. Tests : préfixe jetable, contrôleur, reconnexion, démarrage froid, restart, signaling neuf et login conservé ; stabilité de 270–1800 secondes. La promotion automatique doit être activée et UU normalement calme pendant 45 minutes.

Seul le service pont s’arrête. Copie complète avec 1 GiB de réserve, installation dans le même préfixe, comparaison exacte des comptes, nouveau room et deux contrôles runtime. XRDP ne change pas. State et préfixe partagent le filesystem. Échec, reboot ou interruption restaure l’ancien, conserve le snapshot et bloque la répétition automatique. `--now` saute uniquement l’attente d’inactivité.

## Tâches, confidentialité et sandbox

L’UUID reçu à `thread.started` permet `codex exec resume` ; sans UUID un nouveau thread reprend le contexte. Retry augmente de 15 minutes à 24 heures. Résultats de schéma testés séparément : `ready-for-review`, `no-change`, `blocked` ; phases de promotion : `promotion-waiting-idle`, `promotion-running`, `promoted`, `promotion-blocked`.

Répertoires privés `0700`, fichiers `0600`, push du clone désactivé, Codex workspace-write/never et service `NoNewPrivileges=yes` ; l’authentification garde besoin du réseau. Sous Ubuntu 24.04, les mount namespaces du user service ne doivent pas bloquer Bubblewrap imbriqué. Pour `codex-sandbox-deferred`, installez seulement le profil AppArmor distro ci-dessous sans relâcher globalement les restrictions. `retry` conserve preuves et clone, remplace le thread inutilisable et importe staging seulement avec les hashes installer/server/healthd corrects.

`disable` garde les preuves ; `disable --purge-state` supprime aussi configuration et état privés. Sur un autre ordinateur, copiez seulement les sources et choisissez son propre profil d’entrée.

[Mise à jour](reusable-upgrade.md) · [Sécurité](security.md)

## Commandes et valeurs techniques

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
uu-remote upgrade apply --now
```

```bash
sudo apt install apparmor-profiles
sudo install -o root -g root -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
uu-remote update retry
systemd-run --user --wait --pipe --collect \
  --property=NoNewPrivileges=yes \
  /usr/bin/bwrap --die-with-parent --unshare-user --uid 0 --gid 0 \
  --ro-bind / / /bin/true
systemctl --user cat uu-remote-repair-monitor.service
./scripts/configure-updater.sh status
./scripts/configure-updater.sh disable
./scripts/configure-updater.sh disable --purge-state
```

## Code source et sujets associés


Les détails techniques sont disponibles en anglais et en chinois simplifié:

- [automated-repair-agent-handoff](../../automated-repair-agent-handoff.md) · [简体中文](../zh-Hans/automated-repair-agent-handoff.md)
- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
