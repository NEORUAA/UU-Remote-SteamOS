[English](../../porting.md) · [العربية](../ar/porting.md) · [Deutsch](../de/porting.md) · [Español](../es/porting.md) · [Français](../fr/porting.md) · [日本語](../ja/porting.md) · [한국어](../ko/porting.md) · [Русский](../ru/porting.md) · [Tiếng Việt](../vi/porting.md) · [简体中文](../zh-Hans/porting.md) · [繁體中文](../zh-Hant/porting.md)

[Inicio](../../../i18n/README.es.md)

# Adaptar a otros escritorios Linux

GNOME x86-64 permite reutilizar el backend RDP adaptando instalación. KDE/Xfce necesitan adaptadores propios. El instalador actual admite Ubuntu 24.04/26.04; los demás son destinos de adaptación.

Instalar el relé requiere la cadena revisada exacta o una salida verificada existente; los paquetes APT habituales no proporcionan automáticamente esa cadena. Véanse [requisitos de compilación y reutilización de caché](source-build.md).

![Capas de adaptación](../../images/uu-plus-porting.png)

[SVG editable](../../images/uu-plus-porting.svg)

| Capa | Reutilizable | Adaptación / fuente |
| --- | --- | --- |
| Núcleo | Wine/UU aislado, manifiesto, SDL/FreeRDP, broker/plugin, lienzo y gestor | Mantener protocolos y separar Unicode/teclas; [broker](../../../src/uu_input_broker.c), [adaptador](../../../src/freerdp-adapter.c), [plugin](../../../src/plugin.c), [captura](../../../src/uu_manager_capture.c) |
| Distribución | Receta, validación, configuración y servicio | Paquetes/rutas/bibliotecas/lanzadores; [instalador](../../../install.sh), [build](../../../scripts/build-winpr.sh), [validación](../../../scripts/verify-freerdp-runtime.py), [servicio](../../../systemd/uu-remote-bridge.service) |
| Escritorio | Eventos RDP y protocolos texto/acciones | Sesión, captura/entrada, portapapeles, geometría y acciones; [inicio](../../../scripts/uu-remote-bridge), [texto](../../../src/uu_x11_input.c), [modos](../../../scripts/uu-display-modes.py) |

Las API públicas FreeRDP usan la conexión RDP existente; el servidor puede cambiar independientemente del hook Windows UU. Unicode requiere portapapeles del escritorio y pegado, hoy X11/Xwayland. El gestor queda en X11 privado Wine. [Arquitectura](architecture.md).

| Plataforma | Reutilización y trabajo principal |
| --- | --- |
| Ubuntu 24.04/GNOME 46 | Instalador/backend existente; backport libei opcional |
| Ubuntu 26.04/GNOME 50 | Integración Plus; libei del sistema, UU 4.42 |
| Debian/GNOME | Núcleo/lienzo/RDP; paquetes y Wine Debian, preflight, daemon, bibliotecas; [APT/dpkg](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html) |
| Fedora/GNOME | Núcleo/backend; RPM/DNF, rutas, permisos; [GRD](https://packages.fedoraproject.org/pkgs/gnome-remote-desktop/gnome-remote-desktop/) |
| Arch/GNOME | Núcleo/backend; pacman, rutas/herramientas fijadas, GNOME/libei rolling; [GRD](https://archlinux.org/packages/extra/x86_64/gnome-remote-desktop/) |
| KDE Plasma | Núcleo/lienzo/gestor; sesión, captura, entrada, salidas, portapapeles, acciones KDE; [KRDP](https://github.com/KDE/krdp) requiere integrar autenticación/códec/texto |
| Xfce/X11 | Núcleo/lienzo/gestor/X11; sesión, geometría, acciones. VNC X11 con `legacy` es un punto de partida |

Cambiar el gestor de paquetes resuelve solo instalación; conecte captura, entrada, geometría y acciones.

| Interfaz | Implementación actual / adaptación |
| --- | --- |
| Arquitectura | `x86_64`, AMD64 PE; otros hosts requieren ejecución AMD64 y validación |
| Paquetes | Ubuntu, `apt-get`, `dpkg`, i386, WineHQ Ubuntu; mapear al destino |
| Wine | `/opt/wine-stable/bin/wine`, `wineserver`, `winepath`; rutas uniformes en inicio/limpieza |
| Herramientas | MinGW/CMake/Meson/Ninja/archivos fijados; igualar o revisar perfil; [fuentes](source-build.md) |
| Sesión/captura | `gnome-shell`, D-Bus y `/usr/libexec/gnome-remote-desktop-daemon`; resolver o sustituir servidor |
| Credenciales | Keyring, `secret-tool`, `grdctl`, `org.gnome.desktop.remote-desktop.rdp`; TLS/control separado de cuenta UU |
| Salidas | `org.gnome.Mutter.DisplayConfig`, monitor virtual; interfaz del compositor, XRandR en X11 |
| Texto | `uu-x11-input`/`xclip`, `CLIPBOARD`/`PRIMARY`; display correcto, clipboard nativo en Wayland |
| Acciones | `_NET_SHOWING_DESKTOP`, `org.gnome.Shell.OverviewActive`; acciones/estado del gestor destino |
| Servicio | `systemctl --user`, D-Bus gráfico; adaptar sesión/init |
| Utilidades | `/usr/bin/xfreerdp`, `xtigervncviewer`, `obconf`, `zenity`; rutas, fuentes/DPI, credenciales interactivas y protección relé |

El lienzo privado Wine/Xvfb y las salidas físicas/virtuales son diferentes. Conserve cuatro perfiles cuando sea posible y sustituya la lógica Mutter para KDE/Xfce.

1. Elija una distribución/sesión x86-64; registre OS/escritorio/Wine/UU.
2. Adapte paquetes, rutas, bibliotecas, servicio y lanzadores; valide el relé.
3. Conecte captura/entrada, bus, display, credenciales, geometría y portapapeles.
4. Pruebe controlador real: puntero, clic, rueda, arrastre, atajos, Unicode, pegado, reconexión, gestor y popups.
5. Revise cuatro tamaños, restauración, reversión, limpieza y acciones.

Aporte mapas, rutas, versiones y resultados sin binarios UU/cuentas. Véanse [comparación](upstream-comparison.md) y [calidad](quality-guide.md).
