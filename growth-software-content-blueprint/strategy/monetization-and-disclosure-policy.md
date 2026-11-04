# Monetization and Disclosure Policy

Status in this draft corpus: **no sponsored content, no affiliate links, no vendor relationships.** Every vendor link points to the official site. This policy describes how monetization is added later without compromising editorial trust. It is drawn from DOCX §8.

## Revenue streams and timing

| Stream | Timing | Safeguards |
|---|---|---|
| Affiliate referrals | Launch, once programs actually accept the site | Unique redirect keys, visible disclosure, click tracking only (never assumed sales) |
| Sponsored listicle modules | Launch, carefully | Labelled at the point of display. Editorial verdict and order stay independent. |
| Sponsored category visibility | After baseline UX | Dated, labelled card or banner that is visually distinct from editorial results |
| Claimed / premium profiles | Phase 2 | Defined fields only. Payment never buys a score, rank or removal of criticism. |
| Vendor subscriptions | Phase 2/3 | Only after buyer activity can be demonstrated. Manual invoicing first. |

The DOCX suggests illustrative test pricing for later experiments: free basic listing, $49/month enhanced profile, $99/month featured profile, and $100–$200 per sponsored comparison/listicle campaign. These are hypotheses, not forecasts. Never promise impressions, rankings, traffic or leads.

## Non-negotiable rules

1. Paid promotion is labelled **"Sponsored"** or **"Advertisement"** at the point of display.
2. A vendor can't buy a better editorial score, an organic rank, a "best overall" verdict, or the removal of criticism.
3. Affiliate relationships never determine ranking or inclusion.
4. Every paid package records its slot, duration, URL, disclosure, reporting and renewal terms.
5. No fake reviews, ratings, badges, unverified "verified" labels or fabricated performance statistics.

## Affiliate links (when confirmed)

- Never invent affiliate URLs, programs, commission rates or coupon codes. In the research log, affiliate status is `Not confirmed` for every page.
- When a program is confirmed, record it in an affiliate inventory (product, program name, terms URL, date confirmed). Replace the official link with the tracked `/go/{partner-key}/` redirect described in the DOCX, and use:
  `rel="sponsored nofollow noopener noreferrer"`
- Add this disclosure near the top of any page with affiliate links, replacing the current "no affiliate links" sentence:

  > **Affiliate disclosure:** Some links on this page are affiliate links. If you buy through them, BRAND_NAME may earn a commission at no extra cost to you. Commissions never affect which products we include, the order they appear in, or what we say about them. [How we evaluate software]

- Keep link labels honest ("Visit Semrush", "See Semrush pricing"). Never disguise a commercial link as a citation.
- Never publish a placeholder such as `AFFILIATE_URL_PENDING` as a working link. The validator rejects it.

## Sponsored placements (when contracted)

Only add a sponsored module when there is a signed agreement. Recommended markup, extractable into WordPress:

```html
<aside aria-label="Sponsored placement">
  <p><strong>Sponsored</strong>: {Vendor} paid for this placement. It is shown separately from our editorial picks and does not affect their order or our assessments.</p>
  ...
</aside>
```

Rules:
- Place it outside the editorial product list, never inside it.
- Show a start and end date in the admin. It stops rendering automatically after the end date.
- Report sponsored impressions and clicks separately from organic performance.

## Vendor subscriptions (later)

Not built here. Product profiles, once built, should use a consistent field structure (see `wordpress-migration-notes.md`) so that claimed profiles and vendor-supplied updates can be added with editorial review before publication. Vendors never get direct publishing rights.

## Standard on-page editorial disclosure (current draft)

Every page currently carries:

> Independent editorial assessment based on official product information. No vendor paid for inclusion or placement, and this page contains no affiliate links.

Update this sentence page by page when monetization is added. Don't remove it wholesale.
