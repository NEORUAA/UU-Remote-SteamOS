<div dir="ltr">

[English](../../upstream-comparison.md) · [العربية](../ar/upstream-comparison.md) · [Deutsch](../de/upstream-comparison.md) · [Español](../es/upstream-comparison.md) · [Français](../fr/upstream-comparison.md) · [日本語](../ja/upstream-comparison.md) · [한국어](../ko/upstream-comparison.md) · [Русский](../ru/upstream-comparison.md) · [Tiếng Việt](../vi/upstream-comparison.md) · [简体中文](../zh-Hans/upstream-comparison.md) · [繁體中文](../zh-Hant/upstream-comparison.md)

[الرئيسية](../../../i18n/README.ar.md)

</div>

<div dir="rtl">

# ما الذي يغيره Plus

![أساس المشروع الأصلي وتغييرات Plus والتوقعات التصميمية](../../images/uu-plus-evolution-en.png)

[SVG قابل للتحرير](../../images/uu-plus-evolution-en.svg)

الأساس [مشروع Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)، المرجع [`e2854e2b`](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/commit/e2854e2b50c48ead1246bec027c2e13b5693a10a). عزل Wine ومرحّل GNOME والإدخال والإدارة والخدمة موروثة.

## التغييرات في الاستخدام اليومي

| المجال | أساس المشروع الأصلي | تغيير Plus | الاستخدام |
| --- | --- | --- | --- |
| المضيف | Ubuntu 24.04 وlibei معزول | تكييف Ubuntu 26.04/GNOME 50 واختيار libei؛ يبقى هدف 24.04 | اقرأ دليل المنصة والبناء المناسب للمضيف |
| Windows UU | 4.33.0.8907 افتراضيًا وبيانات مراجعة | 4.42.0.2770 المراجع افتراضيًا | اختر بيانًا يطابق نسخة UU |
| الصورة | دقة محفوظة وتغيير حجم RDP | أربعة أحجام حتى 4K، ملاءمة كاملة واستعادة الحجم | اختر 720p أو1080p أو1440p أو4K وتحقق من اللوحة الحالية |
| نص الهاتف | تطبيع IME ولصق Unicode | تحسين مسارات Plus ومسار النص العام لـFreeRDP | أدخل الصينية والكود والنص المتعدد الأسطر |
| الحافظة | حافظة RDP ومعاملات Unicode | رقعة مصدر SDL لفحص الخلفية وتغيير المالك وذاكرة التنسيقات | انسخ النص الحالي والصقه والمرحّل في الخلفية |
| الإدارة | عرض نافذة مستقل وإعادة التركيز | التقاط مستقل للنوافذ والمنبثقات وإعادة استخدام العارض | افتح حساب UU أو إعداداته ثم عد إلى سطح المكتب |
| المؤشر | حماية اختيارية بحجم ثابت | بديل من السمة وإصلاح البدء؛ الافتراضي متوقف | فعّل حماية المؤشر عند الحاجة |
| الإجراءات | التحكم بالفأرة ولوحة المفاتيح | ربط إجراءات سطح المكتب والنظرة العامة في GNOME | اربط إجراءات المتحكم بخلفية GNOME |
| الأدوات | متطلبات المرحّل وأوامر UU | جودة/VNC/FreeRDP/Openbox بخطوط وDPI ودخول محلي | افتح الأداة بإعداداتها الخاصة |
| البناء والاستعادة | Nightly SDL/WinPR ثابت وإعادة اتصال الخدمة | مصادر مرقعة ثابتة وفحص واستعادة الأحجام والعارض | جهّز مرحّلًا مطابقًا واحتفظ بإعداداتك أثناء الصيانة |

## تصنيف التنفيذ

- نص الهاتف: تطوير مسارات الإدخال في Plus — [uu_input_broker.c](https://github.com/lachlanchen/uu-remote-ubuntu-bridge/blob/e2854e2b50c48ead1246bec027c2e13b5693a10a/src/uu_input_broker.c) · [uu_input_broker.c](../../../src/uu_input_broker.c) · [freerdp-adapter.c](../../../src/freerdp-adapter.c)
- الحافظة: رقعة مصدر SDL — [freerdp-sdl-owner-refresh.patch](../../../vendor/freerdp-sdl-build/freerdp-sdl-owner-refresh.patch)
- الإدارة: التقاط مستقل ومعالجة العارض — [uu_manager_capture.c](../../../src/uu_manager_capture.c) · [uu-remote-console](../../../scripts/uu-remote-console)
- الأدوات: تكامل جديد مع سطح المكتب — [uu-desktop-tool.py](../../../scripts/uu-desktop-tool.py) · [uu-tools-fonts.conf](../../../desktop/uu-tools-fonts.conf)

## مسارات الإدخال

يختار تثبيت RDP الجديد المسار <span dir="ltr">`rdp-public`</span>، ويرسل الوسيط الإدخال إلى API FreeRDP العامة. يُلصق Unicode بما فيه ASCII حرفيًا في الوضع التلقائي، وتبقى المفاتيح الفعلية منفصلة. يحفظ التحديث المسار. يستخدم <span dir="ltr">`legacy`</span> المفاتيح للمحارف الممكنة واللصق لـCJK والأسطر؛ البدء دون إعداد يستخدم <span dir="ltr">`legacy`</span> أيضًا.

لمقارنة FPS والتأخر، ثبّت النسخ ودقة المصدر والجودة/FPS ومعدل البت والشبكة والحمل وسجّل طريقة القياس؛ راجع [دليل القياس](performance-evidence.md).

</div>
