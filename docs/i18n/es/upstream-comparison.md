[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[Inicio](../../../i18n/README.es.md)

# Qué cambia Plus

![Base original, cambios de Plus y previsiones de diseño](../../images/uu-plus-evolution-en.png)

[SVG editable](../../images/uu-plus-evolution-en.svg)

Parte del [proyecto de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge), referencia [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a). Wine aislado, relé GNOME, entrada, gestor y servicio vienen del original.

## Cambios en el uso diario

| Área | Base del original | Cambio de Plus | Uso diario |
| --- | --- | --- | --- |
| Host | Ubuntu 24.04 y backport libei aislado | Adaptación a Ubuntu 26.04/GNOME 50, libei del sistema o backport; conserva el destino 24.04 | Consultar la guía de plataforma y compilación del host |
| Windows UU | 4.33.0.8907 por defecto y manifiestos revisados | 4.42.0.2770 revisado como opción predeterminada | Elegir el manifiesto de la versión UU instalada |
| Lienzo | Resolución guardada y cambio de tamaño RDP | Cuatro perfiles hasta 4K, escritorio completo y recuperación del tamaño | Elegir 720p, 1080p, 1440p o 4K y consultar el lienzo actual |
| Texto móvil | Normalización IME y pegado Unicode | Revisión de las rutas Plus y ruta de texto pública FreeRDP | Escribir chino, código y texto de varias líneas |
| Portapapeles | Portapapeles RDP y transacciones Unicode | Parche SDL de comprobación en segundo plano, propietario y caché | Copiar y pegar el texto actual con el relé en segundo plano |
| Gestión | Vista privada de ventana y devolución del foco | Captura independiente de ventanas/diálogos y visor reutilizable | Abrir cuenta o ajustes UU y volver al escritorio |
| Cursor | Protección opcional de tamaño fijo | Alternativa del tema y correcciones de inicio; desactivado por defecto | Activar la protección del cursor cuando haga falta |
| Acciones | Control de escritorio por teclado y ratón | Mapeo GNOME de escritorio/vista general | Conectar acciones del controlador al backend GNOME |
| Utilidades | Dependencias del relé y comandos UU | Calidad/VNC/FreeRDP/Openbox con fuentes, DPI y credenciales locales | Abrir cada herramienta con sus propios ajustes |
| Compilación y recuperación | Nightly SDL/WinPR fijo y reconexión del servicio | Fuentes parcheadas fijas, comprobación y recuperación de perfiles/visor | Preparar un relé compatible y conservar ajustes al mantenerlo |

## Implementación

- Texto móvil: iteración de las rutas de entrada Plus — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- Portapapeles: parche de fuentes SDL — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- Gestión: captura independiente y visor — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- Utilidades: nueva integración del escritorio — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## Rutas de entrada

Las instalaciones RDP nuevas eligen `rdp-public`: el broker usa las API públicas FreeRDP. Unicode, incluido ASCII, se pega literalmente en modo automático; las teclas físicas van separadas. Actualizar conserva la ruta. `legacy` envía teclas para caracteres representables y pegado para CJK/saltos; el inicio sin configurar también usa `legacy`.

Para comparar FPS y latencia, mantén fijas las versiones, resolución, calidad/FPS, bitrate, red y carga, y registra el método de medición; consulta [la guía de medición](performance-evidence.md).
