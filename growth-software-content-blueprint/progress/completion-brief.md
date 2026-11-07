# Completion Brief (verification and completion pass, 5 November 2026)

You are bringing ONE existing, already-drafted page to editor-ready state. Project root: `/home/user/11-Microservice/growth-software-content-blueprint`.

## Read first

- `progress/agent-brief.md`, `strategy/html-article-spec.md`, `strategy/site-brief.md`
- Your page's entry in `strategy/url-manifest.json` and its current file and `strategy/research/{ID}.csv`.

All their rules still apply:
- No fabrication.
- Exactly one table.
- Question H2s with two-sentence answer capsules.
- Exactly one experience marker, left unchanged.
- The JSON-LD FAQ matches the visible FAQ exactly.
- Internal links are flat URLs from the manifest only.
- No testing claims.

## The gap you're closing

Vendor websites are blocked by the network policy: direct fetches get a proxy 403, so don't retry them. claude.com, support.claude.com and anthropic.com are the exception and can be fetched directly with `curl -sS -L URL`. Because of the block, most facts are logged `Needs verification` and pricing reads "See official pricing".

## Steps

1. **Reuse first.** Figures already confirmed today are in `strategy/research/A001.csv` (SEO tools), `A017.csv` (SEO pricing) and `A030.csv` (ChatGPT and Claude). If your page covers the same product, reuse those figures and URLs so the pages stay consistent.
2. **Search official domains only.** For every product and material claim (plan names, prices monthly and annual, the units that drive the next tier, free plan or trial, key features and limits), use the **WebSearch** tool with `allowed_domains` set to the vendor's OFFICIAL domains only (e.g. `["hubspot.com"]`, `["help.instantly.ai","instantly.ai"]`). Use mode `standard`. Budget: 15–30 searches. Prefer pricing, help-center and docs pages over blog posts.
3. **Add a figure only if the results clearly state it from an official page.** Link it inline to that official URL (`target="_blank" rel="noopener noreferrer"`) and add "(checked 5 November 2026)". Log it as `Search-confirmed`, with source_type `official-pricing` or `official-docs`, date_checked `2026-11-05`, and the note `confirmed via search index of official page; re-fetch before publishing`.
   - If sources conflict, look dated, or come only from forums, community posts or third parties, leave the number out and tell the reader to check the official page.
   - Never present a claim supported only by community or forum posts as fact.
4. **Correct and remove.** Fix renamed plans or products and discontinued features. Remove claims you can't support.
5. **Worked cost scenarios** (pricing guides and comparisons): use confirmed figures only, and label the assumptions as hypothetical. Log the arithmetic as `editorial-knowledge` / `Not stated` / `calculation from stated assumptions`.
6. **Update the one table** with the confirmed figures.
7. **Fairness.** Every product gets the same depth and the same type of evidence, with candid best-for and skip-it-if guidance.
   - If the page compares Claude/Anthropic with other AI vendors, balance the evidence. Don't favour Claude.
   - In that case, also add one sentence to the disclosure aside saying the draft was prepared with an AI model from one of the compared vendors and needs independent human review.
8. **Polish.** Tighten generic passages. Keep the page near the manifest `target_word_range`; the validator's band is the hard limit.
9. **Validate.** Run `python3 scripts/validate_content.py ID && python3 scripts/check_internal_links.py --quiet ID` and fix every FAIL.

## Don't

- Run git.
- Edit scripts, the manifest, the spec, or any page or research file other than your own.

## Final reply (brief)

- The Search-confirmed claims (product: figure).
- What you corrected or removed.
- What remains Needs verification.
- The validator result and word count.
