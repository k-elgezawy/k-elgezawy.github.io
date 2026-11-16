My earlier LinkedIn post explored a custom authentication function in Oracle APEX. Before implementing the password comparison, there is another design decision worth checking: what exactly identifies an account?

If `Alice`, `ALICE`, and ` Alice ` can reach the same account in one component but different accounts in another, even a correct password verifier can sit behind an inconsistent identity model. This walkthrough uses synthetic data to expose that problem before changing a login flow.

## Separate the login flow from the credential verifier

An authentication scheme establishes identity; APEX then exposes the signed-in identity through `APP_USER`. Prefer an available preconfigured scheme when it fits your identity provider and operational requirements. Custom authentication means owning the integration and its failure paths, not only writing a Boolean function. [Oracle: authentication concepts](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/understanding-authentication.html)

For a username/password scheme, `APEX_AUTHENTICATION.LOGIN` invokes the scheme's credential check, then handles successful post-authentication processing, logging, and redirection. Its `p_uppercase_username` parameter defaults to `TRUE`. That default matters when the account repository distinguishes letter case. [Oracle: LOGIN API](https://docs.oracle.com/en/database/oracle/apex/26.2/aeapi/LOGIN-Procedure.html)

## Run a normalization preflight with disposable data

Suppose a proposed policy treats usernames as case-insensitive and ignores surrounding spaces. This query demonstrates the resulting collisions without creating or changing a table:

```sql
with demo_users (user_id, login_name) as (
    select 101, 'Alice' from dual union all
    select 102, 'ALICE' from dual union all
    select 103, ' bob ' from dual union all
    select 104, 'BOB'   from dual union all
    select 105, 'Carla' from dual
)
select upper(trim(login_name)) as login_key,
       count(*) as matching_accounts
from demo_users
group by upper(trim(login_name))
having count(*) > 1
order by login_key;
```

Expected rows for these ASCII examples:

```text
LOGIN_KEY  MATCHING_ACCOUNTS
ALICE      2
BOB        2
```

Those are two different account records competing for each proposed key. Resolve the ownership and migration policy before enforcing uniqueness. Do not arbitrarily select the first matching record.

This is a design probe, not a universal username rule. A tenant-specific identity may need a composite key including the tenant. International names require an explicit policy for Unicode, collation, and normalization; this ASCII demonstration does not settle those rules. Apply your chosen policy consistently to registration, lookup, recovery, and account linking.

## Make APEX's case handling explicit

If your reviewed identity policy deliberately preserves case, an illustrative login-page process with existing username and password items can call:

```sql
begin
    apex_authentication.login(
        p_username           => :P9999_USERNAME,
        p_password           => :P9999_PASSWORD,
        p_uppercase_username => false
    );
end;
```

Adapt the item names and review the active authentication scheme before use. Put this call in the login process; the scheme's verifier supplies its credential decision. Changing the parameter alone does not migrate existing account keys or fix a conflicting lookup query. Never uppercase or trim the password to mirror a username rule.

## Give password storage its own contract

A single SHA-512 hash, even with concatenated account fields, is not a modern adaptive password-storage design. Use a maintained verifier implementing a suitable password-hashing scheme such as Argon2id, with per-password salts and reviewed work factors. Retain the algorithm and parameters needed for verification and upgrades. [OWASP: password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

Define a generic user-facing failure response, controlled login throttling, recovery behavior, and appropriate multifactor authentication. Keep detailed diagnostics protected and exclude credentials from logs. [OWASP: authentication guidance](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

Before rollout, test valid credentials, wrong passwords, unknown and disabled accounts, case variants, whitespace, duplicate normalized names, and verifier failure. Check the resulting `APP_USER` and account mapping. The examples above illustrate design and expected results; they do not implement a complete credential service or assert a measured performance improvement.

[Original LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7401531916522393600/)
