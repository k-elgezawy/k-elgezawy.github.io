A page that displays an error has not necessarily undone every database change made along the way. Transaction boundaries deserve explicit attention in APEX.

### Read the documented commit points

Oracle documents implicit commits after rendering, before branching on submit, and before redisplaying a page following validation failure. Computations and certain session-state changes can also introduce commits. This is why “validation failed, so everything rolled back” is unsafe reasoning. [Oracle's processing guide](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/how-does-page-processing-and-page-rendering-work.html).

For a business operation, validate inputs before changing business rows. Keep related changes together in a package operation, inspect called routines for commits, and avoid unnecessary session-state assignments between dependent changes. An explicit commit makes earlier work permanent; a later exception cannot reverse it.

### A wizard spans requests

A five-step wizard is not one database transaction stretched across five pages. Store incomplete input as draft state, for example in an appropriately designed collection or draft model. Validate again when finalizing, and define cancellation as a business action against that draft state.

Leaving a browser page does not issue a universal rollback. It also cannot undo changes committed by earlier requests.

*Editorial correction: the original post incorrectly promised blanket rollback on validation failure or cancellation, and a single automatic commit for every wizard.*

Before adopting a design, test failure paths and commit boundaries in an isolated development environment. This article explains the documented behavior; it does not report a database test.