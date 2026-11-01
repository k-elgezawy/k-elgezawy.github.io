APEX can consume an external REST API through REST Data Sources or APEX_WEB_SERVICE. The first successful request is only the beginning of a reliable integration.

For declarative reports, start by evaluating a REST Data Source. For custom orchestration, MAKE_REST_REQUEST returns a response body that your PL/SQL can process. Outbound network access, TLS configuration, credentials, and the remote service's contract still matter; you do not need to create a new ORDS endpoint just to make an outbound call.

### Check the response before parsing

Inspect the HTTP status, expected content type, and response shape. A server error may return HTML rather than the JSON your code expects. Set sensible timeouts and distinguish authentication failures from temporary outages.

### Match the JSON structure

An object containing currency names is not the same as an array of currency rows. Choose JSON_OBJECT_T, JSON_TABLE, or APEX_JSON APIs that match the actual payload. Do not invent an array index for object keys.

### Keep secrets out of page code

Use configured credentials where supported. Avoid logging access tokens or complete sensitive responses. For write requests, decide how retries avoid duplicate business actions.

*Editorial correction: the original parsing example treated a JSON object like an array and referenced an unverified GET_KEY API. This revision replaces it with structure-aware guidance.*

Reference: [Oracle: calling REST APIs without a data source](https://docs.oracle.com/en/database/oracle/apex/26.1/apxdc/calling-rest-apis-data-source.html).