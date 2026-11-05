My original LinkedIn walkthrough connected a Cohere service to Oracle APEX App Builder. The useful starting point is a workspace service definition: provider, endpoint, model, and credential are configured together before you ask the assistant to help with code.

## Create the workspace service

In APEX 26.2, open **App Builder → Workspace Utilities → All Workspace Utilities → Generative AI**. Create a service, select **Cohere**, and give it a clear name and Static ID. Navigation labels can differ by APEX version. Oracle describes the [configuration workflow](https://docs.oracle.com/en/database/oracle/apex/26.2/apxdc/configuring-generative-ai-service.html).

This is an illustrative configuration record, not an import file or executable script:

```text
Name: Cohere Development Assistant
Static ID: COHERE_DEV_ASSISTANT
AI Provider: Cohere
Used by App Builder: On
Default for New Apps: Off (enable if required)
Base URL: https://api.cohere.ai/v2
AI Model: command-r-08-2024
Credential: a workspace Web Credential
```

The endpoint and model above come from my original example. Confirm that your installed APEX version supports the endpoint and that your provider account can access the chosen model. Check [Cohere's current model catalog](https://docs.cohere.com/docs/models); availability can vary by hosting platform.

## Separate the two switches

**Used by App Builder** enables the service for builder features. **Default for New Apps** chooses the default service for newly created applications. Decide each setting independently; they serve different purposes. See Oracle's [service attribute reference](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/editing-a-generative-as-service.html).

Select or create the Web Credential in APEX. Keep the API key out of JavaScript, screenshots, articles, and repositories. Oracle documents [credential storage and runtime controls](https://docs.oracle.com/en/database/oracle/apex/26.2/htmdb/creating-generative-ai-service-objects.html), including token and timeout settings.

## Test with a small, reviewable request

Run **Test Connection** before saving. Then try a prompt using invented schema names:

```text
Given demo_orders(order_id, customer_id, amount), write a read-only
SQL query returning total amount by customer_id. Explain how SUM
handles null amounts. Do not invent columns or execute the query.
```

Review the proposed SQL, assumptions, null handling, and access rules before using it. A successful connection proves connectivity; the generated answer still needs technical review. Use synthetic examples while evaluating the assistant, and choose deliberately which application information may be sent to the external provider.
