حقل البحث ممكن يعرض إجابة غلط رغم إن كل رد من السيرفر صحيح. المستخدم يكتب كلمة جديدة، فيرجع ردها أولًا، ثم رد أقدم يكتب فوقها. البوست الأصلي على LinkedIn عرض طابورًا مسمّى يستبدل الطلبات القديمة للتعامل مع السباق ده.

المقال هنا يضيف Callback كاملة وحدًا إضافيًا مهمًا: مسح الحقل لازم يبطل صلاحية النتيجة القديمة، حتى لو المسح لا يرسل أي طلب.

## ضع الطلبات المرتبطة في طابور ثابت

في `apex.server.process`، الإعداد `queue.action: "replace"` يجعل العمل الأقدم على نفس الطابور غير مطلوب. الطلب المنتظر ممكن يفشل بحالة `superseded`، والطلب الذي تمت مقاطعته ممكن يفشل بحالة `abort`. دي انتقالات متوقعة في البحث، وليست أسبابًا لمقاطعة المستخدم بتنبيهات. استخدم اسمًا ثابتًا لكل حقل بحث مستقل. [Oracle: server API](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/apex.server.html)

لا تولّد اسم طابور جديدًا لكل ضغطة؛ الطلبات وقتها لا تشترك في نفس حدود الاستبدال. وبالمثل، حقلا بحث غير مرتبطين لا ينبغي أن يلغيا عمل بعضهما.

## أنشئ مثال تطوير كاملًا

في صفحة تطوير رقمها 10، أنشئ Text Field باسم `P10_SEARCH`. أضف الكود التالي إلى Static Content region:

```html
<p id="product-search-result" role="status" aria-live="polite"></p>
```

