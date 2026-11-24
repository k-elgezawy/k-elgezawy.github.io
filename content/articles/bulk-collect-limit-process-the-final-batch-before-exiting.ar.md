ممكن مهمة معالجة على دفعات تنتهي بدون Exception، وفي هدوء تتجاوز آخر سجلاتها. البوست الأصلي على LinkedIn شرح سببًا من الأسباب: فحص `%NOTFOUND` للمؤشر قبل استخدام الصفوف التي رجعت في آخر عملية جلب.

السؤال المفيد أثناء المراجعة بسيط: **هل عالجنا الـCollection الحالية قبل ما نقرر إن المؤشر انتهى؟** الشرح ده يجعل الإجابة قابلة للملاحظة بأرقام تعريف افتراضية وعدّاد ومجموع للتحقق.

## آخر عملية جلب ممكن يكون فيها شغل

لو عندك 1,075 صفًا وحد الجلب 500، فالمجموعات المفيدة تكون 500 و500 و75. الخروج المبكر ممكن يتجاهل المجموعة الأخيرة. دليل التطوير من Oracle يشرح لماذا شرط الخروج المبني على العدّاد يتجنب المشكلة. [Oracle Database Development Guide](https://docs.oracle.com/en/database/oracle/oracle-database/26/adfns/database-development-guide.pdf)

المشكلة في الترتيب التالي:

```sql
FETCH c_orders BULK COLLECT INTO l_ids LIMIT 500;
EXIT WHEN c_orders%NOTFOUND;
-- Work on l_ids would happen too late here.
```

استخدام `%NOTFOUND` نفسه مش ممنوع. مثال Oracle للجلب على دفعات يعالج الـCollection ثم يفحص الخاصية بعدها. هنا هنختار بدلًا من ذلك الخروج عندما تكون الـCollection فارغة، قبل معالجتها. [Oracle: أمثلة الجلب على دفعات](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/bulk-sql-and-bulk-binding.html)

## تجربة كاملة بدون جداول العمل

شغّل البلوك التالي في جلسة تطوير مع تفعيل DBMS Output. يقرأ أرقامًا مولّدة من `DUAL`؛ لا ينشئ جداول ولا يغيّر بيانات العمل. دي تجربة توضيحية بنتائج متوقعة، وليست ادعاء بتنفيذها على قاعدة بياناتك.

المؤشر يولّد بحد أقصى 1,075 رقم تعريف، ثم يرشّحها. الفلتر الخارجي يجعل حالة الصفر صفوف واضحة. حجم الدفعة في كل الحالات 500.

```sql
DECLARE
    PROCEDURE check_case(p_rows PLS_INTEGER) IS
        CURSOR c_ids IS
            SELECT order_id
            FROM (
                SELECT LEVEL AS order_id
                FROM dual
                CONNECT BY LEVEL <= 1075
            )
            WHERE order_id <= p_rows
            ORDER BY order_id;
        TYPE id_list IS TABLE OF NUMBER;
        l_ids      id_list;
        l_seen     PLS_INTEGER := 0;
        l_sum      NUMBER := 0;
        l_expected NUMBER := p_rows * (p_rows + 1) / 2;
    BEGIN
        OPEN c_ids;
        LOOP
            FETCH c_ids BULK COLLECT INTO l_ids LIMIT 500;
            EXIT WHEN l_ids.COUNT = 0;
            IF p_rows = 1075 THEN
                DBMS_OUTPUT.PUT_LINE('batch=' || l_ids.COUNT);
            END IF;
            FOR i IN 1 .. l_ids.COUNT LOOP
                l_seen := l_seen + 1;
                l_sum := l_sum + l_ids(i);
            END LOOP;
        END LOOP;
        CLOSE c_ids;
        IF l_seen <> p_rows OR l_sum <> l_expected THEN
            RAISE_APPLICATION_ERROR(-20001, 'Count/checksum mismatch');
        END IF;
        DBMS_OUTPUT.PUT_LINE(
            'rows=' || p_rows || ', seen=' || l_seen || ', sum=' || l_sum
        );
    EXCEPTION
        WHEN OTHERS THEN
            IF c_ids%ISOPEN THEN
                CLOSE c_ids;
            END IF;
            RAISE;
    END;
BEGIN
    check_case(0);
    check_case(1);
    check_case(499);
    check_case(500);
    check_case(501);
    check_case(1000);
    check_case(1075);
END;
/
```

رجوع صفر صفوف في الجلب على دفعات هو نهاية طبيعية، وليس حالة `NO_DATA_FOUND` نحتاج اصطيادها. والجلب التالي يستبدل الدفعة السابقة. [Oracle: جملة FETCH](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/FETCH-statement.html)

## اختبر الحدود ثم تحقّق من هوية البيانات

القيم النهائية المتوقعة:

| عدد الصفوف المدخل | الصفوف المحسوبة | مجموع أرقام التعريف |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| 499 | 499 | 124750 |
| 500 | 500 | 125250 |
| 501 | 501 | 125751 |
| 1000 | 1000 | 500500 |
| 1075 | 1075 | 578350 |

الحالة الأخيرة المفروض تطبع كمان `batch=500` ثم `batch=500` ثم `batch=75`. الجلب الأخير الفارغ لا يطبع سطر دفعة. في نسخة منفصلة، شغّل `check_case(1075)` وحدها واستبدل شرط عدد عناصر الـCollection بشرط `%NOTFOUND` المبكر: الحالة دي المفروض تفشل في التحقق بعد حساب 1,000 رقم فقط. تشغيل كل الحالات بشرط الخروج الخاطئ هيتوقف عند حالة فاشلة أسبق.

العدد مع المجموع أقوى في المثال من العدد وحده، لكنه لا يثبت تطابق هوية بيانات عامة بشكل قاطع. المطابقة الحقيقية تحتاج مقارنة مفاتيح العمل الثابتة ونتيجة كل عملية. وفرّق أيضًا بين `COUNT` للدفعة الحالية وبين `%ROWCOUNT` التراكمي للمؤشر. [Oracle: خصائص المؤشر](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/cursors-overview.html)

## انقل الفكرة إلى المعالجة الفعلية

قبل إضافة DML، حدّد هل جملة SQL واحدة تقدر تعبّر عن العملية. لو محتاج معالجة إجرائية، خلّي الجلب والمعالجة والمسؤولية عن المعاملة واضحين. حد الجلب ليس سياسة Commit، ولا سقفًا لاستهلاك ذاكرة المهمة بالكامل؛ راجع حجم السجل وأي Collections أخرى محتفظ بها وطبيعة الحمل.

لو أضفت `FORALL`، لا تفترض إن عدد أرقام التعريف المجلوبة يساوي عدد الصفوف المتأثرة. حتى Update لا يطابق أي صف يحتاج مطابقة ومراجعة. افحص `SQL%BULK_ROWCOUNT` واستخدم حدودًا مناسبة لو الـCollection بقت متقطعة. `SAVE EXCEPTIONS` يسمح باستكمال بقية التنفيذات، لكنه ما زال يحتاج معالجة أخطاء مقصودة وقرارًا بخصوص التغييرات الناجحة. [Oracle: جملة FORALL](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/FORALL-statement.html)

افصل تصميم المعاملات والاستكمال بعد الفشل عن تجربة حلقة الجلب دي. المهمة الموثوقة تحاسب على كل مفتاح تم اختياره، بما فيه آخر دفعة صغيرة.

[البوست الأصلي على LinkedIn](https://www.linkedin.com/posts/karim-el-gezawy-460752219_plsql-oracledatabase-sql-activity-7527866844540649472-Ii0c)
