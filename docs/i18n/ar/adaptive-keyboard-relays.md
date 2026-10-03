[English](../../adaptive-keyboard-relays.md) · [العربية](../ar/adaptive-keyboard-relays.md) · [Español](../es/adaptive-keyboard-relays.md) · [Français](../fr/adaptive-keyboard-relays.md) · [日本語](../ja/adaptive-keyboard-relays.md) · [한국어](../ko/adaptive-keyboard-relays.md) · [Tiếng Việt](../vi/adaptive-keyboard-relays.md) · [中文（简体）](../zh-Hans/adaptive-keyboard-relays.md) · [中文（繁體）](../zh-Hant/adaptive-keyboard-relays.md) · [Deutsch](../de/adaptive-keyboard-relays.md) · [Русский](../ru/adaptive-keyboard-relays.md)

<div dir="rtl">

[← العودة إلى الصفحة العربية](../../../i18n/README.ar.md)

# ترحيل لوحة المفاتيح المتكيف

يحمل XRDP بيانات التخطيط وscancodes، ويحمل RFB/X11 رموز keysyms، وترسل لوحة UU على الكمبيوتر أحداث Windows فعلية، بينما يرسل IME الهاتف Unicode. يحافظ الفصل بينها على معنى الرموز.

دع XRDP يختار التخطيط الذي يبلغه العميل. يفرض `setxkbmap ... -layout jp` غير المشروط في `~/.xsessionrc` التخطيط الياباني على الجميع. احتفظ بإصلاح Mac الياباني كأمر مقصود، لا حلقة عامة عند كل دخول. لا يعتمد IBus والنص الدلالي والطرفية على XKB الفعلي.

## عارض VNC المخصص

يستخدم الترحيل بملء الشاشة `UURB_VNC_GRAB_KEYBOARD=on` و`-GrabKeyboard=1`. بدونهما قد يستهلك سطح المكتب الوسيط Shift/Ctrl/Alt/Super: تتحول `(` إلى `8` و`?` إلى `/` و`@` إلى `2`. يستخدم x11vnc الخيارات `-modtweak -xkb -add_keysyms` لاستعادة modifiers والرموز المفقودة، على IPv4 loopback فقط.

عطّل grab فقط عندما لا يكون العارض مخصصاً للترحيل. يفحص اختبار RFB/Xvfb المعزول 21 رمز Shift و`你好` مقابل XKB ياباني. اختبر بعد ذلك حقلاً مؤقتاً للأحرف والرموز وCtrl+A/C/V وEnter/Backspace وIME الحقيقي، وليس حقل كلمة مرور.

## حدود التخطيط

يتبع X11 المباشر تخطيط الجلسة الهدف. لا يقدم UU معرف تخطيط موثوقاً لكل اتصال؛ لا يمكن استنتاج `&` أو `'` من `Shift+7` وحده. يستخدم XRDP/RFB البيانات أو keysyms والهاتف Unicode. عدّل ملف العميل المناسب صراحة بدلاً من فرض تخطيط عام. يحتفظ `rdp-public/auto` بنص Unicode حرفياً؛ المفاتيح الفعلية تحتفظ بالمسار المعتاد.

[البنية](architecture.md) · [الأمان](security.md)

## الأوامر والقيم التقنية

<div dir="ltr" align="left">

```text
UURB_VNC_GRAB_KEYBOARD=on
-GrabKeyboard=1
-repeat -nobell -modtweak -xkb -add_keysyms
```

</div>

<div dir="ltr" align="left">

```bash
./install.sh --skip-packages --skip-account-login \
  --vnc-grab-keyboard off
./scripts/test-vnc-keyboard-relay.sh
```

</div>

<div dir="ltr" align="left">

```text
vnc-symbols=23/23 order=exact target-layout=jp
isolated VNC keyboard acceptance passed
```

</div>

## المصدر والموضوعات المرتبطة


تتوفر التفاصيل الهندسية بالإنجليزية والصينية المبسطة:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [semantic-text-and-clipboard](../../semantic-text-and-clipboard.md) · [简体中文](../zh-Hans/semantic-text-and-clipboard.md)

</div>
