[English](../../architecture.md) · [العربية](../ar/architecture.md) · [Español](../es/architecture.md) · [Français](../fr/architecture.md) · [日本語](../ja/architecture.md) · [한국어](../ko/architecture.md) · [Tiếng Việt](../vi/architecture.md) · [中文（简体）](../zh-Hans/architecture.md) · [中文（繁體）](../zh-Hant/architecture.md) · [Deutsch](../de/architecture.md) · [Русский](../ru/architecture.md)

[← Retour à l’accueil français](../../../i18n/README.fr.md)

# Architecture

## Deux bureaux, deux directions

L’application Windows officielle de UU fonctionne dans un préfixe Wine dédié. Son pilote noyau ne contrôle pas GNOME. Le pont fournit une fenêtre relais sur un affichage X11 privé : l’image va d’Ubuntu au contrôleur UU, tandis que clavier, souris et texte validé reviennent. La visionneuse de gestion constitue une branche locale indépendante. Les sources utilisent le manifeste UU 4.42 et un build FreeRDP/SDL épinglé.

Une installation neuve choisit `rdp`, entrée `rdp-public`, cible `auto`, 1920 × 1080, suivi de résolution `off` et texte téléphone `auto`. Les mises à jour conservent les réglages. Sans configuration installée, le lanceur utilise `legacy`. Les quatre formats courants sont 720p, 1080p, 1440p et 4K. VNC est une option explicite X11/XRDP avec `legacy`, pas un remplacement de Wayland.

## Image et commandes

GNOME Remote Desktop démarre sur le D-Bus de la session choisie. FreeRDP rejoint le loopback, normalement `127.0.0.1:3390`, vérifie l’empreinte TLS et reçoit le secret par stdin. Xvfb utilise Xauthority et `-nolisten tcp`. Avec `rdp-public`, XComposite compose seulement la fenêtre SDL liée sur le root privé ; UU capture, encode et transmet cette image.

Un patch propre à la version sélectionne le `SendInput` existant. Le broker public envoie au pipe local du plugin `uurb-full-input`, puis les fonctions FreeRDP livrent les événements sur la connexion RDP existante. `/dvc:uurb-full-input` charge le plugin sans nouveau canal d’entrée côté serveur. `legacy` essaie d’abord Wine pour les événements ordinaires et envoie le reste non accepté au broker. XTEST direct est facultatif sur X11 ; une livraison ambiguë n’est pas rejouée.

## Texte et presse-papiers

Touches physiques et `KEYEVENTF_UNICODE` restent distincts. `rdp-public/auto` conserve littéralement chaque texte Unicode validé, même ASCII. `legacy/auto` transforme le texte représentable en accords de touches et colle sémantiquement chinois, tabulations ou sauts de ligne. L’auxiliaire possède `CLIPBOARD` et `PRIMARY`, vérifie les nouveaux propriétaires et envoie `Shift+Insert` sur le chemin choisi. La barrière confirme la transaction de sélection ; l’application doit avoir le focus et accepter le collage. Les échanges ordinaires utilisent `cliprdr`. L’auxiliaire VNC envoie seulement le texte GameViewer vers Ubuntu, sans lecture inverse ni touche de collage.

## Gestion et cycle de vie

`uu-remote open` capture gestionnaire et popups associés via XComposite vers TigerVNC local. Les commandes reviennent à la fenêtre propriétaire correspondante. Fermer récupère les auxiliaires et rend le focus au relais ; la fenêtre UU reste mapped. Ce n’est pas une étape intermédiaire du flux de bureau.

La qualité change le canevas privé, pas le moniteur physique. Une restauration est préparée avant modification ; son échec est signalé. Le service utilisateur supervise ses enfants et nettoie seulement son préfixe. GNOME assure l’entrée Wayland ; l’adaptateur appelle FreeRDP, pas libei directement. L’ancien backport libei est optionnel, Ubuntu 26.04 intègre déjà la correction. Terminal et démarrage autonome suivent des branches distinctes.

[Qualité](quality-guide.md) · [Compilation](source-build.md) · [Sécurité](security.md)

![UU / GNOME](../../images/architecture-premium-v2-en.png)

![Video / Input](../../images/uu-plus-data-flow-en.gif)

[PNG](../../images/uu-plus-data-paths-en.png) · [SVG](../../images/uu-plus-data-paths-en.svg)

![UU manager](../../images/manager-premium-en.png)

## Commandes et valeurs techniques

```text
GNOME -> GNOME Remote Desktop -> loopback RDP -> SDL FreeRDP
  -> private X11 / UU capture -> UU controller
UU controller -> SendInput hook -> broker -> uurb-full-input
  -> FreeRDP input -> GNOME Remote Desktop -> GNOME
GameViewer + popups -> XComposite -> loopback x11vnc -> local TigerVNC
```

## Code source et sujets associés

- [install.sh](../../../install.sh#L358)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L6)
- [scripts/runtime-settings.sh](../../../scripts/runtime-settings.sh)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1010)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1758)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1437)
- [scripts/uu-manual-plane.py](../../../scripts/uu-manual-plane.py#L155)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1040)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1844)
- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [src/uu_input_bridge.c](../../../src/uu_input_bridge.c#L688)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L1081)
- [src/plugin.c](../../../src/plugin.c#L200)
- [src/freerdp-adapter.c](../../../src/freerdp-adapter.c#L48)
- [src/uu_input_bridge_legacy.c](../../../src/uu_input_bridge_legacy.c#L595)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L1101)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L454)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L641)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1182)
- [src/uu_x11_input.c](../../../src/uu_x11_input.c#L1000)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1266)
- [src/uu_wine_clipboard_bridge.c](../../../src/uu_wine_clipboard_bridge.c#L195)
- [src/uu_x11_clipboard.c](../../../src/uu_x11_clipboard.c#L329)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L1121)
- [src/uu_manager_capture.c](../../../src/uu_manager_capture.c#L464)
- [src/uu_manager_capture.c](../../../src/uu_manager_capture.c#L1090)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L1193)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L622)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L299)
- [scripts/uu-quality.py](../../../scripts/uu-quality.py#L329)
- [scripts/uu-display-modes.py](../../../scripts/uu-display-modes.py#L166)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L199)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1121)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L2207)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L478)
- [systemd/uu-remote-bridge.service](../../../systemd/uu-remote-bridge.service)

Les détails techniques sont disponibles en anglais et en chinois simplifié:

- [native-ubuntu-terminal](../../native-ubuntu-terminal.md) · [简体中文](../zh-Hans/native-ubuntu-terminal.md)
- [unattended-startup](../../unattended-startup.md) · [简体中文](../zh-Hans/unattended-startup.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
