[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [中文（简体）](../zh-Hans/reusable-upgrade.md) · [中文（繁體）](../zh-Hant/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md)

[← Volver al inicio en español](../../../i18n/README.es.md)

# Actualizaciones repetibles conservando el inicio de sesión

`uu-remote-upgrade` y `uu-remote upgrade` unen actualización del repositorio, promoción UU aceptada, renovación del puente y comprobaciones. `status` muestra estado, `check` no modifica el producto, `apply` espera inactividad. `apply --now` sólo omite esa espera, sin forzar binarios desconocidos o no aceptados.


Después de seleccionar el tag de la versión, ejecute `git switch main` antes de las actualizaciones habituales que descargan fuentes. La rama mantenida es `origin/main`; el tag explícito de reinstalación sigue siendo `v0.1.0`. Para conservar deliberadamente las fuentes seleccionadas en el tag durante la actualización, use `--no-pull`.

## Transacción

Se exige checkout limpio y no detached. Fetch y fast-forward no mezclan historiales divergentes; el script vuelve a ejecutarse si cambia la fuente. Antes del cambio corren tests y parser shell. Se comprueban producto aprobado, relay, ruta, tiempos y marcadores de cuenta. Sólo continúa un instalador oficial cuyo hash y acceptance coinciden con el manifiesto.

La promoción copia el prefijo Wine completo, instala en el mismo prefijo, aplica parches y compara byte a byte login del registro y ambos árboles de cuenta. Siguen dos verificaciones runtime y un intervalo estable. Después guarda el runtime del puente y renueva helpers/service, preservando el environment. Conserva track y ajustes Codex. XRDP sólo se consulta; un cambio de estado activo hace fallar la operación.

## Recuperación y entrada

El fallo o interrupción restaura todo el prefijo y marca `promotion-blocked`, sin reintento automático. Reencolar explícitamente la misma versión aceptada exige un commit distinto del código de promoción; las tareas viejas quedan en `tasks/retired/`. Si falla la renovación de fuente, se restaura el runtime posterior a la promoción. Los timers no borran snapshots.

Los valores X11 de ejemplo no deben copiarse a otro equipo: manda su ruta guardada. El verificador rápido no escribe en su aplicación; tras actualizar compruebe texto de teléfono, teclas físicas rápidas y movimiento/clic/arrastre/rueda.

El bus persistente `/run/user/UID/bus` evita consultar un user manager distinto desde terminales anidados. El incidente histórico 4.34 de julio de 2026 no describe Plus 4.42 actual. Sus correcciones cubrieron verificador faltante, timestamp PE y carrera de readiness; las verificaciones actuales esperan hasta 45 segundos al listener real y auxiliar seleccionado. En otro equipo sólo copie fuente, no prefijo, keyring o estado privado. `~/.local/bin` debe estar en `PATH`.

[Actualizaciones automáticas](automatic-updates.md) · [Teclado](adaptive-keyboard-relays.md)

## Comandos y valores técnicos

```bash
uu-remote-upgrade status
uu-remote upgrade status
uu-remote upgrade check
uu-remote upgrade apply
uu-remote upgrade apply --now
./scripts/upgrade-uu-remote.sh apply --now
```

```text
UURB_TEXT_KEY_DELAY_MS=8
UURB_PHYSICAL_KEY_DELAY_MS=0
UURB_KEYBOARD_ROUTE=x11
UURB_NETWORK_INTERFACE=default
unix:path=/run/user/UID/bus
~/.local/state/uu-remote-updater/tasks/*/promotion/snapshot-prefix
~/.local/state/uu-remote-upgrader/transactions/TIMESTAMP/
~/.local/state/uu-remote-upgrader/latest
```

```bash
git status --short
git switch main
git pull --ff-only origin main
./install.sh --skip-packages --skip-account-login
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/upgrade-uu-remote.sh check
```

## Código fuente y temas relacionados


Los detalles técnicos están disponibles en inglés y chino simplificado:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
