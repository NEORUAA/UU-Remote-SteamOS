<div dir="rtl">

[English](../CONTRIBUTING.md) · [العربية](CONTRIBUTING.ar.md) · [Deutsch](CONTRIBUTING.de.md) · [Español](CONTRIBUTING.es.md) · [Français](CONTRIBUTING.fr.md) · [日本語](CONTRIBUTING.ja.md) · [한국어](CONTRIBUTING.ko.md) · [Русский](CONTRIBUTING.ru.md) · [Tiếng Việt](CONTRIBUTING.vi.md) · [简体中文](CONTRIBUTING.zh-Hans.md) · [繁體中文](CONTRIBUTING.zh-Hant.md)

[العربية · UU Remote Ubuntu Plus](README.ar.md)

# المساهمة في UU Remote Ubuntu Plus

نرحب بتقارير المشاكل والترجمة والتوثيق والكود. احتفظ بحقوق النشر وترخيص MIT لـ[جسر Lachlan Chen](https://github.com/lachlanchen/uu-remote-ubuntu-bridge).

## وصف المشكلة والمسار

اذكر Ubuntu/GNOME/Wine/UU وحجم الصورة ومسار الإدخال وخطوات التكرار. ميّز Ubuntu المضيف والإدارة المحلية وUbuntu المتحكم. قدّم تغييرات صغيرة وطريقة القياس، واستخدم [نموذج التوافق](https://github.com/llmir/uu-remote-ubuntu-plus/issues/new?template=compatibility.yml).

## بيئة التطوير

استخدم Ubuntu وPython النظام. الحزم للبناء والاختبارات المعزولة، ويدير install.sh التشغيل. اختر المترجم عبر WINEGCC/MINGW_CC/HOST_CC دون مسارات شخصية، واستخدم Wine وXvfb مؤقتين.

<div dir="ltr" align="left">

```bash
sudo apt-get update
sudo apt-get install --no-install-recommends \
  build-essential binutils gcc-mingw-w64-x86-64-win32 \
  wine wine64 wine64-tools xvfb x11-utils x11-xserver-utils xclip xcompmgr
```

</div>

## فحص المصدر

نفّذ bash -n للـshell المعدّل ثم الفحوص التالية. احتفظ بتحذيرات C الصارمة. قد تحتاج الاختبارات Wine/Xvfb/systemd؛ اذكر المتجاوزة. UURB_TEST_SYSTEMD=1 فقط مع ناقل مستخدم عامل.

<div dir="ltr" align="left">

```bash
python3 -m compileall -q scripts tests
python3 -m unittest discover -s tests -v
./scripts/build-compat.sh
git diff --check
```

</div>

## التوثيق والرسوم

نفّذ اختبارات التوثيق الحالية. تشترك SVG الإنجليزية والصينية في التصميم؛ أوامر Node/Sharp الأخيرة لإعادة الرسم عند الحاجة فقط. افحص الصورة والبيانات الوصفية كاملة، واحتفظ برموز الدفع الأصلية.

<div dir="ltr" align="left">

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_documentation.py -q
npm install --no-save --package-lock=false sharp
node scripts/render-doc-graphics.cjs
```

</div>

## التحقق من التثبيت

ثبّت على مضيف مصرح به وجهّز اتصال استعادة للانقطاع القصير. يتضمن الفحص الكامل 270 ثانية استقرار؛ جرّب الصورة والإدخال وإعادة الاتصال بمتحكم حقيقي. أوقف بيئة UU وحدها.

<div dir="ltr" align="left">

```bash
./install.sh --skip-packages --skip-account-login
./scripts/verify.sh --quick
./scripts/verify.sh
./uninstall.sh --dry-run
```

</div>

## إصدارات UU الجديدة

تحتاج قائمة معتمدة وSHA-256 كاملة وتفسير التغييرات متساوية الطول. وثّق الاستعادة الدقيقة والبدء والإدخال والإزالة. لا تنشر ملفات احتكارية أو سجلات خاصة. انظر [صيانة الأصل (English)](../docs/upstream-maintenance.md).

## الملفات العامة

راجع القائمة والاختلافات المرحلية. استبعد البناء والبيئات والمخبأ وحالة .omc والاعتمادات ومعرفات الأجهزة والنص. احتفظ بالمصادقة وTLS وفحص القوائم والإزالة القابلة للعكس.

<div dir="ltr" align="left">

```bash
git status --short
git diff --cached
```

</div>

## المراجعة

اشرح المشكلة والنتيجة والفحوص المنفذة واطلب مراجعة مستقلة. FPS المضبوطة ليست قياساً. اقرأ [الجودة](../docs/i18n/ar/quality-guide.md) و[Ubuntu](../docs/i18n/ar/ubuntu-26.04-port.md) و[الأمان](../docs/i18n/ar/security.md)، واحتفظ بـMIT وحقوق النشر.

</div>
