# CLAUDE.md: Project memory for InsightToolz (growth-software content site)

This file is the complete hand-off memory for this project. Read it fully before doing anything. It was last updated on **7 November 2026**. At that point 87 commits were on branch `claude/dazzling-cray-wjh11a` of `amitsinghs98/11-Microservice`, with the project in folder `growth-software-content-blueprint/`.

---

## 1. What this is

**InsightToolz** (https://insighttoolz.com) is an independent growth-software discovery and comparison site for agencies and lean marketing teams. It's an editorial publication, not a review marketplace.

- **Positioning:** "use-case fit, clear pricing context, and honest limitations".
- **Content:** 300 articles (A001–A300) in 15 topical clusters, plus 16 hub pages (H00 umbrella `/growth-stack/`, H01–H15 category hubs), so **316 pages**.
- **Two layers:**
  1. `site/` holds plain semantic HTML. This is the editorial source of truth: no CSS or JS, one file per page.
  2. `web/` holds a zero-dependency Node generator that wraps `site/` pages in a styled, deployable site (`web/dist/`). The design comes from the owner's **MakeToolz** codebase (maketoolz.com, also the owner's site), re-themed emerald/teal.
- **Owner:** dev@hyerstudios.com (Hyer Studios; also runs MakeToolz, DeployHyre and SaasHyre).
- **Author:** **David Esper**, assigned and authorised by the owner, "Lead editor and head of research, growth software". Author page: `/author/david/`.
- **Draft date** in pages: 4 November 2026. Facts were checked on 4–7 November 2026.

## 2. Owner's decisions and preferences (follow these)

- **Flat URLs for every post and hub** (`/best-seo-software/`, `/semrush-alternatives/`, `/seo-software-pricing/`, `/semrush-vs-ahrefs/`, `/seo/`). The owner says "flat is more beneficial". The **only** nested URL is the author page, `/author/david/`, which the owner explicitly wanted.
- **Brand and domain:** InsightToolz and https://insighttoolz.com, stored in `site.config.json`.
- **Colours:** emerald/teal. `--brand:#047857` (text-safe), gradient `#0f9f6e → #0ea5b7 → #3b82f6`.
- **Scope of the new site:** content only. MakeToolz tools, downloaders, proxies and ads were deliberately **not** carried over.
- **How the owner works:** fast and hands-on. Often says "go all in". Likes batches of agent work, wants Claude to ask before each new batch, and has asked to pause after N pages. Wants things committed and pushed.
- **Git:**
  - Branch `claude/dazzling-cray-wjh11a` only. Never force-push. **No PR unless asked.** A PR exists: https://github.com/amitsinghs98/11-Microservice/pull/2 (opened early; not merged).
  - Commit trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` and `Claude-Session: https://claude.ai/code/session_01F7mF13RMbAVFLatoUamk3B`. Never put model IDs in commits.
  - A stop hook asks you to commit any uncommitted changes. Commit finished work, but never half-written agent output.
- **Pending ask from the owner:** move the project to its own GitHub repo. Claude can't create repos in that environment; the owner must create an empty repo (suggested name `insighttoolz` or `growth-software-content-blueprint`, private). Then push this folder there with history (`git subtree split --prefix=growth-software-content-blueprint`).

## 3. Hard rules (never break)

1. **Never fabricate** prices, features, limits, integrations, quotes, reviews, ratings, review counts, test results, performance lifts, affiliate terms, commissions, vendor relationships, search volumes or **first-hand experience**.
2. **Never invent an author persona or credentials.** The owner once asked for a "John Doe"-style made-up author; that was declined. David Esper is real and assigned by the owner. His bio states only his role and method. `web/authors.json` → `credentials` and `links` stay empty until David supplies real facts.
3. **Experience sections are human-only.** Every article has exactly one `<p><mark>[YOUR EXPERIENCE HERE — the skill will not invent this]</mark></p>`. Only David fills it, via `progress/david-experience-intake.md` → `python3 scripts/apply_experience.py`.
4. **No testing claims.** Banned: "we tested", "users rate", "best-in-class", "game-changing", "in today's digital landscape". See `strategy/site-brief.md`.
5. **Sources:** official vendor domains only; never G2/aggregators/affiliate listicles. **Don't copy** G2, DeployHyre, SaasHyre or MakeToolz wording (avoid duplicate content across the owner's sites).
6. **Never** print, commit or expose secrets, tokens or `.env` files. `inputs/content-strategy.docx` is gitignored; it's in the zip but not in git.
7. **Neutrality:** pages comparing Claude/Anthropic with other AI tools (A021, A030, A031–A034, A037) carry a disclosure that the draft was prepared with an AI model from one of the compared vendors and needs independent human review. Keep ChatGPT and the others at equal depth.
8. **Pages stay drafts** (noindex) until a human approves them.

