ممكن التقرير يظهر على الشاشة بينما الـ Dynamic Action لسه مستنية الحدث اللي اتضبطت عليه. ابدأ التشخيص بتحديد اللحظة المناسبة للتنفيذ: التحميل الأول للصفحة، تحديث مكوّن بعينه، أو اكتمال طلب Ajax.

## افصل بين توقيت السيرفر والمتصفح

أثناء تجهيز الصفحة، يبني APEX الاستجابة باستخدام عمليات السيرفر والشروط واستعلامات المناطق. في المتصفح، يحدث Page Load لما يكون الـ DOM جاهز. لو المهمة تعتمد على مكونات APEX اللي بتتأخر في التهيئة، راجع حدث `apexreadyend` في التوثيق. تحديث منطقة عملية منفصلة. حدث After Refresh ينطبق على المكوّنات اللي بتطلق حدث التحديث.

## مثال عملي لعد الصفوف الظاهرة بعد تحديث التقرير

في تطبيق تطوير، أعطِ الـ Classic Report معرّفًا ثابتًا `orders_report`. أضف عنصرًا ثابتًا بمعرّف `orders_row_count` خارج التقرير. عرّف الدالة التالية ضمن تعريفات JavaScript في الصفحة. اضبط محدد الصفوف على حسب قالب تقريرك.

```javascript
function updateVisibleOrderCount() {
  const report = document.getElementById("orders_report");
  const label = document.getElementById("orders_row_count");
  if (report && label) {
    const count = report.querySelectorAll("tbody tr").length;
    label.textContent = String(count);
  }
}
```

استدعِ `updateVisibleOrderCount();` من Dynamic Action بحدث Page Load للعرض الأول. استدعِ الدالة مرة ثانية من Dynamic Action بحدث After Refresh يستهدف الـ Classic Report بعد كل تحديث لاحق. المثال يعد صفوف الجدول المرسومة، بما فيها أي صفوف من القالب تطابق المحدد. لو المطلوب إجمالي الصفوف عبر جميع صفحات التقرير، احسب العدد على السيرفر.

## شخّص المشكلة بتتبّع التنفيذ على الجانبين

فعّل APEX Debug وراجع تنفيذ تجهيز الصفحة أو طلب Ajax على السيرفر. بعدها استخدم أدوات المطور في المتصفح للتأكد إن الحدث اتنفّذ، وإن المحدد طابق العنصر المطلوب، وإن طلب Ajax رجع بنجاح. لو التقرير بطيء، قِس زمن استعلام المنطقة وطلب الشبكة قبل تعديل إعداد الحدث.

[دليل Dynamic Actions من Oracle](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/understanding-dynamic-actions.html) و[مرجع أحداث JavaScript في Oracle APEX](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/apex.html).
