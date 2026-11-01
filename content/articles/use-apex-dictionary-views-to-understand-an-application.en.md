Opening every page is a slow way to answer “where is this item used?” APEX dictionary views expose application metadata that you can query for inventories, reviews, and documentation.

Start with Application → Utilities → Oracle APEX Views. Select a view, inspect its available columns, and copy the generated query. Oracle also provides `APEX_DICTIONARY` to discover the available views. [Oracle's walkthrough](https://docs.oracle.com/en/database/oracle/apex/24.2/htmdb/accessing-apex-views.html).

### Build a focused inventory

This read-only example lists item definitions:

```sql
select page_id, item_name, display_as
from apex_application_page_items
where application_id = :APP_ID
order by page_id, item_name;
```

In an APEX application, `:APP_ID` supplies the current application identifier. In a standalone SQL tool, bind an explicit identifier and establish the appropriate workspace context. The named columns also appear in [Oracle's metadata example](https://www.oracle.com/ocom/groups/public/%40otn/documents/webcontent/301715.html); confirm the installed release through the view browser.

Then inspect region, button, process, and dynamic-action views. Group findings by application and page. Look for unexpected component names, obsolete references, or repeated logic worth reviewing.

An item inventory does not prove every dependency. Dynamic SQL, generated JavaScript, plug-ins, and external services may require additional investigation. Likewise, a missing page-level authorization value is a review signal, not proof that the page is unprotected.

*Editorial clarification: metadata queries support analysis, but do not constitute a complete dependency or security audit.*

Keep reusable review queries in source control and compare results when application structure changes.