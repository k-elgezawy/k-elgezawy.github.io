For an expense form with repeated travel lines, Alpine.js can manage row editing while APEX handles server processing. My original example used a modal dialog, a static-content region, and P10_LINES_JSON to carry dates, descriptions, transport types, and costs.

### Keep the browser state synchronized

Inside an Alpine component, watch its rows and serialize them to the APEX item:

```javascript
this.$watch('rows', value => {
  apex.item('P10_LINES_JSON')
    .setValue(JSON.stringify(value));
});
```

Alpine's watcher already observes nested changes; the original extra `{ deep: true }` option is unnecessary. [Alpine: $watch](https://alpinejs.dev/magics/watch).

**Editorial correction:** updating a hidden item does not save business data or automatically update server session state. Submit it with the page or explicitly send it through an AJAX request, then run an authorized persistence process. Display “saved” only after that process succeeds. [APEX: item API](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/item.html).

### Validate before persistence

JSON_TABLE can project submitted JSON into relational columns. Select deliberate error handling; parsing does not replace checks for required fields, valid dates, permitted transport values, nonnegative costs, and payload size. Recalculate authoritative totals on the server. [Oracle: JSON_TABLE](https://docs.oracle.com/en/database/oracle/oracle-database/26/sqlrf/JSON_TABLE.html).

Verify request ownership and every submitted line ID, and detect concurrent changes with a version check. Persist validated changes within the intended transaction.

*Further correction: replacing all rows with delete-plus-insert is not a universally safe duplicate-prevention strategy. It can disrupt identities, references, auditing, and concurrent edits. Choose persistence rules for the actual data model.*

Interactive Grid remains a valid option. A custom form earns its additional code when the required interaction justifies it.