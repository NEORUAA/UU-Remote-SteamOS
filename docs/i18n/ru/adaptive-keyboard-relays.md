[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [中文（简体）](../zh-Hans/adaptive-keyboard-relays.md) · [中文（繁體）](../zh-Hant/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md)

[← На главную на русском](../../../i18n/README.ru.md)

# Адаптивные клавиатурные ретрансляторы

XRDP передаёт метаданные раскладки и scancodes, RFB/X11 — keysyms, UU на компьютере — физические Windows-события, IME телефона — Unicode. Их разделение сохраняет смысл символов.

Позвольте XRDP выбрать сообщённую клиентом раскладку. Безусловный `setxkbmap ... -layout jp` в `~/.xsessionrc` перезаписывает её для всех. Исправление для японского Mac запускайте явно, а не в глобальном цикле входа. IBus, семантический текст и терминал не должны зависеть от физического XKB.

## Отдельный VNC viewer

Полноэкранный relay использует `UURB_VNC_GRAB_KEYBOARD=on` и `-GrabKeyboard=1`. Иначе промежуточный desktop может перехватить Shift/Ctrl/Alt/Super: `(` становится `8`, `?` — `/`, `@` — `2`. x11vnc применяет `-modtweak -xkb -add_keysyms` для модификаторов и отсутствующих keysyms, только на IPv4 loopback.

Отключайте grab лишь для viewer другого назначения. Изолированный RFB/Xvfb-тест проверяет 21 Shift-символ и `你好` на японском XKB. Затем проверьте временное текстовое поле: обычные знаки, Shift, Ctrl+A/C/V, Enter/Backspace и реальную IME. Не используйте поле пароля.

## Ограничение раскладки

Прямой X11 следует раскладке целевого сеанса. UU не сообщает надёжный идентификатор раскладки каждой связи: из `Shift+7` нельзя угадать `&` или `'`. XRDP/RFB используют метаданные/keysyms, телефон Unicode. Явно меняйте нужный профиль клиента, а не общий desktop для всех. `rdp-public/auto` сохраняет текст Unicode буквально; физические клавиши идут обычным путём.

[Архитектура](architecture.md) · [Безопасность](security.md)

## Команды и технические значения

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

## Исходный код и связанные темы


Подробные технические страницы доступны на английском и упрощённом китайском:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
