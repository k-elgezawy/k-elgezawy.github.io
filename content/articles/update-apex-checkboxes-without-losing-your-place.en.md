A checkbox in a long report should save its change without sending the user back to the top. A reliable implementation needs both a secure callback and deliberate refresh behavior.

### Define the update contract

Send the row identifier, requested state, and expected row version to an authorized Ajax callback. On the server, validate the state, enforce access to that specific row using trusted identity, and reject stale versions. Checking the identifier alone is insufficient.

Disable repeated edits while saving. Return explicit success or an actionable failure; restore the old checkbox state when saving fails. Use declarative controls or properly escaped rendering rather than concatenating untrusted values into HTML.

### Restore after the region refresh

For a report that emits `apexafterrefresh`, register restoration before refreshing. This fragment belongs in the successful-save handler; `tasks` is the region's Static ID:

```javascript
const y = window.scrollY;
apex.jQuery("#tasks").one("apexafterrefresh", function () {
  requestAnimationFrame(() => window.scrollTo(0, y));
});
apex.region("tasks").refresh();
```

Serialize saves and refreshes so unrelated refreshes cannot consume this handler. For a scrollable container, capture its `scrollTop` instead. Reapply status styling after refresh, include text labels alongside colors, and restore keyboard focus where practical.

*Editorial correction: the original callback lacked row authorization and concurrency checks. Its scroll functions were not connected to refresh completion, and one global localStorage key could mix unrelated pages.*

References: [Ajax process API](https://docs.oracle.com/en/database/oracle/apex/24.2/aexjs/apex.server.html), [refresh events](https://docs.oracle.com/en/database/oracle/apex/24.2/aexjs/apex.html), and [region refresh](https://docs.oracle.com/en/database/oracle/apex/24.2/aexjs/region.html).