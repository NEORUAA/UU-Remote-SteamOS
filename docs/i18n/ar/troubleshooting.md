<div dir="rtl">

[English](../../troubleshooting.md) · [العربية](../ar/troubleshooting.md) · [Deutsch](../de/troubleshooting.md) · [Español](../es/troubleshooting.md) · [Français](../fr/troubleshooting.md) · [日本語](../ja/troubleshooting.md) · [한국어](../ko/troubleshooting.md) · [Русский](../ru/troubleshooting.md) · [Tiếng Việt](../vi/troubleshooting.md) · [简体中文](../zh-Hans/troubleshooting.md) · [繁體中文](../zh-Hant/troubleshooting.md)

[العربية · UU Remote Ubuntu Plus](../../../i18n/README.ar.md)

# حل المشكلات

## الفحوص الأولى

نفّذ من مجلد المصدر. السجلات في <span dir="ltr">`~/.local/state/uu-remote-bridge`</span> والإعدادات في <span dir="ltr">`~/.config/uu-remote-bridge/environment`</span>. أرفق الإصدارات والأخطاء دون الحساب أو النص المكتوب. أعد التثبيت بعد تعديل المصدر.

<div dir="ltr" align="left">

```bash
uu-remote status
./scripts/verify.sh --quick
uu-remote logs
uu-remote network
```

</div>

## الجهاز غير متصل بعد الإقلاع

سجّل الدخول مرة في الإدارة الرسمية ثم أغلقها طبيعياً. افحص خدمات المستخدم وسلسلة المفاتيح. بعد تغيير كلمة المرور جدّد الاعتماد المشفر باستخدام <span dir="ltr">`./scripts/configure-unattended.sh enable --replace-credential`</span>. افحص الاستعادة عند خروج الخادم.

<div dir="ltr" align="left">

```bash
uu-remote login
./scripts/configure-unattended.sh status
journalctl --user -b -u uu-keyring-unlock.service -u uu-remote-bridge.service --no-pager
```

</div>

## البحث عن المسار لا ينتهي

تحقق من اكتمال تشغيل المضيف. قد تؤخر سجلات الإدخال وBluetooth القديمة في Wine البداية. يحفظ الإصلاح نسخة السجل وينظف المدخلات المعروفة في بيئة UU ثم يعيد تشغيل الجسر، مع الحفاظ على Bluetooth في Ubuntu.

<div dir="ltr" align="left">

```bash
uu-remote repair-registry
./scripts/verify.sh --quick
```

</div>

## صورة سوداء أو بيضاء أو سطح آخر

افحص جلسة GNOME المفتوحة ومنفذ RDP وسجلات SDL. اختر <span dir="ltr">`--desktop-target xrdp`</span> لجلسة XRDP و<span dir="ltr">`physical`</span> للسطح المحلي. <span dir="ltr">`--desktop-relay vnc`</span> خاص بـX11، ويستخدم Wayland مسار RDP.

<div dir="ltr" align="left">

```bash
systemctl --user status uu-remote-bridge.service
/usr/bin/grdctl status
loginctl list-sessions
tail -80 ~/.local/state/uu-remote-bridge/freerdp.log
tail -80 ~/.local/state/uu-remote-bridge/gnome-remote-desktop.log
```

</div>

## فراغ أو قص أو 4K ثقيلة

قارن المصدر وحجم الصورة واختر 720p/1080p/1440p/4K. الصورة وFPS جهاز التحكم ومعدل البت إعدادات مستقلة. التغيير يعيد الاتصال مؤقتاً ويتراجع عند الفشل. افحص أيضاً تغيير حجم XRDP.

<div dir="ltr" align="left">

```bash
uu-remote quality status
uu-remote quality gui
uu-remote quality apply 1080p
```

</div>

## الصورة تعمل والإدخال لا يعمل

افتح الإدارة عبر uu-remote open، ولا تشغّل بيئة Wine نفسها على عرض X آخر. إغلاق العارض يعيد التركيز للمرحّل. نص الهاتف يستخدم الحافظة ولصق RDP، والمفاتيح الفعلية تبقى أحداثاً. افحص محقن الإدخال بعد التحديث. إذا أنهت النقرة الأولى الجلسة، افحص UU SendInput bridge active وUU Wine event-log compatibility active والوسيط، ثم استعد المكونات عبر <span dir="ltr">`uu-remote restart`</span>.

<div dir="ltr" align="left">

```bash
uu-remote open
./scripts/verify.sh --quick
tail -80 ~/.local/state/uu-remote-bridge/input-injector.log
```

</div>

## مفاتيح بطيئة أو رموز خاطئة

