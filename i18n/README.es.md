<div align="center">

[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

<a href="README.es.md"><img src="../docs/images/uu-plus-logo.png" alt="UU Remote Ubuntu Plus" width="140"></a>

# UU Remote Ubuntu Plus

**Tus ideas te acompañan; tu entorno de desarrollo se queda en Ubuntu.**

El editor, las terminales y las sesiones de tus aplicaciones se quedan en Ubuntu. Conéctate desde el teléfono, Mac o Windows, disfruta de Vibe Coding a tu manera y cambia de pantalla para seguir escribiendo.

[![Ubuntu 24.04 / 26.04](https://img.shields.io/badge/Ubuntu-24.04%20%7C%2026.04-E95420?logo=ubuntu&logoColor=white)](../docs/i18n/es/ubuntu-26.04-port.md)
[![GNOME 46 / 50](https://img.shields.io/badge/GNOME-46%20%7C%2050-4A86CF?logo=gnome&logoColor=white)](../docs/i18n/es/architecture.md)
[![UU Remote 4.42](https://img.shields.io/badge/UU_Remote-4.42.0.2770-00A870)](../patches/uu-remote-4.42.0.2770.json)
[![MIT](https://img.shields.io/badge/License-MIT-2F81F7)](../LICENSE)

<img src="../docs/images/vibe-coding-cross-device-en.png" alt="UU Remote Ubuntu Plus" width="1120">

</div>

Plus conecta NetEase UU Remote con la sesión GNOME en la que ya has iniciado sesión.
La aplicación oficial de UU para Windows se ejecuta en un entorno Wine dedicado.
Un relé local presenta el escritorio real y una ventana independiente permite
gestionar la cuenta y los ajustes de UU. Las aplicaciones y los archivos siguen
en la misma sesión cuando alternas entre el uso local y el remoto.

El proyecto parte de **[UU Remote Ubuntu Bridge de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
Plus amplía la compatibilidad con Ubuntu y UU, añade cuatro tamaños de lienzo
y mejora la entrada, el portapapeles y las herramientas de gestión.

El instalador está dirigido a x86-64 Ubuntu 24.04 / GNOME 46 y Ubuntu 26.04 / GNOME 50 con UU 4.42.0.2770. Las instalaciones nuevas seleccionan 1080p y dejan desactivada la protección opcional del cursor.

Las once páginas de idioma y sus guías técnicas describen Plus en cada idioma; el inglés es la referencia canónica.

## De la instalación al trabajo remoto

1. Instala el puente en el escritorio Ubuntu.
2. Ejecuta `uu-remote open` e inicia sesión en UU desde la ventana de gestión.
3. Conecta con este equipo desde el controlador UU del teléfono, Mac o Windows.
4. Elige un tamaño de lienzo y utiliza tus aplicaciones habituales.

## Funciones y mejoras

El proyecto original aporta el relé del escritorio, el teclado y el ratón, el tratamiento del IME del teléfono y la recuperación de servicios. Plus desarrolla esa base con compatibilidad más reciente, controles de calidad más claros y mejoras para el uso diario.

| Uso diario | Qué añade Plus |
| --- | --- |
| Ubuntu y UU más recientes | Ubuntu 26.04 / GNOME 50 y UU 4.42, conservando la instalación de Ubuntu 24.04. |
| Elegir el lienzo | Cambia entre 720p, 1080p, 1440p y 4K desde un selector gráfico. Ajusta el escritorio completo al lienzo y recupera el tamaño guardado. |
| Chino, código y copiar/pegar | Corrige la entrega de texto del teléfono y la actualización del portapapeles. El texto nuevo llega al escritorio y los fragmentos de código y textos de varias líneas conservan su contenido. |
| Abrir ajustes y seguir conectado | Captura por separado la gestión de UU y sus menús. Al cerrar el visor, el foco de entrada vuelve al relé del escritorio. |
| Herramientas locales más cómodas | Acceso a calidad, VNC, FreeRDP y Openbox, con mejoras de fuentes, DPI y arranque. |
| Instalar y mantener | Compila el relé desde fuentes fijadas y comprueba los componentes antes de instalar. Recupera cambios fallidos de lienzo y permite previsualizar la desinstalación. |

Consulta la [comparación con el proyecto original](../docs/i18n/es/upstream-comparison.md) para los cambios y el contexto de versiones.

<img src="../docs/images/experience-refinements-en.png" alt="Experiencia y mediciones" width="1120">

[Experiencia y mediciones](../docs/i18n/es/performance-evidence.md)

## Instalación rápida

En un host Ubuntu x86-64 con la sesión GNOME abierta, clona el proyecto:

```bash
git clone https://github.com/llmir/uu-remote-ubuntu-plus.git
cd uu-remote-ubuntu-plus
```

La instalación necesita la cadena de herramientas revisada para compilar el relé o un resultado verificado que coincida con el perfil del producto; los binarios del relé no están incluidos. Ubuntu 26.04 ofrece la preparación de herramientas de referencia; Ubuntu 24.04 utiliza la reutilización de una salida verificada. [Preparación de herramientas y reutilización del relé](../docs/i18n/es/source-build.md#reference-toolchain)

Cuando las herramientas o la salida correspondiente estén listas, ejecuta el instalador normal:

```bash
./install.sh
./scripts/verify.sh --quick
uu-remote open
```

El instalador prepara las dependencias, compila los componentes, configura GNOME
Remote Desktop y arranca los servicios de usuario. Solicita una contraseña del relé,
la guarda en GNOME Keyring y abre UU para iniciar sesión. Una reinstalación conserva
los ajustes y la cuenta existentes. Para empezar en 4K:

```bash
./install.sh --resolution 3840x2160
```

Comparte tu entorno y los pasos de reproducción mediante el [formulario de compatibilidad](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

La primera instalación puede descargar y compilar dependencias. Consulta
[Compilación](../docs/i18n/es/source-build.md) y [Seguridad](../docs/i18n/es/security.md).
Obtén el cliente UU para Windows del sitio oficial de NetEase [uuyc.163.com](https://uuyc.163.com/). El puente lo ejecuta en un entorno Wine dedicado. UU conserva su propia licencia.

## Resumen técnico

<img src="../docs/images/architecture-premium-v2-en.png" alt="Rutas de imagen, entrada y gestión local de UU en Ubuntu." width="1120">

El escritorio Ubuntu pasa por GNOME RDP al relé SDL / FreeRDP y después por UU al controlador. El teclado y el ratón vuelven a la misma sesión mediante el puente de entrada. La cuenta y los ajustes de UU tienen su propia ventana local.

Usa `uu-remote open` para la gestión; el puente sigue funcionando cuando se cierra el visor. `uu-remote console` ofrece una vista opcional en el navegador local. Los módulos y rutas se explican en [Arquitectura](../docs/i18n/es/architecture.md).

## Resolución y calidad

<img src="../docs/images/quality-controls-cartoon-v2-en.png" alt="Ubuntu canvas and UU controller quality controls" width="1120">

Abre **UU Remote 画质与分辨率** en GNOME o ejecuta:

```bash
uu-remote quality gui
```

El escritorio completo se ajusta al lienzo y la resolución del monitor físico se
mantiene. Un cambio de preajuste reconecta brevemente el puente; si falla, se restaura
la configuración anterior.

```bash
uu-remote quality list
uu-remote quality apply 2160p
uu-remote quality status
uu-remote quality guide
```

La calidad de codificación, los FPS y True Color se eligen en el **controlador UU**:
**Centro de control → Calidad** en el ordenador, **Operaciones → Pantalla** en el teléfono.

El límite de bitrate se configura por separado:

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` solicita un máximo de 20 Mbps; `0` lo elimina. Tamaño, calidad, FPS solicitados y
bitrate son controles independientes. Consulta la [guía de calidad](../docs/i18n/es/quality-guide.md).

## Entrada y cursor

El texto del IME del teléfono, los fragmentos de código y el texto multilínea llegan a Ubuntu por la ruta de texto. Las teclas físicas y los atajos mantienen sus eventos de teclado. Plus corrige la entrega de texto y la actualización del portapapeles para escribir y copiar/pegar a diario. Consulta [Relés de teclado](../docs/i18n/es/adaptive-keyboard-relays.md) para los modos de entrada.

La protección opcional del cursor procede del proyecto original; Plus mejora los
recursos del cursor y su tratamiento. Para activarla:

```bash
./install.sh --skip-packages --skip-account-login \
  --cursor-guard on --cursor-size auto
```

`auto` sigue el tamaño del cursor del escritorio; un valor como `24` fija el cursor
alternativo. `--cursor-guard off` la desactiva. La reinstalación reconecta UU brevemente.

## Uso diario y mantenimiento

```bash
uu-remote status
uu-remote network
uu-remote logs
uu-remote restart
uu-remote stop
```

`uu-remote open` abre la gestión; `uu-remote login` permite iniciar sesión o recuperarla.
Reiniciar, iniciar sesión y reinstalar interrumpen brevemente la conexión.

Guarda tus cambios locales, actualiza el código y reinstala:

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

Los cambios del código en ejecución se aplican al reinstalar.
Consulta [Actualización](../docs/i18n/es/reusable-upgrade.md) para `uu-remote upgrade` y
[Actualizaciones automáticas](../docs/i18n/es/automatic-updates.md) para el mantenimiento opcional.

Para desinstalar conservando el estado de la cuenta UU:

```bash
./uninstall.sh --dry-run
./uninstall.sh
```

`./uninstall.sh --purge` también elimina el prefijo Wine dedicado, las credenciales
del relé y la habilitación de GNOME RDP.

## Más allá de Ubuntu

El instalador actual se dirige a Ubuntu 24.04 y 26.04 x86-64. La [guía de adaptación a Linux](../docs/i18n/es/porting.md) divide las futuras adaptaciones en tres capas:

- Reutilizar el núcleo de compatibilidad UU, el relé y la entrada.
- Adaptar paquetes de la distribución, rutas Wine y servicios.
- Conectar los mecanismos propios del escritorio para captura, entrada, modos de pantalla y acciones.

Otras distribuciones GNOME pueden reutilizar más integración existente. KDE y Xfce necesitan sus propios componentes de escritorio.

## Documentación y contribuciones

- [Calidad](../docs/i18n/es/quality-guide.md), [Compilación](../docs/i18n/es/source-build.md) y [Ubuntu 26.04](../docs/i18n/es/ubuntu-26.04-port.md)
- [Arquitectura](../docs/i18n/es/architecture.md), [Seguridad](../docs/i18n/es/security.md) y [Resolución de problemas](../docs/i18n/es/troubleshooting.md)
- [Comparación](../docs/i18n/es/upstream-comparison.md) y [Mediciones](../docs/i18n/es/performance-evidence.md)
- [Cambios](CHANGELOG.es.md) y [Contribuir](CONTRIBUTING.es.md)

Indica las versiones, los ajustes y los pasos para reproducir el comportamiento.

## Apoya el proyecto

**Invítame a un café ☕**

UU y Ubuntu siguen cambiando. Seguiré adaptando Plus a las nuevas versiones y afinando la entrada de texto, copiar y pegar y la calidad de imagen. Un café ayuda a cubrir las pruebas de versiones, las herramientas de desarrollo y los tokens.

| PayPal | Alipay · CNY | AlipayHK · HKD | WeChat · CNY | WeChat · HKD |
| :---: | :---: | :---: | :---: | :---: |
| <a href="https://paypal.me/mirmirlin"><img src="../docs/images/support-paypal-en.png" alt="PayPal" width="160"></a> | <a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support-alipay-cny-en.png" alt="Alipay · CNY" width="160"></a> | <a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support-alipay-hkd-en.png" alt="AlipayHK · HKD" width="160"></a> | <a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support-wechat-zh-en.png" alt="WeChat · CNY" width="160"></a> | <a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support-wechat-en-en.png" alt="WeChat · HKD" width="160"></a> |

<details>
<summary>Códigos de pago de Alipay y WeChat</summary>

<p><a href="../docs/i18n/es/support.md#alipay-cny">Alipay CNY</a><br><a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support/alipay-cny.jpg" alt="Alipay CNY" width="240"></a></p>

<p><a href="../docs/i18n/es/support.md#alipay-hkd">AlipayHK HKD</a><br><a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support/alipay-hkd.png" alt="AlipayHK HKD" width="240"></a></p>

<p><a href="../docs/i18n/es/support.md#wechat-zh">WeChat · CNY</a><br><a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support/wechat-zh.png" alt="WeChat · CNY" width="240"></a></p>

<p><a href="../docs/i18n/es/support.md#wechat-en">WeChat · HKD</a><br><a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support/wechat-en.png" alt="WeChat · HKD" width="240"></a></p>

</details>

También son bienvenidos los errores con pasos para reproducirlos, las notas de adaptación a Linux y los pull requests. Gracias por ayudar a dar forma a la próxima versión.

[Apoya UU Remote Ubuntu Plus](../docs/i18n/es/support.md)

## Créditos y licencia

Basado en **[UU Remote Ubuntu Bridge de Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
Se conservan el aviso de copyright y la [licencia MIT](../LICENSE).
UU y las dependencias mantienen sus propias licencias y marcas.
Este es un proyecto comunitario independiente.

Iconos de los medios de pago: [Simple Icons](https://simpleicons.org/) (CC0); las marcas conservan sus respectivos derechos.
