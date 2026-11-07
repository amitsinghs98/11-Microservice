# Build Progress

Resume here after any interruption. Read this file, `strategy/url-manifest.json` (status field) and `qa/article-status.csv`. Then queue any batch below that isn't marked done. Agents follow `progress/agent-brief.md`. Existing v1 drafts are rewritten to the v2 spec (see `strategy/html-article-spec.md`).

## Scope

- 300 articles (A001–A100 from the DOCX, A101–A300 from the additional-200 map), 15 cluster hubs (H01–H15) and the umbrella hub H00.
- Standard: seo-content-writer (question H2s with answer capsules, fetched inline sources, one table, experience marker, JSON-LD).

## Batch queue (5 pages per agent)

| Batch | IDs | Status |
|---|---|---|
| W1 | A001–A100 (20 batches) | in progress |
| W2 | A101–A200 (20 batches) | queued |
| W3 | A201–A300 (20 batches) | queued |
| W4 | H00–H15 (hubs) | queued |
| QA | full validation, link audit, index, sitemap, reports | queued |

## Log

- 2026-11-04: Skeleton, manifest (100 articles), v1 spec and QA scripts created. 52 v1 drafts were written before a container restart interrupted the first agent run, and were checkpointed in commit b78568e.
- 2026-11-04: Scope expanded to 300 articles and 15 clusters. Adopted the seo-content-writer standard (spec v2, site brief, keyword map). Validator enforces the v2 rules. Wave W1 launched.
- 2026-11-04: A071–A075 v2 done (agent report). **Blocker:** the Firecrawl MCP daily credit allowance is exhausted (resets 2026-11-05 19:42 UTC), and the environment network policy denies vendor hosts (for example www.hubspot.com and www.salesforce.com return proxy 403). Writers are cutting every number they can't confirm, and logging those claims as `Needs verification` or `Not stated`. A re-verification pass is needed once access is restored. QA note: A072 relinked `/compare/activecampaign-vs-hubspot/` to A053, but A095 is in the manifest, so restore that link.
- 2026-11-04: A076–A080 v2 done. v1 numbers without a source were removed from A076 and A077. A re-fetch pass is needed to restore HubSpot, Zoho, Attio, Capsule and Bitrix24 free-plan caps and prices.
- 2026-11-04: A086–A090 v2 done (0 fetched). QA: relabel arithmetic and hypothetical rows that were logged as 'Verified'. Unconfirmed facts to check: Hotjar is part of Contentsquare; Google Optimize was retired in 2023; Meta restricted third-party posting to Facebook Groups.
- 2026-11-04: A041–A045 v2 done (0 fetched). Brief updated: keep figures already logged Verified today, and never mark arithmetic as Verified. A041 and A042 lost their earlier Verified MailerLite and Mailchimp figures; restore them from the research CSV notes in QA.
- 2026-11-04: A046–A050 v2 done (0 fetched). QA recovery: the v1 research fragments, including Verified rows from when fetching worked, are in commit b78568e. Use `git show b78568e:growth-software-content-blueprint/strategy/research/AXXX.csv` to restore verified figures that rewrites removed.
- 2026-11-04: A081–A085, A091–A095 and A096–A100 v2 done. They reuse figures logged Verified earlier today in A091, A061, A051, A055 and A031/A032; re-fetch those before launch. Confirm: GA4 retired its rule-based attribution models; n8n licence terms.
- 2026-11-04: A016–A020 and A031–A035 v2 done. The v1 SEO pricing figures for A016–A018 had no research log, so they were removed and logged as Not stated. A017 (pricing guide) needs the biggest re-fetch pass.
- 2026-11-04: A036–A040 and A051–A055 v2 done. QA: spot-check A037's claim that Claude Max is $100 and the $200 tier is 'Ultra' against claude.com/pricing.
- 2026-11-04: A061–A065 v2 done.
- 2026-11-04: A006–A010 v2 done.
- 2026-11-04: A066–A070 v2 done.
- 2026-11-04: A001–A005 v2 done (0 fetched; v1 figures removed and logged as Not stated).
- 2026-11-04: A056–A060 v2 done. Their claims were checked with WebSearch restricted to official domains, not a direct fetch. QA: give these rows their own status ('Verified via official-domain search'), and re-fetch the claims before publishing.
- 2026-11-04: A021–A025 v2 done. **Neutrality risk:** Claude is the only product with confirmed prices (anthropic.com was the only reachable site), so cluster-2 tables carry numbers for Claude alone. QA: either restore the other vendors' figures (A031 log or a re-fetch), or move Claude's prices out of the tables, so the tables don't look tilted.
- 2026-11-04: A026–A030 v2 done. **Conflict-of-interest flag:** A030 (ChatGPT vs Claude) was drafted by a Claude model; only Claude's facts could be verified. It needs a human neutrality review and OpenAI's figures before publishing.
- 2026-11-04: A011–A015 v2 done (figures confirmed via official-domain WebSearch). **Wave W1 (A001–A100) complete.**

