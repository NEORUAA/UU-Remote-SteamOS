[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [中文（简体）](../zh-Hans/automatic-updates.md) · [中文（繁體）](../zh-Hant/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Русский](../ru/automatic-updates.md)

[← Volver al inicio en español](../../../i18n/README.es.md)

# Comprobaciones automáticas y reparación reanudable

El mantenimiento separa observación, reparación privada de fuente y promoción en vivo aceptada explícitamente. Las comprobaciones normales no interrumpen un relay funcional.

## Configuración y timers

Plus inicia su propio historial de versiones con `v0.1.0`. Los tags fechados de rutas de entrada pertenecen al historial del proyecto original y no están incluidos en este repositorio independiente. La instalación normal no los necesita. Una vez disponible el tag de Plus localmente, selecciónelo con `--track v0.1.0 --branch main`; el configurador aún usa por defecto los nombres antiguos y rechaza un tag inexistente.

Después de seleccionar el tag de la versión, ejecute `git switch main` antes de las actualizaciones habituales que descargan fuentes. La rama mantenida es `origin/main`; el tag explícito de reinstalación sigue siendo `v0.1.0`. Para conservar deliberadamente las fuentes seleccionadas en el tag durante la actualización, use `--no-pull`.

`--auto-promote-accepted` sólo permite versiones posteriores aceptadas por el mantenedor y ligadas a hashes, no borradores de Codex. Modelo, reasoning y ejecutable absoluto se guardan en `updater.json`; Codex debe estar conectado como ese usuario. Todas las ventanas de uso incluido deben estar bajo el umbral predeterminado 20%; si no puede verificarse se aplaza al menos una hora.

`uu-remote-update-check.timer` corre cada día cerca de 04:20 con demora aleatoria y 12 minutos tras arrancar; `Persistent=true` recupera una comprobación perdida. El monitor empieza a los siete minutos y luego 15 minutos después de cada ejecución.

## Observar y reparar

El checker sigue la redirección HEAD oficial, elimina claves query temporales y compara versiones completas. ETag, tamaño y sidecar hash evitan descargas iguales. Un endpoint más antiguo no es una actualización. Dos fallos de salud separados 20 segundos generan evidencia y task, sin detener Wine/RDP/UU. Sólo `--auto-reinstall`, opt-in aparte, permite recuperación.

Las descargas tienen límite 1 GiB. Los hashes desconocidos se extraen estáticamente y se analizan en un clone privado. El contrato se copia como contexto `0600`. Un wrapper no extraíble necesita staging explícito sin red. Codex no usa sudo, cambia el prefijo activo, hace push ni aprueba su interpretación binaria.

## Promoción aceptada

Hash oficial, manifiesto `approved`, acceptance schema-1 y evidencia deben coincidir en el mismo commit obtenido de `origin/main`, con hashes del instalador y server parcheado ligados. Se prueban prefijo desechable, controlador, reconexión, arranque frío, reinicio de servicio, signaling nuevo y login conservado; estabilidad de 270–1800 segundos. Debe habilitarse promoción automática y UU estar normalmente 45 minutos inactivo.

Sólo se detiene el servicio del puente. Se copia todo el prefijo con 1 GiB extra, se instala allí, se comparan datos de cuenta, se espera nuevo room y dos checks runtime. XRDP no cambia. State y prefijo deben compartir filesystem. Fallo, reboot o interrupción restaura el anterior, conserva snapshot y bloquea reintentos automáticos. `--now` únicamente omite la espera de actividad.

## Tasks, privacidad y sandbox

Al recibir `thread.started` se guarda UUID para `codex exec resume`; sin UUID se crea otro thread desde el mismo contexto. Retry crece de 15 minutos a 24 horas. El resultado de esquema se prueba independientemente: `ready-for-review`, `no-change`, `blocked`; fases de promoción: `promotion-waiting-idle`, `promotion-running`, `promoted`, `promotion-blocked`.

Directorios privados `0700`, archivos `0600`, push del clone desactivado, Codex workspace-write/never y servicio `NoNewPrivileges=yes`; la autenticación aún necesita red. En Ubuntu 24.04 una mount namespace del user service no debe impedir Bubblewrap anidado. Ante `codex-sandbox-deferred`, instale el perfil distro AppArmor con las órdenes siguientes, sin relajar globalmente las restricciones. `retry` conserva evidencia y checkout, reemplaza thread inutilizable e importa staging sólo con hashes installer/server/healthd correctos.

`disable` conserva evidencia; `disable --purge-state` elimina también configuración privada. A otra máquina lleve sólo fuente y elija su perfil de entrada.

[Upgrade](reusable-upgrade.md) · [Seguridad](security.md)

## Comandos y valores técnicos

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
uu-remote upgrade apply --now
```

```bash
sudo apt install apparmor-profiles
sudo install -o root -g root -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
uu-remote update retry
systemd-run --user --wait --pipe --collect \
  --property=NoNewPrivileges=yes \
  /usr/bin/bwrap --die-with-parent --unshare-user --uid 0 --gid 0 \
  --ro-bind / / /bin/true
systemctl --user cat uu-remote-repair-monitor.service
./scripts/configure-updater.sh status
./scripts/configure-updater.sh disable
./scripts/configure-updater.sh disable --purge-state
```

## Código fuente y temas relacionados


Los detalles técnicos están disponibles en inglés y chino simplificado:

- [automated-repair-agent-handoff](../../automated-repair-agent-handoff.md) · [简体中文](../zh-Hans/automated-repair-agent-handoff.md)
- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
