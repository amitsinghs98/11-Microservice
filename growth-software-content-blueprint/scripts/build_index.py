#!/usr/bin/env python3
"""Generate derived files from the manifest and the per-article research fragments.

Outputs:
  site/index.html                    plain, unstyled content directory (QA/navigation only)
  strategy/topical-cluster-map.md    cluster -> hub -> pillar -> children map, plus cannibalization notes
  strategy/research-source-log.csv   merged from strategy/research/*.csv (fragments are kept as the editable source)
Usage: python3 scripts/build_index.py
"""
import csv, glob, html, io, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TYPE_LABEL = {"pillar-listicle": "Pillar buying guide", "listicle": "Buying guides", "comparison": "Comparisons",
              "alternatives": "Alternatives", "pricing-guide": "Pricing guides", "guide": "How-to guides",
              "strategic-guide": "How-to guides"}
ORDER = ["Pillar buying guide", "Buying guides", "Comparisons", "Alternatives", "Pricing guides", "How-to guides"]
CANNIBAL = [
    ("A053", "A095", "HubSpot vs ActiveCampaign appears twice. Differentiated: A053 = email-marketing buyer (Marketing Hub, email/automation, contact-tier economics); A095 = platform/RevOps decision (Smart CRM + Sales Hub + Marketing Hub vs ActiveCampaign, seats and contacts). Consider merging into one URL with a 301 if SERPs show a single intent."),
    ("A041", "A056", "Small-business email software vs free email software. A056 must stay focused on free-plan limits and upgrade triggers."),
    ("A048", "A081", "Lifecycle email automation vs general marketing automation for small teams. A048 = event/trigger-driven journeys; A081 = all-round automation for lean teams."),
    ("A081", "A096", "Marketing automation pillar vs free marketing automation tools. A096 limited to free tiers and their caps."),
    ("A003", "A019", "Rank tracking software (agency scale) vs choosing rank tracking for a local SEO agency (local-pack/grid concepts and buying process)."),
    ("A007", "A009", "AI SEO tools vs content optimization tools. A007 = workflow-wide AI assistance including AI visibility; A009 = briefs/scoring/refresh."),
    ("A009", "A023", "Content optimization tools vs AI content-brief tools. A023 limited to brief generation inside the AI content cluster."),
    ("A021", "A024", "AI writing tools (pillar) vs AI blog writing tools (long-form only)."),
    ("A022", "A025", "AI copywriting (ads/landing/product copy) vs AI email copywriting (sequences/subject lines)."),
    ("A043", "A044", "Cold email software (agency sending infrastructure) vs sales engagement platforms (SDR team multichannel cadences)."),
    ("A064", "A068", "B2B lead generation software (company-wide) vs prospecting tools for agencies (agency new-business)."),
    ("A065", "A066", "Contact databases (find people) vs enrichment software (append data to existing records)."),
    ("A067", "A080", "Lead scoring software (products) vs lead scoring vs enrichment (concept explainer)."),
    ("A062", "A078", "Best CRM for agencies (product list) vs how to choose a CRM for an agency (decision process)."),
    ("A082", "A083", "Workflow automation for agencies (client-facing ops) vs no-code automation platforms (marketing ops generally)."),
    ("A084", "A100", "Marketing analytics software vs attribution guide. A100 focuses on attribution models and their limits."),
    ("A099", "H00", "Full-funnel growth stack guide vs /growth-stack/ hub. A099 = implementation guide; H00 = living index/navigation overview (per DOCX)."),
    ("A178", "A288", "Customer journey analytics twice. A178 = lifecycle/CRM teams joining marketing, support and billing data; A288 = SaaS product teams stitching anonymous and authenticated product journeys. Pages cross-link; watch SERPs and merge with a 301 if Google treats them as one intent."),
    ("A176", "A254", "Customer community platforms (first purchase) vs community alternatives (switching from an incumbent). A254 keeps to switch triggers and migration."),
    ("A021", "A035", "AI writing tools pillar vs free AI writing tools. A035 limited to free tiers and their caps."),
    ("A064", "A241", "B2B lead generation software vs webinar platforms for B2B lead generation. A241 stays on webinar platforms; A064 links to it as one channel."),
]