## Pending decision: flat URLs (owner request, 2026-11-04)

The owner wants plain, flat URLs (for example `/best-ai-writing-tools/` or `/instantly-alternatives/`) instead of `/best/…/`. Run the migration **after all writing is finished**, so in-flight agents don't produce mixed links. The scheme:

| Page type | Old | New |
|---|---|---|
| Best-of | `/best/{slug}/` | `/best-{slug}/` (no doubled `best-`). A001–A100 use the DOCX source slug as-is, for example `/best-seo-software/`. |
| Comparison | `/compare/{a}-vs-{b}/` | `/{a}-vs-{b}/` |
| Alternatives | `/alternatives/{product}/` | `/{product}-alternatives/` |
| Pricing | `/pricing/{topic}/` | `/{topic}-pricing/` (DOCX source slug where it has one, for example `/seo-software-pricing/`) |
| Guides | `/guides/{slug}/` | `/{slug}/` |
| Category hubs | `/categories/{x}/` | `/{x}/` (for example `/seo/`, `/content-operations/`) |
| Umbrella hub | `/growth-stack/` | unchanged |

Migration steps: update the manifest, move the files, rewrite every internal href, canonical and JSON-LD URL, check for collisions, then re-run all QA.
- 2026-11-05: A container restart stopped the workflow. On disk: A101–A259, all passing validation. Resumed the run (wf_c75cbb6e-5f6) to finish A260–A300, H00–H15 and the pending fact-check stages.

2026-11-05: Flat URL migration done. `build_manifest.py` now has a `flatten()` function; 315 pages were moved with `git mv` (`/growth-stack/` was unchanged); 4,002 hrefs, canonicals and JSON-LD URLs were rewritten; the old-to-new map is in `strategy/url-migration-map.csv`. After re-running QA: 316/316 pages pass, 3,090 internal links, 0 broken, 0 orphans.

2026-11-05: Completion pass on A001, A017 and A030 (search-confirmed vendor figures from official domains, corrections for renamed plans, A030 rebalanced with ChatGPT figures and a disclosure note about the AI vendor). All three pass QA. Figures are Search-confirmed and need a direct fetch before publishing.

2026-11-05: Completion pass on A011, A012 and A013 (brief: progress/completion-brief.md). 6 money pages now complete: A001, A011, A012, A013, A017, A030. Paused at the owner's request. Next in the queue: A014, A015, A021, A031–A034, A037, A041, A051–A055, A057, A061, A071–A075, A077, A081, A091–A095, A097, A106, A113, A135, A159, A179, A198, A207, A208, A219, A239, A254, A260, A298, A299.

2026-11-06: Completion pass on 10 more money pages: A014, A015, A021, A031, A032, A033, A034, A037, A041, A051. In total 16 money pages are complete: A001, A011–A015, A017, A021, A030–A034, A037, A041, A051. The AI-cluster pages compared with Claude (A021, A031–A034, A037) were rebalanced with ChatGPT and other vendors' figures and carry an AI-vendor disclosure sentence. Still queued: A052–A055, A057, A061, A071–A075, A077, A081, A091–A095, A097, A106, A113, A135, A159, A179, A198, A207, A208, A219, A239, A254, A260, A298, A299.

2026-11-07: Brand InsightToolz, domain insighttoolz.com and author David Esper set. Semrush keyword validation done for all 316 keywords, with 46 retargets. 10 new pillars and hubs at pillar depth for clusters 6–15. Cross-cluster links cut to 22%. Experience/approval sheet created for David. All 316 pages pass QA; 3,169 internal links, 0 broken.
