Repeating :APP_USER in every form is easy to forget. For application-owned tables, a database column default can provide a consistent starting point for recording who created a row.

The expression is:

```sql
sys_context('APEX$SESSION', 'APP_USER')
```

APEX sets up this context while processing a request. A CREATED_BY column can use the expression as its default, so an insert that omits the column can receive the current APEX username.

### Know what a default does

A normal default applies when the column is omitted or DEFAULT is specified. It does not prevent a caller from explicitly supplying a different value, and it does not automatically maintain UPDATED_BY. An explicit NULL also needs separate consideration; DEFAULT ON NULL is a different database feature.

### Plan for non-APEX writers

A scheduled job, integration, or SQL client may have no APEX user context. Decide how those paths establish an auditable actor. Do not silently label every background change as an interactive user.

For stronger audit requirements, control write privileges and enforce the policy in a trusted database layer. Test an APEX insert, a non-APEX insert, an explicit value, and an update in a development schema.

The goal is less repeated page configuration, with a clear understanding of the boundary between a convenient default and a protected audit trail.

Reference: [Oracle: understanding authentication and APP_USER](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/understanding-authentication.html).