## 4. Content standard (the seo-content-writer v2 spec, in `strategy/html-article-spec.md`)

- **One H1**, kept as the manifest/source title. Don't change H1s.
- **Every content H2 is a question**, with a **two-sentence answer capsule** directly beneath it.
- **Exactly one `<table>`** per article.
- **Exactly one experience marker** (or a filled `data-experience="filled"` block).
- **Inline sources only.** No Sources/References section. Each sourced claim gets an inline link to the official URL plus "(checked D Month 2026)".
- **Primary keyword** in the first 100 words (enforced) and ideally in the title tag.
- **Title tag** is 50–60 characters + ` | InsightToolz`. **Meta description** is 120–160 characters.
- **JSON-LD:** one `@graph` with a BreadcrumbList and a FAQPage whose entries are identical to the visible FAQ H3s and answers. The web build adds an `Article` node (author David Esper, publisher InsightToolz).
- **No** `Review`, `AggregateRating` or `Product` markup.
- **Hubs:** no experience marker; BreadcrumbList plus FAQPage.

## 5. Site architecture and SEO structure

- **15 clusters.** Hub, pillar and topic for each:
  - 1: `/seo/`, pillar A001
  - 2: `/ai-content/`, A021
  - 3: `/email-outreach/`, A041
  - 4: `/crm-lead-gen/`, A061
  - 5: `/automation-analytics/`, A081
  - 6: `/content-operations/`, A101
  - 7: `/paid-media/`, A121
  - 8: `/ecommerce-growth/`, A141
  - 9: `/customer-retention/`, A161
  - 10: `/affiliate-partnerships/`, A181
  - 11: `/website-experience/`, A201
  - 12: `/data-revops/`, A221
  - 13: `/webinars-demand-gen/`, A241
  - 14: `/agency-operations/`, A261
  - 15: `/product-led-growth/`, A281
- **Umbrella hub:** `/growth-stack/` (H00), grouped by funnel stage: Acquisition, Conversion, Retention, Measurement, Operations.
- **Page types:**
  - listicle (215) and pillar-listicle (15)
  - comparison (20)
  - alternatives (18)
  - pricing-guide (6)
  - guide (25) and strategic-guide (1)
  - category-hub (15) and topical-hub (1)
- **Silo rules, currently all met:**
  - Every hub links all 20 of its cluster's articles.
  - Every article links its hub **and** its pillar, with varied anchors.
  - Cross-cluster links are **≤2 destinations per article**, except stack-spanning guides A040, A098 and A099. The overall cross-cluster share is **22%** (target 20–25%), enforced by `scripts/limit_cross_links.py`.
- **Pillars for clusters 6–15** were added on 7 November 2026: the central topic was rewritten to about 3,000 words, and hubs H06–H15 were expanded to about 2,400–2,800 words.
- **Cannibalization pairs** are documented in `scripts/build_index.py` (CANNIBAL) and `strategy/duplicate-intent-review.csv`. The main risks are A053/A095 (HubSpot vs ActiveCampaign twice) and A178/A288 (customer journey analytics). Both are differentiated by buyer; merge with a 301 if SERPs show a single intent.

## 6. Keyword research (Semrush, US database, 7 November 2026)

- **Raw data:** `strategy/semrush/batch0–3.csv` (all 316 primary keywords) and `variants.csv` (89 head-term variants).
- **Results:** `strategy/keyword-validation.csv`.
  - **Tiers:** 194 weak (under 50 searches/month or not in Semrush), 43 strong, 36 opportunity, 30 moderate, 13 hard.
  - **46 retargets:** intent-matched head terms, with no two pages on one term. They're applied as a manifest override; `source_primary_keyword` keeps the original.
  - **Effect:** summed primary-keyword volume went from about 122k to about 200k searches/month.
- **Applied on every retargeted page:** title, meta and deck. H1s and URLs are unchanged.
- **Anomaly:** Semrush returned 1,500,000/month for "knowledge base software" and "online course platforms". Treat these as errors; they weren't used.
- **Best opportunities (US searches/month, keyword difficulty):**
  - password managers: 12.1k, KD 32
  - ahrefs alternatives: 9.9k, KD 34
  - podcast hosting platforms: 4.4k, KD 21
  - affiliate marketing platforms: 3.6k, KD 16
  - shopify alternatives: 3.6k, KD 21
  - hootsuite alternatives: 1.6k, KD 9
  - semrush vs ahrefs: 9.9k, KD 50
  - hubspot vs salesforce: 6.6k, KD 48

## 7. Fact status (`strategy/research-source-log.csv`, merged from `strategy/research/{ID}.csv`)

