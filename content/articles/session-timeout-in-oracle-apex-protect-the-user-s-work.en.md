A user can spend several minutes typing into a form without sending a request to the server. From the user's perspective, they are working. From the server's perspective, the session may be idle.

### Begin with the built-in warning

Review maximum session length, maximum idle time, and Session Timeout Warning in Seconds. APEX can warn before expiry. An idle-time warning can offer an extension; a maximum-length warning asks the user to save before the limit is reached.

Test the experience with realistic time limits: leave a form open, type without submitting, wait for the warning, then try to save. Also test a request made after expiry. The page should explain what happened and provide a clear way to sign in again.

### Treat draft saving as a separate feature

For long forms, consider an authenticated server-side draft with explicit ownership and retention. Show when the last save succeeded. A changed item in the browser is not yet a persisted draft.

### Be careful with periodic pings

A timer calling an Ajax process may keep an otherwise idle session active and undermine the intended timeout policy. It also adds traffic and does not eliminate maximum-session limits, network failures, or browser suspension.

*Editorial correction: my original example suggested a regular KEEP_ALIVE call. This revision recommends built-in warnings first and a deliberate draft-saving design instead of an unconditional heartbeat.*

Reference: [Oracle session security attributes](https://docs.oracle.com/en/database/oracle/apex/26.1/htmdb/configuring-security-attributes.html).