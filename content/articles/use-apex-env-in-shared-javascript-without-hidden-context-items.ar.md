ملف JavaScript المشترك بين صفحات APEX غالبًا يحتاج يعرف الصفحة الحالية أو مكان صورة خاصة بالتطبيق. إنشاء عناصر مخفية لمجرد تكرار معلومات السياق التي يوفرها الإطار يضيف قيمًا أخرى تحتاج صيانة.

في البوست الأصلي على LinkedIn، عرضت `apex.env`. الشرح التالي يحوّل الفكرة إلى Helper مشتركة صغيرة، مع تهيئة صريحة وأنواع بيانات واضحة وفصل بين سلوك المتصفح والقرارات التي ينفّذها السيرفر.

## اقرأ السياق بأنواع البيانات الموثّقة

توثّق Oracle الخصائص `APP_ID` و`APP_PAGE_ID` و`APP_FILES` كنصوص داخل `apex.env`. الكائن متاح من APEX 21.2؛ والمرجع المرتبط هنا يصف 26.2. راجع التوثيق المناسب للإصدار الذي تشغّله. [Oracle JavaScript API](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/apex.html#env)

لفحص محدد أثناء التطوير داخل صفحة تطبيق APEX، اعرض القيم التي تحتاجها فقط:

```javascript
console.table({
    pageId: apex.env.APP_PAGE_ID,
    pageIdType: typeof apex.env.APP_PAGE_ID,
    filesBase: apex.env.APP_FILES
});
```

في الصفحة 10، القيمة المتوقعة لـ`pageId` هي النص `"10"`، ولـ`pageIdType` هي `"string"`. ومسار الملفات يتحدد حسب التطبيق. لذلك المقارنة الصارمة مع الرقم `10` تفشل؛ قارِن مع النص `"10"` بشكل مقصود. تجنّب نسخ الكائن كاملًا إلى تذاكر الدعم أو السجلات المشتركة، خصوصًا معرّفات الجلسات ومعلومات المستخدمين.

## ابنِ Helper مشتركة صغيرة

داخل تطبيق تطوير، ارفع صورة توضيحية باسم `company-logo.svg` إلى Static Application Files. أضف الكود التالي إلى Static Content region في صفحة اختبار:

```html
<p id="page-context"></p>
<img id="company-logo" alt="Company logo" width="120" height="40">
<p id="dashboard-help" hidden>Dashboard-specific help.</p>
```

أنشئ ملف `page-context-demo.js` بالمحتوى التالي:

```javascript
window.kgPageContextDemo = (function () {
    "use strict";

    function init() {
        const env = apex.env;
        const badge = document.getElementById("page-context");
        const logo = document.getElementById("company-logo");
        const help = document.getElementById("dashboard-help");

        if (badge) {
            badge.textContent =
                "App " + env.APP_ID + " / Page " + env.APP_PAGE_ID;
        }
        if (logo) {
            logo.src = env.APP_FILES + "company-logo.svg";
        }
        if (help) {
            help.hidden = env.APP_PAGE_ID !== "10";
        }
    }

    return { init: init };
}());
```

فحص وجود العناصر يسمح لصفحة أخرى بتحميل نفس الملف بدون احتياجها لمنطقة المثال. وتكتب الـHelper النص باستخدام `textContent`، وبالتالي لا تفسّر قيمة الشارة باعتبارها HTML. [MDN: textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)

يقرأ الملف السياق الحالي عند تشغيل `init`. ويبني مسار الصورة من بادئة ملفات التطبيق التي توفرها APEX، بدل كتابة مسار خاص بمساحة عمل معينة. طابق اسم الملف مع الصورة المرفوعة، وتحقّق من طلب تحميلها في Network panel داخل المتصفح.

## حمّل الملف ثم هيّئ الصفحة

ارفع ملف JavaScript إلى Static Application Files واستخدم Reference URL الظاهر له. في JavaScript File URLs لصفحة الاختبار، يمكن أن تكون الإشارة:

```text
#APP_FILES#page-context-demo.js
```

ولمشاركته على مستوى التطبيق، استخدم JavaScript File URLs داخل User Interface Attributes. انسخ Reference الذي توفره APEX، بما فيه أي صيغة مناسبة لتحميل النسخة المصغّرة، وتجنّب تحميل نفس الملف مرة على مستوى التطبيق ومرة أخرى في الصفحة. [Oracle: ملفات الـHelpers المشتركة](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/including-helper-functions-all-pages.html)

في خاصية Execute When Page Loads بصفحة الاختبار، استدعِ:

```javascript
window.kgPageContextDemo.init();
```

تفرّق Oracle بين تحميل ملفات JavaScript وتعريف الدوال وتنفيذ كود عند تحميل الصفحة. استدعاء الـHelper بعد تهيئة الصفحة يفصل التعامل مع DOM عن لحظة تحميل الملف نفسه. [خصائص JavaScript للصفحة](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/editing-page-attributes-in-page-designer.html)

## تحقّق من السلوك وحدوده

في الصفحة 10، المفروض الشارة تعرض التطبيق والصفحة الحاليين، والصورة تتحمّل، ونص المساعدة يظهر. وفي صفحة اختبار أخرى، يفضل نص المساعدة مخفيًا. وفي صفحة بدون منطقة المثال، فحص العناصر المفروض يتجنب أخطاء الوصول لعناصر غير موجودة.

لو تحديث جزئي استبدل DOM الخاص بالمنطقة، استدعِ الـHelper مرة أخرى من معالجة التحديث المناسبة؛ استدعاء تحميل الصفحة الأصلي لا يهيّئ العناصر التي أُنشئت بدل القديمة. الـHelper دي لا تضيف Event Listeners، لذلك تكرار تعيين القيم لا يراكم Handlers.

استخدم السياق للعرض ومسارات الملفات. قيم المتصفح وإخفاء العناصر مش فحص صلاحيات؛ تحقّق من العمليات المحمية والوصول للبيانات على السيرفر. واحتفظ بعناصر العمل الحقيقية عندما تمثّل مدخلات أو حالة على السيرفر. الأمثلة بتوضح نمط تكامل وسلوكًا متوقعًا، ولا تدّعي تنفيذ الكود على تطبيقك.

[البوست الأصلي على LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7521843410698399744/)
