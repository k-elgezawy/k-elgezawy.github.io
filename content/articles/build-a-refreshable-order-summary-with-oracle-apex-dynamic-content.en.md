A purchase-order summary can need a layout that follows the business process. My original LinkedIn post used Oracle APEX Dynamic Content to combine a selected order's details with custom HTML. This walkthrough starts with a small summary showing customer, total, and status.

## Return HTML as a CLOB

On a development page, add a Select List named `P10_ORDER_ID` with values `1001` and `1002`. Create a **Dynamic Content** region, set its Static ID to `order_summary`, and use a PL/SQL function body returning a CLOB as its source. Match the item name to your actual page if you use another page number.

The region returns its constructed HTML to APEX. Oracle describes the CLOB source and CSS-class approach in its Dynamic Content guide. [Dynamic Content](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/dynamically-formatting-data.html)

The example query uses two synthetic rows from `DUAL`. Paste this function body into the region source.

```sql
declare
    l_customer varchar2(200);
    l_total    number;
    l_status   varchar2(30);
begin
    select customer_name, order_total, order_status
      into l_customer, l_total, l_status
      from (
          select '1001' as order_id,
                 'Sample <Customer>' as customer_name,
                 125.50 as order_total,
                 'Ready' as order_status
            from dual
          union all
          select '1002', 'Second Customer', 78, 'In review'
            from dual
      )
     where order_id = :P10_ORDER_ID;

    return to_clob(
        '<article class="order-summary"><h3>Order summary</h3><dl>'
    )
        || '<dt>Customer</dt><dd>'
        || apex_escape.html(l_customer) || '</dd>'
        || '<dt>Total</dt><dd>'
        || apex_escape.html(to_char(
               l_total, 'FM999990D00',
               'NLS_NUMERIC_CHARACTERS=''.,'''
           )) || '</dd>'
        || '<dt>Status</dt><dd>'
        || apex_escape.html(l_status) || '</dd>'
        || '</dl></article>';
exception
    when no_data_found then
        return to_clob('<p>Select an available demo order.</p>');
end;
```

The customer name deliberately contains angle brackets so you can check that they appear as text. Values inserted into HTML text nodes pass through `APEX_ESCAPE.HTML`. Keep attribute and URL handling specific to their own output contexts when extending the markup. [HTML escaping](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/HTML-Function.html)

## Send the selected value when refreshing

Add `P10_ORDER_ID` to the region's **Page Items to Submit** property, without a colon. Create a Dynamic Action on the item's Change event, with a Refresh action targeting the summary region. This sends the current selection to the server during the refresh request. [Items to submit](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/configure-items-submit-and-return.html)

## Style and check the summary

Place these rules in the page's Inline CSS or the application's stylesheet.

```css
#order_summary .order-summary {
  padding: 1rem;
  border: 1px solid currentColor;
  border-radius: 0.75rem;
}
#order_summary .order-summary dl {
  display: grid;
  grid-template-columns: minmax(6rem, 1fr) minmax(0, 2fr);
  gap: 0.5rem 1rem;
}
#order_summary .order-summary dd {
  margin: 0;
  overflow-wrap: anywhere;
}
```

Switch between both demo orders and verify that the customer, total, and status change together. Check the empty-selection message, narrow screens, keyboard operation, and an Arabic page direction. Keep the status readable as text.

When replacing the synthetic rows with application data, apply row access rules in the query and authorize access to the region. Use translated text messages for the headings and labels in a multilingual application. Review the rendered HTML after each change to the data or layout.

[Original LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7516717117732401154/)