قارن VPN والوكيل ومسار UU؛ stale يعني جلسة سابقة. إذا ثبت اختيار بطاقة خاطئة جرّب <span dir="ltr">`--network-interface default`</span> واستعد <span dir="ltr">`all`</span>. يمكن اختبار <span dir="ltr">`--physical-key-delay-ms 8`</span> والأصل <span dir="ltr">`0`</span>. الرموز تتبع لوحة Ubuntu، وافحص GRD/libei وواصفات الملفات عند التدهور الطويل.

<div dir="ltr" align="left">

```bash
uu-remote network
ip -4 route show default
```

</div>

## المؤشر غائب أو صغير

الحماية اختيارية ومتوقفة افتراضياً. auto يتبع حجم سطح المكتب، والحجم الثابت من 24 إلى 128. أوقفها باستخدام <span dir="ltr">`--cursor-guard off`</span> دون تغيير الدقة أو DPI العام لـWine.

<div dir="ltr" align="left">

```bash
./install.sh --skip-packages --skip-account-login --cursor-guard on --cursor-size auto
```

</div>

## طرفية UU تخرج أو تعرض النص خطأ

ثبّت الجسر الحالي وافحص قناة الطرفية. اختر PowerShell في UU لفتح shell تسجيل الدخول في Ubuntu. افتح جلسة جديدة عند انزياح النص، وافحص بيانات terminal-bridge.log الوصفية، ولا تستبدل powershell.exe عشوائياً.

<div dir="ltr" align="left">

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/test-terminal-bridge.sh
```

</div>

## أخطاء RDP أو NLA أو SSPI

الاستعلام يفحص وجود الاعتماد دون عرض كلمة المرور. امسح بند الجسر فقط عند الحاجة ثم أعد التثبيت. ابن FreeRDP وWinPR والمكتبات من النسخة المثبتة نفسها.

<div dir="ltr" align="left">

```bash
/usr/bin/secret-tool lookup service uu-desktop-bridge username "$USER" >/dev/null
/usr/bin/grdctl status
```

</div>

## Mac RDP/VNC أو Windows App عالقة

يستخدم FreeRDP الداخلي منفذ مشاركة السطح، والدخول البعيد يفتح جلسة أخرى. استعلم عن منفذ VNC المحلي الفعلي ثم مرره عبر SSH. عند Configuring أعد فتح تطبيق Mac أولاً ثم افحص XRDP.

<div dir="ltr" align="left">

```bash
~/.local/bin/uu-remote-console relay-port
ss -ltnp
```

</div>

## إعادة تشغيل متكررة وصوت وإزالة

يفحص المحقق الكامل الاستقرار. راجع صوت UU وPulseAudio في Wine وجرس VNC بشكل منفصل داخل البيئة المخصصة. عاين الإزالة أولاً؛ العادية تحفظ البيئة و<span dir="ltr">`./uninstall.sh --purge`</span> يحذف حالة الحساب أيضاً. حدّد تدفق الصوت الفعلي عبر <span dir="ltr">`wpctl status`</span>. <span dir="ltr">`UURB_UU_AUDIO=system`</span> هو الوضع المتوافق الافتراضي، وإعداد ALSA الصامت الخاص والتراجع عنه موضحان في الدليل الإنجليزي التفصيلي.

<div dir="ltr" align="left">

```bash
./scripts/verify.sh
uu-remote logs
./uninstall.sh --dry-run
```

</div>

اقرأ [الجودة](quality-guide.md) و[البناء](source-build.md) و[البنية](architecture.md) و[الإدخال](adaptive-keyboard-relays.md) و[الترقية](reusable-upgrade.md). [التفاصيل الهندسية والتاريخ (English)](../../troubleshooting.md) تشرح السجل والتعريفات والصوت وXRDP والطرفية.

## أدلة تفصيلية

- استعادة XRDP ولوحة المفاتيح · [English](../../xrdp-and-keyboard-recovery.md) · [简体中文](../zh-Hans/xrdp-and-keyboard-recovery.md)
- توافق لوحة المفاتيح · [English](../../mobile-keyboard-parity-handoff.md) · [简体中文](../zh-Hans/mobile-keyboard-parity-handoff.md)
- سطح Mac الحالي · [English](../../macos-current-desktop.md) · [简体中文](../zh-Hans/macos-current-desktop.md)
- السطح المادي المشترك · [English](../../shared-physical-desktop.md) · [简体中文](../zh-Hans/shared-physical-desktop.md)
- استعادة الخروج · [English](../../clean-exit-recovery.md) · [简体中文](../zh-Hans/clean-exit-recovery.md)
- وكيل التحكم · [English](../../controller-agent.md) · [简体中文](../zh-Hans/controller-agent.md)
- رسائل الوكيل عبر SSH · [English](../../agent-link.md) · [简体中文](../zh-Hans/agent-link.md)

</div>
