ملخص طلب الشراء قد يحتاج تصميمًا يناسب إجراءات العمل. بوستي الأصلي على LinkedIn استخدم Dynamic Content في Oracle APEX لدمج بيانات الطلب المختار مع HTML مخصص. الشرح التالي يبدأ بملخص صغير يعرض العميل والإجمالي والحالة.

## أرجع HTML في قيمة CLOB

في صفحة تطوير، أضف Select List باسم `P10_ORDER_ID` بقيمتي `1001` و`1002`. أنشئ منطقة **Dynamic Content** وحدّد Static ID بقيمة `order_summary`، واستخدم PL/SQL Function Body returning a CLOB كمصدر. لو رقم صفحتك مختلف، طابق اسم العنصر مع الصفحة الفعلية.

المنطقة ترجع HTML الذي كوّنته إلى APEX. يوضح توثيق Oracle مصدر CLOB واستخدام CSS Classes مع المنطقة. [Dynamic Content](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/dynamically-formatting-data.html)

الاستعلام في المثال يستخدم صفّين افتراضيين من `DUAL`. ضع جسم الدالة التالي في مصدر المنطقة.

```sql
declare
    l_customer varchar2(200);
    l_total    number;
    l_status   varchar2(30);
begin
    select customer_name, order_total, order_status
      into l_customer, l_total, l_status
      from (
          select '1001' as order_id,
                 'Sample <Customer>' as customer_name,
                 125.50 as order_total,
                 'Ready' as order_status
            from dual
          union all
          select '1002', 'Second Customer', 78, 'In review'
            from dual
      )
     where order_id = :P10_ORDER_ID;

    return to_clob(
        '<article class="order-summary"><h3>Order summary</h3><dl>'
    )
        || '<dt>Customer</dt><dd>'
        || apex_escape.html(l_customer) || '</dd>'
        || '<dt>Total</dt><dd>'
        || apex_escape.html(to_char(
               l_total, 'FM999990D00',
               'NLS_NUMERIC_CHARACTERS=''.,'''
           )) || '</dd>'
        || '<dt>Status</dt><dd>'
        || apex_escape.html(l_status) || '</dd>'
        || '</dl></article>';
exception
    when no_data_found then
        return to_clob('<p>Select an available demo order.</p>');
end;
```

اسم العميل يحتوي عمدًا على علامات زاوية لتتأكد أنها تظهر كنص. القيم التي تدخل في مواضع النص داخل HTML تمر عبر `APEX_ESCAPE.HTML`. عند توسيع التصميم، عالج خصائص HTML والروابط بما يناسب سياق كل منها. [حماية النصوص داخل HTML](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/HTML-Function.html)

## أرسل القيمة المختارة عند التحديث

أضف `P10_ORDER_ID` إلى خاصية **Page Items to Submit** في المنطقة، بدون نقطتين قبل الاسم. أنشئ Dynamic Action على حدث Change للعنصر، وأضف إجراء Refresh يستهدف منطقة الملخص. الإعداد ده يرسل الاختيار الحالي إلى السيرفر أثناء طلب التحديث. [العناصر المطلوب إرسالها](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/configure-items-submit-and-return.html)

## نسّق الملخص واختبره

ضع القواعد التالية في Inline CSS للصفحة أو في ملف CSS الخاص بالتطبيق.

```css
#order_summary .order-summary {
  padding: 1rem;
  border: 1px solid currentColor;
  border-radius: 0.75rem;
}
#order_summary .order-summary dl {
  display: grid;
  grid-template-columns: minmax(6rem, 1fr) minmax(0, 2fr);
  gap: 0.5rem 1rem;
}
#order_summary .order-summary dd {
  margin: 0;
  overflow-wrap: anywhere;
}
```

بدّل بين الطلبين وتأكد أن العميل والإجمالي والحالة يتغيروا معًا. راجع رسالة الاختيار الفارغ، والشاشات الصغيرة، واستخدام الكيبورد، واتجاه الصفحة العربية. احتفظ بالحالة مكتوبة كنص واضح.

عند استبدال الصفوف الافتراضية ببيانات التطبيق، طبّق قواعد الوصول للصفوف داخل الاستعلام وصلاحية الوصول للمنطقة. استخدم Text Messages مترجمة للعناوين والتسميات في التطبيق متعدد اللغات. راجع HTML الناتج بعد كل تغيير في البيانات أو التصميم.

[البوست الأصلي على LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7516717117732401154/)
