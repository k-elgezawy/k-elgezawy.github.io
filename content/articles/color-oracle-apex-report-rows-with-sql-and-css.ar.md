عمود الحالة يساعد المستخدم يراجع صفوف Interactive Report في Oracle APEX بسرعة. المثال الأصلي على LinkedIn استخدم علامة HTML صغيرة داخل كل صف، وبعدها CSS لتنسيق الصف الذي يحتوي على العلامة.

## أرجع علامة حالة بقيم محددة

الاستعلام التوضيحي التالي يفترض وجود جدول `demo_records` وعمودي `record_id` و`status_code`. استبدل الأسماء باستعلام تطبيقك. الربط بين الحالة والعرض يُنتج مجموعة ثابتة من نصوص HTML.

```sql
select record_id,
       case status_code
         when 'VALID' then
           '<span class="row-paint" data-state="valid">Valid</span>'
         when 'EXPIRED' then
           '<span class="row-paint" data-state="expired">Expired</span>'
         else
           '<span class="row-paint" data-state="review">Review</span>'
       end as status_badge
from demo_records
```

اضبط العمود المحسوب `STATUS_BADGE` على Plain Text واجعل Escape Special Characters بقيمة No لعرض HTML الناتج. احتفظ بالـEscaping لأعمدة البيانات العادية. لو وسّعت التعبير وأضفت نصًا يدخله المستخدم، طبّق عليه الـEscaping المناسب لسياق العرض قبل دمجه مع HTML. توضح Oracle [فلاتر حماية النصوص وخصائص HTML](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/controlling-output-escaping-in-substitution-strings.html).

الكلمات الظاهرة Valid وExpired وReview توفر وصفًا مقروءًا للحالة بجانب اللون.

## حدّد نطاق CSS لتقرير واحد

أعطِ منطقة التقرير Static ID بقيمة `record_status_report`. أضف القواعد التالية إلى ملف CSS الخاص بالتطبيق أو Inline CSS في الصفحة.

```css
#record_status_report tbody tr:has(.row-paint[data-state="valid"]) > td {
  background-color: #e4f5ea;
  color: #123b24;
}

#record_status_report tbody tr:has(.row-paint[data-state="expired"]) > td {
  background-color: #fbe9e7;
  color: #582018;
}
```

المحدد `:has()` يختار الصف الذي يحتوي على العلامة المطابقة. تطبيق الخلفية على خلايا الصف يساعد اللون يظهر فوق الخلفيات التي يضعها قالب التقرير على الخلايا. يشرح MDN [المحدد ودعم المتصفحات له](https://developer.mozilla.org/en-US/docs/Web/CSS/:has).

حالة Review تحتفظ بتنسيق التقرير المعتاد. عدّل الألوان لتناسب الثيم، وراجع تباين النص في كل مظهر يدعمه التطبيق.

## اختبر تجربة التقرير كاملة

اختبر الحالتين الملونتين والحالة الافتراضية. غيّر الفلاتر والترتيب، وتنقّل بين صفحات التقرير، ثم حدّثه. المحدد يطابق الصفوف التي تُرسم من جديد عندما تظل العلامة موجودة في HTML الخاص بها.

احتفظ بعمود الحالة في تخطيطات التقرير التي تحتاج التنسيق. لو المستخدم أخفى العمود أو استبعده، افحص هل العلامة ما زالت موجودة في الـDOM الناتج. راجع تركيز الكيبورد وتنسيق مرور المؤشر والشاشات الصغيرة وتنزيل الملفات أيضًا. ملف التصدير يحتاج قيمًا مقروءة توضّح الحالة.

الأسلوب يربط قيمة حالة محددة بطريقة عرضها. احتفظ بقرار العمل في الاستعلام أو منطق التطبيق، واستخدم النص الظاهر لتفسير اللون.
