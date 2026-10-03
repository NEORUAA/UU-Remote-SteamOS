<div dir="ltr">

[English](../../source-build.md) · [العربية](../ar/source-build.md) · [Deutsch](../de/source-build.md) · [Español](../es/source-build.md) · [Français](../fr/source-build.md) · [日本語](../ja/source-build.md) · [한국어](../ko/source-build.md) · [Русский](../ru/source-build.md) · [Tiếng Việt](../vi/source-build.md) · [简体中文](../zh-Hans/source-build.md) · [繁體中文](../zh-Hant/source-build.md)

[الرئيسية](../../../i18n/README.ar.md)

</div>

<div dir="rtl">

# بناء المرحّل وإعادة استخدامه

يبني المثبّت عميل FreeRDP SDL مثبت النسخة مع إصلاحات Plus للحافظة والحجم. تسجل [الوصفة](../../../vendor/freerdp-sdl-build/) و[قفل المصدر](../../../vendor/freerdp-sdl-build/source-lock.json) و[ملف المنتج](../../../patches/freerdp-sdl-product.json) المراجعات والأرشيفات والأدوات و13 ملف تشغيل Windows.

<a id="reference-toolchain"></a>

## تجهيز أدوات Ubuntu 26.04 المرجعية

على Ubuntu 26.04 amd64 ينزّل [سكربت التجهيز](../../../scripts/prepare-build-toolchain.py) 17 حزمة Ubuntu رسمية ثابتة، ويتحقق من 14 ملفًا للمترجم وأدوات البناء مقابل `source-lock.json`. يسجّل [بيان الحزم](../../../patches/reference-build-packages.json) الإصدارات والأحجام والبصمات. ينزّل السكربت الملفات ويفكها في دليل خاص ويتحقق منها، ولا يثبّت حزم النظام. شغّله من جذر المستودع:

<div dir="ltr">

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root"
```

</div>

يحدد `--packages-dir` مخبأ الحزم، ويجب أن يكون `--root` دليلًا خاصًا جديدًا أو فارغًا. لإعادة الفك والتحقق من المخبأ فقط، اختر دليلًا فارغًا آخر وأضف `--verify-only`؛ لا يُستخدم اتصال الشبكة:

<div dir="ltr">

```bash
python3 scripts/prepare-build-toolchain.py \
  --packages-dir "$HOME/.cache/uu-plus/reference-packages" \
  --root "$HOME/.cache/uu-plus/reference-root-offline" \
  --verify-only
```

</div>

يطبع السكربت أمر `sudo apt install` الذي يتضمن مسارات ملفات `.deb` المحلية السبعة عشر كلها. نفّذ الأمر يدويًا على Ubuntu 26.04 لتثبيت الأدوات المرجعية. تقرأ وصفة البناء مسارات `/usr` الثابتة؛ دليل الفك الخاص مخصص للتحقق ولا يختار بيئة بناء أخرى.

بعد ذلك شغّل المثبّت العادي. يجهّز بقية اعتماديات البناء على المضيف وحزم WineHQ وتشغيل GNOME، ويبني المرحّل ويفحصه قبل النشر. يتحقق التجهيز من 14 ملفًا مرجعيًا؛ أما البناء الكامل والملفات التشغيلية الثلاثة عشر فيُفحصان في هذا المسار:

<div dir="ltr">

```bash
./install.sh
./scripts/verify.sh --quick
```

</div>

على Ubuntu 24.04 استخدم إخراجًا موجودًا موثّقًا يطابق ملف المنتج الحالي عبر مسار إعادة الاستخدام أدناه. حزم Ubuntu 26.04 المذكورة مخصصة لـ26.04.

## البناء والذاكرة المخبأة

يتطلب البناء من مصادر جديدة ملفات المترجم وأدوات البناء المراجعة نفسها المسجلة في `source-lock.json`، ببايتات مطابقة. حزم APT المعتادة للتوزيعة لا توفر هذه الأدوات تلقائيًا.

يجهز `./install.sh` الحزم ويتحقق قبل استبدال المرحّل. يستخدم `build/freerdp` مجددًا فقط إن تطابقت بيانات المنشأ مع الملف والوصفة والقيم المثبتة. وإلا يبني `scripts/build-winpr.sh` مصادر جديدة بمهمتين وحد 900 ثانية ثم يتحقق.

بعد تثبيت الأدوات المراجعة في مسارات `/usr` المحددة في الوصفة وتجهيز اعتماديات البناء، يمكنك أيضًا إنشاء مخبأ منفصل للمرحّل:

<div dir="ltr">

```bash
UURB_BUILD_DIR=/absolute/path/to/build-work   ./scripts/build-winpr.sh /absolute/path/to/fresh-output
```

</div>

استخدم دليل إخراج جديدًا. تُنشأ مهمة مصدر فريدة تحت دليل العمل دون استخدام بادئة Wine عاملة. لإعادة استخدام إخراج موثّق:

من جذر المستودع، تحقق أولًا من إخراج موجود مقابل ملف المنتج الحالي. يجهّز المثبّت العادي اعتماديات المضيف. استخدم `--skip-packages` فقط عند تثبيت أدوات توافق المضيف وWineHQ وحزم تشغيل GNOME مسبقًا؛ و`--skip-account-login` اختياري لحساب معد مسبقًا.

<div dir="ltr">

```bash
python3 scripts/verify-freerdp-runtime.py --mode build /absolute/path/to/verified/output
```

</div>

ثم أعد استخدامه عبر مدخل المثبّت الموجود:

<div dir="ltr">

```bash
UURB_FREERDP_PREBUILT_DIR=/absolute/path/to/verified/output   ./install.sh
```

</div>

يجب أن تطابق النسخة الوصفة والملفات وبيانات منشأ الملف الحالي. تغيير الملف يتطلب إعادة تشغيل مدخل البناء والتحقق؛ تعديل الإيصال أو مجموع التحقق لا يعتمد ملفات أخرى. يفحص المثبّت النسخة المنقولة قبل تشغيل الخدمة.

## المدخلات والنتائج

تثبت FreeRDP/WinPR وSDL 3.2.28 وSDL_ttf وOpenH264 وFreeType وHarfBuzz وحزم OpenSSL/cJSON/uriparser. تُفحص الرقعة وبصمات MinGW والمترجم والأدوات قبل البناء. التغيير يتطلب وصفة مراجعة.

توحّد خرائط بادئات الملفات والماكرو وتصحيح الأخطاء المسارات. إعداد opaque في FreeRDP يبقى OFF من أول تهيئة، وDLL التوافق له اسم إخراج نسبي؛ لا تُضمّن مسارات الجهاز.

جذران مختلفان للمصدر والإخراج أنتجا البايتات نفسها لكل الملفات الـ13. تهيئة CMake الأولى والمتكررة أعطتا البيانات نفسها. بناء كامل نظيف دون إخراج مسبق استغرق نحو700 ثانية ضمن900 واجتاز فحص التشغيل والمنشأ. راجع [الجودة](quality-guide.md) و[التكلفة](performance-evidence.md).

</div>
