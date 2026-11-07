#!/usr/bin/env node
/**
 * Styled website build for the growth-software content library.
 *
 * Zero dependencies. Reads the semantic pages in ../site/ (the editorial source of truth)
 * plus ../strategy/url-manifest.json and ../site.config.json, and writes a styled,
 * deployable static site to ./dist/ using the design system in ./assets/ (adapted from the
 * owner's MakeToolz generator, re-themed emerald/teal).
 *
 *   node web/build.js          -> writes web/dist/
 *   node web/build.js serve    -> builds and serves web/dist/ on http://localhost:8788
 *
 * The ../site/ pages are never modified. Edit content there, then rebuild.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WEB = __dirname;
const ROOT = path.dirname(WEB);
const DIST = path.join(WEB, 'dist');
const cfg = JSON.parse(fs.readFileSync(path.join(ROOT, 'site.config.json'), 'utf8'));
const pages = JSON.parse(fs.readFileSync(path.join(ROOT, 'strategy', 'url-manifest.json'), 'utf8')).pages;

// ============ SITE CONFIG ============
const SITE = {
  brand: cfg.brand_name || 'BRAND_NAME',
  url: (cfg.domain || 'https://YOUR-DOMAIN.example').replace(/\/$/, ''),
  tagline: 'Growth software, compared honestly',
  desc: 'Independent buying guides, comparisons and pricing guides for the software behind SEO, content, outreach, CRM, automation and measurement.',
  year: '2026',
  // Drafts are not approved for publication yet: every page gets noindex and robots.txt
  // disallows crawling until this is switched to true (see web/README.md).
  indexable: cfg.indexable === true || process.env.INDEXABLE === '1', // INDEXABLE=1 is for audits only
  // Byline shown on every page. Use a real reviewer's name only; never an invented persona.
  author: cfg.author || `${cfg.brand_name || 'BRAND_NAME'} Editorial Team`,
};
// =====================================

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const unesc = s => String(s).replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
const strip = s => unesc(String(s).replace(/<[^>]+>/g, '')).replace(/\s+/g, ' ').trim();
const hash = f => crypto.createHash('md5').update(fs.readFileSync(path.join(WEB, 'assets', f))).digest('hex').slice(0, 8);
const V = { css: hash('style.css'), js: hash('site.js') };

const byId = Object.fromEntries(pages.map(p => [p.id, p]));
// Author profiles. Only facts the author or owner supplied; never invented credentials.
const AUTHORS = JSON.parse(fs.readFileSync(path.join(WEB, 'authors.json'), 'utf8'));
const AUTHOR_SLUG = Object.keys(AUTHORS).find(k => AUTHORS[k].name === SITE.author);
// Author pages live under /author/ (articles stay flat). Override per author with "url" in authors.json.
const AUTHOR = AUTHOR_SLUG ? { slug: AUTHOR_SLUG, ...AUTHORS[AUTHOR_SLUG], url: AUTHORS[AUTHOR_SLUG].url || `/author/${AUTHOR_SLUG}/` } : null;
if (AUTHOR && pages.some(p => p.public_path === AUTHOR.url)) throw new Error(`Author URL ${AUTHOR.url} collides with a page`);
const initials = n => n.split(/\s+/).map(w => w[0]).join('').slice(0, 2).toUpperCase();
const PUBLISHER = { '@type': 'Organization', name: SITE.brand, url: SITE.url + '/', logo: { '@type': 'ImageObject', url: SITE.url + '/favicon.svg' } };
const personLd = () => AUTHOR ? { '@type': 'Person', name: AUTHOR.name, url: SITE.url + AUTHOR.url, jobTitle: AUTHOR.role,
  ...(Object.keys(AUTHOR.links).length ? { sameAs: Object.values(AUTHOR.links) } : {}) } : { '@type': 'Organization', name: SITE.author };
// Adds an Article node (headline, author, publisher, dates) to the page's existing @graph.
function withArticle(jsonld, p, d, canonical) {
  let g; try { g = JSON.parse(jsonld); } catch (e) { return jsonld; }
  const graph = g['@graph'] || [g];
  graph.unshift({ '@type': 'Article', '@id': canonical + '#article', headline: d.h1, description: d.description,
    mainEntityOfPage: canonical, image: `${SITE.url}/og-default.jpg`, datePublished: cfg.draft_date, dateModified: cfg.draft_date,
    author: personLd(), publisher: PUBLISHER });
  return JSON.stringify({ '@context': 'https://schema.org', '@graph': graph }, null, 1);
}
function authorBox() {
  if (!AUTHOR) return '';
  return `<aside class="author-box" aria-label="About the author"><span class="author-avatar" aria-hidden="true">${initials(AUTHOR.name)}</span>` +
    `<div><p class="author-k">Written and researched by</p><p class="author-name"><a href="${AUTHOR.url}">${esc(AUTHOR.name)}</a> · <span>${esc(AUTHOR.role)}</span></p>` +
    `<p class="author-bio">${esc(AUTHOR.short_bio)}</p></div></aside>`;
}
const hubs = pages.filter(p => !p.counted);
const hubByPath = Object.fromEntries(hubs.map(h => [h.public_path, h]));
const articles = pages.filter(p => p.counted);

// Short labels and emoji for the 15 cluster hubs, grouped by funnel stage (same grouping as /growth-stack/).
const HUB_META = {
  '/seo/': ['SEO', '🔎'], '/paid-media/': ['Paid Media', '📢'], '/affiliate-partnerships/': ['Affiliates & Partners', '🤝'],
  '/webinars-demand-gen/': ['Webinars & Demand Gen', '🎤'], '/email-outreach/': ['Email & Outreach', '✉️'],
  '/crm-lead-gen/': ['CRM & Lead Gen', '🎯'], '/website-experience/': ['Website & CRO', '🖥️'], '/ecommerce-growth/': ['Ecommerce', '🛒'],
  '/customer-retention/': ['Retention & CX', '💚'], '/product-led-growth/': ['Product-Led Growth', '🚀'],
  '/automation-analytics/': ['Automation & Analytics', '⚙️'], '/data-revops/': ['Data & RevOps', '📊'],
  '/ai-content/': ['AI Content', '✍️'], '/content-operations/': ['Content Ops', '🗂️'], '/agency-operations/': ['Agency Ops', '🏢'],
};
const GROUPS = [
  ['Acquisition', ['/seo/', '/paid-media/', '/affiliate-partnerships/', '/webinars-demand-gen/', '/email-outreach/']],
  ['Conversion', ['/crm-lead-gen/', '/website-experience/', '/ecommerce-growth/']],
  ['Retention', ['/customer-retention/', '/product-led-growth/']],
  ['Measurement', ['/automation-analytics/', '/data-revops/']],
  ['Operations', ['/ai-content/', '/content-operations/', '/agency-operations/']],
];
const KIND = { 'pillar-listicle': 'Buying guide', listicle: 'Best of', comparison: 'Comparison', alternatives: 'Alternatives',
  'pricing-guide': 'Pricing', guide: 'Guide', 'strategic-guide': 'Guide', 'category-hub': 'Category', 'topical-hub': 'Hub' };

// ---------- parse a source page ----------
function parse(p) {
  const src = fs.readFileSync(path.join(ROOT, p.physical_file_path), 'utf8');
  const get = re => (src.match(re) || [])[1] || '';
  const title = unesc(get(/<title>([\s\S]*?)<\/title>/)).replace(/\s*\|\s*[^|]+$/, '');
  const description = unesc(get(/<meta name="description" content="([^"]*)"/));
  const jsonld = get(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/).trim();
  let body = get(/<article\b[^>]*>([\s\S]*?)<\/article>/);
  const header = (body.match(/<header>([\s\S]*?)<\/header>/) || [])[1] || '';
  const h1 = strip((header.match(/<h1>([\s\S]*?)<\/h1>/) || [])[1] || p.final_h1);
  const paras = [...header.matchAll(/<p>([\s\S]*?)<\/p>/g)].map(m => m[1]);
  const deck = paras.filter(x => !/<time\b/.test(x))[1] || '';
  body = body.replace(/<header>[\s\S]*?<\/header>/, '');
  // Presentation hooks only; the text and links are untouched.
  body = body.replace(/<aside aria-label="Editorial disclosure">/, '<aside class="disclosure" aria-label="Editorial disclosure">')
    .replace(/<nav aria-labelledby="toc-heading">\s*<h2 id="toc-heading">([\s\S]*?)<\/h2>/,
      '<nav class="toc" aria-labelledby="toc-heading"><p class="toc-h" id="toc-heading">$1</p>');
  return { title, description, jsonld, h1, deck, body: body.trim() };
}

// ---------- shared chrome ----------
const LOGO_MARK = '<span class="logo-mark"><svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true">' +
  '<rect x="4" y="13" width="4" height="7" rx="1.2" fill="#fff"/><rect x="10" y="9" width="4" height="11" rx="1.2" fill="#fff"/>' +
  '<rect x="16" y="4" width="4" height="16" rx="1.2" fill="#fff"/></svg></span>';

function nav() {
  const pillar = cn => articles.find(a => a.cluster_num === cn && a.page_type === 'pillar-listicle');
  const items = GROUPS.map(([g, paths]) => {
    const cols = paths.map(hp => {
      const h = hubByPath[hp]; const [label, emo] = HUB_META[hp];
      const kids = articles.filter(a => a.cluster_num === h.cluster_num);
      const pick = [pillar(h.cluster_num), ...kids.filter(a => ['comparison', 'pricing-guide', 'alternatives'].includes(a.page_type))]
        .filter(Boolean).slice(0, 3);
      return `<div class="mega-col mega-text"><span class="mega-h">${emo} ${esc(label)}</span><a href="${hp}">${esc(label)} overview</a>` +
        pick.map(a => `<a href="${a.public_path}">${esc(a.final_h1.replace(/:.*$/, ''))}</a>`).join('') + '</div>';
    }).join('');
    const n = Math.min(paths.length, 3);
    return `<div class="nav-item has-mega"><button class="nav-link" aria-haspopup="true">${g} <span class="caret">▾</span></button>` +
      `<div class="mega mega-articles" style="grid-template-columns:repeat(${n},minmax(190px,1fr))">${cols}` +
      `<div class="mega-foot"><a href="/growth-stack/">See the whole growth stack &rarr;</a></div></div></div>`;
  }).join('');
  const mobile = GROUPS.map(([g, paths]) => `<span class="m-h">${g}</span>` + paths.map(hp =>
    `<a class="m-cat" href="${hp}"><span aria-hidden="true">${HUB_META[hp][1]}</span>${esc(HUB_META[hp][0])}</a>`).join('')).join('');
  return `<header class="site-header">
  <div class="nav-shell">
    <a href="/" class="logo" aria-label="${esc(SITE.brand)} home">${LOGO_MARK}<span class="logo-text">${esc(SITE.brand)}</span></a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="nav-menu" aria-label="Main">
      <div class="m-cats"><span class="m-h">Start here</span><a class="m-cat" href="/growth-stack/"><span aria-hidden="true">🧭</span>The Growth Stack</a>${mobile}</div>
      ${items}
      <a class="nav-link" href="/growth-stack/">Growth Stack</a>
    </nav>
  </div>
</header>`;
}
const NAV = nav();

const FOOTER = (() => {
  const col = (h, list) => `<div><h3>${h}</h3>${list.map(([href, t]) => `<a href="${href}">${esc(t)}</a>`).join('')}</div>`;
  const hubLinks = g => GROUPS.filter(([n]) => g.includes(n)).flatMap(([, ps]) => ps).map(hp => [hp, HUB_META[hp][0]]);
  const pillars = articles.filter(a => a.page_type === 'pillar-listicle').map(a => [a.public_path, a.final_h1.replace(/:.*$/, '')]);
  return `<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <div class="logo footer-logo">${LOGO_MARK}${esc(SITE.brand)}</div>
      <p>${esc(SITE.tagline)}. Use-case fit, clear pricing context and honest limitations. No paid placements.</p>
    </div>
    ${col('Acquire', hubLinks(['Acquisition']))}
    ${col('Convert &amp; retain', hubLinks(['Conversion', 'Retention']))}
    ${col('Measure &amp; operate', hubLinks(['Measurement', 'Operations']))}
    ${col('Start here', [['/growth-stack/', 'The Growth Stack'], ...pillars])}
  </div>
  <div class="container footer-bottom">
    <div class="copyright">© ${SITE.year} ${esc(SITE.brand)}. Independent editorial content. Vendors cannot pay for inclusion or placement. Product names belong to their owners.</div>
  </div>
</footer>`;
})();

const minJson = j => { try { return JSON.stringify(JSON.parse(j)); } catch (e) { return j; } };
const isLive = p => SITE.indexable || ['approved', 'published'].includes(p.status);
function head({ title, description, canonical, jsonld, ogImage, type = 'article', index = SITE.indexable }) {
  // Brand suffix only when the whole title still fits Google's ~60-character display.
  const full = title.includes(SITE.brand) || (title + ' | ' + SITE.brand).length > 60 ? title : `${title} | ${SITE.brand}`;
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(full)}</title>
<meta name="description" content="${esc(description)}">
<link rel="canonical" href="${canonical}">
<meta name="robots" content="${index ? 'index, follow, max-image-preview:large, max-snippet:-1' : 'noindex, follow'}">\n<meta property="og:type" content="${type}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(description)}">
<meta property="og:url" content="${canonical}">
<meta property="og:site_name" content="${esc(SITE.brand)}">
<meta property="og:image" content="${SITE.url}/og-default.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="${esc(SITE.brand)}: ${esc(SITE.tagline)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="${esc(title)}">
<meta name="twitter:description" content="${esc(description)}">
<meta name="twitter:image" content="${SITE.url}/og-default.jpg">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="#0f9f6e">
<!--INLINE_CSS-->
${jsonld ? `<script type="application/ld+json">${minJson(jsonld)}</script>\n` : ''}</head>
<body>
${NAV}
<main>
`;
}
const SITE_JS = fs.readFileSync(path.join(WEB, 'assets', 'site.js'), 'utf8').replace(/^\s*\/\/.*$/mg, '').replace(/\s+/g, ' ').trim();
const tail = `</main>\n${FOOTER}\n<script>${SITE_JS}</script>\n</body>\n</html>\n`;

// ---------- SVG covers (featured cards + share images) ----------
function wrap(text, max) {
  const out = []; let line = '';
  for (const w of text.split(/\s+/)) {
    if ((line + ' ' + w).trim().length > max) { out.push(line.trim()); line = w; } else line += ' ' + w;
  }
  if (line.trim()) out.push(line.trim());
  return out.slice(0, 3);
}
function cover(kicker, title, w = 1200, h = 630) {
  const lines = wrap(title, 26);
  const fs1 = 64, y0 = h / 2 - ((lines.length - 1) * fs1 * 1.12) / 2 + 10;
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f9f6e"/><stop offset=".55" stop-color="#0ea5b7"/><stop offset="1" stop-color="#3b82f6"/></linearGradient></defs>
<rect width="${w}" height="${h}" fill="url(#g)"/>
<circle cx="${w - 150}" cy="${h / 2}" r="120" fill="#fff" fill-opacity=".14"/>
<g transform="translate(${w - 210},${h / 2 - 50})" fill="#fff" fill-opacity=".9"><rect x="0" y="50" width="30" height="50" rx="6"/><rect x="45" y="25" width="30" height="75" rx="6"/><rect x="90" y="0" width="30" height="100" rx="6"/></g>
<text x="70" y="96" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="26" font-weight="800" letter-spacing="3" fill="#fff" fill-opacity=".85">${esc(kicker.toUpperCase())}</text>
${lines.map((l, i) => `<text x="70" y="${y0 + i * fs1 * 1.12}" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="${fs1}" font-weight="900" fill="#fff">${esc(l)}</text>`).join('\n')}
<text x="70" y="${h - 60}" font-family="Inter,Segoe UI,Arial,sans-serif" font-size="28" font-weight="800" fill="#fff">${esc(SITE.brand)}</text>
</svg>`;
}

function thumb() {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f9f6e"/><stop offset=".55" stop-color="#0ea5b7"/><stop offset="1" stop-color="#3b82f6"/></linearGradient></defs>
<rect width="400" height="400" fill="url(#g)"/><circle cx="200" cy="200" r="96" fill="#fff" fill-opacity=".15"/>
<g transform="translate(140,145)" fill="#fff"><rect x="0" y="55" width="32" height="55" rx="7"/><rect x="44" y="28" width="32" height="82" rx="7"/><rect x="88" y="0" width="32" height="110" rx="7"/></g></svg>`;
}

// ---------- page renderers ----------
const slug = p => p.public_path.replace(/\//g, '') || 'home';
const blogCard = a => `<a class="blog-card" href="${a.public_path}"><span class="blog-kicker">${KIND[a.page_type]}</span>` +
  `<h3>${esc(a.final_h1)}</h3><p>${esc(a._desc.length > 150 ? a._desc.slice(0, 147).replace(/\s+\S*$/, '') + '…' : a._desc)}</p>` +
  `<span class="blog-read">Read ${KIND[a.page_type] === 'Comparison' ? 'comparison' : 'guide'} &rarr;</span></a>`;

function renderPage(p, d) {
  const hub = hubByPath[p.parent_hub];
  const canonical = SITE.url + p.public_path;
  const crumbs = [`<a href="/">Home</a>`];
  if (hub && hub.public_path !== '/growth-stack/') crumbs.push(`<a href="/growth-stack/">Growth Stack</a>`);
  if (hub) crumbs.push(`<a href="${hub.public_path}">${esc(HUB_META[hub.public_path] ? HUB_META[hub.public_path][0] : 'Growth Stack')}</a>`);
  crumbs.push(`<span>${esc(d.h1.length > 60 ? d.h1.slice(0, 57) + '…' : d.h1)}</span>`);
  const pill = hub ? `<a class="cluster-pill" href="${hub.public_path}">${esc(HUB_META[hub.public_path] ? HUB_META[hub.public_path][0] : 'Growth Stack')}</a>` : '';
  let more = '';
  if (p.counted) {
    // Rotate through the cluster (next 3 articles after this one, wrapping) so every article
    // receives exactly 3 same-silo inbound links from these blocks.
    const ring = articles.filter(a => a.cluster_num === p.cluster_num);
    const at = ring.indexOf(p);
    const picks = [1, 2, 3].map(k => ring[(at + k) % ring.length]);
    more = `<section class="section keep-reading" aria-labelledby="keep-reading"><div class="sec-head"><h2 id="keep-reading">Keep reading</h2>` +
      `<a class="sec-more" href="${p.parent_hub}">All ${esc(HUB_META[p.parent_hub][0])} guides &rarr;</a></div>` +
      `<div class="blog-grid">${picks.map(blogCard).join('')}</div></section>`;
  }
  return head({ title: d.title, description: d.description, canonical, jsonld: p.counted ? withArticle(d.jsonld, p, d, canonical) : d.jsonld, ogImage: `/og/${slug(p)}.svg`, index: isLive(p) }) +
`<div class="page-hero"><div class="container">
  <nav class="crumbs" aria-label="Breadcrumb">${crumbs.join('<span class="crumb-sep">›</span>')}</nav>
  <h1>${esc(d.h1)}</h1>
  ${d.deck ? `<p class="sub">${d.deck}</p>` : ''}
  <p class="page-meta">${pill}<span>${KIND[p.page_type]}</span><span>By ${AUTHOR ? `<a href="${AUTHOR.url}">${esc(AUTHOR.name)}</a>` : esc(SITE.author)}</span><span>Updated <time datetime="${cfg.draft_date}">${new Date(cfg.draft_date + 'T00:00:00Z').toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric', timeZone: 'UTC' })}</time></span>${isLive(p) ? '' : '<span class="draft-pill">Draft</span>'}</p>
</div></div>
<div class="container content article" data-article-id="${p.id}">
${d.body}
${p.counted ? authorBox() : ''}
${more}
</div>
` + tail;
}

function renderHome() {
  const pillars = articles.filter(a => a.page_type === 'pillar-listicle');
  const [lead, ...rest] = pillars;
  const feat = (a, size) => `<a class="feat-card ${size}" href="${a.public_path}"><span class="feat-media"><img src="/og/${size === 'lg' ? '' : 'thumb-'}${slug(a)}.svg" alt="" width="${size === 'lg' ? 760 : 300}" height="${size === 'lg' ? 428 : 169}" ${size === 'lg' ? 'fetchpriority="high"' : 'loading="lazy"'} decoding="async"></span>` +
    `<span class="feat-body"><span class="feat-pill">${esc(HUB_META[a.parent_hub][0])}</span><h3>${esc(a.final_h1)}</h3>` +
    (size === 'lg' ? `<span class="feat-ex">${esc(a._desc)}</span>` : '') + `<span class="feat-meta">Buying guide</span></span></a>`;
  const tiles = GROUPS.flatMap(([, ps]) => ps).map(hp => {
    const h = hubByPath[hp]; const n = articles.filter(a => a.cluster_num === h.cluster_num).length;
    return `<a class="cat-tile" href="${hp}"><span class="cat-emoji" aria-hidden="true">${HUB_META[hp][1]}</span><span class="cat-name">${esc(HUB_META[hp][0])}</span><span class="cat-n">${n} guides</span></a>`;
  }).join('') + `<a class="cat-tile" href="/growth-stack/"><span class="cat-emoji" aria-hidden="true">🧭</span><span class="cat-name">The Growth Stack</span><span class="cat-n">How all ${hubs.length - 1} fit together</span></a>`;
  const comps = articles.filter(a => a.page_type === 'comparison').slice(0, 6);
  const prices = articles.filter(a => a.page_type === 'pricing-guide');
  const alts = articles.filter(a => a.page_type === 'alternatives').slice(0, 6);
  return head({ title: `${SITE.brand}: ${SITE.tagline}`, description: SITE.desc, canonical: SITE.url + '/', type: 'website',
    jsonld: JSON.stringify({ '@context': 'https://schema.org', '@type': 'WebSite', name: SITE.brand, url: SITE.url + '/' }, null, 1) }) +
`<section class="home-lead"><div class="container">
  <span class="hero-eyebrow"><b>NEW</b> ${articles.length} guides across ${hubs.length - 1} categories</span>
  <h1>Choose growth software <span class="grad">with clear eyes</span></h1>
  <p class="sub">Buying guides, head-to-head comparisons and pricing breakdowns for the tools behind SEO, content, outreach, CRM and measurement, built from official pricing and documentation.</p>
  <div class="hero-ctas">
    <a class="btn btn-primary" href="/growth-stack/">Explore the growth stack →</a>
    <a class="btn btn-ghost" href="${lead.public_path}">Read the SEO buying guide</a>
  </div>
  <p class="trust-row center"><span>✔ Independent editorial</span><span>✔ Prices linked to official pages</span><span>✔ No paid placements</span></p>
</div></section>
<div class="container content">
  <section class="section">
    <div class="sec-head"><h2>Featured buying guides</h2><a class="sec-more" href="/growth-stack/">All categories &rarr;</a></div>
    <div class="featured-grid">${feat(lead, 'lg')}<div class="feat-col">${rest.slice(0, 2).map(a => feat(a, 'sm')).join('')}</div></div>
  </section>
  <section class="section">
    <div class="sec-head"><h2>Browse by category</h2><a class="sec-more" href="/growth-stack/">How the stack fits together &rarr;</a></div>
    <div class="cat-tiles">${tiles}</div>
  </section>
  <section class="section">
    <div class="sec-head"><h2>Head-to-head comparisons</h2></div>
    <div class="blog-grid">${comps.map(blogCard).join('')}</div>
  </section>
  <section class="section">
    <div class="sec-head"><h2>What it really costs</h2></div>
    <div class="blog-grid">${prices.map(blogCard).join('')}</div>
  </section>
  <section class="section">
    <div class="sec-head"><h2>Switching? Start with the alternatives</h2></div>
    <div class="blog-grid">${alts.map(blogCard).join('')}</div>
  </section>
</div>
` + tail;
}

function renderAuthor() {
  const canonical = SITE.url + AUTHOR.url;
  const covers = GROUPS.flatMap(([, ps]) => ps).map(hp => `<a class="cat-tile" href="${hp}"><span class="cat-emoji" aria-hidden="true">${HUB_META[hp][1]}</span><span class="cat-name">${esc(HUB_META[hp][0])}</span></a>`).join('');
  const recent = articles.filter(a => ['pillar-listicle', 'comparison', 'pricing-guide'].includes(a.page_type)).slice(0, 6);
  const ld = { '@context': 'https://schema.org', '@graph': [
    { '@type': 'ProfilePage', '@id': canonical, url: canonical, name: `${AUTHOR.name}, ${AUTHOR.role}`, mainEntity: personLd() },
    { '@type': 'BreadcrumbList', itemListElement: [{ '@type': 'ListItem', position: 1, name: 'Home', item: SITE.url + '/' }, { '@type': 'ListItem', position: 2, name: AUTHOR.name, item: canonical }] }] };
  const creds = AUTHOR.credentials.length ? `<h2>Background</h2><ul>${AUTHOR.credentials.map(c => `<li>${esc(c)}</li>`).join('')}</ul>` : '';
  const links = Object.keys(AUTHOR.links).length ? `<p class="trust-row">${Object.entries(AUTHOR.links).map(([k, v]) => `<a href="${esc(v)}" rel="me noopener" target="_blank">${esc(k)}</a>`).join('')}</p>` : '';
  return head({ title: `${AUTHOR.name}, ${AUTHOR.role}`, description: AUTHOR.short_bio.slice(0, 155).replace(/\s+\S*$/, '') + '…', canonical, jsonld: JSON.stringify(ld, null, 1), type: 'profile' }) +
`<div class="page-hero"><div class="container">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span class="crumb-sep">›</span><span>${esc(AUTHOR.name)}</span></nav>
  <div class="author-head"><span class="author-avatar lg" aria-hidden="true">${initials(AUTHOR.name)}</span><div><h1>${esc(AUTHOR.name)}</h1><p class="sub">${esc(AUTHOR.role)} · ${esc(SITE.brand)}</p>${links}</div></div>
</div></div>
<div class="container content article">
${AUTHOR.long_bio.map(x => `<p>${esc(x)}</p>`).join('\n')}
${creds}
<h2>What ${esc(AUTHOR.name.split(" ")[0])} covers</h2>
<div class="cat-tiles">${covers}</div>
<section class="section keep-reading"><div class="sec-head"><h2>Start with these guides</h2><a class="sec-more" href="/growth-stack/">All categories &rarr;</a></div>
<div class="blog-grid">${recent.map(blogCard).join('')}</div></section>
</div>
` + tail;
}

// ---------- CSS purge (zero-dependency) ----------
// Keeps only rules whose selectors can match the generated HTML, then the result is inlined
// into every page as <style>, so there is no render-blocking stylesheet request.
const KEEP_CLASSES = new Set(['open']); // toggled by the menu script
function splitTop(css) { // -> [{prelude, body}] at depth 0
  const out = []; let i = 0;
  while (i < css.length) {
    const ob = css.indexOf('{', i); if (ob < 0) break;
    let d = 1, j = ob + 1;
    while (j < css.length && d) { if (css[j] === '{') d++; else if (css[j] === '}') d--; j++; }
    out.push({ prelude: css.slice(i, ob).trim(), body: css.slice(ob + 1, j - 1) });
    i = j;
  }
  return out;
}
function purgeCss(css, used) {
  css = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const selOk = sel => {
    const t = sel.replace(/::?[a-z-]+(\([^)]*\))?/gi, ' ').replace(/\[[^\]]*\]/g, ' ');
    for (const c of t.match(/\.[a-z0-9_-]+/gi) || []) if (!used.cls.has(c.slice(1)) && !KEEP_CLASSES.has(c.slice(1))) return false;
    for (const id of t.match(/#[a-z][a-z0-9_-]*/gi) || []) if (!used.ids.has(id.slice(1))) return false;
    for (const tag of t.replace(/[.#][a-z0-9_-]+/gi, ' ').match(/\b[a-z][a-z0-9]*\b/gi) || []) if (!used.tags.has(tag.toLowerCase())) return false;
    return true;
  };
  const walk = c => splitTop(c).map(({ prelude, body }) => {
    if (/^@(media|supports)/i.test(prelude)) { const inner = walk(body); return inner ? `${prelude}{${inner}}` : ''; }
    if (/^@/.test(prelude)) return `${prelude}{${body}}`;
    const sels = prelude.split(',').map(x => x.trim()).filter(x => x === ':root' || x === '*' || selOk(x));
    return sels.length ? `${sels.join(',')}{${body.trim()}}` : '';
  }).join('');
  return walk(css).replace(/\s+/g, ' ').replace(/\s*([{}:;,>])\s*/g, '$1').replace(/;}/g, '}');
}
function usage(htmls) {
  const used = { cls: new Set(), ids: new Set(), tags: new Set(['html', 'body']) };
  for (const h of htmls) {
    for (const m of h.matchAll(/class="([^"]+)"/g)) m[1].split(/\s+/).forEach(c => used.cls.add(c));
    for (const m of h.matchAll(/\sid="([^"]+)"/g)) used.ids.add(m[1]);
    for (const m of h.matchAll(/<([a-z][a-z0-9]*)\b/g)) used.tags.add(m[1]);
  }
  return used;
}
const minHtml = h => h.replace(/\n[ \t]+/g, '\n').replace(/\n{2,}/g, '\n').replace(/<!--(?!INLINE_CSS)[\s\S]*?-->/g, '');

