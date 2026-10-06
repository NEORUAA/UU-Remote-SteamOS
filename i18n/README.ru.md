<div align="center">

[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

<a href="README.ru.md"><img src="../docs/images/uu-plus-logo.png" alt="UU Remote Ubuntu Plus" width="140"></a>

# UU Remote Ubuntu Plus

**Подключайтесь, когда приходит идея. Среда разработки остаётся на Ubuntu.**

Редактор, терминалы и сеансы приложений остаются на Ubuntu. Подключайтесь с телефона, Mac или Windows, занимайтесь Vibe Coding в своём ритме и продолжайте писать код на другом экране.

[![Ubuntu 24.04 / 26.04](https://img.shields.io/badge/Ubuntu-24.04%20%7C%2026.04-E95420?logo=ubuntu&logoColor=white)](../docs/i18n/ru/ubuntu-26.04-port.md)
[![GNOME 46 / 50](https://img.shields.io/badge/GNOME-46%20%7C%2050-4A86CF?logo=gnome&logoColor=white)](../docs/i18n/ru/architecture.md)
[![UU Remote 4.42](https://img.shields.io/badge/UU_Remote-4.42.0.2770-00A870)](../patches/uu-remote-4.42.0.2770.json)
[![MIT](https://img.shields.io/badge/License-MIT-2F81F7)](../LICENSE)

<img src="../docs/images/vibe-coding-cross-device-en.png" alt="UU Remote Ubuntu Plus" width="1120">

</div>

Plus соединяет NetEase UU Remote с открытым сеансом Ubuntu GNOME.
Официальное приложение UU для Windows работает в отдельной среде Wine.
Локальный ретранслятор показывает настоящий рабочий стол, а отдельное окно
служит для входа в аккаунт и настройки UU. Приложения и файлы остаются
в одном сеансе при переходе между локальной и удалённой работой.

Проект основан на **[UU Remote Ubuntu Bridge от Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
Plus расширяет совместимость с Ubuntu и UU, добавляет четыре размера изображения
и улучшает ввод, буфер обмена и управление.

Установщик предназначен для x86-64 Ubuntu 24.04 / GNOME 46 и Ubuntu 26.04 / GNOME 50 с UU 4.42.0.2770. Новая установка выбирает 1080p и оставляет необязательную защиту курсора выключенной.

Все одиннадцать языковых страниц и технические руководства описывают Plus на соответствующем языке; английский служит основным справочным текстом.

## Новое в 0.2.0-work

- **Продолжить терминал:** необязательный `persistent` сохраняет shell, каталог и задачи после переподключения; по умолчанию `fresh`.

- **Получить несколько файлов:** скопируйте обычные файлы на контроллере и вставьте готовую группу в Ubuntu; прогресс показывает принятые байты.

- **Совместимость изображений:** исходный PNG вместе с DIBV5/DIB; отдельный помощник Mac добавляет TIFF для PNG.

- **Исследовать нативный захват:** необязательные CPU/GPU-прототипы экспериментальны и не входят в обычную установку.

[CPU (MIT)](../vendor/uur-native-cpu/NOTICE) · [GPU (AGPL-3.0)](../vendor/uuway-gpu-component/README.md)

<img src="../docs/images/uu-plus-update-20261006-en.png" alt="Новое в 0.2.0-work" width="1120">

Только входящие обычные файлы. Текущая синхронизация Ubuntu → Mac и фокус между двумя контроллерами ещё не исправлены.

[Использование и обновление на английском](../docs/updates/2026-10-06.md) · [SVG](../docs/images/uu-plus-update-20261006-en.svg)

## От установки к удалённой работе

1. Установите мост на рабочем столе Ubuntu.
2. Запустите `uu-remote open` и войдите в UU в окне управления.
3. Подключитесь к Ubuntu через UU на телефоне, Mac или Windows.
4. Выберите размер изображения и работайте в привычных приложениях.

## Возможности и улучшения

Исходный проект предоставляет ретрансляцию рабочего стола, клавиатуру и мышь, обработку телефонного IME и восстановление служб. Plus развивает эту основу новой совместимостью, понятными настройками качества и улучшениями для повседневной работы.

| Повседневная задача | Что добавляет Plus |
| --- | --- |
| Новое Ubuntu и UU | Ubuntu 26.04 / GNOME 50 и UU 4.42 с сохранением установки Ubuntu 24.04. |
| Выбрать размер изображения | Переключение между 720p, 1080p, 1440p и 4K в графическом интерфейсе. Весь рабочий стол помещается в изображение; сохранённая настройка восстанавливается. |
| Китайский текст, код и копирование | Исправляет передачу телефонного текста и обновление буфера. Новый текст доходит до рабочего стола, код и многострочные фрагменты сохраняют содержимое. |
| Открыть настройки, оставаясь на связи | Окна управления UU и меню захватываются отдельно. Потеря фокуса при смене двух контроллеров не устранена. |
| Удобнее локальные инструменты | Открывает качество, VNC, FreeRDP и Openbox с улучшениями шрифтов, DPI и запуска. |
| Установка и обслуживание | Собирает ретранслятор из фиксированных исходников и проверяет компоненты перед установкой. Восстанавливает неудачные изменения изображения и показывает предварительный план удаления. |

Изменения и версии описаны в [сравнении с исходным проектом](../docs/i18n/ru/upstream-comparison.md).

<img src="../docs/images/experience-refinements-en.png" alt="Удобство и измерения" width="1120">

[Удобство и измерения](../docs/i18n/ru/performance-evidence.md)

## Быстрая установка

На хосте Ubuntu x86-64 с открытым сеансом GNOME клонируйте проект:

```bash
git clone https://github.com/llmir/uu-remote-ubuntu-plus.git
cd uu-remote-ubuntu-plus
```

Для установки нужна проверенная цепочка инструментов для сборки ретранслятора либо готовый проверенный результат, соответствующий профилю продукта; бинарные файлы ретранслятора не включены. Для Ubuntu 26.04 есть подготовка эталонных инструментов; Ubuntu 24.04 использует повторное использование проверенного результата. [Подготовка инструментов и повторное использование реле](../docs/i18n/ru/source-build.md#reference-toolchain)

Подготовив инструменты или подходящий результат, запустите обычный установщик:

```bash
./install.sh
./scripts/verify.sh --quick
uu-remote open
```

Установщик готовит зависимости, собирает компоненты, настраивает GNOME Remote
Desktop и запускает пользовательские службы. Пароль ретранслятора сохраняется
в GNOME Keyring, затем открывается UU для входа. Повторная установка сохраняет
настройки и состояние аккаунта. Для начала с 4K:

```bash
./install.sh --resolution 3840x2160
```

Опишите окружение и шаги воспроизведения через [форму совместимости](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

При первой установке могут загружаться и собираться зависимости.
См. [Сборка](../docs/i18n/ru/source-build.md) и [Безопасность](../docs/i18n/ru/security.md).
Загрузите Windows-клиент UU с официального сайта NetEase [uuyc.163.com](https://uuyc.163.com/). Мост запускает его в отдельной среде Wine. UU сохраняет собственную лицензию.

## Техническая схема

<img src="../docs/images/architecture-premium-v2-en.png" alt="Изображение Ubuntu, ввод и локальное управление UU." width="1120">

Рабочий стол Ubuntu проходит через GNOME RDP в ретранслятор SDL / FreeRDP, затем через UU к контроллеру. Клавиатура и мышь возвращаются через мост ввода в тот же сеанс. Для аккаунта и настроек UU служит отдельное локальное окно.

`uu-remote open` открывает управление; мост продолжает работать после закрытия просмотра. Необязательный `uu-remote console` предоставляет локальную веб-страницу. Модули и маршруты описаны в [Архитектуре](../docs/i18n/ru/architecture.md).

## Разрешение и качество

<img src="../docs/images/quality-controls-cartoon-v2-en.png" alt="Ubuntu canvas and UU controller quality controls" width="1120">

Откройте **UU Remote 画质与分辨率** в GNOME или выполните:

```bash
uu-remote quality gui
```

Весь исходный рабочий стол вписывается в изображение; разрешение физического
монитора сохраняется. Изменение кратко переподключает мост, а при неудаче
возвращает предыдущую настройку.

```bash
uu-remote quality list
uu-remote quality apply 2160p
uu-remote quality status
uu-remote quality guide
```

Качество кодирования, FPS и True Color задаются в **контроллере UU**:
**Центр управления → Качество** на компьютере, **Действия → Экран** на телефоне.

Ограничение битрейта задаётся отдельно:

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

`20` запрашивает максимум 20 Mbps; `0` убирает ограничение.
Размер, качество, запрашиваемый FPS и битрейт — отдельные настройки.
См. [Руководство по качеству](../docs/i18n/ru/quality-guide.md).

## Ввод и курсор

Текст телефонного IME, фрагменты кода и многострочный текст поступают в Ubuntu по текстовому пути. Физические клавиши и сочетания сохраняют события клавиатуры. Plus исправляет передачу текста и обновление буфера для повседневного ввода и копирования. Режимы описаны в [Клавиатурных маршрутах](../docs/i18n/ru/adaptive-keyboard-relays.md).

Необязательная защита курсора пришла из исходного проекта.
Plus улучшает ресурсы курсора и их обработку. Включить:

```bash
./install.sh --skip-packages --skip-account-login \
  --cursor-guard on --cursor-size auto
```

`auto` следует размеру курсора рабочего стола; число вроде `24` задаёт запасной курсор.
`--cursor-guard off` выключает защиту. Повторная установка кратко переподключает UU.

## Повседневная работа и обслуживание

```bash
uu-remote status
uu-remote network
uu-remote logs
uu-remote restart
uu-remote stop
```

`uu-remote open` открывает управление, `uu-remote login` — вход или восстановление аккаунта.
Перезапуск, вход и повторная установка кратко прерывают удалённое соединение.

Сохраните локальные изменения, обновите исходники и переустановите:

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

Изменения исполняемого кода применяются после повторной установки.
См. [Обновление](../docs/i18n/ru/reusable-upgrade.md) для `uu-remote upgrade` и
[Автоматические обновления](../docs/i18n/ru/automatic-updates.md) для дополнительного обслуживания.

Удалить мост, сохранив состояние аккаунта UU:

```bash
./uninstall.sh --dry-run
./uninstall.sh
```

`./uninstall.sh --purge` также удаляет выделенный Wine prefix, учётные данные
ретранслятора и включение GNOME RDP.

## Другие дистрибутивы Linux

Текущий установщик рассчитан на Ubuntu 24.04 и 26.04 x86-64. [Руководство по переносу на Linux](../docs/i18n/ru/porting.md) делит будущие порты на три слоя:

- Повторное использование ядра совместимости UU, ретрансляции и ввода.
- Адаптация пакетов дистрибутива, путей Wine и служб.
- Подключение механизмов рабочего стола для захвата, ввода, режимов экрана и действий.

Другие GNOME-дистрибутивы могут использовать больше готовой интеграции. KDE и Xfce требуют собственных механизмов рабочего стола.

## Документы и участие

- [Качество](../docs/i18n/ru/quality-guide.md), [Сборка](../docs/i18n/ru/source-build.md), [Ubuntu 26.04](../docs/i18n/ru/ubuntu-26.04-port.md)
- [Архитектура](../docs/i18n/ru/architecture.md), [Безопасность](../docs/i18n/ru/security.md), [Решение проблем](../docs/i18n/ru/troubleshooting.md)
- [Сравнение](../docs/i18n/ru/upstream-comparison.md), [Измерения](../docs/i18n/ru/performance-evidence.md)
- [История](CHANGELOG.ru.md), [Участие](CONTRIBUTING.ru.md)

Укажите версии, настройки и шаги для воспроизведения поведения.

## Поддержать проект

**Угостите меня кофе ☕**

UU и Ubuntu продолжают обновляться. Я буду адаптировать Plus к новым версиям и улучшать ввод текста, копирование и вставку, качество изображения. Чашка кофе помогает покрыть тестирование версий, инструменты разработки и токены.

| PayPal | Alipay · CNY | AlipayHK · HKD | WeChat · CNY | WeChat · HKD |
| :---: | :---: | :---: | :---: | :---: |
| <a href="https://paypal.me/mirmirlin"><img src="../docs/images/support-paypal-en.png" alt="PayPal" width="160"></a> | <a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support-alipay-cny-en.png" alt="Alipay · CNY" width="160"></a> | <a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support-alipay-hkd-en.png" alt="AlipayHK · HKD" width="160"></a> | <a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support-wechat-zh-en.png" alt="WeChat · CNY" width="160"></a> | <a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support-wechat-en-en.png" alt="WeChat · HKD" width="160"></a> |

<details>
<summary>Платёжные коды Alipay и WeChat</summary>

<p><a href="../docs/i18n/ru/support.md#alipay-cny">Alipay CNY</a><br><a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support/alipay-cny.jpg" alt="Alipay CNY" width="240"></a></p>

<p><a href="../docs/i18n/ru/support.md#alipay-hkd">AlipayHK HKD</a><br><a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support/alipay-hkd.png" alt="AlipayHK HKD" width="240"></a></p>

<p><a href="../docs/i18n/ru/support.md#wechat-zh">WeChat · CNY</a><br><a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support/wechat-zh.png" alt="WeChat · CNY" width="240"></a></p>

<p><a href="../docs/i18n/ru/support.md#wechat-en">WeChat · HKD</a><br><a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support/wechat-en.png" alt="WeChat · HKD" width="240"></a></p>

</details>

Также приветствуются воспроизводимые сообщения об ошибках, опыт переноса на Linux и pull request. Спасибо, что помогаете сделать следующую версию удобнее.

[Поддержать UU Remote Ubuntu Plus](../docs/i18n/ru/support.md)

## Благодарности и лицензия

Основано на **[UU Remote Ubuntu Bridge от Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
Сохранены исходное уведомление об авторских правах и [лицензия MIT](../LICENSE).
UU и зависимости сохраняют собственные лицензии и товарные знаки.
Это независимый общественный проект.

Значки платёжных брендов: [Simple Icons](https://simpleicons.org/) (CC0); права на товарные знаки остаются у их владельцев.
