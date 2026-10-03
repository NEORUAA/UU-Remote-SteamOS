<div dir="rtl">

<div align="center">

[English](../README.md) · [العربية](README.ar.md) · [Español](README.es.md) · [Français](README.fr.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Tiếng Việt](README.vi.md) · [中文 (简体)](README.zh-Hans.md) · [中文（繁體）](README.zh-Hant.md) · [Deutsch](README.de.md) · [Русский](README.ru.md)

<a href="README.ar.md"><img src="../docs/images/uu-plus-logo.png" alt="UU Remote Ubuntu Plus" width="140"></a>

# UU Remote Ubuntu Plus

**اتصل حين تأتيك الفكرة، واترك بيئة التطوير على Ubuntu.**

تظل جلسات المحرر والطرفيات والتطبيقات على Ubuntu. اتصل من هاتفك أو Mac أو Windows، واستمتع بـ Vibe Coding أينما شئت؛ بدّل الشاشة وواصل كتابة الكود.

[![Ubuntu 24.04 / 26.04](https://img.shields.io/badge/Ubuntu-24.04%20%7C%2026.04-E95420?logo=ubuntu&logoColor=white)](../docs/i18n/ar/ubuntu-26.04-port.md)
[![GNOME 46 / 50](https://img.shields.io/badge/GNOME-46%20%7C%2050-4A86CF?logo=gnome&logoColor=white)](../docs/i18n/ar/architecture.md)
[![UU Remote 4.42](https://img.shields.io/badge/UU_Remote-4.42.0.2770-00A870)](../patches/uu-remote-4.42.0.2770.json)
[![MIT](https://img.shields.io/badge/License-MIT-2F81F7)](../LICENSE)

<img src="../docs/images/vibe-coding-cross-device-en.png" alt="UU Remote Ubuntu Plus" width="1120">

</div>

يربط Plus تطبيق NetEase UU Remote بجلسة Ubuntu GNOME التي سجلت الدخول إليها.
يعمل تطبيق UU الرسمي لنظام Windows داخل بيئة Wine مخصصة.
يعرض مرحّل محلي سطح المكتب الحقيقي، وتتيح نافذة إدارة منفصلة استخدام الحساب
وإعدادات UU. تبقى التطبيقات والملفات في الجلسة نفسها عند التنقل بين الاستخدام
المحلي والاتصال عن بُعد.

يعتمد المشروع على **[UU Remote Ubuntu Bridge من Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
يوسّع Plus التوافق مع Ubuntu وUU، ويضيف أربعة أحجام للصورة،
ويحسّن الإدخال والحافظة وأدوات الإدارة.

يستهدف المثبّت x86-64 Ubuntu 24.04 / GNOME 46 وUbuntu 26.04 / GNOME 50 مع UU 4.42.0.2770. يختار التثبيت الجديد 1080p وتبقى حماية المؤشر الاختيارية متوقفة.

تشرح الصفحات والأدلة التقنية Plus بإحدى عشرة لغة، ويمكن متابعة القراءة باللغة نفسها. الإنجليزية هي المرجع الأصلي.

## من الإعداد إلى العمل عن بُعد

1. ثبّت الجسر على سطح مكتب Ubuntu.
2. شغّل <span dir="ltr">`uu-remote open`</span> وسجّل الدخول إلى UU في نافذة الإدارة.
3. اتصل بهذا الجهاز من UU على هاتفك أو Mac أو Windows.
4. اختر حجم الصورة واستخدم تطبيقاتك المعتادة.

## الوظائف والتحسينات

يوفّر المشروع الأصلي مرحّل سطح المكتب ولوحة المفاتيح والفأرة ومعالجة IME للهاتف واستعادة الخدمات. يطوّر Plus هذا الأساس بتوافق أحدث وإعدادات جودة أوضح وتحسينات للاستخدام اليومي.

| الاستخدام اليومي | ما يضيفه Plus |
| --- | --- |
| Ubuntu وUU أحدث | Ubuntu 26.04 / GNOME 50 وUU 4.42 مع الاحتفاظ بمسار تثبيت Ubuntu 24.04. |
| اختيار حجم مناسب | التبديل بين 720p و1080p و1440p و4K بواجهة رسومية. يُعرض سطح المكتب كاملاً في الصورة ويُستعاد الإعداد المحفوظ. |
| الصينية والكود والنسخ واللصق | إصلاح إرسال نص الهاتف وتحديث الحافظة. يصل النص الجديد إلى سطح المكتب وتحافظ مقاطع الكود والنصوص متعددة الأسطر على محتواها. |
| فتح الإعدادات مع البقاء متصلاً | التقاط إدارة UU وقوائمها بصورة مستقلة. إغلاق العارض يعيد تركيز الإدخال إلى مرحّل سطح المكتب. |
| أدوات محلية أسهل | فتح الجودة وVNC وFreeRDP وOpenbox مع تحسين الخطوط وDPI وبدء التشغيل. |
| التثبيت والصيانة | بناء المرحّل من مصادر ثابتة وفحص المكونات قبل التثبيت. استعادة تغييرات الصورة الفاشلة ومعاينة الإزالة قبل تنفيذها. |

التغييرات وسياق الإصدارات في [المقارنة مع الأصل](../docs/i18n/ar/upstream-comparison.md).

<img src="../docs/images/experience-refinements-en.png" alt="التجربة والقياسات" width="1120">

[التجربة والقياسات](../docs/i18n/ar/performance-evidence.md)

## التثبيت السريع

على مضيف Ubuntu ‏x86-64 مع جلسة GNOME مسجل الدخول إليها، استنسخ المشروع:

<div dir="ltr" align="left">

```bash
git clone https://github.com/llmir/uu-remote-ubuntu-plus.git
cd uu-remote-ubuntu-plus
```

</div>

يتطلب التثبيت سلسلة الأدوات المراجعة لبناء المرحّل أو إخراجًا موثّقًا يطابق ملف المنتج؛ لا تتضمن الحزمة ملفات المرحّل الثنائية. يوفر Ubuntu 26.04 مسار تجهيز الأدوات المرجعية، ويستخدم Ubuntu 24.04 إعادة استخدام إخراج موثّق. [تجهيز الأدوات وإعادة استخدام المرحّل](../docs/i18n/ar/source-build.md#reference-toolchain)

بعد تجهيز الأدوات أو الإخراج المطابق، شغّل المثبّت العادي:

<div dir="ltr" align="left">

```bash
./install.sh
./scripts/verify.sh --quick
uu-remote open
```

</div>

يجهز المثبّت الاعتماديات ويبني المكونات ويضبط GNOME Remote Desktop
ويبدأ خدمات المستخدم. تُحفظ كلمة مرور المرحّل في GNOME Keyring،
ثم يُفتح UU لتسجيل الدخول. يحتفظ التثبيت المتكرر بالإعدادات وحالة الحساب.
للبدء بدقة 4K:

<div dir="ltr" align="left">

```bash
./install.sh --resolution 3840x2160
```

</div>

أرسل معلومات البيئة وخطوات التكرار عبر [نموذج التوافق](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

قد يتضمن التثبيت الأول تنزيل مصادر الاعتماديات وبناءها.
انظر [البناء من المصدر](../docs/i18n/ar/source-build.md) و[الأمان](../docs/i18n/ar/security.md).
احصل على عميل UU لنظام Windows من موقع NetEase الرسمي [uuyc.163.com](https://uuyc.163.com/). يشغّله الجسر في بيئة Wine مخصصة. يحتفظ UU بترخيصه الأصلي.

## نظرة تقنية

<img src="../docs/images/architecture-premium-v2-en.png" alt="مسارات صورة Ubuntu والإدخال وإدارة UU المحلية." width="1120">

ينتقل سطح مكتب Ubuntu عبر GNOME RDP إلى مرحّل SDL / FreeRDP، ثم عبر UU إلى جهاز التحكم. تعود لوحة المفاتيح والفأرة عبر جسر الإدخال إلى الجلسة نفسها. لحساب UU وإعداداته نافذة إدارة محلية مستقلة.

شغّل <span dir="ltr">`uu-remote open`</span> للإدارة؛ يستمر الجسر بعد إغلاق العارض. يوفر <span dir="ltr">`uu-remote console`</span> الاختياري عرضاً في المتصفح المحلي. الوحدات ومسارات الإدخال في [البنية](../docs/i18n/ar/architecture.md).

## الدقة والجودة

<img src="../docs/images/quality-controls-cartoon-v2-en.png" alt="Ubuntu canvas and UU controller quality controls" width="1120">

افتح **UU Remote 画质与分辨率** في GNOME أو شغّل:

<div dir="ltr" align="left">

```bash
uu-remote quality gui
```

</div>

يُعرض سطح المكتب كاملاً داخل الصورة، وتبقى دقة الشاشة الفعلية كما هي.
يؤدي تغيير الخيار إلى إعادة اتصال قصيرة؛ يعيد الفشل الإعداد السابق.

<div dir="ltr" align="left">

```bash
uu-remote quality list
uu-remote quality apply 2160p
uu-remote quality status
uu-remote quality guide
```

</div>

تُضبط جودة الترميز وFPS وTrue Color على **جهاز التحكم UU**:
**مركز التحكم → الجودة** على الحاسوب، و**العمليات → العرض** على الهاتف.

يُضبط سقف معدل البت بصورة مستقلة:

<div dir="ltr" align="left">

```bash
uu-remote quality bitrate 20
uu-remote quality bitrate 0
```

</div>

يطلب <span dir="ltr">`20`</span> سقفاً قدره 20 Mbps، ويزيل <span dir="ltr">`0`</span> السقف.
حجم الصورة والجودة وFPS المطلوب ومعدل البت إعدادات منفصلة.
راجع [دليل الجودة](../docs/i18n/ar/quality-guide.md).

## الإدخال والمؤشر

تصل مدخلات IME للهاتف ومقاطع الكود والنصوص متعددة الأسطر عبر مسار النص إلى Ubuntu. تحتفظ المفاتيح الفعلية والاختصارات بأحداث المفاتيح. يصلح Plus إرسال النص وتحديث الحافظة للكتابة والنسخ واللصق اليومي. راجع [مسارات لوحة المفاتيح](../docs/i18n/ar/adaptive-keyboard-relays.md) لأنماط الإدخال.

حماية المؤشر الاختيارية تأتي من المشروع الأصلي.
يحسّن Plus موارد المؤشر ومعالجتها. لتفعيلها:

<div dir="ltr" align="left">

```bash
./install.sh --skip-packages --skip-account-login \
  --cursor-guard on --cursor-size auto
```

</div>

يتبع <span dir="ltr">`auto`</span> حجم مؤشر سطح المكتب، بينما يحدد رقم مثل <span dir="ltr">`24`</span> حجم المؤشر البديل.
يوقف <span dir="ltr">`--cursor-guard off`</span> الحماية. يعيد التثبيت اتصال UU لفترة قصيرة.

## الاستخدام والصيانة

<div dir="ltr" align="left">

```bash
uu-remote status
uu-remote network
uu-remote logs
uu-remote restart
uu-remote stop
```

</div>

استخدم <span dir="ltr">`uu-remote open`</span> للإدارة و<span dir="ltr">`uu-remote login`</span> للدخول أو استعادة الحساب.
تقطع إعادة التشغيل والدخول وإعادة التثبيت الاتصال عن بُعد لفترة قصيرة.

احفظ التعديلات المحلية وحدّث المصدر ثم أعد التثبيت:

<div dir="ltr" align="left">

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
```

</div>

تسري تغييرات كود التشغيل بعد إعادة التثبيت.
راجع [الترقية](../docs/i18n/ar/reusable-upgrade.md) لأوامر <span dir="ltr">`uu-remote upgrade`</span>
و[التحديثات التلقائية](../docs/i18n/ar/automatic-updates.md) للصيانة الاختيارية.

لإزالة الجسر مع الاحتفاظ بحالة حساب UU:

<div dir="ltr" align="left">

```bash
./uninstall.sh --dry-run
./uninstall.sh
```

</div>

يحذف <span dir="ltr">`./uninstall.sh --purge`</span> أيضاً بيئة Wine المخصصة وبيانات اعتماد المرحّل
وإعداد تفعيل GNOME RDP.

## إلى توزيعات Linux أخرى

يستهدف المثبّت الحالي Ubuntu 24.04 و26.04 على x86-64. يقسم [دليل النقل إلى Linux](../docs/i18n/ar/porting.md) المنافذ المستقبلية إلى ثلاث طبقات:

- إعادة استخدام نواة توافق UU والترحيل والإدخال.
- تكييف حزم التوزيعة ومسارات Wine ودمج الخدمات.
- توصيل التقاط الصورة والإدخال وأنماط العرض والإجراءات الخاصة بسطح المكتب.

يمكن لتوزيعات GNOME الأخرى إعادة استخدام قدر أكبر من الدمج الحالي. يحتاج KDE وXfce إلى مكونات سطح مكتب خاصة بهما.

## الوثائق والمساهمة

- [الجودة](../docs/i18n/ar/quality-guide.md)، [البناء](../docs/i18n/ar/source-build.md)، [Ubuntu 26.04](../docs/i18n/ar/ubuntu-26.04-port.md)
- [البنية](../docs/i18n/ar/architecture.md)، [الأمان](../docs/i18n/ar/security.md)، [حل المشكلات](../docs/i18n/ar/troubleshooting.md)
- [المقارنة](../docs/i18n/ar/upstream-comparison.md)، [القياس](../docs/i18n/ar/performance-evidence.md)
- [التغييرات](CHANGELOG.ar.md)، [المساهمة](CONTRIBUTING.ar.md)

اذكر الإصدارات والإعدادات وخطوات إعادة إنتاج السلوك.

## دعم المشروع

**هل أعجبك Plus؟ ادعمني بفنجان قهوة ☕**

يتغير UU وUbuntu باستمرار، وسأواصل تكييف Plus مع الإصدارات الجديدة وتحسين إدخال النصوص والنسخ واللصق وجودة الصورة. تساعد مساهمتك في تكاليف اختبار الإصدارات وأدوات التطوير والرموز المستخدمة أثناء التطوير.

| PayPal | Alipay · CNY | AlipayHK · HKD | WeChat · CNY | WeChat · HKD |
| :---: | :---: | :---: | :---: | :---: |
| <a href="https://paypal.me/mirmirlin"><img src="../docs/images/support-paypal-en.png" alt="PayPal" width="160"></a> | <a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support-alipay-cny-en.png" alt="Alipay · CNY" width="160"></a> | <a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support-alipay-hkd-en.png" alt="AlipayHK · HKD" width="160"></a> | <a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support-wechat-zh-en.png" alt="WeChat · CNY" width="160"></a> | <a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support-wechat-en-en.png" alt="WeChat · HKD" width="160"></a> |

<details>
<summary>رموز الدفع عبر Alipay وWeChat</summary>

<p><a href="../docs/i18n/ar/support.md#alipay-cny">Alipay CNY</a><br><a href="../docs/images/support/alipay-cny.jpg"><img src="../docs/images/support/alipay-cny.jpg" alt="Alipay CNY" width="240"></a></p>

<p><a href="../docs/i18n/ar/support.md#alipay-hkd">AlipayHK HKD</a><br><a href="../docs/images/support/alipay-hkd.png"><img src="../docs/images/support/alipay-hkd.png" alt="AlipayHK HKD" width="240"></a></p>

<p><a href="../docs/i18n/ar/support.md#wechat-zh">WeChat · CNY</a><br><a href="../docs/images/support/wechat-zh.png"><img src="../docs/images/support/wechat-zh.png" alt="WeChat · CNY" width="240"></a></p>

<p><a href="../docs/i18n/ar/support.md#wechat-en">WeChat · HKD</a><br><a href="../docs/images/support/wechat-en.png"><img src="../docs/images/support/wechat-en.png" alt="WeChat · HKD" width="240"></a></p>

</details>

نرحب أيضًا بخطوات واضحة لإعادة إنتاج الأخطاء، وخبرات نقل المشروع إلى Linux، وطلبات الدمج. شكرًا لمساعدتك في تحسين الإصدار القادم.

[دعم UU Remote Ubuntu Plus](../docs/i18n/ar/support.md)

## الشكر والترخيص

مبني على **[UU Remote Ubuntu Bridge من Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge)**.
يُحتفظ بإشعار حقوق النشر الأصلي و[ترخيص MIT](../LICENSE).
تحتفظ UU والاعتماديات بتراخيصها وعلاماتها الخاصة.
هذا مشروع مجتمعي مستقل.

أيقونات وسائل الدفع: [Simple Icons](https://simpleicons.org/) بترخيص CC0؛ تبقى العلامات التجارية ملكًا لأصحابها.

</div>
