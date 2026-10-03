[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [中文（简体）](../zh-Hans/reusable-upgrade.md) · [中文（繁體）](../zh-Hant/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md)

[← На главную на русском](../../../i18n/README.ru.md)

# Повторяемое обновление с сохранением входа

`uu-remote-upgrade` и `uu-remote upgrade` объединяют обновление репозитория, принятую UU-promotion, обновление моста и проверки. `status` показывает состояние, `check` не меняет продукт, `apply` ждёт периода покоя. `apply --now` пропускает только ожидание активности, не разрешая неизвестные или непринятые binaries.


После перехода на тег выпуска выполните `git switch main` перед обычным обновлением с получением исходников. Поддерживаемая ветка — `origin/main`, явно заданный тег переустановки — `v0.1.0`. Чтобы при обновлении намеренно сохранить исходники выбранного тега, используйте `--no-pull`.

## Транзакция

Нужен чистый checkout без detached HEAD. Fetch/fast-forward не объединяет расходящуюся историю; при изменении source скрипт запускается заново. Tests и shell parser выполняются до изменения. Проверяются одобренный продукт, relay, маршрут, задержки и markers аккаунта. Продолжается только официальный installer с точным hash и acceptance манифеста.

Promotion копирует весь Wine-префикс, устанавливает в нём, патчит и сравнивает login registry и оба дерева аккаунта побайтно. Следуют две runtime-проверки с интервалом стабильности. Затем отдельно сохраняется runtime моста, обновляются helpers/service с сохранением environment, track и Codex-настроек. XRDP только опрашивается; изменение active-state делает операцию неуспешной.

## Восстановление и ввод

Ошибка или прерывание возвращает весь префикс и состояние `promotion-blocked`; автоматического повтора нет. Повторная явная постановка той же принятой версии требует изменённого commit promotion-кода; старая task сохраняется в `tasks/retired/`. Ошибка source-refresh восстанавливает runtime после promotion. Timer не удаляет snapshots.

Пример X11-параметров нельзя переносить на другой компьютер: действует сохранённый профиль. Quick verifier не печатает в вашем приложении; после обновления проверьте телефонный текст, быстрые физические клавиши, движение/клик/drag/колесо.

Постоянный bus `/run/user/UID/bus` предотвращает запрос не того user manager из вложенного терминала. История 4.34 июля 2026 не описывает нынешний Plus 4.42. Тогда исправлялись отсутствующий verifier, PE timestamps и гонка готовности; сегодня проверка ждёт реальный listener и выбранный helper до 45 секунд. На другой компьютер переносится только source, не префикс, keyring или private state. Командам нужен `~/.local/bin` в `PATH`.

[Автоматические обновления](automatic-updates.md) · [Клавиатура](adaptive-keyboard-relays.md)

## Команды и технические значения

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

## Исходный код и связанные темы


Подробные технические страницы доступны на английском и упрощённом китайском:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
