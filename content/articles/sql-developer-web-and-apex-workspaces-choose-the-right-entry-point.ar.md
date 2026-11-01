أحيانًا تحتاج تراجع Tables أو Packages أو تشغل SQL من غير التنقل بين صفحات التطبيق. SQL Developer Web أحد الخيارات المتاحة من خلال ORDS.

الرابط المختصر في البوست الأصلي بيوصل إلى [صفحة ORDS الرسمية](https://oracleapex.com/ords/)، وفيها مداخل منفصلة لـSQL Developer Web وAPEX. دي مش شاشة دخول موحدة تقبل أي حساب Workspace.

### طريقة الدخول تعتمد على البيئة

الدخول المباشر لـSQL Developer Web عادة يرتبط بحساب Schema مفعّل للخدمة. وفيه دخول متكامل من SQL Workshop لما إعدادات الـInstance والـSchema تسمح. في APEX 26.2، قائمة SQL Developer Web تعرض Schemas المرتبطة بالـWorkspace والمسموح للمطور الوصول لها.

ابدأ من عنوان APEX أو ORDS الموثوق في مؤسستك، واختار الـSchema والبيئة الصحيحة قبل تنفيذ SQL. سهولة المحرر لا تغير الصلاحيات ولا تجعل عمليات الإنتاج آمنة تلقائيًا.

للمراجعة السريعة، قارن تجربة الاستخدام مع SQL Workshop. وللتغييرات المتكررة، احفظ السكربتات في Source Control واتبع دورة النشر.

*تصحيح تحريري: اسم Workspace وUsername وPassword ليسوا وصفة دخول عامة لكل تثبيت SQL Developer Web.*

المراجع: [تكامل APEX 26.2](https://docs.oracle.com/en/database/oracle/apex/26.2/aeutl/using-restful-services.html) و[نموذج الدخول](https://docs.oracle.com/en/database/oracle/sql-developer-web/20.4/sdweb/about-sdw.html).