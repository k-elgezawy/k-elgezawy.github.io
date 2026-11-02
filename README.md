# Karim El-Gezawy — Oracle APEX Portfolio

Arabic-first, English-enabled professional portfolio, project case studies, certification, teaching resources, and a growing library of bilingual technical articles.

**Live:** https://k-elgezawy.github.io/

## Site content

- Employee Services Portal: self-service requests, attendance, approvals and enterprise-service access.
- Medical Services: medical letters, prescriptions, review queues and approval tracking.
- Inventory: items, movements, balances, reporting and user access.
- Task Management: assignments, priorities, due dates and progress.
- Public Relations: administrative service requests, transport and missions.
- Trips & Holiday Programs: preferences, departure groups, waiting lists and seasonal reporting.
- Employee Appraisals: assessment forms, reviews, completion and results.
- Managers Dashboard: team information, operational indicators and management reporting.
- HR forms, approvals, committees, financial reporting, suppliers and the family-tree application.
- Yunni: end-to-end laser/spa clinic operations, finance and HR.
- TrueLase: appointments, services, billing and inventory integration.
- Verified Oracle APEX Cloud Certified Developer Professional credential.
- Bilingual technical articles with original-source canonical links.

Only curated public descriptions and article content are included. The repository contains no internal application source, database exports, employee/patient data, or credentials. The small project diagrams are illustrative, not screenshots of client systems.

## Build

Requires Python 3.10 or later.

```sh
python -m pip install -r requirements.txt --target .build-deps
python scripts/build.py
python scripts/check_site.py
python -m http.server 8765 --directory docs
```

GitHub Pages serves the committed `/docs` directory on the `main` branch.

## Update

- `content/projects.json`: Arabic and English project case studies.
- `content/articles.json`: article metadata, source URLs, categories and covers.
- `content/articles/<slug>.en.md` and `.ar.md`: full article versions.
- `docs/assets/site.css` and `site.js`: design, language/theme controls and filtering.
- Run `scripts/build.py` and `scripts/check_site.py`, then commit the changed source and generated output.

New articles should use a unique source identifier and canonical URL. Search existing articles and the publication ledger before adding a new item. English and Arabic interface labels should be updated together.

## Public profiles

[LinkedIn](https://www.linkedin.com/in/karim-el-gezawy-460752219/) · [YouTube](https://www.youtube.com/@karimelgezawy7698) · [Hashnode](https://karimelgezawy.hashnode.dev/) · [Medium](https://medium.com/@elgezawykarim)

Content and photography © Karim El-Gezawy. Third-party references retain their original attribution. Oracle is a trademark of Oracle; this independent portfolio does not imply Oracle endorsement.
