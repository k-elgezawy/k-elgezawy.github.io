QUALIFY makes a familiar reporting task easier to express: filtering rows after an analytic function has been evaluated. Oracle AI Database 26ai documents this clause; verify support in the database release your APEX application actually uses.

### One employee per department

Assume EMPNO is unique. This example picks the highest non-null salary in each department, breaking salary ties by employee number:

```sql
select empno, deptno, sal,
       row_number() over (
         partition by deptno
         order by sal desc nulls last, empno
       ) as rn
from emp
qualify rn = 1;
```

The tie-breaker matters. Without a deterministic ordering, equal salaries can produce an arbitrary winner. If every salary in a department is null, this query still selects one employee. If the requirement is to return all tied highest salaries, choose a ranking strategy that preserves ties instead. [Oracle: ROW_NUMBER](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/ROW_NUMBER.html).

### Keep the compatible alternative

On a database without QUALIFY, put the analytic calculation in an inner query:

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

QUALIFY is evaluated after analytic calculations; WHERE filters their input rows. Neither query promises a final display order without an outer ORDER BY. [Oracle: SELECT and QUALIFY](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/SELECT.html).

*Editorial correction: the original post broadly attributed support to “23ai” and claimed faster execution. This revision uses the verified 26ai documentation. Shorter SQL is not evidence of a faster execution plan.*