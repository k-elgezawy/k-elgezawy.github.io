Ajax Callback مفيد لما تحتاج نتيجة محددة من السيرفر بدون Submit كامل، زي جلب إجمالي طلب بعد تغيير الطلب المختار.

### حدد شكل الطلب والرد

المتصفح يرسل رقم الطلب، والـCallback يتحقق من القيمة وصلاحية الوصول للسجل، ويحسب النتيجة ويرجع JSON. بعدها المتصفح يحدث الجزء المطلوب. ده مثال لطلب GET_ORDER_TOTAL وتحديث P15_TOTAL، بشرط وجود الـItems والـCallback واستجابة JSON مطابقة.

```javascript
apex.server.process(
  'GET_ORDER_TOTAL',
  { x01: apex.item('P15_ORDER_ID').getValue() },
  { dataType: 'json' }
).done(function (data) {
  apex.item('P15_TOTAL').setValue(data.total);
}).fail(function () {
  apex.message.alert('تعذر تحميل الإجمالي. حاول مرة أخرى.');
});
```

استخدم APEX_JSON لتكوين الرد بدل تركيب JSON يدويًا بالنصوص.

### الصلاحيات تتطبق على السيرفر

القيمة المرسلة في x01 مدخل غير موثوق. وجودها في Hidden Item أو عنصر مقفول لا يثبت إن المستخدم مسموح له يشوف السجل. راجع صلاحية العملية وصلاحية السجل نفسه.

لو المستخدم يغير الاختيار بسرعة، امنع استجابة قديمة من الكتابة فوق نتيجة الاختيار الجديد، واعرض حالة التحميل ورسالة واضحة عند الفشل.

الـCallback يشتغل لما JavaScript أو Dynamic Action تستدعيه، مش مرحلة تلقائية في كل تحميل للصفحة. وهو لا ينفذ كل Validations وProcesses الخاصة بالـSubmit تلقائيًا.

الفائدة الأساسية هي طلب صغير له مدخلات ونتيجة ومسؤولية واضحة، مش مجرد استخدام Ajax في كل مكان.

المرجع: [أحداث Dynamic Actions في Oracle](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/managing-dynamic-actions.html).
