An APEX health check should answer four questions: is the application behaving correctly, performing acceptably, enforcing access rules, and producing enough evidence to investigate failures?

### Start with Advisor

Run Advisor from the application's Utilities area. Review its findings, prioritize them, and rerun the checks after fixes. Advisor inspects application metadata; it is useful for integrity and quality checks, but it does not replace execution plans, load testing, or a security review.

### Watch the user journeys that matter

Choose a small set of operations: opening a dashboard, saving a request, completing an approval, and calling an external service. Record their duration and failure rate over a defined time window. Compare equivalent workloads rather than a single fastest run.

### Build a useful operations dashboard

Include slow requests, application errors, unsuccessful authentication attempts, failed automations, and web-service failures where the installed version exposes those logs. Verify view names, columns, retention, and time units in the APEX Dictionary before writing queries. Scope the dashboard to the relevant workspace and application.

Alerts should identify the affected application, the time, and a correlation reference. Avoid emailing sensitive request payloads. Deduplicate repeated alerts and make ownership clear.

*Editorial correction: the original post used an unverified VIEW_DURATION column and treated 3000 as three seconds. That query is intentionally replaced with a version-aware monitoring approach.*

Reference: [Oracle's explanation of Advisor](https://docs.oracle.com/en/database/oracle/apex/22.2/htmdb/running-advisor-to-check-application-integrity.html).