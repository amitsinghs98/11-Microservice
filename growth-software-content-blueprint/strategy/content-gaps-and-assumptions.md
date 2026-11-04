# Content Gaps and Assumptions

Decisions made where the source DOCX or the build brief was silent or conflicting. Each one is conservative and reversible.

## Repository and hosting

1. **Repository location (deviation from brief §3).** The brief asks for a new private GitHub repository named `growth-software-content-blueprint`. This build ran in a cloud session whose GitHub access covers only `amitsinghs98/11-Microservice`, and it can't create repositories. Following the owner's instruction to "use the repo and create a folder", the project lives in the `growth-software-content-blueprint/` folder of that repository, on branch `claude/dazzling-cray-wjh11a`. It is self-contained: copy the folder into a fresh repo with the commands in `README.md` → *Moving to its own repository*.
2. No deployment, GitHub Pages or public publication was performed.

## Source plan

3. **Article count.** The DOCX has exactly 100 entries (5 × 20). Nothing was added to or removed from the counted set.
4. **Hubs are extra pages.** The DOCX defines `/growth-stack/` ("not counted in the 100") and five `/categories/…/` hubs. They were built as H00–H05 and kept outside the count.
5. **Titles.** All H1s keep the DOCX working titles. Writers could refine the SEO `<title>` tag for length, but the H1 and intent are unchanged.
6. **The DOCX says titles are hypotheses.** Search demand, SERP format and keyword difficulty were **not** validated (no SEO data source was used). Check them before publishing, as DOCX §10 instructs.

## Deferred items (future dependencies)

7. **Software profiles (`/software/{product}/`).** The DOCX wants "at least 15 canonical software profiles" before Batch 1 publishes, but names no products, and profiles aren't in the 100. None were created and no article links to one. Recommended first 20 profiles, chosen by how often the products appear across the corpus: Semrush, Ahrefs, SE Ranking, Surfer, Jasper, Copy.ai, Writesonic, ChatGPT, Claude, Mailchimp, Klaviyo, ActiveCampaign, HubSpot, Instantly, Smartlead, Lemlist, Apollo.io, Clay, Pipedrive, Zapier. When they exist, add them to `scripts/build_manifest.py`, then link them from the listicles, comparisons and alternatives pages.
8. **Vendor and trust pages** (`/for-vendors/`, `/submit-software/`, `/claim/{product}/`, About, Editorial Policy, How We Evaluate, Affiliate Disclosure, Sponsored Content Policy, Contact, Privacy, Terms). These are required by the DOCX before launch but are out of scope for this article corpus. Every article's disclosure sentence refers readers to "how we evaluate software and our disclosure policy" as plain text, **not** a link, so there are no broken links. Turn it into a link once those pages exist (listed in `publishing-checklist.md`).
9. **Correction flow.** The DOCX's "Correct this page" link needs a form (WordPress phase). It isn't in the HTML yet.

## Facts and pricing

10. **Verification.** Drafting agents could fetch official vendor pages on 4 November 2026 for a limited number of claims. Only claims logged `Verified` in `research-source-log.csv` were checked against an official source. Everything logged `Needs verification` was written cautiously from general product knowledge and must be confirmed before publication. Pricing pages and comparisons are the priority.
11. **No hands-on testing** was performed for any product. Pages say so and never claim testing.
12. **Affiliate programs.** None are confirmed. Every outbound vendor link is the plain official URL. No placeholder affiliate URLs exist in the HTML.
13. **Sponsored placements.** None. No page is labelled sponsored.
14. **Currency.** Where prices appear, they are the vendor's published USD list prices unless stated otherwise. Taxes are excluded.

## Brand, authorship and metadata

15. **Brand and domain.** Neither was supplied. The placeholders `BRAND_NAME` and `https://YOUR-DOMAIN.example` are set in `site.config.json` and applied with `scripts/apply_config.py`.
16. **Authors.** No author names, bios or credentials were invented. Pages show only a draft-prepared date (4 November 2026, the actual drafting date). Add bylines in WordPress.
17. **Structured data.** No JSON-LD was added, because author and publisher are unknown and couldn't be filled truthfully. Add `Article`/`BreadcrumbList` through the SEO plugin at launch. Never add `Review`/`AggregateRating` markup.
18. **Robots.** `site/robots.txt` allows crawling (the brief: "disallow nothing by default"). Review it at launch. `site/index.html` carries `noindex` because it is a QA directory, not a homepage.

## Cannibalization

19. See `topical-cluster-map.md` → *Cannibalization risks*. The highest risk is **A053 vs A095** (both HubSpot vs ActiveCampaign). They were differentiated by buyer (email marketer vs platform/RevOps owner), but **consider merging them** if live SERPs show a single intent.
