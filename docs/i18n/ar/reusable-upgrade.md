[English](../../reusable-upgrade.md) · [العربية](../ar/reusable-upgrade.md) · [Español](../es/reusable-upgrade.md) · [Français](../fr/reusable-upgrade.md) · [日本語](../ja/reusable-upgrade.md) · [한국어](../ko/reusable-upgrade.md) · [Tiếng Việt](../vi/reusable-upgrade.md) · [中文（简体）](../zh-Hans/reusable-upgrade.md) · [中文（繁體）](../zh-Hant/reusable-upgrade.md) · [Deutsch](../de/reusable-upgrade.md) · [Русский](../ru/reusable-upgrade.md)

<div dir="rtl">

[← العودة إلى الصفحة العربية](../../../i18n/README.ar.md)

# ترقية قابلة للتكرار تحافظ على تسجيل الدخول

يجمع `uu-remote-upgrade` و`uu-remote upgrade` تحديث المستودع وpromotion المقبولة وتجديد الجسر والفحص. يعرض `status` الحالة، ويفحص `check` دون تغيير المنتج، وينتظر `apply` الخمول. يتجاوز `apply --now` انتظار النشاط فقط ولا يفرض ملفاً مجهولاً أو غير مقبول.


بعد الانتقال إلى وسم الإصدار، نفّذ `git switch main` قبل أوامر الترقية التي تجلب المصدر. المصدر المتابع هو `origin/main` ووسم إعادة التثبيت المحدد هو `v0.1.0`. للإبقاء عمداً على نسخة المصدر المحددة بالوسم أثناء الترقية، استخدم `--no-pull`.

## المعاملة

يجب أن يكون checkout نظيفاً وغير detached. لا يدمج fetch/fast-forward تاريخاً متفرعاً؛ يعاد تشغيل السكربت عند تغير المصدر. تجري tests وshell parser قبل التغيير. يُفحص المنتج الموافق عليه والترحيل والمسار والتوقيت وعلامات الحساب. لا يستمر إلا installer رسمي تطابق بصمته وacceptance البيان.

تنسخ promotion كامل Wine prefix، وتثبت في المكان نفسه وتطبق الرقع وتقارن login registry وشجرتي الحساب بايتاً ببايت. يلي ذلك فحصان runtime يفصل بينهما الاستقرار. يُحفظ runtime الجسر منفصلاً ثم تُحدث helpers/service مع الحفاظ على environment وtrack وإعدادات Codex. يُستعلم XRDP فقط، ويؤدي تغير حالته النشطة إلى فشل العملية.

## الاستعادة والإدخال

يعيد الفشل أو الانقطاع كامل prefix ويسجل `promotion-blocked` دون تكرار تلقائي. إعادة صف الإصدار المقبول نفسه صراحة تتطلب commit مختلفاً لأداة promotion؛ تحفظ المهام السابقة في `tasks/retired/`. إذا فشل تجديد المصدر يستعاد runtime المحفوظ بعد promotion. لا تحذف timers النسخ الاحتياطية.

قيم X11 المثال ليست للنسخ إلى جهاز آخر؛ إعداد ذلك الجهاز هو المرجع. لا يكتب quick verifier في تطبيقك؛ افحص بعد التحديث نص الهاتف والمفاتيح السريعة وحركة الفأرة والنقر والسحب والعجلة.

يتجنب bus الدائم `/run/user/UID/bus` سؤال user manager مختلف من طرفية متداخلة. واقعة 4.34 التاريخية في يوليو 2026 ليست حالة Plus 4.42 الحالية. شملت إصلاحاتها verifier مفقوداً وtimestamps PE وسباق readiness؛ ينتظر الفحص الحالي listener الفعلي والمساعد المختار حتى 45 ثانية. انقل المصدر فقط إلى الجهاز الآخر، لا prefix أو keyring أو state الخاص. يجب وجود `~/.local/bin` في `PATH`.

[التحديث التلقائي](automatic-updates.md) · [لوحة المفاتيح](adaptive-keyboard-relays.md)

## الأوامر والقيم التقنية

<div dir="ltr" align="left">

```bash
uu-remote-upgrade status
uu-remote upgrade status
uu-remote upgrade check
uu-remote upgrade apply
uu-remote upgrade apply --now
./scripts/upgrade-uu-remote.sh apply --now
```

</div>

<div dir="ltr" align="left">

```text
UURB_TEXT_KEY_DELAY_MS=8
UURB_PHYSICAL_KEY_DELAY_MS=0
UURB_KEYBOARD_ROUTE=x11
UURB_NETWORK_INTERFACE=default
unix:path=/run/user/UID/bus
~/.local/state/uu-remote-updater/tasks/*/promotion/snapshot-prefix
~/.local/state/uu-remote-upgrader/transactions/TIMESTAMP/
~/.local/state/uu-remote-upgrader/latest
```

</div>

<div dir="ltr" align="left">

```bash
git status --short
git switch main
git pull --ff-only origin main
./install.sh --skip-packages --skip-account-login
./scripts/configure-updater.sh enable --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
./scripts/upgrade-uu-remote.sh check
```

</div>

## المصدر والموضوعات المرتبطة


تتوفر التفاصيل الهندسية بالإنجليزية والصينية المبسطة:

- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)

</div>
