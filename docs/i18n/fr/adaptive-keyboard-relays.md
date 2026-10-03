[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [中文（简体）](../zh-Hans/adaptive-keyboard-relays.md) · [中文（繁體）](../zh-Hant/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md)

[← Retour à l’accueil français](../../../i18n/README.fr.md)

# Relais clavier adaptatifs

XRDP transmet métadonnées de disposition et scancodes ; RFB/X11 des keysyms ; UU ordinateur des événements Windows physiques ; l’IME du téléphone des commits Unicode. Garder ces catégories distinctes préserve le sens des symboles.

Laissez XRDP choisir la disposition signalée par le client. Un `setxkbmap ... -layout jp` inconditionnel dans `~/.xsessionrc` l’écrase pour chaque client. Gardez le correctif Mac japonais comme commande explicite, pas comme boucle globale de connexion. IBus, texte sémantique et terminal restent indépendants du XKB physique.

## Visionneuse VNC dédiée

Le relais plein écran utilise `UURB_VNC_GRAB_KEYBOARD=on` et `-GrabKeyboard=1`. Sinon, le bureau intermédiaire peut absorber Shift/Ctrl/Alt/Super : `(` devient `8`, `?` devient `/`, `@` devient `2`. x11vnc utilise `-modtweak -xkb -add_keysyms` pour reconstruire les modificateurs et proposer les keysyms absents, uniquement sur IPv4 loopback.

Désactivez le grab seulement pour une visionneuse non dédiée. Le test RFB/Xvfb isolé vérifie 21 symboles Shift et `你好` sur XKB japonais. Puis testez un champ jetable : caractères simples, symboles, Ctrl+A/C/V, Enter/Backspace et véritable IME, jamais un champ de mot de passe.

## Limite de disposition

X11 direct suit la disposition de la session cible. UU ne fournit pas d’identifiant fiable par connexion : `Shift+7` seul ne permet pas de choisir entre `&` et `'`. XRDP/RFB utilisent métadonnées ou keysyms, le téléphone Unicode. Modifiez le profil client voulu plutôt que le bureau commun pour tous. `rdp-public/auto` garde les commits Unicode littéraux ; les touches physiques conservent leur chemin normal.

[Architecture](architecture.md) · [Sécurité](security.md)

## Commandes et valeurs techniques

```text
UURB_VNC_GRAB_KEYBOARD=on
-GrabKeyboard=1
-repeat -nobell -modtweak -xkb -add_keysyms
```

```bash
./install.sh --skip-packages --skip-account-login \
  --vnc-grab-keyboard off
./scripts/test-vnc-keyboard-relay.sh
```

```text
vnc-symbols=23/23 order=exact target-layout=jp
isolated VNC keyboard acceptance passed
```

## Code source et sujets associés


Les détails techniques sont disponibles en anglais et en chinois simplifié:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
