A batch job can finish without an exception while quietly skipping its last records. My original LinkedIn post described one cause: testing a bulk cursor's `%NOTFOUND` before using the rows that its latest fetch returned.

The useful review question is simple: **did we process the current collection before deciding that the cursor is finished?** This walkthrough makes that question observable with synthetic IDs, counts, and a checksum.

## The last fetch can still contain work

For 1,075 rows and a fetch limit of 500, the useful groups are 500, 500, and 75. An early exit can discard that final group. Oracle's development guide explains why a counter-based exit avoids this problem. [Oracle Database Development Guide](https://docs.oracle.com/en/database/oracle/oracle-database/26/adfns/database-development-guide.pdf)

This ordering is the problem:

```sql
FETCH c_orders BULK COLLECT INTO l_ids LIMIT 500;
EXIT WHEN c_orders%NOTFOUND;
-- Work on l_ids would happen too late here.
```

`%NOTFOUND` itself is not forbidden. Oracle's bulk-fetch example processes the collection and checks that attribute afterward. Here, we instead exit on an empty collection before processing it. [Oracle: bulk-fetch examples](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/bulk-sql-and-bulk-binding.html)

## A complete experiment without business tables

Run the following block in a development session with DBMS Output enabled. It reads generated numbers from `DUAL`; it creates no tables and performs no business-data changes. It is an illustrative experiment with expected results, not a claim of execution in your database.

The cursor creates at most 1,075 candidate IDs, then filters them. That outer filter makes the zero-row case explicit. Every case uses a batch size of 500.

```sql
DECLARE
    PROCEDURE check_case(p_rows PLS_INTEGER) IS
        CURSOR c_ids IS
            SELECT order_id
            FROM (
                SELECT LEVEL AS order_id
                FROM dual
                CONNECT BY LEVEL <= 1075
            )
            WHERE order_id <= p_rows
            ORDER BY order_id;
        TYPE id_list IS TABLE OF NUMBER;
        l_ids      id_list;
        l_seen     PLS_INTEGER := 0;
        l_sum      NUMBER := 0;
        l_expected NUMBER := p_rows * (p_rows + 1) / 2;
    BEGIN
        OPEN c_ids;
        LOOP
            FETCH c_ids BULK COLLECT INTO l_ids LIMIT 500;
            EXIT WHEN l_ids.COUNT = 0;
            IF p_rows = 1075 THEN
                DBMS_OUTPUT.PUT_LINE('batch=' || l_ids.COUNT);
            END IF;
            FOR i IN 1 .. l_ids.COUNT LOOP
                l_seen := l_seen + 1;
                l_sum := l_sum + l_ids(i);
            END LOOP;
        END LOOP;
        CLOSE c_ids;
        IF l_seen <> p_rows OR l_sum <> l_expected THEN
            RAISE_APPLICATION_ERROR(-20001, 'Count/checksum mismatch');
        END IF;
        DBMS_OUTPUT.PUT_LINE(
            'rows=' || p_rows || ', seen=' || l_seen || ', sum=' || l_sum
        );
    EXCEPTION
        WHEN OTHERS THEN
            IF c_ids%ISOPEN THEN
                CLOSE c_ids;
            END IF;
            RAISE;
    END;
BEGIN
    check_case(0);
    check_case(1);
    check_case(499);
    check_case(500);
    check_case(501);
    check_case(1000);
    check_case(1075);
END;
/
```

The zero-row fetch is normal termination, not a `NO_DATA_FOUND` case to catch. A subsequent bulk fetch replaces the previous batch. [Oracle: FETCH statement](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/FETCH-statement.html)

## Check boundaries, then check identity

Expected final values are:

| Input rows | Seen rows | Sum of IDs |
|---:|---:|---:|
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| 499 | 499 | 124750 |
| 500 | 500 | 125250 |
| 501 | 501 | 125751 |
| 1000 | 1000 | 500500 |
| 1075 | 1075 | 578350 |

The last case should also print `batch=500`, `batch=500`, and `batch=75`. Its final empty fetch produces no batch line. In a separate copy, run only `check_case(1075)` and replace the collection-count exit with the early `%NOTFOUND` exit: that case should fail its assertion after counting only 1,000 IDs. Running all the cases with the broken exit would stop at an earlier failing case.

Count plus checksum is a stronger demonstration than count alone, but it is not proof of exact identity for arbitrary data. A real reconciliation should compare stable business keys and outcomes. Also distinguish the current batch's `COUNT` from the cursor's cumulative `%ROWCOUNT`. [Oracle: cursor attributes](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/cursors-overview.html)

## Carry the lesson into a real batch

Before adding DML, decide whether one SQL statement can express the operation. When procedural work is necessary, keep fetching, processing, and transaction ownership explicit. A fetch limit is not a commit policy or a cap on the entire job's memory usage; review record width, other retained collections, and the workload.

If you add `FORALL`, do not assume that fetched IDs equal affected rows. An update matching no row needs reconciliation too. Inspect `SQL%BULK_ROWCOUNT`; use appropriate bounds if the collection becomes sparse. `SAVE EXCEPTIONS` allows remaining executions to continue, but still requires deliberate error handling and a decision about successful changes. [Oracle: FORALL statement](https://docs.oracle.com/en/database/oracle/oracle-database/26/lnpls/FORALL-statement.html)

Keep transaction and restart design separate from this fetch-loop experiment. A reliable job accounts for every selected key, including the final small batch.

[Original LinkedIn post](https://www.linkedin.com/posts/karim-el-gezawy-460752219_plsql-oracledatabase-sql-activity-7527866844540649472-Ii0c)
