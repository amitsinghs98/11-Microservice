# Publishing Checklist

Use this per page and per launch batch. A page moves through the status ladder in `strategy/url-manifest.json`:

`planned → drafted → QA-passed (automated) → approved (human editor) → published`

Only `approved` and `published` pages go into `site/sitemap.xml`.

## Placeholders to fill before launch

| Placeholder | Where | Action |
|---|---|---|
| `BRAND_NAME` | `<title>` suffix, index page, policy text | Set `brand_name` in `site.config.json`, then run `scripts/apply_config.py` |
| `https://YOUR-DOMAIN.example` | canonical tags, sitemap | Set `domain` in `site.config.json`, then run `scripts/apply_config.py` and `scripts/build_sitemap.py` |
| Author / editor | none in the HTML | Add bylines in the CMS. Never invent credentials. |
| Publisher legal entity, address, staff | none | Supply them for the About, Contact and Terms pages |
| Trust pages | plain-text references in each page's disclosure | Publish About, Editorial Policy, How We Evaluate, Affiliate Disclosure, Sponsored Content Policy, Contact, Privacy and Terms, then link them |
| Affiliate URLs | none | Add only confirmed programs (see `monetization-and-disclosure-policy.md`) |

## Per-page editorial sign-off (human)

- [ ] Search demand and SERP format validated for the primary keyword. The DOCX titles are hypotheses.
- [ ] Every row for this page in `research-source-log.csv` that is marked `Needs verification` has been checked against the official source, then corrected or removed.
- [ ] Every price, plan name, limit, trial and integration claim has an official source link and a "checked on" date within the last 60–90 days.
- [ ] No claims of testing, ratings, review counts, customer numbers or quotes. Run `validate_content.py`, which scans for banned phrasing.
- [ ] Each product's limitations and "skip it if" guidance is fair and current.
- [ ] Facts about any product that appears on several pages are consistent across them.
- [ ] Internal links read naturally and point to published (or soon-to-be-published) pages.
- [ ] Disclosure sentence matches the page's actual commercial status.
- [ ] Byline, editor and last-reviewed date added in the CMS.
- [ ] Status set to `approved` in `strategy/url-manifest.json`.

## Automated QA (run before every commit and launch)

```bash
python3 scripts/validate_content.py
python3 scripts/check_internal_links.py
python3 scripts/build_index.py
python3 scripts/build_sitemap.py
```

Each command must exit 0. Review warnings in `qa/html-validation-summary.md`. For W3C conformance, also run the Nu HTML Checker (`vnu`) on `site/`. The built-in check is heuristic only.

## Launch order (from DOCX §11)

1. **Batch 1, pillars:** A001, A021, A041, A061, A081, plus H00–H05. Also the first 15+ software profiles (not yet built).
2. **Batch 2, comparisons and alternatives:** A011–A015, A030–A034, A050–A055, A071–A075, A091–A095. Verify pricing at publication.
3. **Batch 3, pricing:** A017, A037, A057, A077, A097, plus adjacent price-focused guides.
4. **Batch 4, workflow and education:** A018–A020, A038–A040, A058–A060, A078–A080, A098–A100.
5. **Batch 5:** the remaining best-of pages, each only once it has differentiated criteria and evidence.

DOCX capacity note: prioritise 15–25 strong pages with a tight link structure over publishing all 100 at once. When publishing a partial batch, internal links to unpublished pages must either be removed temporarily or point to pages scheduled in the same release. Run `check_internal_links.py` against the published set.

## Pre-launch platform checks (from DOCX §13, WordPress phase)

- [ ] Canonicals, sitemap, robots directives, redirects, breadcrumbs and structured data checked in the SEO plugin. No duplicate metadata.
- [ ] Pricing fields show checked dates and source links. Missing values show "not publicly listed" or "confirm with vendor".
- [ ] Sponsored slots carry visible labels and expire on schedule.
- [ ] Affiliate redirects resolve only saved keys. There are no open redirects.
- [ ] Privacy-conscious analytics with consent where required.
- [ ] Backups, staging and a rollback plan in place.

## Review cadence

- Pricing guides and comparisons: every 60–90 days.
- Evergreen guides: every 4–6 months, or after a known product change.
