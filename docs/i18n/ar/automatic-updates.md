[English](../../automatic-updates.md) · [العربية](../ar/automatic-updates.md) · [Español](../es/automatic-updates.md) · [Français](../fr/automatic-updates.md) · [日本語](../ja/automatic-updates.md) · [한국어](../ko/automatic-updates.md) · [Tiếng Việt](../vi/automatic-updates.md) · [中文（简体）](../zh-Hans/automatic-updates.md) · [中文（繁體）](../zh-Hant/automatic-updates.md) · [Deutsch](../de/automatic-updates.md) · [Русский](../ru/automatic-updates.md)

<div dir="rtl">

[← العودة إلى الصفحة العربية](../../../i18n/README.ar.md)

# فحوص تلقائية وإصلاح قابل للاستئناف

تفصل الصيانة بين المراقبة وإصلاح المصدر الخاص وpromotion الحية المقبولة صراحة. لا يقطع الفحص المعتاد ترحيلاً يعمل.

## الإعداد والمؤقتات

يبدأ Plus تاريخ إصداراته المستقل بالوسم `v0.1.0`. وسوم مسارات الإدخال المؤرخة جزء من تاريخ المشروع الأصلي، وليست موجودة في هذا المستودع المستقل. التثبيت العادي لا يحتاج إليها. بعد توفر وسم Plus محلياً، حدده صراحةً باستخدام `--track v0.1.0 --branch main`؛ فما زال الإعداد الافتراضي يختار وسوماً قديمة ويرفض الوسم المفقود.

بعد الانتقال إلى وسم الإصدار، نفّذ `git switch main` قبل أوامر الترقية التي تجلب المصدر. المصدر المتابع هو `origin/main` ووسم إعادة التثبيت المحدد هو `v0.1.0`. للإبقاء عمداً على نسخة المصدر المحددة بالوسم أثناء الترقية، استخدم `--no-pull`.

`--auto-promote-accepted` إلا بإصدارات لاحقة يقبلها maintainer وتربطها hashes، وليس مسودة Codex. يحفظ `updater.json` النموذج وreasoning ومسار Codex المطلق؛ يجب تسجيل دخول المستخدم نفسه. يجب أن تكون كل نوافذ الاستخدام المشمول دون الحد الافتراضي 20%؛ تعذر التحقق يؤجل ساعة على الأقل.

يعمل `uu-remote-update-check.timer` قرب 04:20 يومياً مع تأخير عشوائي وبعد الإقلاع بـ12 دقيقة؛ يعوض `Persistent=true` فحصاً فائتاً. يبدأ monitor بعد سبع دقائق، ثم بعد 15 دقيقة من التشغيل السابق.

## المراقبة والإصلاح

يتبع checker تحويل HEAD الرسمي ويحذف query keys المؤقتة ويقارن الإصدار كاملاً. يمنع ETag والحجم وhash-sidecar تكرار تنزيل الملفات نفسها. الإصدار الأقدم ليس تحديثاً. يسجل فشلان يفصل بينهما 20 ثانية evidence وtask دون إيقاف Wine/RDP/UU. وحده الخيار المنفصل `--auto-reinstall` يسمح بالاستعادة.

حد التنزيل 1 GiB. تُفك hashes المجهولة ساكناً وتُحلل داخل clone خاص مع نسخة عقد `0600`. يتطلب wrapper غير القابل للاستخراج staging صريحاً بلا شبكة. لا يمكن لـ Codex استخدام sudo أو تعديل live-prefix أو push أو اعتماد تفسيره الثنائي.

## Promotion المقبولة

يجب تطابق hash الرسمي وبيان `approved` وacceptance schema-1 وevidence في commit واحد مجلوب من `origin/main`، مع ربط hashes installer/server المعدل. تشمل الاختبارات prefix مؤقتاً وعميل التحكم وإعادة الاتصال والإقلاع البارد وإعادة خدمة وsignaling جديداً والحفاظ على الحساب؛ الاستقرار 270–1800 ثانية. يلزم تمكين auto-promotion وهدوء UU عادة 45 دقيقة.

