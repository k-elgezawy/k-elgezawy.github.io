Sometimes you want to inspect tables, run SQL, or review packages without navigating through application pages. SQL Developer Web is one option provided through Oracle REST Data Services.

The shortened link in my original post resolves to [Oracle's ORDS landing page](https://oracleapex.com/ords/). That page offers separate entry points for SQL Developer Web and APEX. They should not be confused with a universal login that accepts every workspace account.

### Access depends on the environment

A direct SQL Developer Web login normally involves a database schema enabled for that service. APEX can also provide an integrated entry point through SQL Workshop when the instance and schema configuration support it. In APEX 26.2, the SQL Developer Web schema list shows the workspace schemas the developer is authorized to access.

Start from your organization's trusted APEX or ORDS address, choose the intended schema, and confirm the environment before executing SQL. A convenient editor does not change the account's privileges or make production operations safe.

For quick browsing, compare the workflow with SQL Workshop and use whichever fits the task. For repeatable changes, keep scripts in source control and follow the deployment process.

*Editorial correction: a workspace name, username, and password are not a universal login recipe for every SQL Developer Web installation.*

References: [APEX 26.2 integration](https://docs.oracle.com/en/database/oracle/apex/26.2/aeutl/using-restful-services.html) and [SQL Developer Web access model](https://docs.oracle.com/en/database/oracle/sql-developer-web/20.4/sdweb/about-sdw.html).