The useful question is not simply which request looks faster. It is which processing contract the user action needs.

### Use submit for the page's processing flow

A page submit enters APEX page processing: submitted state, applicable computations, validations, processes, and branches. Conditions and button settings determine what actually runs. Submit is a natural fit for a form that already has declarative validation and save processing.

### Use Ajax for a targeted interaction

A dashboard filter usually needs fresh data in selected regions. Submit the relevant filter items and refresh those regions. A custom `apex.server.process` call invokes a named callback; it does not automatically execute the page's full submit-validation lifecycle. [Oracle's Ajax API](https://docs.oracle.com/en/database/oracle/apex/24.2/aexjs/apex.server.html).

Consequently, the callback must enforce its own input rules, authorization, and business invariants, preferably through shared server-side operations. Define what success means and how the interface responds to failure or duplicate clicks.

Both approaches can modify data and participate in database transactions. Ajax can have side effects, including committed changes. Transport choice does not determine business atomicity.

*Editorial correction: the original post described Ajax as having no side effects, reserved transactions for submit, and claimed large systems use events instead of state machines. Those claims were too broad.*

Measure request count, SQL time, payload size, and user effort. Choose the smallest interaction that still preserves the required processing and security guarantees; event handling and explicit business states can work together.

Reference: [APEX page processing](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/how-does-page-processing-and-page-rendering-work.html).