[English](../../security.md) · [العربية](../ar/security.md) · [Español](../es/security.md) · [Français](../fr/security.md) · [日本語](../ja/security.md) · [한국어](../ko/security.md) · [Tiếng Việt](../vi/security.md) · [中文（简体）](../zh-Hans/security.md) · [中文（繁體）](../zh-Hant/security.md) · [Deutsch](../de/security.md) · [Русский](../ru/security.md)

<div dir="rtl">

[← العودة إلى الصفحة العربية](../../../i18n/README.ar.md)

# الأمان

## الصلاحيات والحدود

استخدم الجسر على جهاز وحساب UU مأذون لك بإدارتهما فقط. تعمل المكونات باسم مستخدم Unix المسجل داخل Wine prefix مستقل. يستخدم Xvfb ملفات Xauthority دون TCP، وتنتمي الأنابيب إلى wineserver لذلك prefix. يحصل مساعدا X11 والطرفية على منافذ IPv4 loopback مؤقتة ورموز مستقلة جديدة بطول 256 بت. الدلائل `0700`، ملف تسليم الطرفية `0600`، والحد الأقصى أربع جلسات shell.

لا توجد كلمة مرور مستقلة لـ VNC الإداري، لكنه يستمع إلى loopback فقط ويصدر نافذة UU واحدة بدلاً من root الخاص. يستخدم ترحيل Mac الاختياري VNC موثقاً عبر SSH. يتصل FreeRDP بـ `127.0.0.1` فقط ويتحقق من TLS. يعتمد listener شبكة LAN الخاص بـ GNOME على إعداداته؛ استخدم جداراً نارياً وكلمة مرور قوية مستقلة.

## الأسرار والمحتوى

يحفظ `secret-tool` كلمة المرور في login keyring ويقرأها FreeRDP عبر stdin. يستخدم VNC التقليدي أول ثمانية بايتات مع ملف `0600`. يشفر التشغيل دون حضور كلمة مرور keyring الإضافية بواسطة TPM2/systemd-creds، ولا يفكها إلا في دليل runtime محمي. يتيح GDM autologin الدخول الفعلي بعد الإقلاع؛ لا يحمي TPM من برامج المستخدم المسجل، ويبقى LUKS بحاجة إلى تدخل.

تسجل بيانات الإدخال العدد والنوع وflags والمسار والنتيجة والخطأ دون الأحرف أو الإحداثيات أو الحافظة. لا تسجل الطرفية الأوامر أو الناتج. يُحد النص الدلالي بـ 2048 سجلاً ويبقى عمداً في الحافظة بعد اللصق. لا تنشر الرموز أو registry أو prefixes أو السجلات الخام أو الصور الخاصة.

## الملفات الثنائية والصيانة

يقبل patcher بيان `approved` فقط مع hash كامل وحجم وتواقيع فريدة وتغييرات متساوية الطول. تبقى أصول `.uu-original`. لا يأذن بيان 4.42 بإصدار آخر؛ المسودات تحتاج مراجعة دلالية مستقلة. تتطلب إعادة استخدام الترحيل تطابق source وrecipe وprofile وpins وprovenance.

تُفك حزمة installer غير المعروف دون تشغيل أولاً. الخيار الصريح `--sandbox-install` يستخدم staging Bubblewrap/systemd بلا شبكة. ليس Wine عزلاً قوياً بين عمليات المستخدم نفسه. لا يوافق repair على نتيجته: تحتاج promotion إلى hashes دقيقة وacceptance مودعة واختبارات حقيقية لعميل التحكم والحساب و270 ثانية مستقرة على الأقل. تنسخ المعاملة prefix كاملاً وتستعيده عند الفشل دون تغيير XRDP.

[البناء](source-build.md) · [التحديثات](automatic-updates.md)

## الأوامر والقيم التقنية

<div dir="ltr" align="left">

```text
~/.local/share/wineprefixes/uu-remote
~/.config/uu-remote-bridge/environment
CLIPBOARD / PRIMARY
KEYEVENTF_UNICODE / cliprdr
```

</div>

## المصدر والموضوعات المرتبطة

- [patches/uu-remote-4.42.0.2770.json](../../../patches/uu-remote-4.42.0.2770.json)
- [patches/freerdp-sdl-product.json](../../../patches/freerdp-sdl-product.json)

تتوفر التفاصيل الهندسية بالإنجليزية والصينية المبسطة:

- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)

</div>
