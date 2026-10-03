[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [中文（简体）](../zh-Hans/automatic-updates.md) · [中文（繁體）](../zh-Hant/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Русский](../ru/automatic-updates.md)

[← На главную на русском](../../../i18n/README.ru.md)

# Автоматические проверки и возобновляемый ремонт

Система разделяет наблюдение, private source-repair и явно принятую live-promotion. Обычная проверка не прерывает работающий relay.

## Конфигурация и timers

Собственная история выпусков Plus начинается с `v0.1.0`. Датированные теги маршрутов ввода относятся к истории исходного проекта и не включены в этот независимый репозиторий. Обычная установка не требует этих тегов. Когда тег Plus доступен локально, выберите его явно: `--track v0.1.0 --branch main`. Конфигуратор по умолчанию всё ещё выбирает старые имена и отклоняет отсутствующий тег.

После перехода на тег выпуска выполните `git switch main` перед обычным обновлением с получением исходников. Поддерживаемая ветка — `origin/main`, явно заданный тег переустановки — `v0.1.0`. Чтобы при обновлении намеренно сохранить исходники выбранного тега, используйте `--no-pull`.

`--auto-promote-accepted` разрешает только последующие maintainer-accepted версии с привязанными хешами, не собственный черновик Codex. Model, reasoning и абсолютный путь Codex сохранены в `updater.json`; тот же пользователь должен войти. Все окна included usage должны быть ниже стандартного порога 20%; невозможность проверки откладывает минимум на час.

`uu-remote-update-check.timer` работает ежедневно около 04:20 со случайной задержкой и через 12 минут после boot; `Persistent=true` восполняет пропущенную проверку. Monitor начинает через семь минут и далее спустя 15 минут после предыдущего запуска.

## Наблюдение и repair

Checker следует официальному HEAD redirect, удаляет временные query-ключи и сравнивает полные версии. ETag, размер и hash-sidecar предотвращают повторную загрузку одинакового файла. Более старый endpoint не является обновлением. Две ошибки здоровья через 20 секунд создают evidence и task без остановки Wine/RDP/UU. Только отдельный opt-in `--auto-reinstall` допускает восстановление.

Download ограничен 1 GiB. Неизвестные хеши статически распаковываются и анализируются в private clone с копией контракта `0600`. Нераспаковываемый wrapper требует явного staging без сети. Codex не может sudo, менять live-prefix, push или одобрять свою бинарную интерпретацию.

## Принятая promotion

Официальный hash, `approved`-манифест, schema-1 acceptance и evidence должны совпасть в одном fetched `origin/main` commit, с hashes installer/patched-server. Проверяются disposable prefix, controller, reconnect, cold-start, service restart, новое signaling и сохранение login; стабильность 270–1800 секунд. Автопromotion включается явно и обычно ждёт 45 минут тишины UU.

Останавливается только bridge-service. Полная копия prefix с дополнительным 1 GiB, установка туда же, побайтная проверка аккаунта, новый room и две runtime-проверки. XRDP не изменяется. State и prefix должны быть на одном filesystem. Ошибка, reboot или прерывание возвращает старый prefix, сохраняет snapshot и блокирует автоматический повтор. `--now` пропускает только ожидание покоя.

## Tasks, приватность и sandbox

UUID при `thread.started` сохраняется для `codex exec resume`; без UUID создаётся новый thread с тем же контекстом. Retry растёт от 15 минут до 24 часов. Результат по schema проверяется отдельно: `ready-for-review`, `no-change`, `blocked`; promotion-phases: `promotion-waiting-idle`, `promotion-running`, `promoted`, `promotion-blocked`.

Каталоги `0700`, файлы `0600`, push clone отключён, Codex workspace-write/never, service `NoNewPrivileges=yes`; аутентификации ещё нужна сеть. В Ubuntu 24.04 mount namespace user-service не должна блокировать вложенный Bubblewrap. При `codex-sandbox-deferred` установите только distro AppArmor-profile командами ниже, не ослабляйте ограничения глобально. `retry` сохраняет evidence и checkout, меняет непригодный thread и импортирует staging только с точными hashes installer/server/healthd.

`disable` сохраняет evidence; `disable --purge-state` удаляет и private configuration/state. На другой компьютер копируйте лишь source и выбирайте его собственный input-profile.

[Обновление](reusable-upgrade.md) · [Безопасность](security.md)

## Команды и технические значения

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
uu-remote upgrade apply --now
```

```bash
sudo apt install apparmor-profiles
sudo install -o root -g root -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
uu-remote update retry
systemd-run --user --wait --pipe --collect \
  --property=NoNewPrivileges=yes \
  /usr/bin/bwrap --die-with-parent --unshare-user --uid 0 --gid 0 \
  --ro-bind / / /bin/true
systemctl --user cat uu-remote-repair-monitor.service
./scripts/configure-updater.sh status
./scripts/configure-updater.sh disable
./scripts/configure-updater.sh disable --purge-state
```

## Исходный код и связанные темы


Подробные технические страницы доступны на английском и упрощённом китайском:

- [automated-repair-agent-handoff](../../automated-repair-agent-handoff.md) · [简体中文](../zh-Hans/automated-repair-agent-handoff.md)
- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)
