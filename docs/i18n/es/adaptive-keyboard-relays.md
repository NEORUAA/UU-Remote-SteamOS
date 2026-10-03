[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [中文（简体）](../zh-Hans/adaptive-keyboard-relays.md) · [中文（繁體）](../zh-Hant/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md)

[← Volver al inicio en español](../../../i18n/README.es.md)

# Retransmisión adaptable del teclado

XRDP transporta metadatos de distribución y scancodes; RFB/X11 transporta keysyms; UU de ordenador envía eventos físicos Windows; el IME del teléfono envía Unicode. Mantener estas clases separadas evita perder la intención de los símbolos.

Deje que XRDP elija la distribución declarada por el cliente. Un `setxkbmap ... -layout jp` incondicional en `~/.xsessionrc` la sobrescribe para todos. Mantenga la corrección de un Mac japonés como orden explícita, no como bucle global al iniciar sesión. IBus, texto semántico y terminal no dependen del mapa físico XKB.

## Visor VNC dedicado

El relay a pantalla completa usa `UURB_VNC_GRAB_KEYBOARD=on` y `-GrabKeyboard=1`. Sin captura el escritorio intermedio puede consumir Shift/Ctrl/Alt/Super: `(` pasa a `8`, `?` a `/`, `@` a `2`. x11vnc usa `-modtweak -xkb -add_keysyms` para reconstruir modificadores y admitir keysyms ausentes, siempre en IPv4 loopback.

Desactive grab sólo si el visor no es dedicado. La prueba RFB/Xvfb aislada comprueba 21 símbolos con Shift y `你好` contra XKB japonés. Después use un campo temporal para números, símbolos, Ctrl+A/C/V, Enter/Backspace e IME real, nunca un campo de contraseña.

## Límite de la distribución

X11 directo sigue la distribución de la sesión destino. UU no aporta una identificación fiable por conexión: `Shift+7` no permite adivinar `&` o `'`. XRDP/RFB usan metadatos o keysyms, el teléfono Unicode. Cambie explícitamente el perfil necesario, no el escritorio compartido para todos los clientes. `rdp-public/auto` mantiene literales los commits Unicode; las teclas físicas conservan su ruta normal.

[Arquitectura](architecture.md) · [Seguridad](security.md)

## Comandos y valores técnicos

```text
UURB_VNC_GRAB_KEYBOARD=on
-GrabKeyboard=1
-repeat -nobell -modtweak -xkb -add_keysyms
```

```bash
./install.sh --skip-packages --skip-account-login \
  --vnc-grab-keyboard off
./scripts/test-vnc-keyboard-relay.sh
```

```text
vnc-symbols=23/23 order=exact target-layout=jp
isolated VNC keyboard acceptance passed
```

## Código fuente y temas relacionados


Los detalles técnicos están disponibles en inglés y chino simplificado:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
