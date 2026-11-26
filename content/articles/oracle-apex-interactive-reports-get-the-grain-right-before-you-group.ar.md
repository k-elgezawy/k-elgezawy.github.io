التقرير التفاعلي يقدر يجاوب على أكثر من سؤال عمل بدون ما يتحوّل لصفحات منفصلة. البوست الأصلي على LinkedIn قارن بين Control Break وGroup By وPivot. لكن البداية المهمة تسبق اختيار أي واحدة منها: **الصف الواحد في مصدر البيانات يمثّل إيه؟**

دي تجربة تقارير صغيرة قابلة لإعادة البناء، فيها إجماليات متوقعة وفخ في الربط ممكن ينتج ملخصًا مقنعًا لكنه غلط. الأسماء والمبالغ كلها افتراضية؛ الاستعلامات تقرأ ثوابت من `DUAL` ولا تغيّر بيانات العمل.

## ابدأ بصف واحد لكل فاتورة

داخل تطبيق تطوير، أنشئ Interactive Report region بالاستعلام التالي كمصدر SQL:

```sql
WITH invoices(invoice_id, branch, invoice_date, sales, cost) AS (
    SELECT 1001, 'North', DATE '2026-01-05', 120, 80 FROM dual UNION ALL
    SELECT 1002, 'North', DATE '2026-01-15',  80, 60 FROM dual UNION ALL
    SELECT 1003, 'South', DATE '2026-01-20', 150,110 FROM dual UNION ALL
    SELECT 1004, 'North', DATE '2026-02-05', 100, 70 FROM dual UNION ALL
    SELECT 1005, 'South', DATE '2026-02-12', 130, 90 FROM dual UNION ALL
    SELECT 1006, 'South', DATE '2026-02-20',  70, 40 FROM dual
)
SELECT invoice_id,
       branch,
       invoice_date,
       TO_CHAR(invoice_date, 'YYYY-MM') AS month_label,
       sales,
       cost,
       sales - cost AS margin
FROM invoices
```

صفوف المصدر الستة تمثّل ست فواتير كاملة. `MARGIN` مبلغ، وليس نسبة مئوية. نفترض عملة واحدة وكل التكاليف معروفة. التقرير الحقيقي يحتاج قواعد صريحة لتحويل العملات والمرتجعات والتكاليف المفقودة قبل أن تكون إجمالياته ذات معنى.

احتفظ بالأعمدة الرقمية كأرقام، وطبّق تنسيق العرض من خصائص الأعمدة. استخدم `MONTH_LABEL` لاختيار الشهر في التجربة. وجود السنة يمنع جمع يناير من سنوات مختلفة مع بعضه. [Oracle: خصائص أعمدة التقرير](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/managing-interactive-report-column-attributes.html)

في خصائص Actions Menu للمنطقة، فعّل Control Break وAggregate وGroup By وPivot وFilter وSave Report حسب الحاجة. المطور يتحكم في الإمكانيات المتاحة. [Oracle: إعداد قائمة Actions](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/customizing-the-interactive-report-actions-menu.html)

## اختَر العرض المناسب للسؤال

