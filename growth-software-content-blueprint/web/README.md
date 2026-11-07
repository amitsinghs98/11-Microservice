# Styled website build

`web/` turns the plain editorial pages in `../site/` into a styled, deployable static website. The layout, components and generator approach come from the owner's MakeToolz codebase, re-themed emerald and teal.

- **No dependencies:** Node 18+ only, no npm install.
- **Content source:** `../site/` stays the single source of truth for content. This build never edits it.
- **Output:** `web/dist/`, which is gitignored and rebuilt on every deploy.

## Build and preview

```bash
node web/build.js
```

```bash
node web/build.js serve
```

The second command builds and serves the site at http://localhost:8788.

## What it builds

- All 316 pages (300 articles and 16 hubs) at the same flat URLs as `../site/`, each with:
  - The top bar and mega menu (the 15 categories, grouped by funnel stage)
  - A page header with breadcrumbs, a category tag and a draft label
  - A "Keep reading" block that links to three related guides from the same category
  - The footer
- A homepage with featured buying guides, category tiles, comparisons, pricing guides and alternatives.
- `sitemap.xml`, `robots.txt`, `llms.txt`, `404.html`, `favicon.svg` and an SVG social-share image for every page.
- The page's own title, meta description, canonical URL and JSON-LD carried over unchanged.

## Draft safety (on by default)

Every page gets `<meta name="robots" content="noindex, nofollow">`, and `robots.txt` blocks crawling, because the content is still in draft. Every article still contains a visible `[YOUR EXPERIENCE HERE]` placeholder, and many figures still need a direct re-check on the vendor's site. When pages are approved, add `"indexable": true` to `../site.config.json` and rebuild.

## Brand, domain and colours

- **Name and domain:** `brand_name` and `domain` in `../site.config.json`, currently InsightToolz at https://insighttoolz.com.
- **Colours:** the variables at the top of `assets/style.css`:
  - `--brand` `#0f9f6e`
  - `--brand2` `#0b8a8f`
  - `--grad` `#0f9f6e → #0ea5b7 → #3b82f6`

## Deploy (Cloudflare Pages, same as MakeToolz)

- **Build command:** `node web/build.js`
- **Output directory:** `web/dist`
- **Root:** the `growth-software-content-blueprint` folder

The site is static, so there are no server functions, analytics, ads or tracking scripts. The only script is the mobile menu toggle.

## Author

The byline comes from `author` in `../site.config.json` (currently David Esper). The profile lives in `web/authors.json`.

The build uses them to add:
- A "Written and researched by" box on every article
- An author page at `/author/david/`
- `Article` structured data (author, publisher, dates) alongside each page's breadcrumb and FAQ data

`credentials` and `links` are empty on purpose. Fill them with real facts only, such as past roles, years in the field or a LinkedIn URL. They then appear on the author page and in the author's structured data as `sameAs`.

## Performance and technical SEO

Lighthouse (mobile, simulated throttling) on the homepage, an article and a hub, built with `INDEXABLE=1` as if approved: **Performance 100, SEO 100, Accessibility 100, Best Practices 100**. First paint is 0.6–0.8 s, LCP 0.8–0.9 s, CLS 0, and each page transfers 13–16 KB in 2 requests.

How it's done:

- **Pre-rendered static HTML:** every page is fully rendered at build time. No client-side rendering, no framework and no hydration.
- **One request per page:**
  - The stylesheet is purged at build time to only the selectors the HTML uses (49 KB down to about 15 KB) and inlined as `<style>`.
  - The single script (the mobile menu toggle, about 300 bytes) is inlined too.
  - There are no web fonts (system font stack), no third-party scripts and no tracking.
- **HTML and JSON-LD minified.**
- **Homepage LCP image:** gets `fetchpriority="high"`; other images are lazy-loaded with `decoding="async"`.
- **`content-visibility:auto`** on below-the-fold "Keep reading" blocks.
- **`_headers` (Cloudflare Pages):** security headers (HSTS, nosniff, referrer policy, frame options) and long cache lifetimes for share images and the favicon.
- **Robots:** pages are `index, follow, max-image-preview:large, max-snippet:-1` once approved; drafts are `noindex, follow`.
- **Social previews:** `og-default.jpg` (1200×630, about 37 KB) for every page, because social networks don't render SVG previews. Twitter card tags are included.
- **Accessibility:** brand text colours meet WCAG AA contrast, and links inside running text are underlined.

To re-audit, build with `INDEXABLE=1 node web/build.js`, serve `web/dist` with gzip, and run Lighthouse. **Never deploy that build:** it removes the draft noindex.
