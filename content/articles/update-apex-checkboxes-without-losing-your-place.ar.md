Checkbox داخل تقرير طويل المفروض تحفظ التغيير من غير ما ترجع المستخدم لأول الصفحة. التنفيذ الموثوق محتاج Callback آمنة وسلوك Refresh مقصود.

### حدد عقد التحديث

ابعت معرّف السجل، والحالة المطلوبة، ورقم نسخة السجل المتوقعة إلى Ajax Callback محمية بالصلاحيات. على السيرفر، تحقق من الحالة، ومن صلاحية المستخدم على السجل نفسه باستخدام هوية موثوقة، وارفض التعديل لو النسخة قديمة. فحص المعرّف وحده لا يكفي.

امنع التعديل المتكرر أثناء الحفظ. رجّع نجاحًا واضحًا أو خطأ يمكن التعامل معه، وأعد حالة Checkbox القديمة عند الفشل. استخدم Controls تصريحية أو عرضًا بمعالجة Escape صحيحة، بدل تركيب قيم غير موثوقة داخل HTML.

### استعد المكان بعد تحديث الـRegion

في تقرير يطلق حدث `apexafterrefresh`، سجّل استعادة المكان قبل Refresh. الجزء التالي يوضع داخل معالج نجاح الحفظ؛ و`tasks` هو Static ID للـRegion:

```javascript
const y = window.scrollY;
apex.jQuery("#tasks").one("apexafterrefresh", function () {
  requestAnimationFrame(() => window.scrollTo(0, y));
});
apex.region("tasks").refresh();
```

نفّذ عمليات الحفظ والتحديث بالتتابع، حتى لا يستهلك Refresh آخر هذا المعالج. لو التمرير داخل Container، احفظ `scrollTop` الخاصة به. أعد تطبيق ألوان الحالة بعد التحديث، واستخدم وصفًا نصيًا مع اللون، واستعد تركيز لوحة المفاتيح حيث يمكن.

*تصحيح تحريري: Callback الأصلية لم تتحقق من صلاحية السجل أو تعارض التعديلات. ودوال التمرير لم ترتبط بانتهاء التحديث، ومفتاح localStorage عام واحد قد يخلط بين صفحات مختلفة.*

المراجع: [واجهة Ajax](https://docs.oracle.com/en/database/oracle/apex/24.2/aexjs/apex.server.html)، [أحداث التحديث](https://docs.oracle.com/en/database/oracle/apex/24.2/aexjs/apex.html)، و[تحديث Region](https://docs.oracle.com/en/database/oracle/apex/24.2/aexjs/region.html).