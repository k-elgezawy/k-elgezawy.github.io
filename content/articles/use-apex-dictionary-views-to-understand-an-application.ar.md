فتح كل صفحة يدويًا طريقة بطيئة للإجابة عن «العنصر ده مستخدم فين؟». APEX Dictionary Views بتعرض Metadata التطبيق، وتقدر تستعلم عنها للجرد والمراجعة والتوثيق.

ابدأ من Application → Utilities → Oracle APEX Views. اختار View، وراجع الأعمدة المتاحة، وانسخ الاستعلام الناتج. Oracle بتوفر كمان `APEX_DICTIONARY` لاكتشاف الـViews. [الخطوات الرسمية](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/accessing-apex-views.html).

### اعمل جردًا محددًا

المثال التالي للقراءة فقط، ويعرض تعريفات العناصر:

```sql
select page_id, item_name, display_as
from apex_application_page_items
where application_id = :APP_ID
order by page_id, item_name;
```

داخل تطبيق APEX، `:APP_ID` تمثل رقم التطبيق الحالي. داخل أداة SQL مستقلة، اربط رقم التطبيق صراحة واضبط سياق الـWorkspace المناسب. أسماء الأعمدة مستخدمة أيضًا في [مثال Oracle للـMetadata](https://www.oracle.com/ocom/groups/public/%40otn/documents/webcontent/301715.html)؛ وراجع إصدارك المثبت من متصفح الـViews.

بعدها افحص Views الخاصة بالـRegions والأزرار والـProcesses والـDynamic Actions. اجمع النتائج حسب التطبيق والصفحة، وابحث عن أسماء غير متوقعة، أو مراجع قديمة، أو منطق متكرر يحتاج مراجعة.

جرد العناصر لا يثبت كل الاعتماديات. Dynamic SQL وJavaScript المتولدة والـPlugins والخدمات الخارجية قد تحتاج بحثًا إضافيًا. وبالمثل، غياب قيمة Authorization على مستوى الصفحة مؤشر للمراجعة، وليس دليلًا إن الصفحة غير محمية.

*توضيح تحريري: استعلامات Metadata تساعد في التحليل، لكنها ليست مراجعة كاملة للاعتماديات أو الأمان.*

احفظ استعلامات المراجعة المتكررة في Source Control، وقارن نتائجها عندما يتغير تركيب التطبيق.