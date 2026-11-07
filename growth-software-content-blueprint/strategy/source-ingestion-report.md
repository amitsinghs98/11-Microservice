# Source Ingestion Report

| Source | Location | Used for | Rows |
|---|---|---|---|
| 100-article strategy DOCX | `inputs/content-strategy.docx` (local only, gitignored) | A001–A100 titles, queries, intents, angles, briefs, link notes, cluster and hub structure; extracted by `scripts/extract_source_map.py` | 100 articles, 5 clusters, `/growth-stack/` + 5 hubs |
| Additional 200 articles (CSV) | `inputs/additional-200-articles.csv` | A101–A300, clusters 6–15: title, slug, page type, primary query, angle, writing brief, link targets | 200 articles, 10 clusters |
| Additional 200 articles (MD) | `inputs/additional-200-articles.md` | Human-readable copy of the CSV; used to cross-check | 200 |
| 100- and 300-article master prompts | conversation inputs | Build rules, file layout, QA requirements, hard constraints | n/a |
| seo-content-writer standard | skill | v2 page spec (`strategy/html-article-spec.md`) | n/a |

## Transformations

- Titles were kept verbatim as H1s. `source_slug` is preserved in the manifest next to the final flat `public_path` (`strategy/url-migration-map.csv`).
- Page types were mapped as follows: DOCX intents through `classify()`; CSV types `best→listicle` and `pricing→pricing-guide`.
- Cluster hubs H06–H15 were added for the new clusters. Clusters 6–15 have no pillar in the source, so their hub is the parent.
- Assertions in `build_manifest.py`: IDs are exactly A001–A300, and there are no duplicate paths or titles.

## External evidence

- Official vendor pages were fetched on 4 November 2026 until the Firecrawl credits ran out. After that, only claude.com, anthropic.com, support.claude.com and github.com were reachable; the network policy blocked other vendor hosts (proxy 403).
- Some writers on 5 November used web-search index results restricted to official domains as a fallback. Those rows are logged as `Search-confirmed`, not `Verified`.
- No third-party review sites, affiliate listicles or competitor publishers (G2, DeployHyre, SaasHyre, MakeToolz) were used as sources or copied.
