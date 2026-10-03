[English](../../architecture.md) · [العربية](../ar/architecture.md) · [Español](../es/architecture.md) · [Français](../fr/architecture.md) · [日本語](../ja/architecture.md) · [한국어](../ko/architecture.md) · [Tiếng Việt](../vi/architecture.md) · [中文（简体）](../zh-Hans/architecture.md) · [中文（繁體）](../zh-Hant/architecture.md) · [Deutsch](../de/architecture.md) · [Русский](../ru/architecture.md)

<div dir="rtl">

[← العودة إلى الصفحة العربية](../../../i18n/README.ar.md)

# البنية التقنية

## سطحا مكتب واتجاهان للبيانات

يعمل تطبيق UU الرسمي الخاص بـ Windows داخل بيئة Wine مستقلة. لا يستطيع برنامج الإدخال في نواة Windows التحكم مباشرة في GNOME. يقدم الجسر نافذة ترحيل على شاشة X11 خاصة: تنتقل الصورة من Ubuntu إلى عميل UU، وتعود لوحة المفاتيح والفأرة والنص المعتمد في الاتجاه الآخر. نافذة الإدارة المحلية فرع مستقل. تستخدم المصادر بيان UU 4.42 وبناء FreeRDP/SDL مثبت المصادر.

يختار التثبيت الجديد `rdp` مع `rdp-public` وهدف `auto` وصورة 1920 × 1080، وتتبع الدقة `off` ونص الهاتف `auto`. تحتفظ الترقية بالإعدادات. إذا غابت إعدادات المسار المثبتة يستخدم المشغّل `legacy`. الخيارات العادية أربعة: 720p و1080p و1440p و4K. يُختار VNC صراحة لسطح X11/XRDP ويحتاج `legacy`؛ لا يحل محل Wayland.

## الصورة والإدخال المعتاد

يبدأ GNOME Remote Desktop على D-Bus للجلسة المختارة. يتصل FreeRDP عبر loopback، افتراضياً `127.0.0.1:3390`، ويتحقق من بصمة TLS ويقرأ كلمة المرور من stdin. يستخدم Xvfb ملف Xauthority و`-nolisten tcp`. في `rdp-public` يركّب XComposite نافذة SDL المرتبطة وحدها على root الخاص، ثم يلتقط UU الصورة ويشفّرها وينقلها.

تختار الرقعة المراجعة لكل إصدار مسار `SendInput` الموجود. يرسل broker العام إلى pipe محلي للإضافة `uurb-full-input`، ثم تنقل دوال FreeRDP الأحداث عبر اتصال RDP القائم. تحمل `/dvc:uurb-full-input` الإضافة دون قناة إدخال جديدة على الخادم. يحاول `legacy` إدخال Wine العادي أولاً، ويرسل الباقي غير المقبول إلى broker. يتاح XTEST المباشر اختيارياً على X11؛ لا يعاد الحدث بعد تسليم ملتبس.

## النص والحافظة

المفاتيح الفعلية تختلف عن `KEYEVENTF_UNICODE`. يحفظ `rdp-public/auto` كل النصوص Unicode حرفياً، بما فيها ASCII. يحول `legacy/auto` النص الممكن إلى اختصارات مفاتيح، ويستخدم اللصق الدلالي للصينية وtab والأسطر. يملك المساعد `CLIPBOARD` و`PRIMARY`، يتحقق من المالكين الجديدين ويرسل `Shift+Insert` عبر المسار المختار. يؤكد الحاجز معاملة التحديد؛ لا تزال نافذة الهدف بحاجة إلى التركيز ودعم اللصق. النسخ المعتاد يستخدم `cliprdr`. يرسل مساعد VNC نص GameViewer إلى Ubuntu فقط، دون قراءة عكسية أو مفتاح لصق.

## الإدارة ودورة الحياة

