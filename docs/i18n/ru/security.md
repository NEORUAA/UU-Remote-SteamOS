[English](../../security.md) · [العربية](../ar/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Tiếng Việt](../vi/security.md) · [中文（简体）](../zh-Hans/security.md) · [中文（繁體）](../zh-Hant/security.md) · [Deutsch](../de/security.md) · [Русский](../ru/security.md)

[← На главную на русском](../../../i18n/README.ru.md)

# Безопасность

## Полномочия и границы

Используйте мост только на разрешённом компьютере и с разрешённой учётной записью UU. Он работает от вошедшего Unix-пользователя в отдельном Wine-префиксе. Xvfb использует Xauthority без TCP; pipes принадлежат wineserver этого префикса. Помощники X11 и терминала получают отдельные новые 256-битные токены и временные IPv4-loopback-порты. Каталоги имеют режим `0700`, файл передачи терминала `0600`, допускается максимум четыре shell-сеанса.

У VNC окна управления нет собственного пароля, но он слушает только loopback и экспортирует одно окно UU, а не частный root. Дополнительный Mac relay использует аутентифицированный VNC через SSH. FreeRDP соединяется только с `127.0.0.1` и проверяет TLS. LAN-listener GNOME определяется его настройками: нужны обычный firewall и отдельный надёжный пароль.

## Пароли и содержимое

`secret-tool` хранит пароль relay в login keyring, FreeRDP получает его через stdin. Классический VNC использует первые восемь байтов, файл остаётся `0600`. Автозапуск шифрует дополнительный пароль keyring с помощью TPM2/systemd-creds и расшифровывает только в защищённом runtime-каталоге. GDM autologin даёт физический доступ после загрузки; TPM не защищает от программ уже вошедшего пользователя, а LUKS остаётся интерактивным.

Логи ввода содержат количество, тип, flags, маршрут, результат и ошибку, но не символы, координаты или буфер. Терминал не сохраняет команды и вывод. Семантический текст ограничен 2 048 записями и намеренно остаётся в буфере после вставки. Не публикуйте tokens, registry, префиксы, необработанные логи и личные снимки.

## Бинарные файлы и обновления

Патчер принимает только `approved`-манифест с полными хешами, размером, уникальными сигнатурами и равнодлинными заменами. Оригиналы `.uu-original` сохраняются. Манифест 4.42 не разрешает другие версии; черновики требуют независимой проверки семантики. Для повторного использования relay должны совпасть source, recipe, profile, pins и provenance.

Неизвестный installer сначала распаковывают без запуска. Явный `--sandbox-install` использует staging Bubblewrap/systemd без сети. Wine не обеспечивает сильную изоляцию процессов одного пользователя. Repair не одобряет себя: promotion требует точных хешей, committed acceptance, настоящих проверок controller/login и минимум 270 стабильных секунд. Транзакция копирует весь префикс и восстанавливает при ошибке, не меняя XRDP.

[Сборка](source-build.md) · [Обновления](automatic-updates.md)

## Команды и технические значения

```text
~/.local/share/wineprefixes/uu-remote
~/.config/uu-remote-bridge/environment
CLIPBOARD / PRIMARY
KEYEVENTF_UNICODE / cliprdr
```

## Исходный код и связанные темы

- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [patches/freerdp-sdl-product.json](../../../patches/freerdp-sdl-product.json)

Подробные технические страницы доступны на английском и упрощённом китайском:

- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
