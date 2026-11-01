Two people can open the same record and both receive a successful save message while one overwrites the other's changes. Optimistic concurrency checks help detect that conflict.

In a supported APEX Form, configure Lost Update Type on the Form region and enable Prevent Lost Updates on its corresponding Automatic Row Processing process. Row Values compares a checksum of updateable values. Row Version Column uses a column that changes on every update; Oracle does not recommend that option when a form updates multiple tables.

When a conflict occurs, explain that the record changed and let the user review the latest data. Automatic merging requires its own business rules. A separate custom UPDATE process also needs its own concurrency design.

Test with two separate sessions: open the same record, save a change in the first, then try to save the stale second copy. Confirm that the second write is rejected and the first change remains.

Reference: [Oracle lost update detection](https://docs.oracle.com/en/database/oracle/apex/24.1/htmdb/configuring-lost-update-detection.html).