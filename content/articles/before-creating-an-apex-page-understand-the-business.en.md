When starting an APEX system, I prefer to understand the business operation before generating forms. A good interface becomes much easier to build when ownership, states, and rules are clear.

For a leave request, map submission, manager review, HR checks, balance handling, and notification. Ask what happens when the manager changes, two approvals arrive together, or a request is withdrawn.

### Turn the process into a model

Identify employees, request types, requests, and decision history. Define keys and relationships, then enforce suitable uniqueness, required values, and valid states with database constraints. Put reusable operations behind clear package interfaces such as `leave_request_pkg.approve_request`.

That operation should verify the caller's authority and the request's current state, protect against conflicting changes, and record the decision. Keep APEX processes focused on passing validated context and displaying outcomes.

### Design evidence and ownership

Created and updated timestamps are useful, but they do not preserve a full change history. Record significant transitions with actor, time, previous state, new state, and reason.

If another system owns synchronized source records, treat those records as immutable. Store additional local business metadata in separate extension tables keyed to the source identifiers.

*Editorial clarification: “database first” is a design preference, not a requirement to finish the entire schema before testing an interface. Iterate with users while preserving data ownership and integrity.*

Include access rules, representative performance checks, and operational monitoring from the beginning. Oracle's [APEX overview](https://www.oracle.com/apex/) describes its database foundation; these design choices remain the application team's responsibility.