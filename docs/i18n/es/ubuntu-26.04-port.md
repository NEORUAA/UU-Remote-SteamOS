[English](../../ubuntu-26.04-port.md) · [العربية](../ar/ubuntu-26.04-port.md) · [Deutsch](../de/ubuntu-26.04-port.md) · [Español](../es/ubuntu-26.04-port.md) · [Français](../fr/ubuntu-26.04-port.md) · [日本語](../ja/ubuntu-26.04-port.md) · [한국어](../ko/ubuntu-26.04-port.md) · [Русский](../ru/ubuntu-26.04-port.md) · [Tiếng Việt](../vi/ubuntu-26.04-port.md) · [简体中文](../zh-Hans/ubuntu-26.04-port.md) · [繁體中文](../zh-Hant/ubuntu-26.04-port.md)

[Inicio](../../../i18n/README.es.md)

# Ubuntu 26.04 y GNOME 50

Plus amplía el [puente MIT de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge) a Ubuntu 26.04/GNOME 50 x86-64 y conserva 24.04/GNOME 46. Mantiene aislamiento Wine, manifiestos auditados, broker, relé y servicio supervisado.

Instalar el relé requiere la cadena revisada exacta o una salida verificada existente; los paquetes APT habituales no proporcionan automáticamente esa cadena. Véanse [requisitos de compilación y reutilización de caché](source-build.md).

| Componente | Referencia original | Plus |
| --- | --- | --- |
| Ubuntu | 24.04 | 24.04/26.04; otros requieren `UURB_ALLOW_UNVALIDATED_UBUNTU=1` |
| Windows UU | 4.33.0.8907 | 4.42.0.2770 aprobado; manifiestos anteriores seleccionables |
| libei | Backport 1.2.1 aislado | Biblioteca del sistema si contiene la reparación; backport en otro caso |
| Relé | SDL nightly fijado y WinPR | Fuente FreeRDP/SDL fijada con parches; [compilación](source-build.md) |
| CI | 24.04 | Objetivos 24.04/26.04; resultados por ejecución |

La instalación observada usa GRD 50.2 y libei 1.5.0. Para bibliotecas antiguas está el backport `ee27dd5c92e4e9496a36ca2d4112049fe02d2269`. `UURB_LIBEI_MODE=system|backport` guarda la selección; `verify.sh` comprueba la biblioteca cargada. Wine procede de WineHQ stable.

## Uso

Cuatro perfiles con ajuste completo y puntero; instalación nueva en 1080p, actualización conserva ajustes. Cambiar tamaño guardado reconecta con reversión; reaplicarlo restaura el lienzo vivo. El usuario confirmó reconexión y menú nativo hasta 4K. RDP nuevo usa `rdp-public`; actualizar conserva la ruta. Unicode y teclas físicas son operaciones distintas. Gestor y ventanas emergentes se capturan aparte; cerrar el visor devuelve foco al relé, con el gestor todavía mapeado. El portapapeles del escritorio funciona; el del gestor está aislado.

| Función | Resultado |
| --- | --- |
| Chino directo desde teléfono/Mac | Confirmado por el usuario durante integración |
| Texto copiar/pegar | Normal según usuario |
| Actualización Mac UU | Reconexión, chino y pegado normales; 4K similar |
| Solapamiento/foco del gestor | Resuelto según usuario; comprobaciones seleccionadas normales |
| Acciones Android | Backend bidireccional normal; botones pendientes |
| Cursor opcional | Tema y comprobaciones parciales normales; formas completas pendientes |
| Monitor físico/salida virtual | Pendiente en este equipo |
| Teléfono → ToDesk → Mac → UU | Repetición de `a` pendiente |

Lanzadores VNC/FreeRDP/Openbox tienen fuentes CJK, DPI y credenciales locales. Dock pertenece a GNOME. Límites del control saliente y resolución física son distintos del lienzo entrante. Véanse [calidad](quality-guide.md), [arquitectura](architecture.md), [comparación](upstream-comparison.md).

## Actualizar

Mantenga Plus como `origin` y añada el original:

```bash
git remote add upstream https://github.com/lachlanchen/uu-remote-ubuntu-bridge.git
git fetch upstream
```

Revise en una rama de desarrollo. Tras cambiar scripts/componentes:

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

La instalación interrumpe brevemente la conexión; el digest indica cambios hasta reinstalar. [Actualizaciones reutilizables](reusable-upgrade.md) cubre recuperación del runtime; la reversión de perfiles cubre el lienzo. Un hash UU desconocido bloquea parches automáticos; una versión nueva requiere revisión semántica, manifiesto aprobado y comprobación: [mantenimiento](../../upstream-maintenance.md). El repositorio distribuye fuente MIT/manifiestos; dependencias y UU conservan licencias.
