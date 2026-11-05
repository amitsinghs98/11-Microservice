# WordPress Migration Notes

WordPress is **not** built in this repository. These notes explain how to move the static corpus into the WordPress MVP that the source DOCX describes (§4–§7) without losing URLs, links or disclosures.

## 1. Map each file to a WordPress object

| Static page type | WordPress object | Notes |
|---|---|---|
| `/growth-stack/` (H00) | Page | Hierarchical page at the root |
| `/{cluster}/` (H01–H15) | Page | A root-level Page with the hub body |
| `/best-…/`, `/…-vs-…/`, `/…-alternatives/`, `/…-pricing/`, guides | Native Post | Set `guide_type` to best-of / comparison / alternatives / pricing / how-to. The type is a taxonomy, not part of the URL |
| `/software/{product}/` (future) | `software` CPT | One canonical record per product |

## 2. Preserve the permalink

All URLs are flat (`strategy/url-architecture.md`), which maps directly to WordPress's built-in **Post name** permalink structure (`/%postname%/`). No custom rewrite rules are needed.

- Set Settings → Permalinks → Post name.
- Import the manifest and set each post or page slug to `public_path` without the slashes.
- Posts and Pages share the root namespace, so check slug collisions on import. The build already guarantees the 316 paths are unique.

## 3. Field mapping

| HTML source | WordPress field |
|---|---|
| `<h1>` | Post title |
| `<header>` deck paragraph (the paragraph after the `<h1>`) | Excerpt |
| Everything inside `<article>` after `</header>` | Post body (Custom HTML or Classic block, or convert to blocks) |
| `<title>`, without the ` \| BRAND_NAME` suffix | SEO title (Yoast/Rank Math) |
| `<meta name="description">` | SEO meta description |
| `<link rel="canonical">` | Leave the SEO plugin's self-canonical **unless** the URL differs. Don't output two canonicals. |
| `data-article-id` | Custom field `source_article_id` |
| `data-content-type` | `guide_type` |
| `data-cluster` | Primary `software_category` |
| `primary_keyword`, `search_intent`, `angle` from the manifest | Editorial post fields `primary_keyword`, `search_intent`, `methodology_summary` |
| Research-log rows for this page | `data_sources[]`, `last_fact_checked_at` |

## 4. Preserve structure

- **Heading IDs:** keep `id` on `<section>` and headings. The Gutenberg Custom HTML block preserves them. If you convert to blocks, set the "HTML anchor" on each heading so TOC links keep working.
- **Tables:** keep `<caption>` and `<th scope>`. Gutenberg's Table block drops `scope`, so use the Custom HTML block for comparison tables, or render them from software records later.
- **Disclosures:** keep the `<aside aria-label="Editorial disclosure">` at the top. Later, render it from `affiliate_disclosure_required` and `sponsorship_disclosure`.
- **External links:** keep `target="_blank" rel="noopener noreferrer"`. For confirmed affiliate links, switch to `/go/{key}/` with `rel="sponsored nofollow noopener noreferrer"`.
- **Internal links:** these are root-relative and work unchanged when the permalinks match the manifest.

## 5. Fields that become structured data later

When the software database exists, replace repeated inline product facts with fields on the `software` CPT. This avoids drift across the roughly 300 product mentions in the corpus. Fields:

`product_name`, `vendor_name`, `official_url`, `vendor_pricing_url`, `pricing_model`, `starting_price`, `billing_period`, `free_plan`, `free_trial`, `usage_allowance`, `add_on_notes`, `price_checked_at`, `price_source_urls[]`, `primary_use_cases[]`, `key_features[]`, `integrations[]`, `strengths[]`, `limitations[]`, `best_for`, `not_for`, `affiliate_url`, `sponsored_status`, `sponsored_label`, `sponsored_start_at`, `sponsored_end_at`, `related_software_ids[]`, `alternative_product_ids[]`, `comparison_post_ids[]`, `guide_post_ids[]`, `category`.

The product sections in the listicles (one `<h3>` per product with best for, pricing, strengths, limitations and official link) map one-to-one to a "product card" render block.

## 6. If WordPress uses different paths

Any change from the manifest paths needs:

1. A 301 redirect from the manifest path to the new path.
2. A rewrite of internal links. Search and replace on `href="/old/path/"` across post content, or update the manifest and re-export.
3. A re-run of `scripts/check_internal_links.py` against an export, or a crawl of staging with a link checker.

## 7. Canonicals and sitemaps in WordPress

- Let the single SEO plugin generate canonicals and the XML sitemap. Don't import `site/sitemap.xml`.
- Exclude thin taxonomy archives (`software_feature`, `pricing_model`) and filter URLs from the sitemap and index until they have real content (DOCX §12).
- Make sure the theme doesn't output a second `<link rel="canonical">`.

## 8. Suggested import procedure

1. Parse each `site/**/index.html` with a script (Python + WP-CLI, or the REST API).
2. Extract the title, excerpt, body, meta and IDs as in §3.
3. Create posts as **drafts**, with author left unset for the editor to assign.
4. Set the permalink from the manifest. Attach the category and `guide_type`.
5. An editor reviews each draft against `publishing-checklist.md` before publishing.
