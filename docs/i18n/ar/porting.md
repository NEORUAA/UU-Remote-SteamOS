<div dir="ltr">

[English](../../porting.md) · [العربية](../ar/porting.md) · [Deutsch](../de/porting.md) · [Español](../es/porting.md) · [Français](../fr/porting.md) · [日本語](../ja/porting.md) · [한국어](../ko/porting.md) · [Русский](../ru/porting.md) · [Tiếng Việt](../vi/porting.md) · [简体中文](../zh-Hans/porting.md) · [繁體中文](../zh-Hant/porting.md)

[الرئيسية](../../../i18n/README.ar.md)

</div>

<div dir="rtl">

# النقل إلى أسطح Linux أخرى

GNOME على x86-64 هو الأقرب: احتفظ بـRDP وعدّل التثبيت. KDE/Xfce يحتاجان محولات سطح مكتب. يستهدف المثبّت Ubuntu 24.04/26.04، والبقية أهداف نقل.

يتطلب تثبيت المرحّل سلسلة الأدوات المراجعة المطابقة أو إخراجًا موثّقًا موجودًا؛ حزم APT المعتادة لا توفر تلك الأدوات تلقائيًا. راجع [متطلبات البناء وإعادة استخدام النسخة المخبأة](source-build.md).

![طبقات النقل الثلاث](../../images/uu-plus-porting.png)

[SVG قابل للتحرير](../../images/uu-plus-porting.svg)

| الطبقة | القابل لإعادة الاستخدام | التكييف والمصدر |
| --- | --- | --- |
| الأساس |Wine/UU معزول، بيانات، SDL/FreeRDP، وسيط/ملحق، مساحة/إدارة|حفظ البروتوكولات وفصل Unicode؛ [الوسيط](../../../src/uu_input_broker.c)، [RDP](../../../src/freerdp-adapter.c)، [ملحق](../../../src/plugin.c)، [التقاط](../../../src/uu_manager_capture.c)|
| التوزيعة |وصفة وفحوص وإعداد وخدمة|حزم ومسارات ومكتبات ومشغلات؛ [تثبيت](../../../install.sh)، [بناء](../../../scripts/build-winpr.sh)، [فحص](../../../scripts/verify-freerdp-runtime.py)، [خدمة](../../../systemd/uu-remote-bridge.service)|
| سطح المكتب |أحداثRDP ونص وأفعال|جلسة والتقاط وإدخال وحافظة وهندسة وأفعال؛ [بدء](../../../scripts/uu-remote-bridge)، [نص](../../../src/uu_x11_input.c)، [أوضاع](../../../scripts/uu-display-modes.py)|

تستخدم API العامة في FreeRDP الاتصال الموجود؛ يمكن تغيير الخادم مستقلًا عن خطاف UU Windows. يحتاج Unicode حافظة المصدر ولصقًا، حاليًا X11/Xwayland. تبقى الإدارة على X11 الخاص بـWine. [البنية](architecture.md).

| المنصة | إعادة الاستخدام والعمل |
| --- | --- |
| Ubuntu 24.04/GNOME 46 |المثبّت والخلفية الحالية، backport libei اختياري|
| Ubuntu 26.04/GNOME 50 |Plus وlibei النظام وUU 4.42|
| Debian/GNOME |أساس ومساحة/RDP؛ حزم/Wine Debian وفحص وdaemon ومكتبات؛ [APT/dpkg](https://www.debian.org/doc/manuals/debian-reference/ch02.en.html)|
| Fedora/GNOME |أساس وخلفية؛ RPM/DNF ومسارات وصلاحيات؛ [GRD](https://packages.fedoraproject.org/pkgs/gnome-remote-desktop/gnome-remote-desktop/)|
| Arch/GNOME |أساس وخلفية؛ pacman ومسارات وأدوات وتحديثGNOME/libei؛ [GRD](https://archlinux.org/packages/extra/x86_64/gnome-remote-desktop/)|
| KDE |أساس ومساحة وإدارة؛ جلسة والتقاط/إدخال ومخرجات وحافظة وأفعال؛ [KRDP](https://github.com/KDE/krdp) يحتاج دمج التوثيق والترميز والنص|
| Xfce/X11 |أساس ومساحة وإدارة ومساعدات؛ جلسة وهندسة وأفعال، VNC `legacy` نقطة البداية|

تغيير مدير الحزم يعالج التثبيت فقط. اربط التقاط المصدر والإدخال والهندسة والأفعال.

| الواجهة | الحالية وما يتغير |
| --- | --- |
| المعمارية |`x86_64` وAMD64 PE؛ غيرها يتطلب تنفيذAMD64 وفحوصًا|
| الحزم |Ubuntu و`apt-get` و`dpkg` وi386 وWineHQ؛ خريطة هدف|
| Wine |`/opt/wine-stable/bin/wine` و`wineserver` و`winepath`؛ مسارات متسقة|
| البناء |MinGW/CMake/Meson/Ninja والأرشيفات ثابتة؛ طابق أو راجع الملف؛ [دليل](source-build.md)|
| الجلسة |`gnome-shell` وD-Bus و`/usr/libexec/gnome-remote-desktop-daemon`؛ العثور أو الاستبدال|
| الدخول |Keyring و`secret-tool` و`grdctl` و`org.gnome.desktop.remote-desktop.rdp`؛ TLS وخدمة منفصلة عن UU|
| المخرجات |`org.gnome.Mutter.DisplayConfig` وشاشة افتراضية؛ compositor أو XRandR في X11|
| النص |`uu-x11-input`/`xclip` و`CLIPBOARD`/`PRIMARY`؛ شاشة صحيحة وواجهةWayland|
| الأفعال |`_NET_SHOWING_DESKTOP` و`org.gnome.Shell.OverviewActive`؛ مدير النوافذ والحالة|
| الخدمة |`systemctl --user` وD-Bus رسومي؛ جلسة/init الهدف|
| الأدوات |`/usr/bin/xfreerdp` و`xtigervncviewer` و`obconf` و`zenity`؛ مسارات وخطوط/DPI ودخول تفاعلي وحماية المرحّل|

مساحة Wine/Xvfb الخاصة تختلف عن المخارج الفعلية والافتراضية. احتفظ بالخيارات الأربعة واستبدل منطق Mutter على KDE/Xfce.

1. اختر نظامًا وجلسة x86-64 وسجل إصدارات OS والسطح وWine وUU.
2. كيّف الحزم والمسارات والمكتبات والخدمة والمشغلات وافحص المرحّل.
3. اربط الالتقاط والإدخال وbus والشاشة والدخول والهندسة والحافظة.
4. اختبر متحكمًا فعليًا: حركة ونقر وعجلة وسحب واختصارات وUnicode ولصق واتصال وإدارة ومنبثقات.
5. افحص الأحجام الأربعة والاستعادة والتراجع والتنظيف وأفعال السطح/النظرة العامة.

ساهم بالخرائط والمسارات والنسخ والنتائج دون ملفات UU أو حسابات. [المقارنة](upstream-comparison.md)، [الجودة](quality-guide.md).

</div>
