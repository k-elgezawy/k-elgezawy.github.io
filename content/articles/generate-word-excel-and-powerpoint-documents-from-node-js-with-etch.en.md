Teams often need the same document in different formats: invoices, monthly workbooks, or project update decks. A common approach is to build each document with code. That can make even small layout changes require a developer.

ETCH takes a template-first approach. You design a regular Office document, add placeholders where data should appear, then send the template and a JavaScript object to ETCH from Node.js. The template controls the layout; the data supplies the content.

## Start with a Word template

Imagine an invoice template with placeholders such as `{{customer.name}}`, `{{invoiceNumber}}`, and `{{total}}`. Your Node.js code passes the invoice data to ETCH, which returns a completed Word document. A loop such as `{{#each items}}` can repeat a table row for every line item.

The same approach can place an image, QR code, or barcode in the finished file. If a designer wants to change the colors, spacing, or typography, they can edit the Word template while the data preparation code stays focused on the business logic.

## Excel and PowerPoint templates

In Excel, a repeated row can become one row per region, product, or month. The source article also shows formulas and charts adjusting to the generated rows, and a sheet template being copied once for each region.

In PowerPoint, a slide loop can generate a slide for each project, with project details, milestones, and chart data filled from the input. This can help keep recurring reports consistent while the underlying data changes.

## A simple Node.js workflow

The article's example uses the `@get-etch/etch-client` package. At a high level, the program reads a JSON file, creates an ETCH client, processes a template with the data, then saves the resulting document. ETCH also supports PDF output and batch rendering for multiple records.

Before starting, the article lists Node.js 22 or later, an ETCH account, a package token for installing the client, and an API key for requests. Keep these credentials in environment variables and follow the current ETCH setup guide for your package manager.

## When this approach fits

Template-based generation is useful when many documents share a stable design but contain different data. Examples include invoices, sales summaries, certificates, and project updates. It is less useful when every document is a one-off with a completely different layout.

The key design choice is separating content from presentation: let application code prepare trustworthy data, and let the Office template define how that data should look.

Read the [ETCH article and examples](https://get-etch.hashnode.dev/generate-word-excel-and-powerpoint-documents-from-node-js-using-etch).

#NodeJS #JavaScript #DocumentAutomation #Office