// ---------- build ----------
const HTML_OUT = new Map();
function write(rel, content) {
  if (rel.endsWith('.html')) { HTML_OUT.set(rel, content); return; }
  const f = path.join(DIST, rel);
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, content);
}

function build() {
  fs.rmSync(DIST, { recursive: true, force: true });
  fs.mkdirSync(DIST, { recursive: true });
  if (fs.existsSync(path.join(WEB, 'assets', 'og-default.jpg'))) fs.copyFileSync(path.join(WEB, 'assets', 'og-default.jpg'), path.join(DIST, 'og-default.jpg'));
  const parsed = {};
  for (const p of pages) { parsed[p.id] = parse(p); p._desc = parsed[p.id].description; }
  for (const p of pages) {
    write(path.join(p.public_path, 'index.html'), renderPage(p, parsed[p.id]));
    write(`og/${slug(p)}.svg`, cover(KIND[p.page_type], p.final_h1.replace(/:.*$/, '')));
    if (p.page_type === 'pillar-listicle') write(`og/thumb-${slug(p)}.svg`, thumb());
  }
  write('index.html', renderHome());
  if (AUTHOR) write(AUTHOR.url.slice(1) + 'index.html', renderAuthor());
  write('og/default.svg', cover('Growth software', SITE.tagline));
  write('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0f9f6e"/><stop offset="1" stop-color="#0ea5b7"/></linearGradient></defs><rect width="32" height="32" rx="8" fill="url(#g)"/><rect x="7" y="17" width="5" height="9" rx="1.5" fill="#fff"/><rect x="14" y="12" width="5" height="14" rx="1.5" fill="#fff"/><rect x="21" y="6" width="5" height="20" rx="1.5" fill="#fff"/></svg>');
  write('404.html', head({ title: 'Page not found', description: 'This page does not exist.', canonical: SITE.url + '/404.html', type: 'website' }) +
    `<section class="home-lead"><div class="container"><h1>Page not found</h1><p class="sub">That page doesn't exist. Try the growth stack overview instead.</p><div class="hero-ctas"><a class="btn btn-primary" href="/growth-stack/">Go to the growth stack →</a></div></div></section>\n` + tail);
  const livePages = pages.filter(isLive);
  const anyLive = livePages.length > 0;
  const urls = anyLive ? ['/', ...(AUTHOR ? [AUTHOR.url] : []), ...livePages.map(p => p.public_path)] : [];
  write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    urls.map(u => `  <url><loc>${SITE.url}${u}</loc><lastmod>${cfg.draft_date}</lastmod></url>`).join('\n') + '\n</urlset>\n');
  write('robots.txt', anyLive ? `User-agent: *\nAllow: /\n\nSitemap: ${SITE.url}/sitemap.xml\n`
    : '# No approved pages yet: crawling disabled. Approve pages (scripts/apply_experience.py) or set "indexable": true.\nUser-agent: *\nDisallow: /\n');
  write('llms.txt', `# ${SITE.brand}\n\n> ${SITE.desc}\n\n## Categories\n` +
    hubs.map(h => `- [${h.title}](${SITE.url}${h.public_path})`).join('\n') + '\n\n## Buying guides\n' +
    articles.filter(a => a.page_type === 'pillar-listicle').map(a => `- [${a.final_h1}](${SITE.url}${a.public_path})`).join('\n') + '\n');
  const css = purgeCss(fs.readFileSync(path.join(WEB, 'assets', 'style.css'), 'utf8'), usage(HTML_OUT.values()));
  for (const [rel, h] of HTML_OUT) {
    const f = path.join(DIST, rel);
    fs.mkdirSync(path.dirname(f), { recursive: true });
    fs.writeFileSync(f, minHtml(h).replace('<!--INLINE_CSS-->', `<style>${css}</style>`));
  }
  write('_headers', `/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n  Permissions-Policy: interest-cohort=()\n  Strict-Transport-Security: max-age=31536000; includeSubDomains\n/og/*\n  Cache-Control: public, max-age=604800\n/og-default.jpg\n  Cache-Control: public, max-age=604800\n/favicon.svg\n  Cache-Control: public, max-age=2592000\n`);
  console.log(`CSS: ${(css.length / 1024).toFixed(1)} KB inlined (from ${(fs.statSync(path.join(WEB, 'assets', 'style.css')).size / 1024).toFixed(1)} KB)`);
  console.log(`Built ${pages.length + 1} pages -> web/dist/ (${articles.length} articles, ${hubs.length} hubs, home)` +
    ` [indexable pages: ${pages.filter(isLive).length}]`);
}

build();

if (process.argv[2] === 'serve') {
  const http = require('http');
  const port = Number(process.argv[3]) || 8788;
  const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.xml': 'application/xml', '.txt': 'text/plain' };
  http.createServer((req, res) => {
    let u = decodeURIComponent(req.url.split('?')[0]);
    let f = path.join(DIST, u);
    if (!f.startsWith(DIST)) { res.writeHead(403); return res.end(); }
    if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
    if (!fs.existsSync(f)) { res.writeHead(404, { 'Content-Type': types['.html'] }); return res.end(fs.readFileSync(path.join(DIST, '404.html'))); }
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream' });
    res.end(fs.readFileSync(f));
  }).listen(port, () => console.log(`Serving web/dist on http://localhost:${port}`));
}
