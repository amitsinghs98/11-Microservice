# Pillar and Silo Brief (clusters 6–15), 7 November 2026

Project root: `/home/user/11-Microservice/growth-software-content-blueprint`. You own **one cluster**. Read first:

- `progress/agent-brief.md`
- `progress/completion-brief.md`, for the sourcing method: official-domain WebSearch only, Search-confirmed logging, never invent figures
- `strategy/html-article-spec.md` and `strategy/site-brief.md`. The brand is **InsightToolz**, the domain is **https://insighttoolz.com** and the author is David Esper. Don't add bylines to the HTML; the web build does that.
- In `strategy/url-manifest.json`, read every entry for your cluster: page_type, primary_keyword, source_primary_keyword, cluster_pillar and target_word_range. `strategy/keyword-validation.csv` has the Semrush data for your cluster.

## Your four jobs

**1. Expand the cluster hub to pillar depth** (target_word_range 1800–2800). The hub is the H-page whose cluster_num is yours.

- Make it the definitive guide to the whole category:
  - What the category covers, and where it borders neighbouring clusters
  - A map of the subcategories and how they fit together
  - Buying criteria that apply across the category
  - How to build a shortlist
  - Typical stack setups by team size
  - Common mistakes
  - An FAQ
- Keep the guided directory that links **all 20** cluster articles, grouped by page type, each with 1–2 sentences of context.
- Give the cluster pillar the most prominent link near the top.
- Follow the standard rules: question H2s, each with a two-sentence answer capsule; exactly one table; JSON-LD with a BreadcrumbList and a FAQPage that matches the visible FAQ exactly.
- **Hubs never carry the experience marker.**

**2. Rewrite the pillar article to pillar depth** (target_word_range 2000–3000). The pillar is the article whose page_type is `pillar-listicle`.

- The H1 stays exactly as it is.
- Use the manifest's `primary_keyword`; it may be newly retargeted. It goes in the deck, within the first 100 words, and in the title tag. The title tag is 50–60 characters before ` | InsightToolz`. The meta description is 120–160 characters.
- Cover the whole category: the best options by buyer type, with candid best-for and skip-it-if guidance for each, and pricing models with figures only where they're confirmed.
- Link **contextually to every other article in the cluster** (all 19). Weave the links into sentences, so they read as natural next steps.
- Keep exactly one experience marker, one table, and JSON-LD with a BreadcrumbList and a FAQPage.
- Source facts from official domains via WebSearch. Reuse figures already confirmed in `strategy/research/*.csv`. Rewrite your research fragment.

**3. Point every other cluster article at the pillar.** In each of the 19 sibling articles, add exactly one contextual link to the pillar's public_path.

- Put it in the most relevant section, by adjusting an existing sentence or adding one natural sentence.
- Vary the anchor text across siblings. Never use "click here" or an exact-match anchor repeated across all of them.
- Don't add any cross-cluster links. **Each article may link to at most 2 destinations outside its cluster.**

**4. Apply keyword retargets.** For any cluster article whose `primary_keyword` differs from its `source_primary_keyword`:

- Rewrite the title tag (50–60 characters + ` | InsightToolz`), the meta description (120–160 characters) and the deck/opening so the new primary keyword appears naturally within the first 100 words.
- Optionally use it in one H2.
- **Don't change the H1 or the URL.** Keep the original phrase as the page's angle.
- If you edit the FAQ, update the JSON-LD so it still matches.

## Check

Run these for every page in your cluster plus its hub, until there are 0 FAILs and 0 broken links:

```bash
python3 scripts/validate_content.py IDS && python3 scripts/check_internal_links.py --quiet IDS
```

Report any word-count or title/meta warnings you couldn't fix.

## Don't

- Run git.
- Edit scripts, the manifest, the spec, or any file outside your cluster (pages and `strategy/research/{ID}.csv` only).
- Change URLs.
- Invent prices, features, testing or experience.

## Final reply (brief)

- Hub word count, and pillar word count
- How many sibling links you added
- Which retargets you applied
- The Search-confirmed claims added
- Validator results
- Anything unresolved
