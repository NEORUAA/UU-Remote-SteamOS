[English](../../security.md) · [العربية](../ar/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Tiếng Việt](../vi/security.md) · [中文（简体）](../zh-Hans/security.md) · [中文（繁體）](../zh-Hant/security.md) · [Deutsch](../de/security.md) · [Русский](../ru/security.md)

[← Retour à l’accueil français](../../../i18n/README.fr.md)

# Sécurité

## Autorisation et frontières

Utilisez le pont uniquement avec un ordinateur et un compte UU autorisés. Il s’exécute comme l’utilisateur Unix connecté, dans son préfixe Wine dédié. Xvfb emploie Xauthority sans TCP ; les pipes appartiennent au wineserver du préfixe. Les auxiliaires X11 et terminal utilisent des ports IPv4 loopback éphémères et des tokens distincts de 256 bits renouvelés au démarrage. Répertoires `0700`, fichier terminal `0600`, quatre shells maximum.

Le VNC de gestion n’a pas de mot de passe propre, mais écoute seulement en loopback et exporte une fenêtre UU, pas le root privé. Le relais Mac facultatif conserve VNC authentifié derrière SSH. FreeRDP vise uniquement `127.0.0.1` et vérifie l’empreinte TLS. Le listener LAN de GNOME relève de sa configuration : protégez-le par pare-feu et mot de passe dédié.

## Secrets et contenu

`secret-tool` stocke le mot de passe dans le trousseau de connexion ; FreeRDP le lit sur stdin. VNC classique prend les huit premiers octets, avec fichier `0600`. Le démarrage autonome chiffre le mot de passe supplémentaire du trousseau via TPM2/systemd-creds, puis le déchiffre uniquement dans un répertoire runtime protégé. GDM autologin ouvre l’accès physique après boot ; TPM ne protège pas contre les programmes de l’utilisateur connecté et LUKS reste interactif.

Les logs d’entrée enregistrent quantité, type, flags, route, résultat et erreur, jamais caractères, coordonnées ou presse-papiers. Le terminal ne journalise ni commandes ni sortie. Le texte sémantique est limité à 2 048 enregistrements et reste volontairement dans les sélections après collage. Préfixes, tokens, registry, logs bruts et captures privées restent hors publication.

## Binaires et maintenance

Le patcher exige un manifeste `approved` avec hashes complets, taille, signatures uniques et remplacements de même longueur ; les originaux `.uu-original` sont conservés. Le manifeste 4.42 n’autorise pas d’autres versions. Les brouillons nécessitent une revue sémantique indépendante. Réutiliser un relais exige source, recipe, profile, pins et provenance concordants.

Les installateurs inconnus sont d’abord extraits sans exécution. `--sandbox-install` est explicite et utilise un staging Bubblewrap/systemd sans réseau. Wine n’isole pas fortement les processus d’un même utilisateur. La réparation ne valide pas son propre résultat : promotion avec hashes exacts, acceptance commitée, tests réels contrôleur/login et au moins 270 secondes stables. La transaction sauvegarde tout le préfixe et le restaure en cas d’échec sans modifier XRDP.

[Compilation](source-build.md) · [Mises à jour](automatic-updates.md)

## Commandes et valeurs techniques

```text
~/.local/share/wineprefixes/uu-remote
~/.config/uu-remote-bridge/environment
CLIPBOARD / PRIMARY
KEYEVENTF_UNICODE / cliprdr
```

## Code source et sujets associés

- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [patches/freerdp-sdl-product.json](../../../patches/freerdp-sdl-product.json)

Les détails techniques sont disponibles en anglais et en chinois simplifié:

- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