def main():
    pages = json.load(open(os.path.join(ROOT, "strategy", "url-manifest.json")))["pages"]
    cfg = json.load(open(os.path.join(ROOT, "site.config.json")))
    brand, domain = html.escape(cfg["brand_name"]), cfg["domain"].rstrip("/")
    by_id = {p["id"]: p for p in pages}
    hubs = [p for p in pages if not p["counted"]]
    # ---------- site/index.html ----------
    out = io.StringIO()
    w = out.write
    w('<!doctype html>\n<html lang="en">\n<head>\n  <meta charset="utf-8">\n'
      '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
      f'  <title>Content library index | {brand}</title>\n'
      '  <meta name="description" content="Plain directory of every growth-software buying guide, comparison, alternatives page, pricing guide and how-to guide in the draft content library.">\n'
      '  <meta name="robots" content="noindex">\n'
      f'  <link rel="canonical" href="{domain}/">\n</head>\n<body>\n  <main id="main-content">\n'
      '    <h1>Content library index</h1>\n'
      '    <p>An unstyled directory of the draft content library for internal navigation and QA. It is not a homepage. '
      f'It lists {sum(p["counted"] for p in pages)} articles in five clusters, plus {len(hubs)} hub pages.</p>\n'
      '    <p>Start with the umbrella hub: <a href="/growth-stack/">' + html.escape(by_id["H00"]["title"]) + '</a>.</p>\n')
    for h in hubs[1:]:
        cn = h["cluster_num"]
        w(f'    <section id="cluster-{cn}">\n      <h2>Cluster {cn}: {html.escape(h["cluster"])}</h2>\n'
          f'      <p>Category hub: <a href="{h["public_path"]}">{html.escape(h["title"])}</a></p>\n')
        kids = [p for p in pages if p["counted"] and p["cluster_num"] == cn]
        for label in ORDER:
            group = [p for p in kids if TYPE_LABEL[p["page_type"]] == label]
            if not group:
                continue
            w(f'      <h3>{label}</h3>\n      <ul>\n')
            for p in group:
                w(f'        <li>{p["id"]}: <a href="{p["public_path"]}">{html.escape(p["final_h1"])}</a></li>\n')
            w('      </ul>\n')
        w('    </section>\n')
    w('  </main>\n</body>\n</html>\n')
    open(os.path.join(ROOT, "site", "index.html"), "w", encoding="utf-8").write(out.getvalue())

    # ---------- topical-cluster-map.md ----------
    m = io.StringIO()
    m.write("# Topical Cluster Map\n\nGenerated by `scripts/build_index.py` from `strategy/url-manifest.json`; "
            "cannibalization notes are maintained in that script.\n\n"
            "**Umbrella topic:** Growth software for agencies and lean marketing teams.\n\n"
            "```text\n/growth-stack/ (H00, umbrella hub)\n")
    for h in hubs[1:]:
        pil = next((p["public_path"] for p in pages if p["counted"] and p["cluster_num"] == h["cluster_num"]
                    and p["page_type"] == "pillar-listicle"), None)
        m.write(f"├── {h['public_path']} ({h['id']})" + (f" → pillar {pil}" if pil else "") + "\n")
    m.write("```\n\nLink flow per cluster: category hub ⇄ pillar ⇄ supporting pages; supporting pages ⇄ siblings; "
            "selected cross-cluster links where a reader's next question lives in another cluster. "
            "Article 99 and the umbrella hub link every pillar; the umbrella hub links all 15 cluster hubs. Clusters 6-15 (A101-A300) have no designated pillar in the source map; their hub is the parent.\n\n")
    for h in hubs[1:]:
        cn = h["cluster_num"]
        m.write(f"## Cluster {cn}: {h['cluster']}\n\nHub: `{h['public_path']}` ({h['id']})\n\n"
                "| ID | Type | Path | Title | Primary keyword |\n|---|---|---|---|---|\n")
        for p in pages:
            if p["counted"] and p["cluster_num"] == cn:
                m.write(f"| {p['id']} | {p['page_type']} | `{p['public_path']}` | {p['final_h1']} | {p['primary_keyword']} |\n")
        m.write("\n")
    m.write("## Cannibalization risks and differentiation\n\n| Pages | Risk and resolution |\n|---|---|\n")
    for a, b, note in CANNIBAL:
        m.write(f"| {a} `{by_id[a]['public_path']}` / {b} `{by_id[b]['public_path']}` | {note} |\n")
    open(os.path.join(ROOT, "strategy", "topical-cluster-map.md"), "w", encoding="utf-8").write(m.getvalue())

    # ---------- research-source-log.csv ----------
    header = ["article_id", "product_or_claim", "source_url", "source_type", "date_checked", "claim_supported",
              "verification_status", "notes"]
    rows = []
    for fp in sorted(glob.glob(os.path.join(ROOT, "strategy", "research", "*.csv"))):
        for r in csv.DictReader(open(fp, encoding="utf-8")):
            rows.append([(r.get(k) or "").strip() for k in header])
    with open(os.path.join(ROOT, "strategy", "research-source-log.csv"), "w", newline="", encoding="utf-8") as f:
        cw = csv.writer(f)
        cw.writerow(header)
        cw.writerows(rows)
    from collections import Counter
    print("index + cluster map written; research rows:", len(rows), dict(Counter(r[6] for r in rows)))


if __name__ == "__main__":
    main()
