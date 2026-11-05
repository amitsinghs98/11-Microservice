# Publishing Readiness Report

Generated on 5 November 2026 after the final QA pass. **Verdict: structurally complete, not ready to publish.** All 316 pages pass automated QA, but most product facts have not been checked against a live official page, and every article still needs a human to fill its experience marker.

## What is done (automated checks, all passing)

| Check | Result |
|---|---|
| Pages built | 316 = 300 articles (A001–A300) + 16 hubs (H00–H15), 625,321 words |
| `validate_content.py` | 316/316 pass, 0 errors; 147 warnings (mostly "primary keyword not verbatim in H1", because the H1 is kept as the source title) |
| Duplicate titles / meta descriptions | 0 / 0 |
| `check_internal_links.py` | 3,090 internal links, **0 broken**, **0 orphans** (`qa/orphan-pages.csv`; the lowest inbound count is 2) |
| External links | 4,053, official vendor domains only, no affiliate links (`qa/external-link-inventory.csv`) |
| Experience markers | 300 (one per article, none on hubs) |
| JSON-LD | One block per page: BreadcrumbList plus a FAQPage matching the visible FAQ; no Review, Rating or Product markup |
| URLs | Flat single-segment URLs (`strategy/url-architecture.md`); all canonicals and breadcrumbs updated |
| Sitemap | `site/sitemap.xml` holds 0 URLs (none approved yet); `qa/sitemap-staging.xml` holds all 316 |

## Blockers before any page publishes

1. **Fact verification (largest blocker).** Vendor websites were blocked by this session's network policy, and the Firecrawl credits ran out on 4 November. Research log (`strategy/research-source-log.csv`, 3,829 rows):

   | Status | Rows | Meaning |
   |---|---|---|
   | Verified | 264 | Fetched from the official page on 4–5 Nov 2026 |
   | Search-confirmed | 97 | Matched via a search index of the official page only; re-fetch before publishing |
   | Needs verification | 2,323 | Qualitative statement from general knowledge, written cautiously |
   | Not stated | 829 | Cut because it couldn't be confirmed, or an editorial calculation |
   | Not confirmed | 316 | Affiliate-program rows (none used) |

   Only **44 of 300 articles** carry at least one Verified fact; most are in clusters 1–5. Pages without fetched figures say "See official pricing" instead of giving numbers, so they contain no unsourced prices, but feature and limitation statements still need checking.
2. **Experience markers.** 300 literal `[YOUR EXPERIENCE HERE — the skill will not invent this]` markers must be replaced with real first-hand experience, or the section removed.
3. **Neutrality: Claude-only sources.** In 12 cluster-2 pages (A021–A025, A029, A030, A036–A040), Claude's pricing is the only one that could be fetched, because claude.com was the only reachable vendor site. **A030 "ChatGPT vs Claude for marketing" is a conflict of interest** (drafted by an Anthropic model, with only Claude figures verified). A human editor must add OpenAI's figures from openai.com and review the page for balance before publishing. A037's Claude prices were re-checked against claude.com/pricing on 5 Nov 2026 and match.
4. **Brand, domain, author, trust pages.** These are still placeholders. See `strategy/publishing-checklist.md`.
5. **Search demand.** Primary keywords are hypotheses; no volumes were measured.

## Facts flagged for specific review

- Ownership and rename claims that writers made and fact-checkers removed or softened (e.g. Hotjar/Contentsquare, Brandfolder/Smartsheet, Frame.io/Adobe, Marq/Lucidpress, Postmark, Mailgun, SendGrid). Re-add them only with a source.
- Product-retirement claims (Google Optimize sunset, GA4 attribution-model removals), n8n licence terms, and CAN-SPAM penalty figures: confirm against primary sources.
- Worked cost scenarios that use verified list prices (A036, A055, A061, A077 and others): the arithmetic is labelled as hypothetical; re-check the inputs when prices are re-fetched.

## Cannibalization

29 pairs are listed in `strategy/duplicate-intent-review.csv`: 21 documented and differentiated, plus automated keyword-overlap pairs, most of which are different intents (best-of vs pricing vs guide). The closest risks are A053/A095 (HubSpot vs ActiveCampaign twice) and A178/A288 (customer journey analytics twice). Both pairs cross-link and are differentiated by buyer; merge with a 301 if live SERPs show one intent.

## Recommended path to launch

1. Allow vendor domains in the environment's network settings (or use a session with open network access), then run a re-verification pass: re-fetch every `Needs verification` and `Search-confirmed` row, restore exact prices with inline sources, and set rows to Verified.
2. A human editor works through `publishing-checklist.md` per page, starting with the 5 pillars, the 6 pricing guides and the 20 comparisons.
3. Set the brand and domain in `site.config.json`, run `apply_config.py`, mark the pages `approved`, then run `build_sitemap.py`.