- **Rows:** 4,078.
  - Verified: 252 (directly fetched)
  - Search-confirmed: 385 (matched via a search index of the **official** page, because direct fetches were blocked; **must be re-fetched before publishing**)
  - Needs verification: 2,266 (qualitative statements)
  - Not stated: 859 (cut, or editorial calculations)
  - Not confirmed: 316 (affiliate rows, no affiliates used)
- **Environment blockers in the original session:**
  - The network proxy blocked most vendor sites (403). Only claude.com, support.claude.com, anthropic.com and github.com were directly fetchable.
  - The Firecrawl credits ran out.
  - The owner declined an environment change that would have allowed 20 vendor hosts.
  - With open network access, re-fetch every Search-confirmed and Needs-verification row.
- **"Completed money pages"** (deep verification pass done), 16 in total: A001, A011–A015, A017, A021, A030–A034, A037, A041, A051.
- **Queued money pages** for the same pass, 33 in total:
  - A052–A055, A057, A061, A071–A075, A077, A081, A091–A095, A097
  - A106, A113, A135, A159, A179, A198, A207, A208, A219, A239, A254, A260, A298, A299
  - The new pillars got a sourcing pass while being rewritten.
- **Known open flags:**
  - ChatGPT Business annual seat price: OpenAI pages conflict.
  - Moz has no figures (moz.com is unreachable via search).
  - Constant Contact has no figures (A041).
  - Writesonic plan allowances: its pricing page and docs conflict.
  - Amplitude acquired Statsig on 5 May 2026. **Verified** via statsig.com and Amplitude investor pages.

## 8. Publishing workflow (status ladder: planned → drafted → QA-passed → approved → published)

1. **Fill experience and approve.** David fills `progress/david-experience-intake.md` (16 money pages, one tailored prompt each). He writes 2–5 sentences of real experience and sets `Approved: yes`. Then run `python3 scripts/apply_experience.py`, which:
   - replaces the marker with `<p data-experience="filled">`
   - sets the page status to `approved`

   The validator accepts either the marker or a filled block.
2. **Rebuild and check.** Run `python3 scripts/validate_content.py && python3 scripts/check_internal_links.py && python3 scripts/build_index.py && python3 scripts/build_sitemap.py && node web/build.js`.
3. **Indexing is per page:**
   - **Approved pages:** `index, follow, max-image-preview:large, max-snippet:-1`, and they're included in the sitemap.
   - **Draft pages:** `noindex, follow`.
   - **robots.txt:** disallows everything until at least one page is approved.
   - Global override: `"indexable": true` in `site.config.json`. Audit-only: `INDEXABLE=1`, which you must never deploy.
4. **Deploy (Cloudflare Pages, like MakeToolz):**
   - Root: `growth-software-content-blueprint/`
   - Build command: `node web/build.js`
   - Output: `web/dist`
   - `_headers` is generated.

## 9. Web build (`web/`)

- **`web/build.js`** (Node 18+, no npm dependencies) reads:
  - `site/**/index.html`
  - `strategy/url-manifest.json`
  - `site.config.json`
  - `web/authors.json`
  - `web/assets/style.css`
  - `web/assets/site.js`
  - `web/assets/og-default.jpg`
- **Output includes:**
  - All 316 pages, each with mega menu (5 funnel groups), breadcrumbs, cluster pill, byline, draft pill, author box, and a "Keep reading" block of 3 same-cluster articles (rotating, so every article gets exactly 3 same-silo inbound links).
  - Homepage, author page, 404, sitemap.xml, robots.txt, llms.txt, favicon.svg, SVG covers in `og/`, and `_headers`.
- **Performance:**
  - CSS is purged at build time (49 KB → about 15 KB) and inlined; JS is inlined (about 300 bytes).
  - No web fonts, no third-party scripts, no tracking.
  - HTML and JSON-LD are minified. The homepage LCP image has `fetchpriority=high`; "Keep reading" blocks use `content-visibility`.
- **Lighthouse mobile** (approved-mode audit build): **100/100/100/100** (Performance/SEO/Accessibility/Best Practices). 13–16 KB per page, 2 requests, LCP about 0.9 s, CLS 0.
- **Commands:**
  - Build: `node web/build.js`
  - Preview: `node web/build.js serve` → http://localhost:8788
  - Brand/domain change: edit `site.config.json`, then `python3 scripts/apply_config.py` and rebuild.

## 10. Scripts (`scripts/`, stdlib Python 3)

