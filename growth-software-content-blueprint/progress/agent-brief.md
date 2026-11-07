# Writer Brief (for every drafting agent)

You are writing pages for a static HTML library of growth-software buying guides, to the **seo-content-writer** standard. Project root: `/home/user/11-Microservice/growth-software-content-blueprint`

## Read first, in full

1. `strategy/site-brief.md`: voice, reader, say/don't-say, hard rules
2. `strategy/html-article-spec.md`: **v2 spec**: skeleton, rule of one, question H2s with two-sentence answer capsules, experience marker, fetched inline sources, one table, JSON-LD, links, research log
3. `strategy/editorial-guidelines.md`
4. `strategy/url-manifest.json`: every page's title, page_type, public_path, physical_file_path, parent_hub, cluster_pillar, primary_keyword, angle, brief, source_link_notes and target_word_range. It's the **only** valid source of internal URLs. Skim all 316 entries so your links land on the right pages across the 15 clusters.
5. `strategy/keyword-map.csv`: the primary keyword and secondary topics. Map the secondaries to question H2s.

## For each assigned page

- **If the file already exists**, it is an earlier (v1) draft. Rewrite it to the v2 spec. Keep accurate content and its verified sources, convert headings to questions with answer capsules, cut to one table, add the marker and JSON-LD, and re-check facts. Update its research fragment.
- Write a complete, original, in-depth page (not an outline). Follow the manifest's **angle** and **brief** closely, because they come from the client's strategy. Hit `target_word_range` with substance, not padding.
- Choose real, relevant products (usually 6–10 for best-of pages). Be candid: give best-for and skip-it-if guidance, and name real limitations. Don't praise everything equally.
- **Sources, fetched not remembered:** use your web fetch/scrape tool (for example `firecrawl_scrape`) on official vendor pricing and docs pages. State a specific price, limit or feature only if you fetched the page and confirmed it, and cite it inline next to the claim with "(checked 4 November 2026)". If you can't confirm it, cut the number or the claim. Budget is roughly 4–12 fetches per page (more for pricing and comparison pages). Record every claim in the page's research fragment.
- Primary keyword: in the H1 (kept as the manifest title) and **within the first 100 words after the H1**, ideally in the deck. Don't repeat it mechanically after that.
- Exactly one marker `<p><mark>[YOUR EXPERIENCE HERE — the skill will not invent this]</mark></p>` per article, placed where the reader is most sceptical. Never invent experience, clients, results or tests.
- The title tag is 50–60 characters before ` | InsightToolz`. The meta description is 120–160 characters. Both are unique.
- Vary openings, capsules and FAQ wording. Never reuse paragraphs across pages.

## Live-fetch availability (important)

The Firecrawl credits are exhausted until 2026-11-05 19:42 UTC, and the network policy blocks most vendor sites, so expect fetches to fail.

- Try a fetch once or twice. If it fails, stop retrying.
- **Keep any claim already logged `Verified` today (2026-11-04) in an existing `strategy/research/*.csv` row with a source URL.** An earlier writer fetched those while access worked. Keep the inline citation and "(checked 4 November 2026)", and carry the row into your fragment with a note like "verified by earlier writer". Don't delete verified figures from v1 drafts.
- Cut every other number, describe pricing by its model, and log `Needs verification`.
- Never log your own arithmetic or hypothetical models as `Verified`. Use `editorial-knowledge` with the status `Not stated`, and the note "calculation from stated assumptions".

## Check your work

```bash
cd /home/user/11-Microservice/growth-software-content-blueprint && python3 scripts/validate_content.py IDS && python3 scripts/check_internal_links.py --quiet IDS
```

Replace `IDS` with your IDs, space-separated. Fix every FAIL, and every word-count, title or meta warning you reasonably can. In the link check, `destination file missing` is fine, because other writers are working in parallel. `not in manifest`, `missing trailing slash` and `not root-relative` must be fixed.

## Don't

- Run git.
- Touch files other than your pages and `strategy/research/{ID}.csv`.
- Edit the scripts, manifest or spec.
- Create or link `/software/` pages.

## Final reply (brief)

Per page: ID, word count, products covered, number of fetched and verified claims, and any concerns (cannibalization, unverifiable facts).
