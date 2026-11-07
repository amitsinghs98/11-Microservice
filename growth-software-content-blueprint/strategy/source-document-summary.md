# Source Document Summary

**Source:** `growth_software_platform_blueprint_100_article_map.docx`. It is stored locally as `inputs/content-strategy.docx` and is not committed.
**Extracted:** 4 November 2026 with Pandoc (DOCX → Markdown), via `scripts/extract_source_map.py`. The DOCX is text-based, so OCR was not needed. About 15,900 words were extracted, and every section was read.

## What the document contains

| Section | Content | How this repository uses it |
|---|---|---|
| Cover / Decisions locked | Market: growth software for agencies, founders and lean marketing teams. Platform: WordPress MVP. Revenue: sponsored, affiliate, later vendor subscriptions. Trust model: editorial assessments first. | Sets the audience, voice and monetization guardrails |
| 1. Executive decision | A focused discovery and comparison platform, not a full G2 clone. Listicles first, then a structured software database. | Content-first static blueprint |
| 2. Reference-site patterns | DeployHyre, SaasHyre and MakeToolz patterns to adapt, not copy. Editorial signature: "What it really costs", "Best for / not for", "What we checked", "Price checked on", "Correct this page". | `editorial-guidelines.md` §2 |
| 3. Positioning and IA | Positioning statement, four audience segments, URL patterns (`/growth-stack/`, `/categories/{seo,ai-content,email-outreach,crm-lead-gen,automation-analytics}/`, `/best/`, `/software/`, `/compare/`, `/alternatives/`, `/pricing/`, vendor pages). | `url-architecture.md`, manifest |
| 4. PRD — MVP | User stories, functional requirements (software DB, guide builder, affiliate tracking, sponsored placements, vendor intake, corrections), out of scope. | Out of scope for this static repo. Recorded in `wordpress-migration-notes.md` |
| 5. Page wireframes | Content-first anatomy for the homepage, category hub, listicle, profile, comparison, alternatives and vendor pages. | `html-article-spec.md` section patterns |
| 6. WordPress data model | CPTs, taxonomies, software record fields, editorial post fields, click-event table. | Custom-field mapping in `wordpress-migration-notes.md` |
| 7. Plugin architecture | `growth-discovery-core` module and folder plan. | Not built (explicitly excluded by the build brief) |
| 8. Monetization guardrails | Revenue streams, illustrative test pricing, non-negotiable commercial rules. | `monetization-and-disclosure-policy.md` |
| 9. Editorial operating system | Reusable structures A–D (best-of, alternatives, comparison, pricing) and the research checklist. | `html-article-spec.md`, `editorial-guidelines.md` |
| **10. 100-article topical map** | Umbrella topic, central hub (not counted), and 5 clusters × 20 articles. Each article has a title, suggested slug, primary query, intent/page type, editorial angle, writing brief and internal-link notes. | **`url-manifest.json` and `master-300-article-map.csv` (1:1)** |
| 11. Publishing sequence | Batches 1–5 and a 90-day plan. Pillars 1, 21, 41, 61, 81 come first. | `publishing-checklist.md` launch order |
| 12. SEO / measurement | Indexing, internal linking and schema rules (no fabricated ratings). | Spec and QA scripts |
| 13. Pre-launch QA | WordPress launch checklist. | `publishing-checklist.md` |
| 14. Claude Code master build prompt | WordPress plugin build prompt. | Superseded by the static-HTML build brief for this repository |
| 15. Reference sources | Reference URLs and cautions ("titles are hypotheses; verify vendor facts"). | Respected throughout |

## The 100-article map

| Cluster | Name (exact) | Articles | Pillar |
|---|---|---|---|
| 1 | SEO and organic search growth | 01–20 | 01 Best SEO Software for Agencies and In-House Teams |
| 2 | AI content and creative marketing software | 21–40 | 21 Best AI Writing Tools for Marketing Teams |
| 3 | Email marketing and outbound growth | 41–60 | 41 Best Email Marketing Software for Small Businesses |
| 4 | CRM, lead generation, and sales intelligence | 61–80 | 61 Best CRM Software for Small Businesses |
| 5 | Marketing automation, analytics, CRO, and distribution | 81–100 | 81 Best Marketing Automation Software for Small Teams |

The document contains **exactly 100 entries**, so there is no count discrepancy. All five clusters have 20 each. Every entry includes all six fields.

The document also specifies one central hub, *"The Growth Stack: How to Choose the Software Behind Acquisition, Content, Sales, and Measurement"*, at `/growth-stack/`, explicitly **not counted** in the 100. It also lists five category hub URLs. These six pages are built as additional, uncounted pages `H00`–`H05`.

## Page-type mix (after classification)

- Best-of / commercial-investigation listicles: **56**. This includes the 5 pillars, the free-tier roundups (16, 35, 56, 76, 96) and #40 (AI marketing tool stack).
- Comparisons ("vs"): **11** (11, 15, 30, 31, 51, 53, 55, 71, 75, 91, 95).
- Alternatives: **14** (12, 13, 14, 32, 33, 34, 52, 54, 72, 73, 74, 92, 93, 94).
- Pricing research: **5** (17, 37, 57, 77, 97).
- Informational / how-to / strategic guides: **14** (18, 19, 20, 38, 39, 58, 59, 60, 78, 79, 80, 98, 99, 100). #80 "Lead Scoring vs Lead Enrichment" is a concept explainer, not a product comparison, so it sits in `/guides/`.

The exact classification is in `url-manifest.json` (`page_type`).

## Ambiguities found

1. **Slugs vs URL families.** The map's suggested slugs are flat (`/best-seo-software/`), but Section 3 defines prefixed families. The prefixed families were applied (see `url-architecture.md`), and each source slug is preserved in the manifest's `source_slug` column.
2. **Software profiles.** Sections 3, 5 and 11 call for `/software/{product}/` profiles ("at least 15 canonical software profiles before publishing the first batch"), but the 100-article map doesn't list which products. They are deferred and not linked. See `content-gaps-and-assumptions.md`.
3. **Platform conflict.** The DOCX describes a WordPress + plugin MVP. The build brief explicitly excludes WordPress for this repository. The static HTML corpus is designed to migrate into that WordPress build later.
4. **Article 99 vs central hub.** The DOCX says #99 "also serves as a practical full-funnel implementation guide, but the hub itself should remain a living index". Both exist: H00 at `/growth-stack/` and A099 at `/guides/b2b-growth-stack/`.
5. **Overlapping comparisons.** 53 (HubSpot Marketing Hub vs ActiveCampaign) and 95 (ActiveCampaign vs HubSpot) have very similar intent. See the cannibalization notes in `topical-cluster-map.md`.
6. **Brand and domain.** Neither was supplied ("No brand or domain was supplied"). The owner later set InsightToolz / insighttoolz.com (7 Nov 2026), stored in `site.config.json`.
