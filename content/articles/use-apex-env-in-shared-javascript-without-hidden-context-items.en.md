A shared JavaScript file often needs to know which APEX page is running or where an application image lives. Creating hidden items just to repeat that framework context adds another set of values to maintain.

My original LinkedIn post introduced `apex.env`. This walkthrough turns that idea into a small shared helper with explicit initialization, predictable types, and a clear boundary between browser behaviour and server decisions.

## Read the context with its documented types

Oracle documents `APP_ID`, `APP_PAGE_ID`, and `APP_FILES` as strings in `apex.env`. The object has been available since APEX 21.2; the reference linked here describes 26.2. Check the documentation matching your deployed version. [Oracle JavaScript API](https://docs.oracle.com/en/database/oracle/apex/26.2/aexjs/apex.html#env)

For a focused development check on an APEX application page, inspect only the values you need:

```javascript
console.table({
    pageId: apex.env.APP_PAGE_ID,
    pageIdType: typeof apex.env.APP_PAGE_ID,
    filesBase: apex.env.APP_FILES
});
```

On page 10, expect `pageId` to be the string `"10"` and `pageIdType` to be `"string"`. The asset path depends on the application. A strict comparison with the number `10` therefore fails; compare with `"10"` deliberately. Avoid copying a full environment dump into support tickets or shared logs, especially session identifiers and user information.

## Build a small shared helper

In a development application, upload an illustrative `company-logo.svg` to Static Application Files. Add this markup to a Static Content region on a test page:

```html
<p id="page-context"></p>
<img id="company-logo" alt="Company logo" width="120" height="40">
<p id="dashboard-help" hidden>Dashboard-specific help.</p>
```

Create `page-context-demo.js` with the following content:

```javascript
window.kgPageContextDemo = (function () {
    "use strict";

    function init() {
        const env = apex.env;
        const badge = document.getElementById("page-context");
        const logo = document.getElementById("company-logo");
        const help = document.getElementById("dashboard-help");

        if (badge) {
            badge.textContent =
                "App " + env.APP_ID + " / Page " + env.APP_PAGE_ID;
        }
        if (logo) {
            logo.src = env.APP_FILES + "company-logo.svg";
        }
        if (help) {
            help.hidden = env.APP_PAGE_ID !== "10";
        }
    }

    return { init: init };
}());
```

The checks for missing elements let another page load the same file without needing the demonstration region. The helper writes plain text through `textContent`, so it does not interpret the badge value as HTML. [MDN: textContent](https://developer.mozilla.org/en-US/docs/Web/API/Node/textContent)

The file reads the current context when `init` runs. It constructs the image path from APEX's application-file prefix, rather than embedding a workspace-specific path. Keep the file name aligned with the uploaded asset and verify the resulting request in the browser's Network panel.

## Load the file, then initialize the page

Upload the JavaScript file to Static Application Files and use its displayed Reference URL. In the test page's JavaScript File URLs, that reference can be:

```text
#APP_FILES#page-context-demo.js
```

To share it application-wide, use the JavaScript File URLs setting in User Interface Attributes. Copy the Reference value that APEX supplies, including any relevant minification substitution, and avoid including the same file both globally and again on the page. [Oracle: shared helper files](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/including-helper-functions-all-pages.html)

In the test page's Execute When Page Loads attribute, call:

```javascript
window.kgPageContextDemo.init();
```

Oracle distinguishes loading JavaScript files, declaring functions, and executing page-load code. Calling the helper after the page is initialized keeps DOM access out of the file's top-level loading phase. [Page JavaScript attributes](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/editing-page-attributes-in-page-designer.html)

## Verify the behaviour and its limits

On page 10, the badge should identify the current application and page, the image should load, and the help text should appear. On another test page, the help should remain hidden. On a page without the region, the element checks should avoid missing-element errors.

If a partial refresh replaces this region's DOM, call the helper again from the relevant refresh handling; the original page-load call does not initialize newly replaced elements. This helper adds no event listeners, so repeating its assignments does not stack handlers.

Use this context for presentation and asset references. Browser values and visibility choices are not permission checks; validate protected operations and data access on the server. Keep genuine business items when they represent input or server-side state. These examples show an expected integration pattern, not a claim that code was executed against your application.

[Original LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7521843410698399744/)