أنشئ Ajax Callback على الصفحة باسم `SEARCH_PRODUCTS` بكود PL/SQL التالي. أسماء المنتجات الثلاثة افتراضية؛ لا يقرأ الكود جداول التطبيق ولا يغيّرها. تعيد الـCallback فحص طول المدخل على السيرفر، وتحسب المطابقات الحرفية لجزء من الاسم، وتكتب ردًا منظمًا. قيمة `x01` متاحة في `apex_application.g_x01`. [معاملات الطلب](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/apex.server.html#process)

```sql
DECLARE
    l_term  VARCHAR2(32767) := TRIM(apex_application.g_x01);
    l_count PLS_INTEGER := 0;
BEGIN
    IF LENGTH(l_term) > 60 THEN
        apex_json.open_object;
        apex_json.write('ok', FALSE);
        apex_json.write('error', 'Search term is too long');
        apex_json.close_object;
        RETURN;
    END IF;
    IF l_term IS NOT NULL THEN
        WITH products(product_name) AS (
            SELECT 'Notebook' FROM dual UNION ALL
            SELECT 'Pen' FROM dual UNION ALL
            SELECT 'Pencil' FROM dual
        )
        SELECT COUNT(*) INTO l_count
        FROM products
        WHERE INSTR(LOWER(product_name), LOWER(l_term)) > 0;
    END IF;
    apex_json.open_object;
    apex_json.write('ok', TRUE);
    apex_json.write('count', l_count);
    apex_json.close_object;
END;
```

ولّد JSON باستخدام الحزمة بدل تجميع نص غير محمي بالربط. في المثال ده، الرد الصحيح على `pen` يكون كائنًا فيه `ok: true` و`count: 2`. [Oracle: APEX_JSON](https://docs.oracle.com/en/database/oracle/apex/26.2/aeapi/APEX_JSON.html)

أضف الـHelper التالية إلى خاصية Function and Global Variable Declaration للصفحة. احتفظ بعدّاد الأجيال خارج `run` حتى تشترك فيه كل الاستدعاءات:

```javascript
window.kgProductSearch = (function () {
    "use strict";
    let generation = 0;
    function run() {
        const token = ++generation;
        const output = document.getElementById("product-search-result");
        const term = String(apex.item("P10_SEARCH").getValue() || "").trim();
        if (!output) { return; }
        if (!term) {
            output.textContent = "Type a search term.";
            return;
        }
        if (term.length > 60) {
            output.textContent = "Use a shorter search term.";
            return;
        }
        output.textContent = "Searching...";
        apex.server.process("SEARCH_PRODUCTS", { x01: term }, {
            dataType: "json",
            queue: { name: "p10-product-search", action: "replace" }
        }).done(function (data) {
            if (token !== generation) { return; }
            if (!data || data.ok !== true ||
                    !Number.isInteger(data.count) || data.count < 0) {
                output.textContent = "Unexpected search response.";
                return;
            }
            output.textContent = term + ": " + data.count + " matches";
        }).fail(function (xhr, status) {
            if (token !== generation ||
                    ["abort", "superseded"].includes(status)) { return; }
            output.textContent = "Search failed. Please try again.";
        });
    }
    return { run: run };
}());
```

أنشئ Dynamic Action لحدث Key Release على `P10_SEARCH`، وبداخلها Execute JavaScript Code بالاستدعاء التالي. عطّل Fire on Initialization لهذا الإجراء. المثال يوضح البحث مع الكتابة بلوحة المفاتيح؛ وسّع تغطية الأحداث لو واجهتك تغيّر القيمة من عناصر أخرى أيضًا. [Oracle: إنشاء Dynamic Actions](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/creating-and-editing-dynamic-actions.html)

```javascript
window.kgProductSearch.run();
```

رسائل الحالة في المثال نصوص إنجليزية قصيرة للتوضيح؛ ترجمها بما يناسب مستخدمي التطبيق. الكتابة باستخدام `textContent` تعرض كلمة البحث كنص ولا تفسّرها كـHTML. [MDN: textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)

## لماذا الطابور ومعه عدّاد أجيال؟

العدّاد يصف آخر نية للمستخدم في الواجهة، بما فيها الإجراءات التي لا تستدعي السيرفر. افترض إن طلب `pen` ما زال شغالًا، والمستخدم مسح الحقل. فرع الحقل الفارغ يعرض رسالة الكتابة ثم ينتهي. لا يدخل طلب بديل إلى الطابور، ولذلك العدّاد يمنع الـCallback السابقة من إرجاع عدد قديم إلى الشاشة.

نفس الحماية تنطبق عندما نرفض محليًا كلمة أطول من الحد. وتفيد كمان في تسلسل مثل `pen` ثم `note` ثم `pen` مرة أخرى: مقارنة النص الحالي وحده لا تفرّق بين طلب `pen` الأول والأحدث. الرمز المختلف لكل استدعاء يقدر يفرّق.

المثال يفحص شكل الرد قبل عرض العدد. فشل النقل ورد التطبيق الذي يخالف العقد مساران مختلفان؛ ولا ينبغي لأي منهما أن يظهر في هدوء كأنه صفر نتائج. معاملات دالة الفشل تتبع نمط معاملات Error Callback. [jQuery Ajax callbacks](https://api.jquery.com/jQuery.ajax/)

## اختبر حالة الشاشة النهائية وليس عدد الطلبات فقط

في تطبيق اختبار، تحقّق إن `pen` ترجع 2 و`notebook` ترجع 1، وجزء اسم غير موجود يرجع 0. مع اتصال بطيء، اكتب كلمات متتابعة، وامسح الحقل أثناء وجود طلب جارٍ، وأدخل أكثر من 60 حرفًا. النتيجة الظاهرة لازم تخص آخر استدعاء. اختبر أيضًا فشل السيرفر وردًا غير متوقع الشكل.

الـDebouncing يقلل تكرار بدء الطلبات، لكنه لا يثبت أن الطلبات التي بدأت بالفعل لن تتداخل. تعامل مع تقليل معدل الطلبات وحماية النتيجة من القِدم باعتبارهما مسؤوليتين منفصلتين.

توثّق Oracle أيضًا إن دالة `abort` في الـPromise الراجعة لا تعمل مع استخدام Queue Options؛ فلا تضف الإلغاء اليدوي على افتراض إنه الحل. وبشكل أوسع، الإلغاء من جهة المتصفح ليس بروتوكولًا لمعاملات العمل. استخدم النمط للبحث والمعاينات التي تقبل الاستبدال. البيانات المحمية تحتاج صلاحيات على السيرفر، والحفظ يحتاج تصميمه الخاص للاتساق وإعادة المحاولة. [Oracle: سلوك الـPromise والطابور](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/apex.server.html#process)

المراجع تصف APEX 26.2. تحقّق من التكامل مع الإصدار الذي تشغّله؛ الشرح لا يدّعي تنفيذ الـCallback داخل تطبيقك.

[البوست الأصلي على LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7521498181541580800/)
