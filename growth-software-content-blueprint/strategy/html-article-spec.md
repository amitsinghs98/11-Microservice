# HTML Article Specification

Every page in `site/` follows this spec. `scripts/validate_content.py` enforces the mechanical parts.

## File location

Write each page to its `physical_file_path` from `strategy/url-manifest.json`, for example `site/best/seo-software/index.html`. The manifest is the only source of URLs. Never invent a path.

## Skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{SEO title, at most ~60 characters before the suffix} | BRAND_NAME</title>
  <meta name="description" content="{unique, accurate summary, 120–160 characters}">
  <link rel="canonical" href="https://YOUR-DOMAIN.example{public_path}">
</head>
<body>
  <main id="main-content">
    <article data-article-id="{id}" data-content-type="{page_type}" data-cluster="{cluster_num}">
      <header>
        <p>{Cluster label, e.g. "SEO software"}</p>
        <h1>{final_h1: the manifest title, or a refinement logged in the research log notes}</h1>
        <p>{One- or two-sentence deck}</p>
        <p>Draft prepared <time datetime="2026-11-04">4 November 2026</time>. Time-sensitive facts carry their own checked-on dates.</p>
      </header>

      <aside aria-label="Editorial disclosure">
        <p>Independent editorial assessment based on official product information. No vendor paid for inclusion or placement, and this page contains no affiliate links. See how we evaluate software and our disclosure policy before launch.</p>
      </aside>

      <nav aria-labelledby="toc-heading">
        <h2 id="toc-heading">On this page</h2>
        <ol>
          <li><a href="#quick-answer">Quick answer</a></li>
          ...
        </ol>
      </nav>

      <section id="quick-answer">
        <h2>Quick answer</h2>
        ...
      </section>
      ...
    </article>
  </main>
</body>
</html>
```

## Rules

- Exactly one `<h1>` and one `<article>`. Use `<h2>` for sections and `<h3>` for sub-sections, with no skipped levels.
- Every `<section>` gets a stable, unique, lowercase, hyphenated `id`. Every TOC link must match an existing `id`.
- Tables use `<caption>`, `<thead>`, `<tbody>` and `<th scope="col">`. Row headers use `<th scope="row">`. Keep tables to verifiable criteria. Use "See official pricing" rather than an unverified number.
- No CSS, `<style>`, `style=` attributes, `class=` attributes, scripts, images, iframes, fonts, tracking, site navigation, sidebars or footers.
- No JSON-LD. Author and publisher are not yet known, so truthful structured data can't be populated. Never use Review, AggregateRating or Product rating markup.
- Escape `&` as `&amp;` in text and attributes. Use plain UTF-8 punctuation.
- Indent with two spaces. Keep paragraphs short (2–4 sentences).
- Never write `TODO`, `TBD`, `lorem`, `INSERT`, `YOUR LINK HERE` or `AFFILIATE_URL_PENDING` in a page.

## Links

**Internal links** are root-relative paths that exist in `strategy/url-manifest.json` and end with `/`, for example `<a href="/compare/semrush-vs-ahrefs/">how Semrush and Ahrefs differ on backlink workflows</a>`.

- Every article links to its `parent_hub` (category hub) and, if it isn't the pillar itself, to its `cluster_pillar`.
- Add 2–5 contextual links to closely related pages in the same cluster, covering the targets named in `source_link_notes`.
- Add 1–3 cross-cluster links where they genuinely help the reader.
- Place links inside body sentences that introduce the idea. A short "Related reading" list at the end is optional and never replaces in-body links.
- Use descriptive, varied anchors. Don't reuse the same exact-match anchor for the same destination within a page. Never write "click here" or a bare "read more".
- `/software/{product}/` profiles are deferred and must not be linked. Link the vendor's official site instead.

**External links** look like `<a href="https://vendor.example/pricing" target="_blank" rel="noopener noreferrer">Vendor's pricing page</a>`.

- Use official vendor domains only. Link the homepage or the pricing/docs page that supports the claim next to it.
- Don't link to competing affiliate listicles or review aggregators as evidence.

## Required sections by page type

Adapt section names and order to each article. These are patterns, not boilerplate.

- **listicle / pillar-listicle:** quick answer with "best for" picks; who this guide is for; how we chose (criteria, evidence, no hands-on testing, order not influenced by payment); comparison table; one `<h3>` per product inside a products `<section>` (best for, what it does, key capabilities, pricing model with source link, strengths, limitations, before-you-choose, official site link); recommendations by scenario; buying mistakes and questions to ask; FAQs (`<h3>` question plus answer); verdict.
- **comparison:** quick verdict by buyer type; positioning; side-by-side table; workflow-by-workflow analysis; pricing and a total-cost scenario with stated assumptions; limitations of both; scenario fit; switching considerations; FAQs; balanced verdict.
- **alternatives:** short answer by switch reason; what the incumbent does well; why teams switch (don't invent complaints); selection criteria; table; alternatives grouped by switch reason with fit, strengths, weaknesses and migration notes; decision guide; switching checklist; FAQs; conclusion.
- **pricing-guide:** pricing models in the category; plan structures per vendor, with verified figures only, each with a source link and "checked 4 November 2026"; monthly vs annual billing; limits and add-ons; at least two worked scenarios with assumptions; free plan vs trial; renewal and next-tier triggers; questions to ask sales; unknowns; review cadence.
- **guide / strategic-guide:** the problem; step-by-step method; worked example scenario (hypothetical, labelled as such); checklists or templates; common mistakes; tools by step, linked to the relevant pages; FAQs; next steps.
- **category-hub / topical-hub:** what the category covers and the problem it solves; subcategories and use cases; terminology; decision criteria; how to narrow a shortlist; a guided directory linking **every** page in the cluster with one or two sentences of context each, grouped by page type; FAQs; next steps.

## Research log fragment

For each page, write `strategy/research/{id}.csv` with this header:

`article_id,product_or_claim,source_url,source_type,date_checked,claim_supported,verification_status,notes`

- `source_type` is one of: official-pricing, official-docs, official-site, editorial-knowledge.
- `verification_status` is one of: `Verified` (you fetched the official page on 2026-11-04 and it supports the claim), `Needs verification` (stated cautiously from prior knowledge), or `Not stated` (deliberately omitted because it couldn't be confirmed).
- Add one row per product (official URL), one row per material pricing or limit claim, and a final row `"{id}","Affiliate program","","","2026-11-04","","Not confirmed","No affiliate links used"`.
- Quote any field that contains commas.
