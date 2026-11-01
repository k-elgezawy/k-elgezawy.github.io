Session state is useful application context. It is not, by itself, a security layer for every REST API an application calls.

**Correction to my original post:** putting ADMIN in P0_USER_ROLE and attaching an APEX authorization scheme does not automatically protect an independently reachable ORDS endpoint.

### Protect each entry point

For an APEX page or callback, enforce authorization on the server and check access to the requested rows. Derive roles from a trusted source. A role value that the browser can submit must not become the source of authority.

For an ORDS API, configure the API's own authentication and authorization—for example, the applicable privileges and roles—and enforce business-level row access in its implementation. A caller who bypasses the APEX page must face the same access boundary.

### Treat tenant identity as trusted context

Multi-tenant isolation requires a validated tenant identity and consistent filtering or database policies on every relevant path. A salary threshold in one report query is not a general tenant-isolation design.

Test as an authorized user, a user with the wrong role, a user from another tenant, and an unauthenticated caller. Include direct requests, not only clicks through the UI.

APEX authorization schemes are valuable. Their protection applies where they are enforced; it does not automatically extend to unrelated services.

Reference: [ORDS Developer's Guide](https://docs.oracle.com/en/database/oracle/oracle-rest-data-services/24.3/orddg/oracle-rest-data-services-developers-guide.pdf).