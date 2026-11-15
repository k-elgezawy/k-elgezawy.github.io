استخدمت في البوست الأصلي على LinkedIn مثال طلب الإجازة لشرح مهام الموافقات في Oracle APEX. البداية المفيدة هي الفصل بين ثلاث حاجات: سجل الطلب، والقرار البشري، والعملية التي تربط عدة خطوات معًا.

تصف Task Definition مهمة بشرية قابلة لإعادة الاستخدام. ويمكن لكل طلب يتم تقديمه إنشاء نسخة مستقلة من المهمة. أما Workflow أوسع فيقدر ينسّق أنشطة إضافية؛ والموافقة الواحدة لا تستلزم تصميم Workflow كامل من البداية.

## حدّد القرار والمشاركين فيه

من Shared Components، افتح Task Definitions تحت Workflows and Automations. في مثال للتطوير، أنشئ Approval Task بمعرّف ثابت `LEAVE_APPROVAL`. أما Action Task فتناسب العمل المطلوب إتمامه بدون نتيجة موافقة أو رفض. جهّز صفحة تفاصيل المهمة حتى يستطيع صاحب القرار مراجعة الطلب. [دليل Oracle للإنشاء](https://docs.oracle.com/en/database/oracle/apex/26.1/htmdb/creating-task-definitions.html)

اختَر المشاركين بعناية. يستطيع Potential Owners استلام العمل المتاح، ويتعامل Actual Owner مع المهمة المسندة إليه. ولـBusiness Administrators مسؤوليات إدارية مستقلة. حدّد المدير المناسب من قواعد التطبيق بدل تكرار اسم مستخدم معين داخل الصفحات. تدعم APEX تحديد المشاركين ديناميكيًا واستخدام Authorization Schemes. [مفاهيم Task Definition](https://docs.oracle.com/en/database/oracle/apex/26.1/htmdb/about-task-definitions.html)

## أنشئ مهمة واحدة لكل طلب

المسار التصريحي هو Page Process من نوع Human Task - Create. اختَر التعريف، واربط Details Primary Key Item بمعرّف الطلب المحفوظ، واحفظ معرّف المهمة الناتج في Page Item. رتّب العملية بعد نجاح التحقق وحفظ الطلب. [إعداد عملية الصفحة](https://docs.oracle.com/en/database/oracle/apex/26.1/htmdb/creating-tasks-from-task-definitions.html)

وعند التكامل باستخدام PL/SQL، يوضّح المثال التالي استدعاء الـAPI المكافئ داخل عملية صفحة APEX لمستخدم مسجّل دخوله. يفترض وجود التعريف والمشاركين وعناصر الصفحة، وعدم وجود Task Parameters إلزامية:

```sql
begin
    :P10_TASK_ID := apex_human_task.create_task(
        p_task_def_static_id     => 'LEAVE_APPROVAL',
        p_subject                => 'Leave request ' || :P10_REQUEST_ID,
        p_initiator              => :APP_USER,
        p_initiator_can_complete => false,
        p_detail_pk              => :P10_REQUEST_ID
    );
end;
```

ترجع الدالة معرّف المهمة. ويتوقف الإسناد الأولي على Potential Owners: وجود شخص واحد ينشئ مهمة Assigned، ووجود أكثر من شخص ينشئ مهمة Unassigned يمكن استلامها. وعدم وجود مسؤول محتمل يسبب خطأ. [توثيق CREATE_TASK](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/APEX_HUMAN_TASK.CREATE_TASK-Function.html)

## حافظ على اتساق نتيجة العمل

احتفظ بالربط بين طلب العمل ومعرّف المهمة. قبل إنشاء المهمة، تحقّق على السيرفر من صلاحية المستخدم لتقديم الطلب ومن عدم إنشاء مهمة له بالفعل بسبب تقديم سابق. اجعل منع التكرار جزءًا من تصميم المعاملة.

نفّذ أثر الموافقة صراحةً في طبقة قواعد العمل: إتمام المهمة وحده لا يحدد كل تحديث يحتاجه نظام الإجازات. اضبط التنبيهات ومعالجة الاستثناءات، واختبر بحسابات منفصلة لمقدّم الطلب والمدير ومستخدم غير مختص. اختبر الرفض، وتكرار التقديم، وغياب المسؤولين، وفشل تحديث بيانات العمل. افصل بين حالة المهمة وحالة طلب العمل في التصميم، واجعل معالجة حالات الفشل واضحة للمستخدم المختص.

[البوست الأصلي على LinkedIn](https://www.linkedin.com/feed/update/urn:li:activity:7451510112554295296/)
