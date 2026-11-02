Changing Compatibility Mode in Oracle APEX deserves a review, even when the application already runs on a newer APEX installation. My original LinkedIn post focused on that decision: prepare a recoverable copy, inspect the application, and test the user journeys before changing runtime behavior.

## Understand what you are changing

Compatibility Mode controls selected runtime behavior for an application. It is separate from the installed APEX release, the Universal Theme version, and the application’s own version label. Oracle documents mode changes by release; newer modes include earlier compatibility changes. Review the [release-specific behavior notes](https://docs.oracle.com/en/database/oracle/apex/26.2/htmrn/changed-behavior.html) rather than assuming that every JavaScript or visual difference is caused by this setting.

## Build a review sequence

1. **Capture a baseline.** Keep an application export or source revision and record the existing mode. Preserve related deployment information needed to reproduce the application. An application export is not a backup of all business data or external services.
2. **Use a development copy.** Establish how the important journeys behave before changing anything. A list of page numbers is less useful than a list of tasks users must complete.
3. **Inspect the available upgrades.** In Utilities → Upgrade Application, review the offered component changes individually. Treat the wizard as a targeted migration tool, not proof that every customization is compatible.
4. **Review theme and custom code separately.** Check the Universal Theme and application JavaScript against the target release. Keep these changes distinguishable so a regression can be traced to its cause.
5. **Change the mode deliberately.** In Application Definition → Definition → Properties, select the reviewed Compatibility Mode. Repeat the same journeys and compare the results with the baseline.

Oracle’s [application upgrade guide](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/upgrading-apex-applications.html) explains the component-upgrade and compatibility-setting paths. The practical goal is evidence that the application still works, not simply a newer setting value.

## Test outcomes, not only page rendering

For example, take one request from creation through validation, save, review, and approval. Check required fields, LOV selections, Dynamic Actions, dialogs, report filters, downloads, and access rules relevant to that journey. Include cancellation and rejected input. Record expected and observed outcomes, with enough detail to investigate a difference.

These are proposed checks, not claims that every listed component changes with each compatibility mode.

## Update the checking tools too

My earlier post recommended Advisor. There is an important release-specific update: APEX Advisor is deprecated in APEX 26.2. Oracle points to enhanced APEXlang quality and security checks in SQLcl 26.3.0 CODESCAN. See the [official deprecation notice](https://docs.oracle.com/en/database/oracle/apex/26.2/htmrn/deprecated-features.html). Use tools supported by your installed release, and keep functional testing alongside static checks.

A useful change record answers four questions: what changed, why it changed, what was tested, and how the previous application definition can be recovered if necessary.
