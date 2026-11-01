APEX provides useful session controls, but developers need to understand their boundaries before relying on them. My original post overstated those protections.

**Editorial correction:** I could not substantiate the claimed Browser Signature, User Agent Hash, Session Origin Fingerprint, Strict/Medium/Relaxed matching modes, or a setting named “Session ID Reuse Not Allowed” in the official documentation. The claim that stolen cookies cannot be reused was also unjustified. Do not implement security based on those claims.

### Session cloning has a different purpose

Oracle documents session cloning as a way to open a separate application session with a new identifier and copied session values. It helps separate state between browser tabs; it is not a guarantee against session theft. [Oracle: session cloning](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/managing-session-state-values.html).

### Configure real controls deliberately

Use HTTPS and appropriate idle and maximum session timeouts. Review Rejoin Sessions carefully: Oracle recommends disabling it unless workspace isolation is implemented through hostname configuration. A convenient URL setting has security consequences. [Oracle: instance security](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/managing-instance-security.html).

The original User-Agent comparison is not a reliable device identity check: a client can send that header, and the example did not establish a trusted baseline. I have removed it.

Keep authorization checks on the server, protect sensitive operations, and test logout and timeout behavior. A compromised user device remains a serious problem; no blanket promise of automatic protection belongs in an application security design.