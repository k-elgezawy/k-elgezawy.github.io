QUALIFY بتسهل التعبير عن مهمة متكررة في التقارير: فلترة الصفوف بعد حساب Analytic Function. الخاصية موثقة في Oracle AI Database 26ai؛ تأكد من دعمها في إصدار قاعدة البيانات اللي تطبيق APEX عندك بيستخدمه فعليًا.

### موظف واحد لكل قسم

نفترض إن EMPNO فريد. المثال بيختار أعلى راتب غير فارغ في كل قسم، ويحسم تساوي الرواتب برقم الموظف:

```sql
select empno, deptno, sal,
       row_number() over (
         partition by deptno
         order by sal desc nulls last, empno
       ) as rn
from emp
qualify rn = 1;
```

حسم التعادل مهم؛ من غير ترتيب حتمي، تساوي الرواتب ممكن ينتج اختيارًا غير محدد. لو كل الرواتب في قسم فارغة، الاستعلام يظل يختار موظفًا واحدًا. ولو المطلوب كل الموظفين المتعادلين في أعلى راتب، اختار طريقة ترتيب تحتفظ بالتعادل. [توثيق ROW_NUMBER](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/ROW_NUMBER.html).

### احتفظ بالبديل المتوافق

لو الإصدار لا يدعم QUALIFY، ضع الحساب في استعلام داخلي:

```sql
select empno, deptno, sal, rn
from (
  select empno, deptno, sal,
         row_number() over (
           partition by deptno
           order by sal desc nulls last, empno
         ) as rn
  from emp
)
where rn = 1;
```

QUALIFY تُقيّم بعد الحسابات التحليلية، بينما WHERE بتفلتر الصفوف الداخلة للحساب. ولا واحد من الاستعلامين يضمن ترتيب العرض النهائي بدون ORDER BY خارجي. [توثيق SELECT وQUALIFY](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/SELECT.html).

*تصحيح تحريري: البوست الأصلي نسب الدعم بشكل عام إلى “23ai” وادعى سرعة أعلى. النسخة دي تعتمد على توثيق 26ai المتحقق منه. قِصر الاستعلام لا يثبت إن خطة تنفيذه أسرع.*