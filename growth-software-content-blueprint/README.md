# Growth Software Content Blueprint

A plain-HTML content library and internal-link blueprint for an independent growth-software discovery platform for agencies and lean marketing teams. It contains **300 articles in 15 topical clusters, plus 16 hub pages** (316 pages). A001–A100 come from the source strategy DOCX (`inputs/content-strategy.docx`, not committed) and A101–A300 from `inputs/additional-200-articles.csv`.

This is **draft editorial content**, not a website. It has no CSS, JavaScript, framework, CMS or deployment. The HTML is semantic and unstyled, so it is easy to serve statically or import into WordPress later.

> Status: drafted and mechanically QA'd. **Not publication-ready until an editor verifies the facts** flagged in `strategy/research-source-log.csv`. See `qa/publishing-readiness-report.md`.

## Layout

```text
site/                     web root: serve this directory at "/"
  index.html              plain QA directory of every page (noindex)
  growth-stack/           H00 umbrella hub
  {hub}/                  H01–H15 cluster hubs, e.g. seo/, content-operations/
  best-{topic}/ {a}-vs-{b}/ {product}-alternatives/ {topic}-pricing/ {guide}/
                          the 300 articles, one flat folder each (see strategy/url-architecture.md)
  sitemap.xml robots.txt
strategy/                 manifest, maps, policies, research log
  url-manifest.json       canonical page list (source of truth for every URL)
  master-300-article-map.csv
  research/{ID}.csv       per-page research fragments (merged into research-source-log.csv)
scripts/                  stdlib-only Python 3 tools
qa/                       generated QA reports
progress/build-progress.md
site.config.json          domain and brand placeholders
```

## Clusters

Clusters 1–5 (A001–A100) have a designated pillar; clusters 6–15 use their hub as the parent. The full list is in `strategy/topical-cluster-map.md`.

| # | Cluster | Hub | Pillar |
|---|---|---|---|
| 1 | SEO and organic search growth | `/seo/` | `/best-seo-software/` |
| 2 | AI content and creative marketing software | `/ai-content/` | `/best-ai-writing-tools/` |
| 3 | Email marketing and outbound growth | `/email-outreach/` | `/best-email-marketing-software/` |
| 4 | CRM, lead generation, and sales intelligence | `/crm-lead-gen/` | `/best-crm-software-for-small-business/` |
| 5 | Marketing automation, analytics, CRO, and distribution | `/automation-analytics/` | `/best-marketing-automation-software/` |

## Preview locally

```bash
cd growth-software-content-blueprint/site
```

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000/. Root-relative links only work when `site/` is served as the web root. Opening files directly with `file://` breaks them.

## Run QA

```bash
python3 scripts/validate_content.py
```

```bash
python3 scripts/check_internal_links.py
```

```bash
python3 scripts/build_index.py
```

```bash
python3 scripts/build_sitemap.py
```

- `validate_content.py` checks structure, metadata, IDs, TOC fragments, placeholders, banned claims ("we tested", "users rate"…) and word counts. It updates page status and writes `qa/article-status.csv` and `qa/html-validation-summary.md`. The HTML check is heuristic, not W3C validation.
- `check_internal_links.py` resolves every internal link against the manifest and `site/`, exits non-zero on any broken link, and writes `qa/internal-link-audit.csv`, `strategy/internal-linking-map.csv`, `strategy/anchor-text-map.csv` and `qa/external-link-inventory.csv`.
- `build_index.py` regenerates `site/index.html` and `strategy/topical-cluster-map.md`, and merges the research fragments.
- `build_sitemap.py` writes `site/sitemap.xml` with **approved/published pages only**. Use `--staging` to write `qa/sitemap-staging.xml` with every drafted page.

If the source DOCX changes, regenerate the manifest:

```bash
python3 scripts/extract_source_map.py && python3 scripts/build_manifest.py
```

## Publish later (no deployment has been done)

1. Verify facts and sign off pages per `strategy/publishing-checklist.md`. Set their status to `approved` in `strategy/url-manifest.json`.
2. Set the real `domain` and `brand_name` in `site.config.json`, then run `python3 scripts/apply_config.py` and the QA commands above.
3. **Static hosting:** point any static host at `site/` as the document root. Deploy only `site/`, never `strategy/`, `qa/` or `scripts/`.
4. **WordPress:** follow `strategy/wordpress-migration-notes.md`.

## Moving to its own repository

This folder was built inside `amitsinghs98/11-Microservice` because the build session couldn't create a new repository. To move it into a new private repository with the GitHub CLI:

```bash
cp -r growth-software-content-blueprint ~/growth-software-content-blueprint && cd ~/growth-software-content-blueprint
```

```bash
git init -b main && git add . && git commit -m "Import growth software content blueprint"
```

```bash
gh repo create growth-software-content-blueprint --private --source=. --push
```

`.gitignore` already excludes `*.docx`, `.env*` and other secrets.

## Key documents

- `strategy/source-document-summary.md`: what the DOCX contains and the ambiguities found
- `strategy/editorial-guidelines.md` and `strategy/html-article-spec.md`: writing and markup rules
- `strategy/monetization-and-disclosure-policy.md`: affiliate and sponsored rules (none are active)
- `strategy/content-gaps-and-assumptions.md`: every judgement call and deferred item
- `qa/publishing-readiness-report.md`: current state and what's left
