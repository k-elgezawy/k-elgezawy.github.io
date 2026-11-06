A dashboard and its Excel download often serve different readers. The dashboard might show totals by month, while a reviewer needs one row per order. A dedicated export query gives that workbook its own columns, ordering, and rules without adding a second report region to the page.

## Build the workbook from a query

In a development APEX application, create a button that submits the page. Add a PL/SQL page process and restrict it to that button. Keep this download request separate from processes that save or change data. The example uses two synthetic orders from `DUAL`, so it needs no application tables.

```sql
declare
    l_query apex_exec.t_context;
    l_file  apex_data_export.t_export;
begin
    l_query := apex_exec.open_query_context(
        p_location => apex_exec.c_location_local_db,
        p_sql_query => q'[
            select 1001 as order_id, date '2026-01-15' as order_date,
                   125.50 as order_total
            from dual
            union all
            select 1002, date '2026-01-16', 78.00
            from dual
            order by order_id
        ]'
    );
    begin
        l_file := apex_data_export.export(
            p_context   => l_query,
            p_format    => apex_data_export.c_format_xlsx,
            p_file_name => 'sample-orders'
        );
    exception
        when others then
            apex_exec.close(l_query);
            raise;
    end;
    apex_exec.close(l_query);
    apex_data_export.download(p_export => l_file);
end;
```

The query context supplies typed rows. `APEX_DATA_EXPORT.EXPORT` builds the XLSX payload, and `DOWNLOAD` sends it as the response. Close the query context before calling `DOWNLOAD`; by default, the download stops the APEX engine. The inner exception handler releases the context if building the workbook fails, without intercepting normal download termination. See Oracle's references for [EXPORT](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/APEX_DATA_EXPORT-EXPORT-Function.html), [DOWNLOAD](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/APEX_DATA_EXPORT-DOWNLOAD-Procedure.html), and [closing the query context](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/APEX_EXEC.CLOSE-Procedure.html).

## Decide what users can export

- **Scope:** A standalone query does not inherit an Interactive Report's runtime filters. If the file follows page filters, pass their validated values as binds. If users expect the current report view, consider its native download instead.
- **Access:** Apply authorization to the page process and enforce row access in the query. Select only columns approved for the workbook. A hidden UI column is not an export permission.
- **Response:** Use a request that expects a file. A callback whose JavaScript expects JSON needs a different download flow.

## Test what the reviewer receives

Start with the two sample rows. Check the filename, column order, and that the totals are numeric. With your authorized development data, check an empty result, a restrictive filter, and two users with different scopes. Verify the workbook contents against the intended export rules, including any row limit, before enabling the button for users.

[Original LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7519513038740262912/)
