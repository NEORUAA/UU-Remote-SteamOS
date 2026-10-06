[English](../CHANGELOG.md) · [العربية](CHANGELOG.ar.md) · [Deutsch](CHANGELOG.de.md) · [Español](CHANGELOG.es.md) · [Français](CHANGELOG.fr.md) · [日本語](CHANGELOG.ja.md) · [한국어](CHANGELOG.ko.md) · [Русский](CHANGELOG.ru.md) · [Tiếng Việt](CHANGELOG.vi.md) · [简体中文](CHANGELOG.zh-Hans.md) · [繁體中文](CHANGELOG.zh-Hant.md)

[Inicio](README.es.md)

# Historial de cambios

Las versiones del puente y del Windows UU aprobado se gestionan por separado.

## Plus 0.2.0-work — 2026-10-06

- **Retoma el terminal:** el modo opcional `persistent` conserva shell, directorio y tareas al reconectar; el valor predeterminado sigue siendo `fresh`.

- **Recibe varios archivos:** copia archivos regulares en el controlador y pega el lote completo en Ubuntu; progreso por bytes recibidos.

- **Compatibilidad de imágenes:** PNG original con DIBV5/DIB; un asistente Mac opcional añade TIFF para PNG.

- **Explora captura nativa:** prototipos CPU/GPU opcionales y experimentales, fuera de la instalación predeterminada.

Solo archivos regulares entrantes. La sincronización actual Ubuntu → Mac y el foco entre dos controladores siguen pendientes.

[CPU (MIT)](../vendor/uur-native-cpu/NOTICE) · [GPU (AGPL-3.0)](../vendor/uuway-gpu-component/README.md) · [Uso y actualización en inglés](../docs/updates/2026-10-06.md)

## Plus 0.1.0 — 2026-10-03

Plus se basa en el puente original con licencia MIT.

### Novedades

- Lienzo: Cuatro perfiles hasta 4K, escritorio completo y recuperación del tamaño.
- Texto móvil: Revisión de las rutas Plus y ruta de texto pública FreeRDP.
- Gestión: Captura independiente de ventanas/diálogos y visor reutilizable.
- Cursor: Alternativa del tema y correcciones de inicio; desactivado por defecto.
- Acciones: Mapeo GNOME de escritorio/vista general.
- Utilidades: Calidad/VNC/FreeRDP/Openbox con fuentes, DPI y credenciales locales.
- Compilación y recuperación: Fuentes parcheadas fijas, comprobación y recuperación de perfiles/visor.
- Páginas de inicio y guías esenciales en once idiomas, con gráficos editables de arquitectura, adaptación y comparación.

### Correcciones

- Portapapeles: Parche SDL de comprobación en segundo plano, propietario y caché.
- Reapertura del gestor, títulos UTF-8, captura de diálogos propios y devolución del foco al cerrar el visor.
- Envío de texto móvil, inicio del hook de entrada, entradas parciales y cierre acotado del terminal nativo.
- Puntero sobre todo el lienzo, tamaño/bitrate independientes, protección de RDP manual y lanzadores reversibles.

### Compatibilidad

- Ubuntu 24.04 / GNOME 46 · Ubuntu 26.04 / GNOME 50 · x86-64.
- Windows UU: 4.42.0.2770 revisado como opción predeterminada.

## Original heredado — sin publicar

El original aporta transacciones Unicode del portapapeles, edición de composición y dictados largos, diseños de teclado físico, entrada autenticada, diagnóstico de red/runtime, aislamiento Bluetooth de Wine y recuperación de sesiones desatendidas.

## Original0.2.0 — 2026-07-18

Diagnóstico de red/digest instalado, adaptador predeterminado/fijo; recuperación de descriptores GNOME/libei, límites/Keyring/PythonGI; ritmo de texto móvil configurable, teclas físicas sin demora, `SendInput` primero y fallback con foco confirmado; X11/XTEST autenticado, telemetría, limpieza y recuperación de red; guías XRDP y desatendidas.

## Original0.1.0 — 2026-07-17

Primer puente soportado Wine/UU/Xvfb/SDLFreeRDP/GNOME, broker/reinyección/servicio; ajustes guardados, auditoría/reversión/clipboard RDP; TPM2/GDM opcional; normalización móvil, sesiones Wayland/Xorg/XRDP, compatibilidad de eventos Wine y limpieza de prefijos.

Versiones originales: [v0.1.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.1.0) · [v0.2.0](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/releases/tag/v0.2.0). Historial detallado y registros originales: [CHANGELOG.md — e2854e2b](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b/CHANGELOG.md).
