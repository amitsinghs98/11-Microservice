# HTML Article Specification (v2: seo-content-writer standard)

Every page in `site/` follows this spec. `scripts/validate_content.py` enforces the mechanical parts. Inputs to read before writing: `strategy/site-brief.md` (voice, say/don't-say, hard rules), `strategy/editorial-guidelines.md`, `strategy/keyword-map.csv` and the page's record in `strategy/url-manifest.json`.

## Core principle

AI engines and searchers lift a **specific sentence** and the **link next to it**. Make each answer trivial to extract, and make it impossible to detach a claim from its source.

## The rule of one

- One question per H2.
- A two-sentence answer directly under every content H2. Those first two sentences answer the question completely on their own, with no setup. Detail follows.
- One source per factual claim, linked inline on the words that state the claim. Never put a "Sources" or "References" block at the end.
- **Exactly one `<table>` per page**, the comparison table.
- One first-hand experience section, holding the marker below.

## File location

Write each page to its `physical_file_path` from `strategy/url-manifest.json`. That manifest is the only source of URLs.

## Skeleton

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{50–60 characters before the suffix} | BRAND_NAME</title>
  <meta name="description" content="{120–160 characters, unique, contains the primary keyword}">
  <link rel="canonical" href="https://YOUR-DOMAIN.example{public_path}">
  <script type="application/ld+json">
  {JSON-LD: see "Schema" below}
  </script>
</head>
<body>
  <main id="main-content">
    <article data-article-id="{id}" data-content-type="{page_type}" data-cluster="{cluster_num}">
      <header>
        <p>{Cluster label}</p>
        <h1>{manifest title, unchanged}</h1>
        <p>{Deck: one or two sentences that answer the page's core question and contain the primary keyword. Together with the first section, the primary keyword must appear within the first 100 words of body text.}</p>
        <p>Draft prepared <time datetime="2026-11-04">4 November 2026</time>. Time-sensitive facts carry their own checked-on dates.</p>
      </header>

      <aside aria-label="Editorial disclosure">
        <p>Independent editorial assessment based on official product information. No vendor paid for inclusion or placement, and this page contains no affiliate links. No hands-on product testing was performed for this draft.</p>
      </aside>

      <nav aria-labelledby="toc-heading">
        <h2 id="toc-heading">On this page</h2>
        <ol>
          <li><a href="#which-tool-should-you-choose">Which tool should you choose?</a></li>
          ...
        </ol>
      </nav>

      <section id="which-tool-should-you-choose">
        <h2>Which {category} tool should you choose?</h2>
        <p>{Answer capsule: two sentences that fully answer the question.}</p>
        ...
      </section>

      <section id="first-hand-experience">
        <h2>{A question a sceptical reader would ask, e.g. "What do these tools get wrong in real agency use?"}</h2>
        <p>{Two-sentence capsule from the documented evidence, carefully hedged.}</p>
        <p><mark>[YOUR EXPERIENCE HERE — the skill will not invent this]</mark></p>
      </section>
      ...
      <section id="faq">
        <h2>What else do buyers ask about {topic}?</h2>
        <p>{Two-sentence capsule.}</p>
        <h3>{Question?}</h3>
        <p>{Answer.}</p>
        ...
      </section>
    </article>
  </main>
</body>
</html>
```

## Headings

- Exactly one `<h1>`: the manifest title, unchanged, so the source title is preserved.
- **Every content `<h2>` is a question ending in `?`.** The TOC heading "On this page" is exempt. Order the H2s the way a reader's questions arrive, not by search volume. Map the page's angle and brief dimensions to H2s.
- `<h3>` for sub-questions or per-product blocks. Product block H3s can be the product name, for example "Semrush: best for multi-channel agency teams". Don't skip heading levels.
- Every `<section>` has a stable, unique, lowercase, hyphenated `id`. Every TOC link resolves.

## Experience marker (mandatory)

No first-hand experience was supplied. Every article (not hubs) contains exactly one literal marker:

`<p><mark>[YOUR EXPERIENCE HERE — the skill will not invent this]</mark></p>`

Put it where a reader is most sceptical, usually right after the first answer capsule or in the limitations section. **Never fabricate an anecdote, client, result, measurement or test** to fill it.

## Sources: fetched, not remembered

- For every factual claim about a product (price, plan, limit, feature, integration, free plan, trial), fetch the official page with your web tool, confirm the claim is actually on that page, and link it inline:
  `…the Pro plan <a href="https://vendor.example/pricing" target="_blank" rel="noopener noreferrer">lists 500 tracked keywords</a> (checked 4 November 2026).`
- **If you can't fetch and confirm it, cut the claim, or state it without the number** ("pricing is per seat; check the current tiers on the vendor's pricing page").
- Prefer primary sources: official pricing, docs, help-center articles and the company's own announcements. Never use an affiliate listicle or review aggregator as evidence.
- Log each claim in `strategy/research/{ID}.csv` (format below).
- General, non-product statements (how attribution models work, what DMARC is) need no source unless they include a statistic. Never write statistics you didn't fetch.

## The one table

A comparison table with verifiable columns only: best for, pricing model, one material limit, official link. Use `<caption>`, `<thead>`, `<tbody>`, `<th scope="col">` and `<th scope="row">`. Write "See official pricing" rather than an unverified number. Guides may use their one table for a checklist, template or decision matrix instead.

## Schema (JSON-LD in `<head>`)

There is one `<script type="application/ld+json">` block with an `@graph` containing:

1. `BreadcrumbList`: Home (`https://YOUR-DOMAIN.example/`) → hub (`parent_hub`, using the hub's manifest title) → this page.
2. `FAQPage`: `mainEntity` lists exactly the `<h3>` questions in the FAQ section and their answer text. It must be **identical to the visible text** (plain text, no HTML).

Don't add `Article`/`BlogPosting` (author and publisher are unknown), `Review`, `AggregateRating`, `Product` or ratings. No other `<script>` is allowed. The JSON must parse.

Hubs: `BreadcrumbList` only (H00: Home → this page). Add `FAQPage` if the hub has an FAQ section.

## Page-type patterns

Adapt these. Each is a set of reader questions, not boilerplate. Every H2 is phrased as a question.

- **listicle / pillar-listicle:** Which should you choose (best-for picks)? Who is this for and what problem does it solve? How did we choose (criteria, evidence, no testing, order not influenced by payment)? How do they compare (the table)? Per-product H3 blocks: best for, what it does, key capabilities, pricing model with an inline source, strengths, limitations, skip it if, official link. Which fits your scenario? What mistakes do buyers make? FAQ. What's the verdict? Soft CTA to the next page.
- **comparison:** Which should you choose (verdict by buyer type)? How are they positioned? How do they compare (the table)? Workflow-by-workflow questions. What does each really cost (scenario with stated assumptions; fetched figures only)? Where does each fall short? How hard is switching? FAQ. Verdict.
- **alternatives:** Which alternative fits your reason for switching? What does the incumbent do well? Why do teams switch (legitimate triggers only; no invented complaints)? How do the alternatives compare (table)? Alternatives grouped by need, with migration notes. What should you check before switching (export, contracts, automations)? FAQ. Verdict.
- **pricing-guide:** How is this priced? Plan structures per vendor (fetched figures only, each with an inline source and checked date). Monthly or annual? What triggers the next tier? Two or more worked scenarios with assumptions. What's not public (quote-only)? Questions to ask sales. Review cadence.
- **guide / strategic-guide:** What's the problem? What are the steps (ordered, with decision points, roles, data fields and QA)? A worked example, labelled hypothetical. A template or checklist (the table). What goes wrong? Which tools help at each step (internal links)? FAQ. Next steps.
- **category-hub / topical-hub:** What does this category cover, and what jobs does it do? What are the subcategories and boundaries (including boundaries with neighbouring clusters)? What criteria matter? How do you narrow a shortlist? A guided directory that links **every** page in the cluster, grouped by page type, with one or two sentences of context each. FAQ. A method note. Hubs don't carry an experience marker.

## Links

**Internal links** are root-relative `public_path` values from the manifest, with a trailing slash.

- Every article links to its `parent_hub`. Original-cluster articles also link to their `cluster_pillar`.
- 2–5 contextual links to closely related pages in the same cluster, covering `source_link_notes`, which you convert to real manifest URLs.
- 1–3 cross-cluster links only where the reader's next step genuinely lives there. The 300-page manifest has 15 clusters, so search it for the right page.
- Put links inside sentences, with descriptive anchors that vary in wording. Never use "click here" or a bare "read more", and never repeat an exact-match anchor mechanically.
- Never link to `/software/` (profiles are deferred).

**External links** are official vendor domains only, written as `target="_blank" rel="noopener noreferrer"`. No affiliate links.

## Banned

CSS, `style=`, `class=`, non-JSON-LD scripts, images, iframes, site navigation, footers, author bios (no author is known), `TODO`/`TBD`/`lorem`, invented numbers, testing claims, ratings, and a trailing Sources block.

## Research log fragment `strategy/research/{ID}.csv`

Header: `article_id,product_or_claim,source_url,source_type,date_checked,claim_supported,verification_status,notes`

- `source_type`: official-pricing | official-docs | official-site | editorial-knowledge
- `verification_status`:
  - `Verified`: fetched on 2026-11-04 and the page supports the claim.
  - `Needs verification`: a qualitative statement from general knowledge, kept cautious.
  - `Not stated`: deliberately cut because it couldn't be confirmed.
- One row per product (its official URL) and one per material claim. The final row is:
  `{ID},Affiliate program,,,2026-11-04,,Not confirmed,No affiliate links used`
- Quote any field that contains a comma.
