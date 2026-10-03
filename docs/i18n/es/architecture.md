[English](../../architecture.md) · [العربية](../ar/architecture.md) · [Español](../es/architecture.md) · [Français](../fr/architecture.md) · [日本語](../ja/architecture.md) · [한국어](../ko/architecture.md) · [Tiếng Việt](../vi/architecture.md) · [中文（简体）](../zh-Hans/architecture.md) · [中文（繁體）](../zh-Hant/architecture.md) · [Deutsch](../de/architecture.md) · [Русский](../ru/architecture.md)

[← Volver al inicio en español](../../../i18n/README.es.md)

# Arquitectura

## Dos escritorios, dos direcciones

La aplicación oficial de UU para Windows se ejecuta en un prefijo Wine dedicado. Su controlador de entrada del kernel no controla GNOME. El puente ofrece una ventana de retransmisión en X11 privado: la imagen va de Ubuntu al controlador UU; teclado, ratón y texto confirmado regresan. El visor de administración es una rama local independiente. La fuente usa el manifiesto UU 4.42 y una compilación fijada de FreeRDP/SDL.

Una instalación nueva elige `rdp`, entrada `rdp-public`, destino `auto`, 1920 × 1080, seguimiento de resolución `off` y texto de teléfono `auto`. Las actualizaciones conservan los valores guardados. Sin configuración instalada el lanzador recurre a `legacy`. Las cuatro opciones normales son 720p, 1080p, 1440p y 4K. VNC es explícito, exige X11/XRDP y `legacy`; no sustituye una sesión Wayland.

## Imagen y entrada

GNOME Remote Desktop se inicia en el D-Bus de la sesión elegida. FreeRDP conecta por loopback, normalmente `127.0.0.1:3390`, fija la huella TLS y recibe la credencial por stdin. Xvfb usa Xauthority y `-nolisten tcp`. En `rdp-public`, XComposite compone únicamente la ventana SDL vinculada sobre el root privado; UU captura, codifica y transporta esa imagen.

El parche revisado de cada versión selecciona el `SendInput` existente. El broker público envía eventos a la tubería local de `uurb-full-input`; las funciones de FreeRDP los llevan por la conexión RDP existente a GNOME. `/dvc:uurb-full-input` carga el complemento sin requerir un nuevo canal de entrada del servidor. `legacy` intenta primero Wine para eventos ordinarios y remite lo no aceptado al broker. XTEST directo es opcional en X11; una entrega ambigua no se repite.

## Texto y portapapeles

Las teclas físicas y `KEYEVENTF_UNICODE` son entradas distintas. `rdp-public/auto` conserva literalmente todos los commits Unicode, incluso ASCII. `legacy/auto` traduce lo representable a combinaciones y usa pegado semántico para chino, tabuladores o saltos de línea. El auxiliar nativo posee `CLIPBOARD` y `PRIMARY`, verifica los nuevos propietarios y envía `Shift+Insert` por la ruta elegida. La barrera confirma una transacción de selección; la aplicación debe tener foco y admitir pegar. La copia normal usa `cliprdr`. El acompañante VNC sólo lleva texto de GameViewer a Ubuntu, sin leer de vuelta ni pulsar pegar.

## Administración y ciclo de vida

`uu-remote open` captura el gestor y sus ventanas emergentes asociadas mediante XComposite hacia TigerVNC local. Las entradas del visor vuelven a la ventana propia correspondiente. Al cerrar se recogen procesos auxiliares y se recupera el foco del relay; UU sigue mapped. No es una etapa del flujo del escritorio.

La calidad cambia el lienzo privado, no el monitor físico. Se prepara recuperación antes del cambio y se informa si ésta falla. El servicio de usuario supervisa sus hijos y sólo limpia su prefijo. GNOME gestiona la entrada Wayland; el adaptador llama a FreeRDP, no a libei directamente. El backport antiguo de libei es opcional y Ubuntu 26.04 ya incluye la corrección. Terminal y arranque desatendido tienen rutas separadas.

[Calidad](quality-guide.md) · [Compilación](source-build.md) · [Seguridad](security.md)

![UU / GNOME](../../images/architecture-premium-v2-en.png)

![Video / Input](../../images/uu-plus-data-flow-en.gif)

[PNG](../../images/uu-plus-data-paths-en.png) · [SVG](../../images/uu-plus-data-paths-en.svg)

![UU manager](../../images/manager-premium-en.png)

## Comandos y valores técnicos

```text
GNOME -> GNOME Remote Desktop -> loopback RDP -> SDL FreeRDP
  -> private X11 / UU capture -> UU controller
UU controller -> SendInput hook -> broker -> uurb-full-input
  -> FreeRDP input -> GNOME Remote Desktop -> GNOME
GameViewer + popups -> XComposite -> loopback x11vnc -> local TigerVNC
```

## Código fuente y temas relacionados

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

Los detalles técnicos están disponibles en inglés y chino simplificado:

- [native-ubuntu-terminal](../../native-ubuntu-terminal.md) · [简体中文](../zh-Hans/native-ubuntu-terminal.md)
- [unattended-startup](../../unattended-startup.md) · [简体中文](../zh-Hans/unattended-startup.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
