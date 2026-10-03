[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[Русский · UU Remote Ubuntu Plus](../../../i18n/README.ru.md)

# Устранение неполадок

## Первые проверки

Выполняйте команды из каталога исходников. Журналы: `~/.local/state/uu-remote-bridge`, настройки: `~/.config/uu-remote-bridge/environment`. Передавайте версии и ошибки без данных аккаунта и введённого текста. После изменения исходников нужна установка.

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

## Офлайн после загрузки

Войдите через официальный менеджер и закройте его обычно. Проверьте службы пользователя и связку ключей. После смены пароля обновите зашифрованные данные: `./scripts/configure-unattended.sh enable --replace-credential`. При выходе сервера проверьте восстановление.

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

## Бесконечный поиск маршрута

Сначала проверьте запуск хоста. Старые записи устройств ввода и Bluetooth в Wine могут задерживать старт. Команда сохраняет реестр, очищает известные записи выделенного префикса и перезапускает мост, сохраняя Bluetooth Ubuntu.

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

## Чёрный, белый или чужой рабочий стол

Проверьте вошедший сеанс GNOME, порт RDP и журналы SDL. Для XRDP выберите `--desktop-target xrdp`, для физического рабочего стола `physical`. `--desktop-relay vnc` только для X11; Wayland использует RDP.

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

## Пустые края, обрезка, тяжёлое 4K

Сравните исходный стол и холст. Доступны 720p/1080p/1440p/4K. Холст, FPS контроллера и битрейт настраиваются отдельно. Смена кратко переподключает, сбой возвращает прежний режим. Проверьте динамические размеры XRDP.

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

## Изображение есть, управления нет

Открывайте менеджер через uu-remote open, не запускайте тот же Wine-префикс на другом X-дисплее. Закрытие просмотрщика возвращает фокус ретранслятору. Текст телефона идёт через буфер/RDP, физические клавиши остаются событиями. Проверьте инжектор после переустановки. Если первый щелчок завершает сеанс, проверьте UU SendInput bridge active, UU Wine event-log compatibility active и broker; `uu-remote restart` восстанавливает компоненты.

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

## Задержки, неверные символы, ухудшение со временем

Сравните VPN, прокси и UU-маршрут; stale относится к прошлому сеансу. При подтверждённой ошибке адаптера пробуйте `--network-interface default`, возврат — `all`. Для клавиш можно проверить `--physical-key-delay-ms 8`, по умолчанию `0`. Символы зависят от раскладки Ubuntu. Проверьте GRD/libei и дескрипторы при долгих сеансах.

```bash
uu-remote network
ip -4 route show default
```

## Нет курсора или он мал

Защита курсора по умолчанию выключена. auto следует размеру рабочего стола, фиксированный размер — 24–128. `--cursor-guard off` выключает её без смены разрешения и глобального Wine DPI.

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

## Терминал UU закрывается или смещает текст

Установите текущий мост и проверьте канал. Выбор PowerShell в UU открывает shell входа Ubuntu. При смещении создайте новый сеанс, проверьте метаданные terminal-bridge.log. Не заменяйте powershell.exe случайным файлом.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

## Ошибки RDP, NLA, SSPI

Запрос проверяет наличие данных без вывода пароля. При необходимости удалите только запись моста в связке ключей и переустановите. FreeRDP, WinPR и DLL должны быть одной закреплённой версии.

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

## Mac RDP/VNC, Windows App зависает

Внутренний FreeRDP уже использует порт общего стола; удалённый вход создаёт другой сеанс. Узнайте реальный loopback-порт VNC и перенаправьте через SSH. При Configuring сначала перезапустите клиент Mac, затем проверьте XRDP.

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

## Перезапуски, звук и удаление

Полный проверяющий скрипт контролирует стабильность. UU-аудио, Wine PulseAudio и VNC-звонок проверяйте отдельно в выделенной среде. Сначала просмотр удаления; обычное сохраняет префикс, `./uninstall.sh --purge` удаляет и аккаунт. Определите поток через `wpctl status`. `UURB_UU_AUDIO=system` — совместимое значение по умолчанию; отдельная тихая ALSA и отмена настройки описаны в подробном английском руководстве.

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

Далее: [качество](quality-guide.md), [сборка](source-build.md), [архитектура](architecture.md), [ввод](adaptive-keyboard-relays.md), [обновление](reusable-upgrade.md). [Технические подробности и история (English)](../../troubleshooting.md) раскрывают реестр, драйверы, звук, XRDP и терминал.

## Подробные руководства

- Восстановление XRDP и клавиатуры · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- Совместимость клавиатуры · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- Текущий рабочий стол с Mac · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- Общий физический стол · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- Восстановление после выхода · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- Агент контроллера · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- Сообщения агентов через SSH · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)