يلتقط `uu-remote open` مدير UU والنوافذ المنبثقة المرتبطة عبر XComposite إلى TigerVNC محلي. تعود أحداث العارض إلى النافذة المملوكة المناسبة. الإغلاق ينهي العمليات المساعدة ويعيد التركيز إلى الترحيل؛ تبقى نافذة UU mapped. ليس هذا الفرع مرحلة في سلسلة صورة سطح المكتب.

تغير الجودة اللوحة الخاصة ولا تغير الشاشة الفعلية. تُجهز الاستعادة قبل التغيير، ويُبلغ عن فشلها. تشرف خدمة المستخدم على عملياتها وتُنظف prefix الخاص بها فقط. يعالج GNOME إدخال Wayland؛ يستدعي المحول FreeRDP ولا يستدعي libei مباشرة. التصحيح القديم لـ libei اختياري، وفي Ubuntu 26.04 يوجد الإصلاح في النظام. للطرفية والتشغيل دون حضور مساران منفصلان.

[الجودة](quality-guide.md) · [البناء من المصدر](source-build.md) · [الأمان](security.md)

![UU / GNOME](../../images/architecture-premium-v2-en.png)

![Video / Input](../../images/uu-plus-data-flow-en.gif)

[PNG](../../images/uu-plus-data-paths-en.png) · [SVG](../../images/uu-plus-data-paths-en.svg)

![UU manager](../../images/manager-premium-en.png)

## الأوامر والقيم التقنية

<div dir="ltr" align="left">

```text
GNOME -> GNOME Remote Desktop -> loopback RDP -> SDL FreeRDP
  -> private X11 / UU capture -> UU controller
UU controller -> SendInput hook -> broker -> uurb-full-input
  -> FreeRDP input -> GNOME Remote Desktop -> GNOME
GameViewer + popups -> XComposite -> loopback x11vnc -> local TigerVNC
```

</div>

## المصدر والموضوعات المرتبطة

- [install.sh](../../../install.sh#L358)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L6)
- [scripts/runtime-settings.sh](../../../scripts/runtime-settings.sh)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1010)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1758)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1437)
- [scripts/uu-manual-plane.py](../../../scripts/uu-manual-plane.py#L155)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1040)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1844)
- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [src/uu_input_bridge.c](../../../src/uu_input_bridge.c#L688)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L1081)
- [src/plugin.c](../../../src/plugin.c#L200)
- [src/freerdp-adapter.c](../../../src/freerdp-adapter.c#L48)
- [src/uu_input_bridge_legacy.c](../../../src/uu_input_bridge_legacy.c#L595)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L1101)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L454)
- [src/uu_input_broker.c](../../../src/uu_input_broker.c#L641)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1182)
- [src/uu_x11_input.c](../../../src/uu_x11_input.c#L1000)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1266)
- [src/uu_wine_clipboard_bridge.c](../../../src/uu_wine_clipboard_bridge.c#L195)
- [src/uu_x11_clipboard.c](../../../src/uu_x11_clipboard.c#L329)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L1121)
- [src/uu_manager_capture.c](../../../src/uu_manager_capture.c#L464)
- [src/uu_manager_capture.c](../../../src/uu_manager_capture.c#L1090)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L1193)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L622)
- [scripts/uu-remote-console](../../../scripts/uu-remote-console#L299)
- [scripts/uu-quality.py](../../../scripts/uu-quality.py#L329)
- [scripts/uu-display-modes.py](../../../scripts/uu-display-modes.py#L166)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L199)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L1121)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L2207)
- [scripts/uu-remote-bridge](../../../scripts/uu-remote-bridge#L478)
- [systemd/uu-remote-bridge.service](../../../systemd/uu-remote-bridge.service)

تتوفر التفاصيل الهندسية بالإنجليزية والصينية المبسطة:

- [native-ubuntu-terminal](../../native-ubuntu-terminal.md) · [简体中文](../zh-Hans/native-ubuntu-terminal.md)
- [unattended-startup](../../unattended-startup.md) · [简体中文](../zh-Hans/unattended-startup.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)

</div>
