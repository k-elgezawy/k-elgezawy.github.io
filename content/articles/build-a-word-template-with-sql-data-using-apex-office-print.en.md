My LinkedIn post highlighted APEX Office Print (AOP) as a way to maintain document layouts with familiar Office templates. A small order document makes the workflow concrete. Its data query defines the values, while a Word template places those values on the page.

## Define a small data contract

Start in a development application with the AOP plug-in installed and an appropriately licensed AOP service configured. AOP combines structured data and a template on its rendering server. The vendor documents its deployment options and licensing. [AOP overview](https://www.apexofficeprint.com/docs/)

This illustrative query uses synthetic values from `DUAL`. It returns a document filename, a `data` cursor containing the order header, and a nested `lines` cursor.

```sql
select
    'demo-order' as "filename",
    cursor(
        select
            1001 as "order_no",
            'Demo Customer' as "customer_name",
            cursor(
                select 'Planning session' as "description",
                       2 as "quantity", 75 as "unit_price"
                from dual
                union all
                select 'Review session', 1, 50 from dual
            ) as "lines"
        from dual
    ) as "data"
from dual
```

The quoted aliases preserve the lowercase names used by the template. Keep the query and template field names aligned. The `data` cursor provides the document's root values, and the nested cursor supplies the repeating records. [SQL structure](https://www.apexofficeprint.com/docs/getting-started/sql-structure/)

## Put the matching tags in Word

Create a DOCX file and add the following tags as ordinary document text. Apply Word styles to the heading and paragraphs around them.

```text
Order {order_no}
Customer {customer_name}

{#lines}
{description} | Quantity {quantity} | Unit price {unit_price}
{/lines}
```

The loop repeats the enclosed content for each line. Keep tag spelling and case consistent with the SQL aliases. Once this simple paragraph version works, adapt the layout to a table using the vendor's DOCX guidance. [DOCX template tags](https://www.apexofficeprint.com/docs/templates/templates-docx/)

## Connect and review the output

Upload the template as an APEX Static Application File. In the AOP Dynamic Action, select that template source, enter its filename, choose SQL as the data type, and supply the query. Choose the required output format, such as PDF, then invoke the action from your print button. Attribute labels can vary with the installed plug-in version. [AOP Dynamic Action settings](https://www.apexofficeprint.com/docs/apex-plugins/aop-da/)

Check that order 1001 and both lines appear. Test a long description, an empty lines collection, and an Arabic layout before using real data. With application tables, enforce document access and row authorization in the data path. Select the destination service according to the information the document contains.

Keep the template version alongside the data contract. A heading change can stay in the template. Adding a new tag requires a corresponding value in the query and another output review.

[Original LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7490663722621833216/)
