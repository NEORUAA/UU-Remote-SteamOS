[English](../../porting.md) · [العربية](../ar/porting.md) · [Deutsch](../de/porting.md) · [Español](../es/porting.md) · [Français](../fr/porting.md) · [日本語](../ja/porting.md) · [한국어](../ko/porting.md) · [Русский](../ru/porting.md) · [Tiếng Việt](../vi/porting.md) · [简体中文](../zh-Hans/porting.md) · [繁體中文](../zh-Hant/porting.md)

[Accueil](../../../i18n/README.fr.md)

# Adapter à d’autres bureaux Linux

GNOME x86-64 permet de garder RDP en adaptant l’installation. KDE/Xfce demandent des adaptateurs. Ubuntu 24.04/26.04 sont les cibles actuelles ; les autres restent des projets de portage.

L’installation du relais exige la chaîne vérifiée exacte ou une sortie validée existante ; les paquets APT ordinaires ne fournissent pas automatiquement cette chaîne. Voir [prérequis de compilation et réutilisation du cache](source-build.md).

![Trois couches du portage](../../images/uu-plus-porting.png)

[SVG modifiable](../../images/uu-plus-porting.svg)

| Couche | Réutilisation | Adaptation / sources |
| --- | --- | --- |
| Cœur | Wine/UU isolé, manifeste, SDL/FreeRDP, courtier/plugin, canevas/gestionnaire | Protocoles cohérents, Unicode séparé des touches ; [courtier](../../../src/uu_input_broker.c), [RDP](../../../src/freerdp-adapter.c), [plugin](../../../src/plugin.c), [capture](../../../src/uu_manager_capture.c) |
| Distribution | Recette, checks, configuration/service | Paquets, chemins, bibliothèques, lanceurs ; [installation](../../../install.sh), [build](../../../scripts/build-winpr.sh), [checks](../../../scripts/verify-freerdp-runtime.py), [service](../../../systemd/uu-remote-bridge.service) |
| Bureau | Événements RDP, texte/actions | Session, capture/entrée, presse-papiers, géométrie, actions ; [démarrage](../../../scripts/uu-remote-bridge), [texte](../../../src/uu_x11_input.c), [modes](../../../scripts/uu-display-modes.py) |

Les API publiques FreeRDP utilisent la connexion existante. Le serveur peut changer indépendamment du hook UU Windows. Unicode exige presse-papiers source et collage, actuellement X11/Xwayland. Le gestionnaire reste dans le X11 privé Wine. [Architecture](architecture.md).

| Plateforme | Réutilisation et adaptation |
| --- | --- |
| Ubuntu 24.04/GNOME 46 | Installateur/backend existant, backport libei facultatif |
| Ubuntu 26.04/GNOME 50 | Intégration Plus, libei système, UU 4.42 |
| Debian/GNOME | Cœur/canevas/RDP ; paquets/Wine Debian, préflight, daemon, bibliothèques ; [APT/dpkg](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html) |
| Fedora/GNOME | Cœur/backend ; RPM/DNF, chemins, permissions ; [GRD](https://packages.fedoraproject.org/pkgs/gnome-remote-desktop/gnome-remote-desktop/) |
| Arch/GNOME | Cœur/backend ; pacman, chemins/outils, évolution GNOME/libei ; [GRD](https://archlinux.org/packages/extra/x86_64/gnome-remote-desktop/) |
| KDE Plasma | Cœur/canevas/gestionnaire ; session, capture/entrée, sorties, clipboard, actions KDE ; [KRDP](https://github.com/KDE/krdp) nécessite intégration authentification/codec/texte |
| Xfce/X11 | Cœur/canevas/gestionnaire/helpers ; session, géométrie, actions ; VNC X11 `legacy` comme départ |

Changer de gestionnaire de paquets ne traite que l’installation. Reliez capture, entrée, géométrie et actions.

| Interface | Implémentation / portage |
| --- | --- |
| Architecture | `x86_64`, AMD64 PE ; autre hôte : exécution AMD64 et checks |
| Paquets | Ubuntu, `apt-get`, `dpkg`, i386, WineHQ Ubuntu ; mapping cible |
| Wine | `/opt/wine-stable/bin/wine`, `wineserver`, `winepath` ; chemins cohérents |
| Outils | MinGW/CMake/Meson/Ninja/archives fixés ; même profil ou revue ; [build](source-build.md) |
| Session/capture | `gnome-shell`, D-Bus, `/usr/libexec/gnome-remote-desktop-daemon` ; localiser/remplacer |
| Identifiants | Keyring, `secret-tool`, `grdctl`, `org.gnome.desktop.remote-desktop.rdp` ; TLS/service séparés du compte UU |
| Sorties | `org.gnome.Mutter.DisplayConfig`, écran virtuel ; interface compositeur, XRandR sous X11 |
| Texte | `uu-x11-input`/`xclip`, `CLIPBOARD`/`PRIMARY` ; display adapté, interface Wayland native |
| Actions | `_NET_SHOWING_DESKTOP`, `org.gnome.Shell.OverviewActive` ; actions/état du gestionnaire cible |
| Service | `systemctl --user`, D-Bus graphique ; adapter session/init |
| Utilitaires | `/usr/bin/xfreerdp`, `xtigervncviewer`, `obconf`, `zenity` ; chemins, polices/DPI, saisie identifiants, protection relais |

Le canevas privé Wine/Xvfb est distinct des sorties physiques/virtuelles. Gardez les quatre profils lorsque possible ; remplacez la logique Mutter pour KDE/Xfce.

1. Choisir une distribution/session x86-64 et noter OS/bureau/Wine/UU.
2. Adapter paquets, chemins, bibliothèques, service et lanceurs ; vérifier le relais.
3. Relier capture/entrée, bus, display, identifiants, géométrie, clipboard.
4. Tester depuis le vrai contrôleur : pointeur, clics, roue, déplacement, raccourcis, Unicode, collage, reconnexion, gestionnaire/popups.
5. Vérifier quatre tailles, restauration, retour automatique, nettoyage et actions.

Contribuez mapping, chemins, versions et résultats, sans binaires UU/comptes. [Comparaison](upstream-comparison.md), [qualité](quality-guide.md).
