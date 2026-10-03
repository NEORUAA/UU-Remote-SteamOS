[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[Español · UU Remote Ubuntu Plus](README.es.md)

# Contribuir a UU Remote Ubuntu Plus

Puedes aportar informes, traducciones, documentación o código. Conserva la autoría y licencia MIT del [puente de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge).

## Describir problema y recorrido

Incluye versiones Ubuntu/GNOME/Wine/UU, lienzo, ruta de entrada y reproducción. Distingue controlar Ubuntu, el gestor local y Ubuntu controlando otro equipo. Cambios pequeños y métodos de medición facilitan revisión. Usa el [formulario de compatibilidad](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

## Dependencias de desarrollo

Usa Ubuntu y Python del sistema. Estos paquetes sirven para compilar y pruebas aisladas; install.sh gestiona la instalación. Selecciona compiladores con WINEGCC, MINGW_CC y HOST_CC, sin rutas personales. Usa prefijos Wine y displays Xvfb temporales.

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

## Comprobar código

Ejecuta bash -n sobre los shell modificados y los controles siguientes. Mantén avisos C estrictos. Algunas pruebas necesitan Wine, Xvfb o bus systemd; informa las omitidas. UURB_TEST_SYSTEMD=1 solo con servicios de usuario utilizables.

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

## Documentación e ilustraciones

Ejecuta las pruebas de documentación existentes. Los SVG inglés/chino de flujo y adaptación comparten diseño; los dos últimos comandos son solo para regenerar con Node y Sharp. Revisa imágenes completas y metadatos, conserva códigos de pago originales.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

## Validar instalación

Instala en un anfitrión autorizado y prepara una vía de recuperación para la breve desconexión. El verificador completo incluye 270 segundos de estabilidad; comprueba imagen, entrada y reconexión con controlador real. Detén solo el prefijo UU, nunca pkill wine global.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

## Versiones nuevas de UU

Nuevos ejecutables requieren revisión y manifiestos aprobados con SHA-256 completos y justificación de parches de igual longitud. Documenta restauración idéntica, arranque, entrada y retirada. No publiques binarios propietarios ni registros privados. Consulta [mantenimiento upstream (English)](../docs/upstream-maintenance.md).

## Preparar archivos públicos

Revisa lista y cambios preparados. Excluye builds, prefijos Wine, cachés, estado .omc, credenciales, identificadores y texto introducido. Mantén autenticación, TLS, comprobación de manifiestos y eliminación reversible.

```bash
git status --short
git diff --cached
```

## Solicitar revisión

Explica problema, comportamiento nuevo y comprobaciones ejecutadas. Solicita revisión independiente; FPS configurados no son mediciones. Lee [calidad](../docs/i18n/es/quality-guide.md), [Ubuntu](../docs/i18n/es/ubuntu-26.04-port.md) y [seguridad](../docs/i18n/es/security.md), conservando MIT y autoría.
