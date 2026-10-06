[English](../../performance-evidence.md) · [العربية](../ar/performance-evidence.md) · [Deutsch](../de/performance-evidence.md) · [Español](../es/performance-evidence.md) · [Français](../fr/performance-evidence.md) · [日本語](../ja/performance-evidence.md) · [한국어](../ko/performance-evidence.md) · [Русский](../ru/performance-evidence.md) · [Tiếng Việt](../vi/performance-evidence.md) · [简体中文](../zh-Hans/performance-evidence.md) · [繁體中文](../zh-Hant/performance-evidence.md)

[Inicio](../../../i18n/README.es.md)

# Experiencia y rendimiento

![Mejoras de texto chino, portapapeles y gestión](../../images/experience-refinements-en.png)

[SVG editable](../../images/experience-refinements-en.svg)

![Área de píxeles y selección de cuatro lienzos](../../images/canvas-pixel-scale-en.png)

[SVG editable](../../images/canvas-pixel-scale-en.svg)

Elija 720p/1080p/1440p/4K según pantalla y conexión; calidad UU, FPS solicitados y bitrate son independientes.

**0.2.0-work · 2026-10-06:** Solo archivos regulares entrantes. La sincronización actual Ubuntu → Mac y el foco entre dos controladores siguen pendientes. [Uso y actualización en inglés](../../updates/2026-10-06.md)

## Mejoras cotidianas

Las mejoras recientes se centran en la entrada de chino, el pegado de texto y el manejo de ventanas.

| Escena | Contexto | Experiencia anterior | Experiencia mejorada |
| --- | --- | --- | --- |
| Chino desde el teléfono | Entrada móvil anterior en Plus | Parte del texto enviado no llegaba correctamente al escritorio | El chino enviado por conexión directa del teléfono llega correctamente al escritorio Ubuntu |
| Copiar y pegar | Relay de texto anterior en Plus | Después de copiar texto nuevo, todavía podía pegarse contenido anterior | El texto recién copiado se actualiza para pegarlo en el escritorio; copiar y pegar texto desde el ordenador funciona |
| Ajustes y ventanas de UU | Vista de gestión anterior en Plus | La gestión podía superponerse al escritorio o dejar el foco en otro lugar | La gestión UU y sus menús se capturan por separado. La pérdida de foco al cambiar entre dos controladores sigue sin resolverse. |
| Nitidez y tamaño | Prueba de ampliación del lienzo de Plus | Ampliar la fuente 4K probada no añadía detalle y empeoraba la imagen | Cuatro perfiles muestran todo el escritorio y recuperan el tamaño guardado; 4K es suficiente para la fuente probada |
| Reconexión | Actualización del cliente Mac UU | La actualización de Mac UU requería revisar el uso cotidiano | La reconexión, el chino directo y el pegado siguen funcionando; la experiencia 4K se siente similar |

La [comparación](upstream-comparison.md) distingue la base heredada, la compatibilidad con versiones nuevas, las funciones añadidas y las correcciones durante el uso de Plus.

![Base original, cambios de Plus y previsiones de diseño](../../images/uu-plus-evolution-en.png)

[SVG editable](../../images/uu-plus-evolution-en.svg)

**Previsión de diseño:** actualizar el texto a tiempo y devolver el foco de forma predecible debería reducir los intentos repetidos de pegado y las interrupciones entre ajustes y escritorio. Un lienzo menor aporta menos píxeles por imagen; la respuesta visible también depende de captura, codificación, red y pantalla del controlador.

## Píxeles y selección

| Lienzo | Píxeles por imagen | Relación con1080p |
| --- | ---: | ---: |
| 1280 × 720 | 921,600 | 0.44× |
| 1920 × 1080 | 2,073,600 | 1.00× |
| 2560 × 1440 | 3,686,400 | 1.78× |
| 3840 × 2160 | 8,294,400 | 4.00× |

Es relación de área. Captura puede usar origen completo; compresión, movimiento y red determinan carga real. Ajuste inteligente no cambia resolución física.

| Control | Uso |
| --- | --- |
| Lienzo Ubuntu | Imagen relé; empezar1080p,4K para texto/espacio |
| Calidad/FPS/True Color | Compresión, frecuencia solicitada y color disponible |
| `uu-remote quality bitrate 20` | Máximo20 Mbps; `0` elimina límite; bajo puede suavizar movimiento |

[Guía de calidad](quality-guide.md): menús/comandos/recuperación.

## Coste de compilación

Compilación completa desde fuentes limpias, preparación y checks:

| Dato | Observación |
| --- | --- |
| Tiempo | 699.851 s (~11min40s) |
| Límites | CPU equivalente a2 núcleos; memoria4 GiB |
| Pico reportado | ~1.8 GB, lectura redondeada del servicio |
| Swap | 0 bytes |
| Salida | 13 binarios Windows |
| Reproducibilidad | Bytes idénticos con entradas fijas en distintos directorios |

La entrada normal usa rutas normalizadas/configuración explícita. Descargas y compilador afectan al tiempo en otro equipo; puede reutilizar salida verificada: [fuentes](source-build.md).

| Entorno | Ubuntu | GNOME | Windows UU |
| --- | --- | --- | --- |
| Original | 24.04 | 46 | 4.33.0.8907 |
| Plus local | 26.04 | 50 | 4.42.0.2770 |

## Medición igualada

Los registros existentes no contienen mediciones igualadas de FPS del controlador ni de latencia entre entrada y pantalla visible para el upstream fijo frente a Plus. Los tiempos del relay y los experimentos de cuota de CPU miden componentes.


Fije host/controlador, resolución, aplicación, red, calidad/FPS y bitrate. Use entornos independientes con versiones fijadas y considere instalación original24.04. Mida una acción hasta respuesta visible; cuente actualizaciones visibles en movimiento repetible. Repita, informe dispersión/claridad y conserve método.
