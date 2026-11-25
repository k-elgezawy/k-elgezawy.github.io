A search field can display the wrong answer even when every server response is valid. The user types a new term, its response arrives first, and an older response overwrites it later. My original LinkedIn post introduced a named replacement queue for this race.

This article adds a complete sample callback and an extra boundary: clearing the field must also invalidate the old result, even when clearing sends no request.

## Give related requests one stable queue

With `apex.server.process`, `queue.action: "replace"` makes older work on the same queue obsolete. Waiting requests can fail as `superseded`; an interrupted request can fail as `abort`. Those are expected transitions for this search, not reasons to interrupt the user with alerts. Use one stable name per independent search widget. [Oracle: server API](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/apex.server.html)

Do not generate a new queue name for every keystroke: those calls would no longer share a replacement boundary. Equally, two unrelated search widgets should not cancel each other's work.

## Create a complete development example

On a development page numbered 10, create a Text Field named `P10_SEARCH`. Add this markup to a Static Content region:

```html
<p id="product-search-result" role="status" aria-live="polite"></p>
```

Create a page Ajax Callback named `SEARCH_PRODUCTS` using the following PL/SQL. The three product names are synthetic; no application tables are read or changed. The callback checks input length again on the server, counts literal substring matches, and writes a structured response. `x01` is available as `apex_application.g_x01`. [Request parameters](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/apex.server.html#process)

```sql
DECLARE
    l_term  VARCHAR2(32767) := TRIM(apex_application.g_x01);
    l_count PLS_INTEGER := 0;
BEGIN
    IF LENGTH(l_term) > 60 THEN
        apex_json.open_object;
        apex_json.write('ok', FALSE);
        apex_json.write('error', 'Search term is too long');
        apex_json.close_object;
        RETURN;
    END IF;
    IF l_term IS NOT NULL THEN
        WITH products(product_name) AS (
            SELECT 'Notebook' FROM dual UNION ALL
            SELECT 'Pen' FROM dual UNION ALL
            SELECT 'Pencil' FROM dual
        )
        SELECT COUNT(*) INTO l_count
        FROM products
        WHERE INSTR(LOWER(product_name), LOWER(l_term)) > 0;
    END IF;
    apex_json.open_object;
    apex_json.write('ok', TRUE);
    apex_json.write('count', l_count);
    apex_json.close_object;
END;
```

Generate JSON with the package rather than concatenating unescaped text. In this example, a valid response for `pen` is an object with `ok: true` and `count: 2`. [Oracle: APEX_JSON](https://docs.oracle.com/en/database/oracle/apex/26.2/aeapi/APEX_JSON.html)

Add this helper to the page's Function and Global Variable Declaration attribute. Keep its generation counter outside `run`, so every invocation shares it:

```javascript
window.kgProductSearch = (function () {
    "use strict";
    let generation = 0;
    function run() {
        const token = ++generation;
        const output = document.getElementById("product-search-result");
        const term = String(apex.item("P10_SEARCH").getValue() || "").trim();
        if (!output) { return; }
        if (!term) {
            output.textContent = "Type a search term.";
            return;
        }
        if (term.length > 60) {
            output.textContent = "Use a shorter search term.";
            return;
        }
        output.textContent = "Searching...";
        apex.server.process("SEARCH_PRODUCTS", { x01: term }, {
            dataType: "json",
            queue: { name: "p10-product-search", action: "replace" }
        }).done(function (data) {
            if (token !== generation) { return; }
            if (!data || data.ok !== true ||
                    !Number.isInteger(data.count) || data.count < 0) {
                output.textContent = "Unexpected search response.";
                return;
            }
            output.textContent = term + ": " + data.count + " matches";
        }).fail(function (xhr, status) {
            if (token !== generation ||
                    ["abort", "superseded"].includes(status)) { return; }
            output.textContent = "Search failed. Please try again.";
        });
    }
    return { run: run };
}());
```

Create a Key Release Dynamic Action on `P10_SEARCH`, with an Execute JavaScript Code action containing the following call. Disable Fire on Initialization for this action. This demonstrates keyboard-driven search; extend the chosen event coverage if your interface also changes the value through other controls. [Oracle: creating Dynamic Actions](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/creating-and-editing-dynamic-actions.html)

```javascript
window.kgProductSearch.run();
```

The example's status strings are deliberately short English placeholders; translate them for your application's audience. Writing through `textContent` displays the term as text rather than interpreting it as HTML. [MDN: textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)

## Why a queue and a generation counter?

The counter describes the latest UI intent, including actions that do not call the server. Suppose a request for `pen` is still running when the user clears the field. The empty-field branch displays the prompt and returns. No replacement request is queued, so the counter prevents that earlier callback from restoring a stale count.

The same guard protects the local rejection of an overlong term. It also matters for a sequence such as `pen`, `note`, then `pen` again: matching the current text alone cannot distinguish the first `pen` request from the newest one. A unique invocation token can.

The sample checks the response shape before displaying a count. A transport failure and an application response with an invalid contract are separate paths; neither should silently look like zero matches. The promise failure callback follows the error-callback argument pattern. [jQuery Ajax callbacks](https://api.jquery.com/jQuery.ajax/)

## Verify the final state, not only the request count

In a test application, verify `pen` gives 2, `notebook` gives 1, and an absent substring gives 0. Under slow-network conditions, type successive terms, clear while a request is in flight, and enter more than 60 characters. The visible result should always belong to the latest invocation. Also check server failures and an unexpected response shape.

Debouncing reduces how frequently calls start; it does not prove that already-started requests cannot overlap. Treat rate control and stale-result handling as separate responsibilities.

Oracle also documents that the returned promise's `abort` method does not work when queue options are used; do not add manual promise cancellation as an assumed fix. More broadly, client cancellation is not a business transaction protocol. Use this pattern for replaceable lookups and previews. Protected data still needs server authorization, and saving needs its own consistency and retry design. [Oracle: promise and queue behavior](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/apex.server.html#process)

The references describe APEX 26.2. Validate the integration against your deployed version; this walkthrough does not claim the callback was executed in your application.

[Original LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7521498181541580800/)
