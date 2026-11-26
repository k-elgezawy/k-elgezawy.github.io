An Interactive Report can answer several business questions without becoming several separate pages. My original LinkedIn post compared Control Break, Group By, and Pivot. The important starting point comes before choosing any of them: **what does one source row represent?**

Here is a small, reproducible reporting exercise. It includes expected totals and a join trap that can produce a convincing but incorrect summary. All names and amounts are synthetic; the queries read constants from `DUAL` and change no business data.

## Start with one row per invoice

In a development application, create an Interactive Report region with this SQL source:

```sql
WITH invoices(invoice_id, branch, invoice_date, sales, cost) AS (
    SELECT 1001, 'North', DATE '2026-01-05', 120, 80 FROM dual UNION ALL
    SELECT 1002, 'North', DATE '2026-01-15',  80, 60 FROM dual UNION ALL
    SELECT 1003, 'South', DATE '2026-01-20', 150,110 FROM dual UNION ALL
    SELECT 1004, 'North', DATE '2026-02-05', 100, 70 FROM dual UNION ALL
    SELECT 1005, 'South', DATE '2026-02-12', 130, 90 FROM dual UNION ALL
    SELECT 1006, 'South', DATE '2026-02-20',  70, 40 FROM dual
)
SELECT invoice_id,
       branch,
       invoice_date,
       TO_CHAR(invoice_date, 'YYYY-MM') AS month_label,
       sales,
       cost,
       sales - cost AS margin
FROM invoices
```

The six source rows represent six complete invoices. `MARGIN` is an amount, not a percentage. All amounts use one assumed currency and all costs are known. A real report needs explicit rules for currency conversion, returns, and missing costs before its totals are meaningful.

Leave numeric columns numeric and apply display formatting in column attributes. Use `MONTH_LABEL` for the demonstration's month selection. Including the year avoids combining January from different years. [Oracle: report column attributes](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/managing-interactive-report-column-attributes.html)

In the region's Actions Menu attributes, enable Control Break, Aggregate, Group By, Pivot, Filter, and Save Report as appropriate. Developers control which capabilities are available. [Oracle: Actions menu configuration](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/customizing-the-interactive-report-actions-menu.html)

## Choose the view that matches the question

**Control Break answers: which invoices belong to each branch?** Enable a break on `BRANCH`, keeping the detailed invoice rows. Add Sum aggregates on `SALES`, `COST`, and `MARGIN`. You should still be able to inspect the six invoices beneath their branch headings. [Oracle: Control Break](https://docs.oracle.com/en/database/oracle/apex/26.1/aeeug/creating-control-break.html)

**Group By answers: how much did each branch contribute?** Select `BRANCH` as the grouping column, Sum for the three amounts, and Count on the non-null `INVOICE_ID`. The expected summary is:

| Branch | Invoice count | Sales | Cost | Margin |
|---|---:|---:|---:|---:|
| North | 3 | 300 | 210 | 90 |
| South | 3 | 350 | 240 | 110 |

Here the count means invoices because the source grain is one invoice. That interpretation would change if the query returned invoice lines. [Oracle: Group By](https://docs.oracle.com/en/database/oracle/apex/26.1/aeeug/grouping-columns.html)

**Pivot answers: how do branch sales compare across months?** Set the row column to `BRANCH`, the pivot column to `MONTH_LABEL`, and the function to Sum of `SALES`. Expected cells are:

| Branch | 2026-01 | 2026-02 |
|---|---:|---:|
| North | 200 | 100 |
| South | 150 | 200 |

Pivot changes the arrangement used for comparison; it cannot repair duplicated source amounts. [Oracle: Pivot reports](https://docs.oracle.com/en/database/oracle/apex/26.1/aeeug/managing-pivot-reports.html)

These user-guide workflows reference 26.1; the developer settings reference 26.2. The 26.2 report experience was refreshed, so use the named operations and check the layout in your deployed version. [Oracle: 26.2 report changes](https://blogs.oracle.com/apex/whats-new-in-interactive-reports-and-ai-interactive-reports)

## Reconcile after changing filters

Without filters, the six invoices total sales 650, cost 450, and margin 200. Filtering `MONTH_LABEL` to `2026-02` should leave three invoices, sales 300, cost 200, and margin 100. Switching between details, grouping, and pivot should preserve the intended filtered population.

Save a private view named “February branch review” if that option is available to your authenticated user. Treat it as a saved report definition, not a historical copy of the underlying records. Clear or reset the filter deliberately before checking the all-month totals again. A hidden filter can make two otherwise-correct summaries appear inconsistent.

## A join can break every view at once

This separate example contains two invoices worth 100 each. The first invoice has two lines. Predict the totals before running the read-only query:

```sql
WITH invoices(invoice_id, invoice_total) AS (
    SELECT 1, 100 FROM dual UNION ALL
    SELECT 2, 100 FROM dual
), invoice_lines(invoice_id, line_id) AS (
    SELECT 1, 11 FROM dual UNION ALL
    SELECT 1, 12 FROM dual UNION ALL
    SELECT 2, 21 FROM dual
)
SELECT SUM(i.invoice_total) AS repeated_total,
       SUM(DISTINCT i.invoice_total) AS distinct_amount_total,
       COUNT(DISTINCT i.invoice_id) AS invoice_count
FROM invoices i
JOIN invoice_lines l ON l.invoice_id = i.invoice_id
```

Expected output is `REPEATED_TOTAL = 300`, `DISTINCT_AMOUNT_TOTAL = 100`, and `INVOICE_COUNT = 2`. The correct invoice total is 200.

The join repeats the first header amount. `SUM(DISTINCT invoice_total)` also fails: it removes equal amounts, not duplicate invoice identities. A distinct invoice count can be correct while the monetary sum is wrong. Oracle documents that aggregate `DISTINCT` operates on distinct argument values. [Oracle: aggregate semantics](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/Aggregate-Functions.html)

Keep invoice-level amounts at invoice grain. If lines are needed only to select eligible invoices, consider an `EXISTS` filter; if line measures are needed, aggregate them to the required grain before joining. Then reconcile keys and amounts against a known population.

Use a new page when the underlying question, authorization, or data contract actually differs. For alternate analytical presentations of the same permitted rows, start by making the source grain reliable, then choose the reporting view. The SQL results above are expected values checked by arithmetic, not a claim of execution in your APEX application.

[Original LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7517515074228383744/)