**Control Break تجيب: أي فواتير تخص كل فرع؟** فعّل التجميع البصري على `BRANCH` مع الاحتفاظ بصفوف الفواتير التفصيلية. أضف Sum في Aggregate لأعمدة `SALES` و`COST` و`MARGIN`. المفروض تظل قادرًا على مراجعة الفواتير الست تحت عناوين الفروع. [Oracle: Control Break](https://docs.oracle.com/en/database/oracle/apex/26.1/aeeug/creating-control-break.html)

**Group By تجيب: كل فرع ساهم بكام؟** اختَر `BRANCH` كعمود التجميع، وSum للمبالغ الثلاثة، وCount على `INVOICE_ID` غير الفارغ. الملخص المتوقع:

| الفرع | عدد الفواتير | المبيعات | التكلفة | الهامش |
|---|---:|---:|---:|---:|
| North | 3 | 300 | 210 | 90 |
| South | 3 | 350 | 240 | 110 |

العدد هنا يعني فواتير لأن صف المصدر يمثّل فاتورة واحدة. المعنى يتغيّر لو الاستعلام يرجع بنود الفاتورة. [Oracle: Group By](https://docs.oracle.com/en/database/oracle/apex/26.1/aeeug/grouping-columns.html)

**Pivot تجيب: مبيعات الفروع تتقارن إزاي عبر الشهور؟** اختَر `BRANCH` لصفوف المقارنة، و`MONTH_LABEL` لعمود الـPivot، والدالة Sum على `SALES`. الخلايا المتوقعة:

| الفرع | 2026-01 | 2026-02 |
|---|---:|---:|
| North | 200 | 100 |
| South | 150 | 200 |

الـPivot تغيّر ترتيب العرض للمقارنة، لكنها لا تصلح مبالغ مكررة في المصدر. [Oracle: تقارير Pivot](https://docs.oracle.com/en/database/oracle/apex/26.1/aeeug/managing-pivot-reports.html)

خطوات دليل المستخدم المشار إليه تخص 26.1، وإعدادات المطور تخص 26.2. تجربة التقارير اتحدثت في 26.2، فاستخدم أسماء العمليات وراجع ترتيب الواجهة في إصدارك. [Oracle: تغييرات تقارير 26.2](https://blogs.oracle.com/apex/whats-new-in-interactive-reports-and-ai-interactive-reports)

## طابق الإجماليات بعد تغيير الفلاتر

بدون فلاتر، الفواتير الست مجموعها مبيعات 650 وتكلفة 450 وهامش 200. فلترة `MONTH_LABEL` على `2026-02` المفروض تترك ثلاث فواتير، بمبيعات 300 وتكلفة 200 وهامش 100. التنقل بين التفاصيل والتجميع والـPivot لازم يحافظ على مجموعة البيانات المفلترة المقصودة.

احفظ عرضًا خاصًا باسم «مراجعة الفروع في فبراير» لو الخيار متاح للمستخدم المسجل. اعتبره تعريف تقرير محفوظًا، وليس نسخة تاريخية من السجلات نفسها. امسح أو أعد ضبط الفلتر بشكل مقصود قبل مراجعة إجماليات كل الشهور. فلتر غير ملحوظ ممكن يجعل ملخصين صحيحين يبدوان متعارضين.

## الربط ممكن يفسد كل العروض مرة واحدة

المثال المنفصل ده فيه فاتورتان، كل واحدة بقيمة 100، والفاتورة الأولى لها بندان. توقّع الإجماليات قبل تشغيل الاستعلام الذي يقرأ فقط:

```sql
WITH invoices(invoice_id, invoice_total) AS (
    SELECT 1, 100 FROM dual UNION ALL
    SELECT 2, 100 FROM dual
), invoice_lines(invoice_id, line_id) AS (
    SELECT 1, 11 FROM dual UNION ALL
    SELECT 1, 12 FROM dual UNION ALL
    SELECT 2, 21 FROM dual
)
SELECT SUM(i.invoice_total) AS repeated_total,
       SUM(DISTINCT i.invoice_total) AS distinct_amount_total,
       COUNT(DISTINCT i.invoice_id) AS invoice_count
FROM invoices i
JOIN invoice_lines l ON l.invoice_id = i.invoice_id
```

الناتج المتوقع هو `REPEATED_TOTAL = 300` و`DISTINCT_AMOUNT_TOTAL = 100` و`INVOICE_COUNT = 2`. إجمالي الفواتير الصحيح 200.

الربط يكرّر مبلغ رأس الفاتورة الأولى. واستخدام `SUM(DISTINCT invoice_total)` يفشل أيضًا: يزيل المبالغ المتساوية، وليس تكرار هوية الفاتورة. ممكن عدد الفواتير المختلفة يكون صحيحًا بينما مجموع الأموال غلط. توثّق Oracle إن `DISTINCT` داخل التجميع يعمل على القيم المختلفة للمعامل. [Oracle: قواعد التجميع](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Aggregate-Functions.html)

احتفظ بمبالغ الفواتير على مستوى الفاتورة. لو البنود مطلوبة فقط لاختيار الفواتير المؤهلة، فكّر في فلتر `EXISTS`. ولو محتاج مقاييس البنود، جمّعها للمستوى المطلوب قبل الربط. بعد كده طابق المفاتيح والمبالغ مع مجموعة بيانات معروفة.

أنشئ صفحة جديدة عندما يختلف سؤال العمل أو الصلاحيات أو عقد البيانات فعلًا. أما طرق التحليل المختلفة لنفس الصفوف المسموح بها، فابدأ بصحة مستوى المصدر ثم اختَر عرض التقرير. نواتج SQL المذكورة قيم متوقعة راجعنا حساباتها، وليست ادعاء بتنفيذها داخل تطبيق APEX الخاص بك.

[البوست الأصلي على LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7517515074228383744/)