توقف خدمة الجسر وحدها. تُنسخ كل البيئة مع 1 GiB احتياط، ويثبت داخلها وتُقارن بيانات الحساب بدقة ثم ينتظر room جديد وفحصان runtime. لا يتغير XRDP. يجب أن يكون state وprefix على filesystem واحد. يعيد الفشل أو reboot أو الانقطاع القديم، ويحفظ snapshot ويمنع إعادة تلقائية. يتجاوز `--now` انتظار الخمول فقط.

## المهام والخصوصية وsandbox

يُحفظ UUID عند `thread.started` لاستعمال `codex exec resume`؛ دون UUID يبدأ thread جديد من السياق نفسه. يزيد retry من 15 دقيقة إلى 24 ساعة. تُختبر نتائج schema مستقلاً: `ready-for-review` و`no-change` و`blocked`؛ حالات promotion: `promotion-waiting-idle` و`promotion-running` و`promoted` و`promotion-blocked`.

الدلائل الخاصة `0700` والملفات `0600`، وpush clone معطل، وCodex workspace-write/never والخدمة `NoNewPrivileges=yes`؛ لا تزال المصادقة تحتاج شبكة. في Ubuntu 24.04 يجب ألا تعطل mount namespace لخدمة المستخدم Bubblewrap المتداخل. عند `codex-sandbox-deferred` ثبّت profile AppArmor الخاص بالتوزيعة بالأوامر التالية، دون تخفيف عالمي. يحافظ `retry` على evidence/checkout ويستبدل thread المعطوب، ولا يستورد staging إلا مع hashes installer/server/healthd المطابقة.

يبقي `disable` الأدلة؛ يحذف `disable --purge-state` الإعدادات والحالة الخاصة أيضاً. انقل المصادر فقط إلى جهاز آخر واختر ملف إدخاله الخاص.

[الترقية](reusable-upgrade.md) · [الأمان](security.md)

## الأوامر والقيم التقنية

<div dir="ltr" align="left">

```bash
git switch main
git fetch --tags origin
./scripts/configure-updater.sh enable \
  --track v0.1.0 --branch main \
  --model codex-auto-review --reasoning-effort medium \
  --auto-promote-accepted
uu-remote update
systemctl --user list-timers --all \
  uu-remote-update-check.timer uu-remote-repair-monitor.timer
journalctl --user -u uu-remote-update-check.service -n 100 --no-pager
journalctl --user -u uu-remote-repair-monitor.service -n 100 --no-pager
uu-remote upgrade apply --now
```

</div>

<div dir="ltr" align="left">

```bash
sudo apt install apparmor-profiles
sudo install -o root -g root -m 0644 \
  /usr/share/apparmor/extra-profiles/bwrap-userns-restrict \
  /etc/apparmor.d/bwrap-userns-restrict
sudo apparmor_parser -r /etc/apparmor.d/bwrap-userns-restrict
uu-remote update retry
systemd-run --user --wait --pipe --collect \
  --property=NoNewPrivileges=yes \
  /usr/bin/bwrap --die-with-parent --unshare-user --uid 0 --gid 0 \
  --ro-bind / / /bin/true
systemctl --user cat uu-remote-repair-monitor.service
./scripts/configure-updater.sh status
./scripts/configure-updater.sh disable
./scripts/configure-updater.sh disable --purge-state
```

</div>

## المصدر والموضوعات المرتبطة


تتوفر التفاصيل الهندسية بالإنجليزية والصينية المبسطة:

- [automated-repair-agent-handoff](../../automated-repair-agent-handoff.md) · [简体中文](../zh-Hans/automated-repair-agent-handoff.md)
- [release-tracks](../../release-tracks.md) · [简体中文](../zh-Hans/release-tracks.md)
- [upstream-maintenance](../../upstream-maintenance.md) · [简体中文](../zh-Hans/upstream-maintenance.md)

</div>
