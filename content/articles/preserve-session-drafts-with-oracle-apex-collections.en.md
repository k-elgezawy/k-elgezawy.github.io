A multi-step form needs somewhere to hold rows while the user reviews them. My original LinkedIn post introduced APEX Collections for this job. The detail that matters in practice is the draft's lifecycle: creating, revisiting, editing, and finally submitting it.

Treat a collection as temporary APEX-managed session data. Its SQL interface is the database view `APEX_COLLECTIONS`; do not design around assumptions of purely browser memory or zero database work. Use persistent draft tables when a request must survive beyond its session or be reviewed by another user. [Oracle: using collections](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/about-using-collections.html)

## Initialize without resetting on refresh

For a development demonstration, add a page process that initializes the following uniquely named collection. The sample uses synthetic products and assumes normal, sequential page requests in an active APEX application session.

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

`COLLECTION_EXISTS` checks the current user, session, and application. `CREATE_COLLECTION` normally raises an error if that collection already exists. This guard preserves the existing draft when the process is visited again. It is not a concurrency lock: coordinate simultaneous initialization requests in your application. [Existence check](https://docs.oracle.com/en/database/oracle/apex/24.2/aeapi/COLLECTION_EXISTS-Function.html), [creation API](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/CREATE_COLLECTION-Procedure.html)

Keep an explicit “Start again” action separate from routine rendering. Calling a truncate/reset operation on every render defeats the draft's purpose. Keep initialization separate from an “Add product” action, which needs its own duplicate-submission rules.

## Read typed attributes with meaningful aliases

In a Classic Report, use:

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

The mapping is part of your application contract: `C001` means product name, `N001` quantity, and `N002` unit price. Document it in a small package when several pages share it. Keep numbers in numeric attributes and retain normal text escaping in reports. Oracle documents the typed attributes and collection query pattern. [Key concepts](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/key-collections-concepts.html)

For a newly initialized collection, the expected rows are:

```text
SEQ_ID  PRODUCT_NAME  QUANTITY  UNIT_PRICE  LINE_TOTAL
1       Notebook     2         12.50       25.00
2       Pen          3          2.00        6.00
```

The total is 31.00; actual decimal formatting follows your report settings. Refreshing the page should retain those two rows rather than append another pair.

## Update one attribute without clearing its neighbours

On an explicit development test action, change the first row's quantity:

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

The numeric overload changes `N001`; the product and unit price remain intact. The expected Notebook line total becomes 50.00 and the overall total 56.00. A missing member raises an error. [Numeric attribute update](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/UPDATE_MEMBER_ATTRIBUTE-Procedure-Signature-5.html)

This differs from `UPDATE_MEMBER`, which nullifies attributes you do not supply. That distinction can explain why changing a quantity unexpectedly erases a description or price. [Member replacement semantics](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/UPDATE_MEMBER-Procedure.html)

## Define the boundary of the draft

Browser tabs sharing the same application session can reach the same named collection. For independent drafts, use a server-managed draft identifier and consistent ownership checks; a fixed collection name is not a per-tab isolation mechanism.

Do not assume `SEQ_ID` is a permanent business identifier. Deletion can leave gaps and resequencing can change IDs. For an editable grid, follow Oracle's guidance to store a stable row key in a collection attribute. [Sequence behaviour](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/RESEQUENCE_COLLECTION-Procedure.html), [grid guidance](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/key-collections-concepts.html)

Before final submission, validate quantity ranges, product access, and current prices on the server. Save accepted data through a deliberate business transaction and clear the temporary draft only after the save succeeds. Test refreshes, two tabs, an expired session, missing rows, and a failed final save. These examples explain expected behaviour; they do not claim execution against an application or measured performance results.

[Original LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7405717744706486272/)
