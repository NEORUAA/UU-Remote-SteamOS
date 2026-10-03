[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[Español · UU Remote Ubuntu Plus](../../../i18n/README.es.md)

# Solución de problemas

## Comprobaciones iniciales

Ejecuta los comandos desde el código fuente. Registros en `~/.local/state/uu-remote-bridge` y configuración en `~/.config/uu-remote-bridge/environment`. Comparte versiones y errores sin datos de cuenta ni texto escrito. Reinstala tras modificar el código.

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

## Sin conexión después de iniciar o reiniciar

Inicia sesión una vez en el gestor oficial y ciérralo normalmente. Revisa servicios de usuario y desbloqueo del llavero. Si cambió la contraseña, renueva la credencial cifrada con `./scripts/configure-unattended.sh enable --replace-credential`. Revisa recuperación e inyección cuando termine el servidor.

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

## Buscando rutas indefinidamente

Comprueba que el anfitrión haya terminado de arrancar. Registros antiguos de dispositivos de entrada y Bluetooth pueden retrasar Wine. La reparación guarda una copia del registro, limpia entradas reconocidas del prefijo UU y reinicia el puente, conservando Bluetooth de Ubuntu.

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

## Imagen negra, blanca o escritorio equivocado

Comprueba la sesión GNOME iniciada, el puerto RDP y los registros SDL. Distingue sesiones activas: XRDP usa `--desktop-target xrdp`, el escritorio físico `physical`. `--desktop-relay vnc` es opcional para X11; Wayland usa RDP.

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

## Bordes vacíos, recorte o 4K demasiado pesado

Compara escritorio origen y lienzo. El selector ofrece 720p, 1080p, 1440p y 4K. Lienzo, FPS del controlador y bitrate se configuran aparte. El cambio reconecta brevemente y revierte si falla; comprueba también el tamaño dinámico de XRDP.

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

## Hay imagen pero no responde la entrada

Abre el gestor con uu-remote open, sin iniciar el mismo prefijo Wine en otro display X. Al cerrar el visor vuelve el foco al relé. El texto del móvil y varias líneas usan portapapeles/RDP; las teclas físicas mantienen eventos. Reinstala y comprueba el inyector tras actualizar. Si el primer clic termina la sesión, comprueba UU SendInput bridge active, UU Wine event-log compatibility active y el broker; `uu-remote restart` restaura los componentes.

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

## Teclas lentas, símbolos incorrectos o degradación

Compara VPN, proxy y transporte UU; stale indica una sesión antigua. Si confirmas una interfaz equivocada, prueba `--network-interface default`, restaura con `all`. Prueba ritmo físico con `--physical-key-delay-ms 8`, por defecto `0`. Los símbolos dependen del teclado Ubuntu; revisa GRD/libei y descriptores en fallos prolongados.

```bash
uu-remote network
ip -4 route show default
```

## Cursor ausente o pequeño

La protección opcional está desactivada por defecto. auto sigue el cursor del escritorio; tamaños fijos de 24 a 128. `--cursor-guard off` la apaga, sin cambiar resolución ni DPI global de Wine.

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

## El terminal termina o coloca mal el texto

Instala el puente actual y verifica el canal. Elige PowerShell en UU para abrir el shell de inicio Ubuntu. Abre una sesión nueva si falla la posición del cursor. Consulta metadatos en terminal-bridge.log, sin sustituir powershell.exe arbitrariamente.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

## Fallos de autenticación RDP, NLA o SSPI

La consulta comprueba presencia sin mostrar contraseña. Si hace falta, elimina solo la entrada del puente en el llavero y reinstala. Compila FreeRDP, WinPR y DLL de la misma versión fijada; no mezcles versiones mayores.

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

## Mac RDP/VNC o Windows App en Configuring

FreeRDP interno ya ocupa el puerto de escritorio compartido; el inicio remoto abre otro escritorio. Consulta el puerto VNC de loopback real y usa un túnel SSH. En Configuring, reinicia primero Windows App en Mac y luego revisa XRDP.

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

## Reinicios periódicos, sonido y desinstalación

El verificador completo comprueba estabilidad. Revisa por separado audio UU, PulseAudio de Wine y campana VNC dentro del entorno dedicado. Previsualiza la eliminación; la normal conserva el prefijo y `./uninstall.sh --purge` elimina también la cuenta. Identifica el flujo real con `wpctl status`. `UURB_UU_AUDIO=system` es el valor compatible; la configuración ALSA silenciosa dedicada y su retirada están en la guía detallada inglesa.

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

Más información: [calidad](quality-guide.md), [compilación](source-build.md), [arquitectura](architecture.md), [entrada](adaptive-keyboard-relays.md), [actualización](reusable-upgrade.md). [Detalles técnicos e historia (English)](../../troubleshooting.md) amplían registro, controladores, sonido, XRDP y terminal.

## Guías detalladas

- Recuperación XRDP y teclado · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- Compatibilidad de teclado · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- Escritorio actual en Mac · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- Escritorio físico compartido · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- Recuperación tras salida · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- Agente controlador · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- Mensajes de agentes por SSH · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)
