الشرح الأصلي على LinkedIn كان عن ربط خدمة Cohere مع Oracle APEX App Builder. البداية العملية هي تعريف خدمة داخل الـWorkspace: تختار المزوّد والرابط والموديل وبيانات الاتصال، وبعدها تطلب من المساعد دعمك في كتابة الكود.

## أنشئ خدمة داخل الـWorkspace

في APEX 26.2 افتح **App Builder → Workspace Utilities → All Workspace Utilities → Generative AI**. أنشئ خدمة، واختر **Cohere**، وحدّد اسمًا واضحًا وStatic ID. أسماء القوائم قد تختلف حسب إصدار APEX. توضح Oracle [خطوات الإعداد](https://docs.oracle.com/en/database/oracle/apex/26.2/apxdc/configuring-generative-ai-service.html).

المثال التالي لتوضيح الإعدادات، وليس ملف استيراد أو سكربت قابلًا للتنفيذ:

```text
Name: Cohere Development Assistant
Static ID: COHERE_DEV_ASSISTANT
AI Provider: Cohere
Used by App Builder: On
Default for New Apps: Off (enable if required)
Base URL: https://api.cohere.ai/v2
AI Model: command-r-08-2024
Credential: a workspace Web Credential
```

الرابط والموديل هنا من المثال الأصلي. تأكد أن إصدار APEX المثبّت يدعم الرابط، وأن حسابك عند المزوّد يتيح الموديل المطلوب. راجع [قائمة موديلات Cohere الحالية](https://docs.cohere.com/docs/models)، لأن الإتاحة قد تختلف بين منصات الاستضافة.

## افصل بين الاختيارين

**Used by App Builder** يتيح الخدمة لخصائص بيئة التطوير. أما **Default for New Apps** فيختار الخدمة الافتراضية للتطبيقات الجديدة. قرّر كل إعداد بشكل مستقل لأن لكل واحد وظيفة مختلفة. راجع [مرجع خصائص الخدمة لدى Oracle](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/editing-a-generative-as-service.html).

اختر أو أنشئ Web Credential داخل APEX. احتفظ بمفتاح API بعيدًا عن JavaScript والصور والمقالات والمستودعات. توثّق Oracle [حفظ بيانات الاتصال وإعدادات التشغيل](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/creating-generative-ai-service-objects.html)، ومنها حدود التوكنز والمهلة الزمنية.

## اختبر بطلب صغير يمكن مراجعته

شغّل **Test Connection** قبل الحفظ، ثم جرّب طلبًا بأسماء جداول افتراضية:

```text
لدي جدول افتراضي demo_orders(order_id, customer_id, amount).
اكتب استعلام SQL للقراءة فقط يعرض إجمالي amount لكل customer_id.
اشرح تعامل SUM مع قيم amount الفارغة. لا تخترع أعمدة ولا تنفّذ الاستعلام.
```

راجع SQL المقترح وافتراضاته وتعامله مع القيم الفارغة وقواعد الوصول قبل استخدامه. نجاح الاتصال يثبت الوصول للخدمة، وتظل الإجابة المولّدة محتاجة مراجعة فنية. استخدم أمثلة افتراضية أثناء التقييم، وحدّد بوضوح معلومات التطبيق المسموح بإرسالها للمزوّد الخارجي.
