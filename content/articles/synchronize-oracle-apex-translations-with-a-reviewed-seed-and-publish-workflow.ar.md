بوستي على LinkedIn كان عن استخدام APEX Automations للحفاظ على تزامن الترجمات أثناء التطوير. مسار العمل القابل للتكرار له ثلاث مراحل: تجميع النصوص المتغيرة، ومراجعة الترجمة، ونشر نسخة اللغة بعد تحديثها.

## جهّز ترجمة التطبيق

للتطبيق الذي يستخدم طريقة Application-Based، عرّف ربط اللغة المطلوبة من Shared Components → Globalization → Application Translations. الربط وسياق الـWorkspace لازم يكونوا موجودين قبل استخدام الـAPIs التالية. توضح Oracle مسار الترجمة كاملًا. [ترجمة التطبيق](https://docs.oracle.com/en/database/oracle/apex/26.1/htmdb/creating-an-application-based-translation.html)

استخدم معرّف تطبيق التطوير وكود اللغة اللذين اخترتهما. المعرّف `12345` واللغة `ar` في الأمثلة للتوضيح. نفّذ كل مرحلة بشكل مستقل داخل سياق الـWorkspace الصحيح.

## اجمع النصوص المتغيرة

عملية Seeding تحدّث مستودع الترجمة بالنصوص القابلة للترجمة من التطبيق الأساسي. بعد تغيير عنوان صفحة أو اسم عنصر أو مكوّن آخر قابل للترجمة، شغّلها لربط اللغة المطلوب.

```sql
begin
    apex_lang.seed_translations(
        p_application_id => 12345,
        p_language       => 'ar'
    );
    commit;
end;
```

صدّر النصوص المتغيرة إلى XLIFF، وحدّث النصوص المترجمة، وطبّق الملف بعد مراجعته. راجع عمل الترجمة الموجود والنصوص الجديدة قبل النشر. يوضّح مرجع الـAPI كيفية مزامنة المستودع التي ينفذها الاستدعاء. [SEED_TRANSLATIONS](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/SEED_TRANSLATIONS-Procedure.html)

## انشر نسخة اللغة بعد المراجعة

بعد تطبيق تغييرات الترجمة، انشر التطبيق الأساسي نفسه مع ربط اللغة المطلوب.

```sql
begin
    apex_lang.publish_application(
        p_application_id => 12345,
        p_language       => 'ar'
    );
    commit;
end;
```

النشر يبني نسخة التطبيق المترجمة بدمج تعريف التطبيق الأساسي مع النصوص المترجمة في المستودع. شغّل التطبيق باللغة المستهدفة وراجع الصفحات المتغيرة. [PUBLISH_APPLICATION](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/PUBLISH_APPLICATION-Procedure.html)

## أتمت تجهيز الترجمة في التطوير

APEX Automation تقدر تشغّل إجراء Seeding بعد أن يحدّد مسار التطوير تغييرًا معتمدًا للمزامنة. حدّد التطبيق واللغة بوضوح، واضبط صلاحية تشغيل المزامنة، وسجّل المرحلة ووقت البداية والمدة والنتيجة. استخدم Automation Execution Log لفحص الأخطاء. اختبر التشغيل عند الطلب قبل تفعيل الجدول. [إنشاء Automation](https://docs.oracle.com/en/database/oracle/apex/26.1/htmdb/creating-an-automation.html)

اربط النشر بإجراء إصدار منفصل بعد المراجعة. لاختبار القبول، غيّر اسم عنصر واحد، وشغّل Seeding، وطبّق ترجمته، ثم انشر وتأكد من ظهور النص المتوقع في صفحة اللغة المستهدفة. راجع أيضًا نصًا لم يُترجم، واللغة المحددة، واتجاه الواجهة عند استهداف العربية.

[البوست الأصلي على LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7456820271790952448/)
