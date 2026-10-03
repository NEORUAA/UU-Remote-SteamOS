[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[Главная](../../../i18n/README.ru.md)

# Что меняет Plus

![Основа upstream, изменения Plus и ожидания от конструкции](../../images/uu-plus-evolution-en.png)

[Редактируемый SVG](../../images/uu-plus-evolution-en.svg)

Основа — [проект Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge), [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a). Wine, GNOME-реле, ввод, менеджер и служба унаследованы.

## Что меняется в повседневной работе

| Область | Основа upstream | Изменение Plus | Как использовать |
| --- | --- | --- | --- |
| Хост | Ubuntu 24.04 и изолированный бэкпорт libei | Адаптация Ubuntu 26.04/GNOME 50, выбор libei; цель 24.04 сохранена | Прочитать руководство платформы и сборки для хоста |
| Windows UU | 4.33.0.8907 по умолчанию и проверенные манифесты | Проверенная 4.42.0.2770 по умолчанию | Выбрать манифест версии UU |
| Размер | Сохранённое разрешение и изменение размера RDP | Четыре режима до 4K, весь рабочий стол и восстановление размера | Выбрать 720p, 1080p, 1440p или 4K и проверить текущий холст |
| Текст телефона | Нормализация IME и вставка Unicode | Развитие путей ввода Plus и публичный текстовый путь FreeRDP | Вводить китайский текст, код и несколько строк |
| Буфер обмена | Буфер RDP и транзакции Unicode | Патч SDL для фоновой проверки, смены владельца и кеша форматов | Копировать текущий текст с ретранслятором в фоне |
| Управление | Отдельное окно и возврат фокуса | Независимый захват окон/диалогов и повторное использование просмотрщика | Открыть аккаунт/настройки UU и вернуться к рабочему столу |
| Курсор | Необязательная защита фиксированного размера | Подстановка из темы и исправления запуска; по умолчанию выключено | Включить защиту курсора при необходимости |
| Действия | Управление мышью и клавиатурой | Действия рабочего стола/обзора GNOME | Связать действия контроллера с бэкендом GNOME |
| Инструменты | Зависимости ретранслятора и команды UU | Качество/VNC/FreeRDP/Openbox, отдельные шрифты, DPI и учётные данные | Открыть инструмент с его локальными настройками |
| Сборка и восстановление | Фиксированный nightly SDL/WinPR и переподключение службы | Фиксированные патчи, проверка компонентов и восстановление режимов/просмотрщика | Подготовить подходящий ретранслятор и сохранить настройки |

## Категории реализации

- Текст телефона: развитие путей ввода Plus — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- Буфер обмена: патч исходников SDL — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- Управление: независимый захват и просмотрщик — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- Инструменты: новая интеграция рабочего стола — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## Пути ввода

Новая установка RDP выбирает `rdp-public`: брокер передаёт ввод публичным API FreeRDP. Unicode, включая ASCII, вставляется буквально в автоматическом режиме; физические клавиши идут отдельно. Обновление сохраняет путь. `legacy` отправляет представимые символы клавишами, CJK/переносы — вставкой; запуск без настройки также использует `legacy`.

Для сравнения FPS и задержки зафиксируйте версии, разрешение, качество/FPS, битрейт, сеть и нагрузку и опишите метод измерения; см. [руководство измерения](performance-evidence.md).
