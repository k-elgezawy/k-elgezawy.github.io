النموذج الذي يتكوّن من عدة خطوات يحتاج مكانًا يحتفظ بالصفوف أثناء مراجعتها. في البوست الأصلي على LinkedIn، عرضت APEX Collections لهذا الاستخدام. التفصيلة المهمة عمليًا هي دورة حياة المسودة: إنشاؤها، والرجوع إليها، وتعديلها، ثم تقديمها نهائيًا.

تعامل مع Collection كبيانات مؤقتة تديرها APEX ضمن الجلسة. واجهة قراءتها بـSQL هي Database View اسمها `APEX_COLLECTIONS`؛ فلا تبنِ التصميم على افتراض أنها مجرد ذاكرة داخل المتصفح أو أنها لا تستهلك أي عمل في قاعدة البيانات. استخدم جداول مسودات دائمة لو الطلب لازم يستمر بعد الجلسة أو يراجعه مستخدم آخر. [Oracle: استخدام Collections](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/about-using-collections.html)

## ابدأ المسودة بدون تصفيرها عند التحديث

في مثال للتطوير، أضف Page Process لإنشاء Collection بالاسم المميز التالي. المثال يستخدم منتجات افتراضية، ويفترض طلبات صفحات متتابعة بشكل عادي داخل جلسة تطبيق APEX فعّالة.

```sql
begin
    if not apex_collection.collection_exists('DEMO_CART_20261117') then
        apex_collection.create_collection(
            p_collection_name => 'DEMO_CART_20261117'
        );
        apex_collection.add_member(
            p_collection_name => 'DEMO_CART_20261117',
            p_c001 => 'Notebook',
            p_n001 => 2,
            p_n002 => 12.50
        );
        apex_collection.add_member(
            p_collection_name => 'DEMO_CART_20261117',
            p_c001 => 'Pen',
            p_n001 => 3,
            p_n002 => 2
        );
    end if;
end;
```

تفحص `COLLECTION_EXISTS` المستخدم والجلسة والتطبيق الحاليين. و`CREATE_COLLECTION` ترفع خطأ عادةً لو نفس الـCollection موجودة بالفعل. الشرط بيحافظ على المسودة الموجودة عند زيارة العملية مرة ثانية. لكنه مش قفل للتزامن: نسّق طلبات الإنشاء المتزامنة داخل التطبيق. [فحص الوجود](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/COLLECTION_EXISTS-Function.html)، [توثيق الإنشاء](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/CREATE_COLLECTION-Procedure.html)

افصل إجراء «ابدأ من جديد» عن عرض الصفحة العادي. استدعاء عملية تصفير أو تفريغ عند كل عرض للصفحة بيضيّع الغرض من المسودة. وافصل الإنشاء الأولي عن إجراء «أضف منتجًا»، الذي يحتاج قواعد مستقلة لمنع تكرار التقديم.

## اقرأ الأعمدة بأنواعها وأسماء واضحة

في Classic Report، استخدم:

```sql
select seq_id,
       c001 as product_name,
       n001 as quantity,
       n002 as unit_price,
       n001 * n002 as line_total
from apex_collections
where collection_name = 'DEMO_CART_20261117'
order by seq_id;
```

معنى الأعمدة جزء من عقد التطبيق: `C001` اسم المنتج، و`N001` الكمية، و`N002` سعر الوحدة. وثّق الربط في Package صغيرة عندما تتشارك فيه عدة صفحات. احتفظ بالأرقام في الأعمدة الرقمية، وبالحماية المعتادة للنصوص عند عرض التقارير. توثّق Oracle أنواع الأعمدة ونمط قراءة Collection. [المفاهيم الأساسية](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/key-collections-concepts.html)

عند إنشاء Collection جديدة، الصفوف المتوقعة هي:

```text
SEQ_ID  PRODUCT_NAME  QUANTITY  UNIT_PRICE  LINE_TOTAL
1       Notebook     2         12.50       25.00
2       Pen          3          2.00        6.00
```

الإجمالي 31.00؛ والتنسيق الفعلي للفواصل والأرقام يتبع إعدادات التقرير. تحديث الصفحة المفروض يحتفظ بالصفّين بدل إضافة نسخة ثانية منهما.

## عدّل قيمة واحدة بدون مسح القيم المجاورة

في إجراء اختبار صريح داخل بيئة التطوير، غيّر كمية الصف الأول:

```sql
begin
    apex_collection.update_member_attribute(
        p_collection_name => 'DEMO_CART_20261117',
        p_seq             => 1,
        p_attr_number     => 1,
        p_number_value    => 4
    );
end;
```

النسخة الرقمية من الدالة الإجرائية بتعدّل `N001`، بينما اسم المنتج وسعر الوحدة يفضلوا كما هم. إجمالي Notebook المتوقع يصبح 50.00، والإجمالي العام 56.00. ولو العضو المطلوب غير موجود يحصل خطأ. [تعديل العمود الرقمي](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/UPDATE_MEMBER_ATTRIBUTE-Procedure-Signature-5.html)

ده مختلف عن `UPDATE_MEMBER` التي تضع NULL في الأعمدة التي لم ترسل قيمها. الفرق ده ممكن يفسّر ليه تعديل الكمية أحيانًا يمسح الوصف أو السعر بدون قصد. [سلوك استبدال العضو](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/UPDATE_MEMBER-Procedure.html)

## حدّد حدود المسودة

تبويبات المتصفح التي تتشارك نفس جلسة التطبيق يمكنها الوصول لنفس Collection المسماة. للمسودات المستقلة، استخدم معرّف مسودة يديره السيرفر مع تحقق ثابت من الملكية؛ اسم Collection ثابت مش وسيلة لعزل كل تبويب لوحده.

ما تعتبرش `SEQ_ID` معرّف عمل دائمًا. الحذف ممكن يترك فجوات، وإعادة الترقيم ممكن تغيّر الأرقام. وفي Editable Grid، اتبع إرشاد Oracle بتخزين مفتاح صف ثابت في أحد أعمدة Collection. [سلوك الترقيم](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/RESEQUENCE_COLLECTION-Procedure.html)، [إرشاد الـGrid](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/key-collections-concepts.html)

قبل التقديم النهائي، تحقّق على السيرفر من نطاق الكمية وصلاحية الوصول للمنتجات والأسعار الحالية. احفظ البيانات المقبولة من خلال معاملة عمل واضحة، ولا تفرّغ المسودة المؤقتة إلا بعد نجاح الحفظ. اختبر تحديث الصفحة، وتبويبين، وانتهاء الجلسة، والصفوف المفقودة، وفشل الحفظ النهائي. الأمثلة بتشرح السلوك المتوقع، ولا تدّعي تنفيذًا على تطبيق أو نتائج أداء مقاسة.

[البوست الأصلي على LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7405717744706486272/)
