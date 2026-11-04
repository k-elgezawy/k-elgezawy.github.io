A status column can help readers scan an Oracle APEX Interactive Report quickly. My original LinkedIn example used a small HTML marker inside each row, then CSS to style the row containing that marker.

## Return a controlled status marker

The following illustrative query assumes a table named `demo_records` with `record_id` and `status_code`. Replace those names with your application's query. The status mapping emits a fixed set of HTML strings.

```sql
select record_id,
       case status_code
         when 'VALID' then
           '<span class="row-paint" data-state="valid">Valid</span>'
         when 'EXPIRED' then
           '<span class="row-paint" data-state="expired">Expired</span>'
         else
           '<span class="row-paint" data-state="review">Review</span>'
       end as status_badge
from demo_records
```

Set the computed `STATUS_BADGE` column to Plain Text and set Escape Special Characters to No so its generated markup can render. Keep ordinary data columns escaped. If you extend the expression to include user-entered text, escape that text for its output context before combining it with HTML. Oracle documents [HTML and attribute escaping](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/controlling-output-escaping-in-substitution-strings.html).

The visible words Valid, Expired, and Review give each row a readable status alongside its color.

## Scope the CSS to one report

Give the report region the Static ID `record_status_report`. Add these rules to your application stylesheet or the page's Inline CSS.

```css
#record_status_report tbody tr:has(.row-paint[data-state="valid"]) > td {
  background-color: #e4f5ea;
  color: #123b24;
}

#record_status_report tbody tr:has(.row-paint[data-state="expired"]) > td {
  background-color: #fbe9e7;
  color: #582018;
}
```

The `:has()` selector matches a row containing the corresponding marker. Applying the background to its cells helps the color appear over cell backgrounds supplied by the report template. MDN explains [the selector and browser support](https://developer.mozilla.org/en-US/docs/Web/CSS/:has).

The Review state keeps the report's normal styling. Adjust the palette for your theme and check contrast in every supported appearance.

## Verify the complete report experience

Test the two colored states and the fallback state. Change filters, sort columns, move between report pages, and refresh the report. The selector will match newly rendered rows when the marker remains in their markup.

Keep the status column in the report layouts that need this treatment. If users hide or exclude that column, verify whether the marker remains in the rendered DOM. Check keyboard focus, hover styling, small screens, and downloads as well. An export should communicate the status through readable values.

This pattern connects a controlled status value to presentation. Keep the underlying business decision in the query or application logic, and use the visible label to explain the color.
