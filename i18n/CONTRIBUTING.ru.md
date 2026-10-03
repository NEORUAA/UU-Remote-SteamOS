[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[Русский · UU Remote Ubuntu Plus](README.ru.md)

# Участвовать в UU Remote Ubuntu Plus

Принимаются отчёты, переводы, документы и код. Сохраняйте авторство и MIT-лицензию [моста Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge).

## Проблема и маршрут

Укажите Ubuntu/GNOME/Wine/UU, холст, путь ввода и воспроизведение. Различайте Ubuntu-хост, локальный менеджер и Ubuntu-контроллер. Делайте небольшие изменения, описывайте метод измерения. Для обратной связи используйте [форму совместимости](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

## Среда разработки

Используйте Ubuntu и системный Python. Пакеты нужны для сборки и отдельных тестов; runtime управляет install.sh. Выбирайте WINEGCC/MINGW_CC/HOST_CC без личных путей, используйте временные Wine/Xvfb.

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

## Проверить исходники

Проверьте shell через bash -n, затем выполните команды. Сохраняйте строгие C-предупреждения. Тестам могут требоваться Wine/Xvfb/systemd: указывайте пропуски. UURB_TEST_SYSTEMD=1 только с рабочей пользовательской шиной.

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

## Документы и иллюстрации

Запустите существующие тесты. Английские/китайские SVG имеют общий макет; последние Node/Sharp-команды нужны только для перерисовки. Проверяйте всё изображение и метаданные, сохраняйте исходные платёжные коды.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

## Проверить установку

Устанавливайте на разрешённом хосте с резервным подключением. Полная проверка включает 270 секунд стабильности; изображение, ввод и переподключение проверяйте реальным контроллером. Завершайте только выделенный префикс.

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

## Новая версия UU

Нужны проверенный манифест, полные SHA-256 и обоснование равной длины правок. Подтвердите точное восстановление, старт, ввод и удаление. Не публикуйте закрытые бинарники и личные журналы. См. [поддержку upstream (English)](../docs/upstream-maintenance.md).

## Публичные файлы

Просмотрите список и индексированные изменения. Исключите сборки, префиксы, кеши, состояние .omc, пароли, ID устройств и введённый текст. Сохраните аутентификацию, TLS, манифесты и обратимое удаление.

```bash
git status --short
git diff --cached
```

## Рецензирование

Опишите проблему, результат и реальные проверки, запросите независимый обзор. Настройка FPS не измерение. Читайте [качество](../docs/i18n/ru/quality-guide.md), [Ubuntu](../docs/i18n/ru/ubuntu-26.04-port.md), [безопасность](../docs/i18n/ru/security.md), сохраняя MIT и авторство.
