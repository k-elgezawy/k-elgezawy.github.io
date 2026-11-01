A slow page, scattered permission checks, and a growing pile of anonymous PL/SQL blocks can make an APEX application difficult to maintain. These were the three problems I highlighted in my original LinkedIn post. Here is a more practical way to approach them.

### 1. Measure performance before changing SQL

Start with the slow user action. Use APEX Debug and the browser's network tools to separate database time, network time, and rendering time. Then inspect the expensive SQL and its execution plan. Pagination and lazy loading can reduce unnecessary work; appropriate indexes can help specific access paths. A WITH clause alone does not guarantee faster SQL.

### 2. Centralize authorization

Define reusable authorization schemes and apply them to pages and operations. Hiding a button is useful for usability, but the server must also reject unauthorized requests. Keep role assignments in a trusted source and enforce row access where the data is read or changed.

### 3. Give business logic a home

Move repeated business rules into focused packages with clear names and small interfaces. Keep page processes easy to follow. Remove unused components only after checking dependencies, and leave a short explanation for decisions that will otherwise be mysterious six months later.

A useful review question is: can another developer explain how this operation is authorized, executed, and diagnosed without opening ten unrelated pages?

*Editorial update: performance gains depend on measurement. This revision removes the original suggestion that these changes automatically double performance.*