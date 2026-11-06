شاشة الـDashboard وملف Excel ممكن يخدموا ناس مختلفة. الشاشة قد تعرض إجمالي الطلبات بالشهر، بينما المراجع محتاج صفًا لكل طلب. استعلام مخصص للتصدير يخلّيك تحدد أعمدة الملف وترتيبها وقواعدها من غير إضافة Report Region ثانية للصفحة.

## جهّز الملف من استعلام

داخل تطبيق APEX للتطوير، اعمل زر يرسل الصفحة، وأضف Page Process بلغة PL/SQL يشتغل عند الضغط على الزر ده فقط. افصل طلب التنزيل عن العمليات اللي بتحفظ أو تعدّل البيانات. المثال يستخدم طلبين افتراضيين من `DUAL`، فمش محتاج جداول تطبيق.

```sql
declare
    l_query apex_exec.t_context;
    l_file  apex_data_export.t_export;
begin
    l_query := apex_exec.open_query_context(
        p_location => apex_exec.c_location_local_db,
        p_sql_query => q'[
            select 1001 as order_id, date '2026-01-15' as order_date,
                   125.50 as order_total
            from dual
            union all
            select 1002, date '2026-01-16', 78.00
            from dual
            order by order_id
        ]'
    );
    begin
        l_file := apex_data_export.export(
            p_context   => l_query,
            p_format    => apex_data_export.c_format_xlsx,
            p_file_name => 'sample-orders'
        );
    exception
        when others then
            apex_exec.close(l_query);
            raise;
    end;
    apex_exec.close(l_query);
    apex_data_export.download(p_export => l_file);
end;
```

الـQuery Context يوفّر الصفوف بأنواع بياناتها. الدالة `APEX_DATA_EXPORT.EXPORT` تجهّز محتوى XLSX، والإجراء `DOWNLOAD` يرسله في الاستجابة. اقفل الـContext قبل استدعاء `DOWNLOAD`، لأن التنزيل بيوقف محرك APEX بالإعداد الافتراضي. معالجة الخطأ الداخلية تحرّر الـContext لو تجهيز الملف فشل، من غير ما تتدخل في الإنهاء الطبيعي للتنزيل. راجع مراجع Oracle عن [EXPORT](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/APEX_DATA_EXPORT-EXPORT-Function.html) و[DOWNLOAD](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/APEX_DATA_EXPORT-DOWNLOAD-Procedure.html) و[إغلاق الـQuery Context](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/APEX_EXEC.CLOSE-Procedure.html).

## حدّد ما يقدر المستخدم يصدّره

- **النطاق:** الاستعلام المستقل مش بياخد تلقائيًا فلاتر الـInteractive Report وقت التشغيل. لو الملف يتبع فلاتر الصفحة، مرّر القيم بعد التحقق منها باستخدام Bind Variables. ولو المطلوب نفس عرض التقرير الحالي، فكّر في التنزيل المدمج في التقرير.
- **الصلاحيات:** طبّق صلاحية على الـPage Process، وطبّق قواعد الوصول للصفوف داخل الاستعلام. اختار الأعمدة المسموح بإرسالها في الملف فقط؛ إخفاء عمود في الواجهة لا يمنع تصديره.
- **الاستجابة:** استخدم طلبًا يتوقّع ملفًا. لو عندك Callback والـJavaScript مستني JSON، هتحتاج مسار تنزيل مختلف.

## اختبر الملف اللي هيوصل للمراجع

ابدأ بالصفّين الافتراضيين، وراجع اسم الملف وترتيب الأعمدة وإن الإجماليات أرقام. في بيئة تطوير مصرح لك باستخدامها، اختبر نتيجة فارغة، وفلتر يضيّق النتائج، ومستخدمين بصلاحيات مختلفة. قارن محتويات الملف بقواعد التصدير المطلوبة، بما فيها أي حد لعدد الصفوف، قبل إتاحة الزر للمستخدمين.

[البوست الأصلي على LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7519513038740262912/)
