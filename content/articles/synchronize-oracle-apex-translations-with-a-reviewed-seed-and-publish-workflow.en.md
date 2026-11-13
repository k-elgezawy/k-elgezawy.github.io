My LinkedIn post explored using APEX Automations to keep translations synchronized during development. A repeatable workflow has three stages: collect changed text, review the translated strings, and publish the updated language version.

## Prepare an application-based translation

For an application using the Application-Based translation method, define its target language mapping in Shared Components → Globalization → Application Translations. The mapping and workspace context need to exist before using the APIs below. Oracle documents the complete translation workflow. [Application-based translations](https://docs.oracle.com/en/database/oracle/apex/26.1/htmdb/creating-an-application-based-translation.html)

Use the development application ID and language code that you have selected. The ID `12345` and language `ar` in these examples are illustrative. Execute each stage separately in the correct APEX workspace context.

## Seed the changed text

Seeding updates the translation repository with translatable strings from the primary application. After a page title, item label, or other translatable component changes, seed the relevant language mapping.

```sql
begin
    apex_lang.seed_translations(
        p_application_id => 12345,
        p_language       => 'ar'
    );
    commit;
end;
```

Export the changed strings to XLIFF, update the target translations, and apply the reviewed file. Existing translation work and newly introduced strings need review before publishing. The API reference describes the repository synchronization performed by this call. [SEED_TRANSLATIONS](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/SEED_TRANSLATIONS-Procedure.html)

## Publish the reviewed language version

After applying the translation changes, publish the same primary application and language mapping.

```sql
begin
    apex_lang.publish_application(
        p_application_id => 12345,
        p_language       => 'ar'
    );
    commit;
end;
```

Publishing builds the underlying translated application by combining the primary application's definition with the repository's translated strings. Run the application in the target language and inspect the changed pages. [PUBLISH_APPLICATION](https://docs.oracle.com/en/database/oracle/apex/26.1/aeapi/PUBLISH_APPLICATION-Procedure.html)

## Automate the development preparation

An APEX Automation can run a seeding action after your development workflow identifies an approved change. Keep the application and language explicit, restrict who can initiate synchronization, and record the stage, start time, duration, and outcome. Use the Automation Execution Log to inspect failures. Test an on-demand run before enabling a schedule. [Creating an Automation](https://docs.oracle.com/en/database/oracle/apex/26.1/htmdb/creating-an-automation.html)

Keep publishing behind a separate reviewed release action. For the acceptance check, change one label, seed it, apply its translation, publish, and confirm that the target-language page displays the expected text. Also check an untranslated string, the selected language, and Arabic direction when Arabic is the target.

[Original LinkedIn post](https://www.linkedin.com/feed/update/urn:li:activity:7456820271790952448/)
