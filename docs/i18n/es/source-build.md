[English](../../source-build.md) · [العربية](../ar/source-build.md) · [Deutsch](../de/source-build.md) · [Español](../es/source-build.md) · [Français](../fr/source-build.md) · [日本語](../ja/source-build.md) · [한국어](../ko/source-build.md) · [Русский](../ru/source-build.md) · [Tiếng Việt](../vi/source-build.md) · [简体中文](../zh-Hans/source-build.md) · [繁體中文](../zh-Hant/source-build.md)

[Inicio](../../../i18n/README.es.md)

# Compilar y reutilizar el relé

El instalador compila FreeRDP SDL fijado con parches Plus de portapapeles y tamaño. [Receta](../../../vendor/freerdp-sdl-build/), [bloqueo de fuentes](../../../vendor/freerdp-sdl-build/source-lock.json) y [perfil](../../../patches/freerdp-sdl-product.json) registran revisiones, archivos, herramientas y 13 binarios Windows.

<a id="reference-toolchain"></a>

## Preparar las herramientas de referencia de Ubuntu 26.04

En Ubuntu 26.04 amd64, el [script de preparación](../../../scripts/prepare-build-toolchain.py) descarga 17 paquetes oficiales de Ubuntu con versiones fijas y verifica 14 archivos del compilador y las herramientas frente a `source-lock.json`. El [manifiesto de paquetes](../../../patches/reference-build-packages.json) registra versiones, tamaños y hashes. El script descarga, extrae en un directorio privado y verifica; no instala paquetes del sistema. Ejecútelo desde la raíz del repositorio:

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root"
```

`--packages-dir` selecciona la caché y `--root` debe ser un directorio privado nuevo o vacío. Para extraer y verificar de nuevo solo desde la caché, elija otra raíz vacía y añada `--verify-only`; no se accede a la red:

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root-offline" \
  --verify-only
```

El script muestra un comando `sudo apt install` con las rutas de los 17 `.deb` locales. Ejecútelo manualmente en Ubuntu 26.04 para instalar las herramientas de referencia. La receta existente usa rutas fijas de `/usr`; la extracción privada sirve para verificar las herramientas, no para seleccionar otro entorno de compilación.

Después ejecute el instalador normal. Prepara las demás dependencias de compilación del host, WineHQ y los paquetes de ejecución de GNOME, compila el relé y valida antes de desplegar. La preparación comprueba 14 archivos de referencia; la compilación completa y sus 13 archivos de ejecución se verifican mediante este flujo:

```bash
./install.sh
./scripts/verify.sh --quick
```

En Ubuntu 24.04, use una salida verificada que coincida con el perfil actual mediante el flujo de reutilización siguiente. Los paquetes anteriores de Ubuntu 26.04 son específicos de 26.04.

## Compilación y caché

Una compilación desde cero requiere los archivos exactos del compilador y las herramientas revisadas registrados en `source-lock.json`, con los mismos bytes. Los paquetes APT habituales de la distribución no proporcionan automáticamente esa cadena.

`./install.sh` prepara dependencias y valida antes de sustituir el relé. Reutiliza `build/freerdp` si la procedencia coincide con perfil, receta y valores fijados. Si no, `scripts/build-winpr.sh` usa fuentes nuevas, dos tareas y 900 segundos, y comprueba el resultado.

Con las herramientas revisadas instaladas en las rutas `/usr` de la receta y las dependencias del host listas, también puede compilar una caché independiente del relé:

```bash
UURB_BUILD_DIR=/absolute/path/to/build-work   ./scripts/build-winpr.sh /absolute/path/to/fresh-output
```

Use un directorio de salida nuevo. El trabajo de fuentes se crea bajo el directorio indicado sin usar un prefijo Wine activo. Para reutilizar una salida verificada:

Desde la raíz del repositorio, valide primero una salida existente frente al perfil actual. El instalador normal prepara las dependencias del host. Use `--skip-packages` solo si ya están instaladas las herramientas de compatibilidad del host, WineHQ y los paquetes de ejecución de GNOME; `--skip-account-login` es opcional si la cuenta ya está configurada.

```bash
python3 scripts/verify-freerdp-runtime.py --mode build /absolute/path/to/verified/output
```

Después reutilice esa salida mediante la entrada existente del instalador:

```bash
UURB_FREERDP_PREBUILT_DIR=/absolute/path/to/verified/output   ./install.sh
```

La caché debe coincidir con receta, binarios fijados y procedencia del perfil actual. Si cambia el perfil hay que ejecutar de nuevo compilación y validación; editar recibos o sumas no aprueba otros binarios. El instalador comprueba también la copia antes de iniciar el servicio.

## Entradas y resultados

Se fijan FreeRDP/WinPR, SDL 3.2.28, SDL_ttf, OpenH264, FreeType, HarfBuzz y paquetes OpenSSL, cJSON, uriparser. Antes de compilar se verifican parche y hashes de MinGW/compilador/herramientas. Un cambio necesita receta revisada.

Los mapas de prefijos de archivos, macros y depuración normalizan rutas. FreeRDP mantiene opaque OFF desde la primera configuración; la DLL de compatibilidad usa salida relativa. Así no se incluyen rutas locales.

Con la cadena fijada, dos raíces distintas generaron los mismos bytes para los 13 archivos. La configuración CMake inicial y repetida produjo iguales metadatos. Una compilación completa desde cero, sin salida precompilada, tardó unos 700 segundos dentro del límite de 900 y pasó comprobaciones de ejecución y procedencia. Véanse [calidad](quality-guide.md) y [coste](performance-evidence.md).