| Script | Purpose |
|---|---|
| `extract_source_map.py` | DOCX → `.tmp/source-article-map.json` (A001–A100) |
| `build_manifest.py` | Builds `strategy/url-manifest.json` and `master-300-article-map.csv`. Contains `flatten()` (flat URLs), PILLARS/NEW_PILLARS, word ranges and keyword overrides from `keyword-validation.csv`. Preserves status. |
| `validate_content.py [IDs]` | All mechanical checks: structure, question H2s, one table, experience marker, keyword in first 100 words, title/meta length, JSON-LD validity, FAQ match, parent-hub link, word bands. Full run writes `qa/` reports and updates statuses. |
| `check_internal_links.py [--quiet IDs]` | Internal link audit, orphans, link and anchor maps, external inventory |
| `build_index.py` | `site/index.html` QA directory, `strategy/topical-cluster-map.md` (CANNIBAL list), merged research log |
| `build_keyword_map.py` | `strategy/keyword-map.csv` |
| `build_sitemap.py [--staging]` | `site/sitemap.xml` (approved only) and `qa/sitemap-staging.xml` |
| `apply_config.py` | Applies the brand and domain from `site.config.json` |
| `limit_cross_links.py` | Silo tightening (max 2 cross-cluster destinations per article) |
| `apply_experience.py` | Merges David's experience and approvals |

## 11. Key files

- **Strategy (`strategy/`):**
  - `site-brief.md`: voice, reader, say/don't-say, author
  - `html-article-spec.md`: the v2 spec
  - `editorial-guidelines.md`, `url-architecture.md`, `monetization-and-disclosure-policy.md`
  - `publishing-checklist.md`, `content-gaps-and-assumptions.md`
  - `wordpress-migration-notes.md`: flat URLs map to the WordPress `/%postname%/` permalink setting
  - `source-document-summary.md`, `source-ingestion-report.md`
  - `url-manifest.json`: the **only** source of URLs
  - `url-migration-map.csv`: old nested paths → flat
- **Agent briefs (`progress/`):**
  - `agent-brief.md`: writer rules
  - `completion-brief.md`: verification/completion pass for money pages; one agent per page; official-domain WebSearch; Search-confirmed logging
  - `pillar-brief.md`: cluster pillar/silo jobs
  - `build-progress.md`: dated log
  - `david-experience-intake.md`
- **QA (`qa/`):**
  - `publishing-readiness-report.md` (with the 7 November update at the top)
  - `html-validation-summary.md`, `article-status.csv`, `internal-link-audit.csv`, `orphan-pages.csv`, `external-link-inventory.csv`
- **Inputs (`inputs/`):**
  - `content-strategy.docx`: the 100-article strategy (private, gitignored)
  - `additional-200-articles.csv` and `.md`: A101–A300 source

## 12. Current QA state (7 November 2026)

- **Validation:** 316/316 pages pass, with 0 errors.
- **Warnings:** most say "primary keyword not verbatim in H1". That's expected, because H1s are kept as source titles.
- **Links:** 3,169 internal links, 0 broken, 0 orphans.
- **Same-cluster linking:** about 6.8 links per article in clusters 1–5 and about 5.9 in clusters 6–15.
- **Experience:** 0 of 300 experience sections filled, so 0 pages are approved and the live sitemap is empty.

## 13. Recommended next steps (in priority order)

1. **David approves pages.** He fills the intake sheet for the 16 money pages, reviews them, and approves. Then rebuild and deploy those pages first.
2. **Re-verify facts.** With open network access, re-fetch all Search-confirmed and Needs-verification rows, starting with the pricing guides, comparisons and pillars.
3. **Run the completion pass** on the 33 queued money pages (`progress/completion-brief.md`, one agent per page, in batches; ask the owner for batch size).
4. **Move the project** to its own repo once the owner creates it.
5. **Optional extras:**
   - Real author credentials and links in `web/authors.json`
   - Per-page raster share images
   - Trust pages: About, Editorial Policy, How We Evaluate, Affiliate Disclosure, Contact, Privacy, Terms. Article disclosures currently mention these as plain text, not links.
   - A "Correct this page" form
   - Software profile pages (`/software/{product}/`, deferred)

## 14. Original user requests (for context)

- "Use the repo and create a folder."
- Build a 100-article plain-HTML library plus internal-link blueprint from the DOCX, then expand it to 300 with the additional-200 CSV.
- "Write all 300 articles properly" to the seo-content-writer standard.
- Flat URLs (owner's request).
- Complete money pages in batches (3, then 10).
- A clone of the owner's MakeToolz design with different colours (content site only, emerald/teal).
- Brand InsightToolz at insighttoolz.com; author David Esper (assigned).
- Semrush keyword validation; pillars for clusters 6–15; tighter silo; flat URLs except `/author/david/`.
- "Optimize the whole site as an SEO expert, lightest weight, fastest to load, 100 scores."
- Run it on localhost.
- This hand-off.
