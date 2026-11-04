#!/usr/bin/env python3
"""Build the canonical URL manifest from the extracted source map.

Inputs : .tmp/source-article-map.json (from scripts/extract_source_map.py)  -> A001-A100
         inputs/additional-200-articles.csv (expansion map)               -> A101-A300
Outputs: strategy/url-manifest.json   (machine-readable, used by all scripts)
         strategy/master-300-article-map.csv

Path rules (documented in strategy/url-architecture.md):
  comparison  -> /compare/{source-slug}/
  alternatives-> /alternatives/{product}/        (source pattern /alternatives/{product}/)
  pricing     -> /pricing/{topic}/               (source pattern /pricing/{product-or-category}/)
  how-to/info -> /guides/{source-slug}/
  best-of     -> /best/{source-slug minus leading "best-"}/
Status values are preserved from an existing manifest so re-running is safe.
"""
import csv, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLUSTERS = {
    1: ("SEO and organic search growth", "/categories/seo/", "H01"),
    2: ("AI content and creative marketing software", "/categories/ai-content/", "H02"),
    3: ("Email marketing and outbound growth", "/categories/email-outreach/", "H03"),
    4: ("CRM, lead generation, and sales intelligence", "/categories/crm-lead-gen/", "H04"),
    5: ("Marketing automation, analytics, CRO, and distribution", "/categories/automation-analytics/", "H05"),
    6: ("Content operations and editorial management", "/categories/content-operations/", "H06"),
    7: ("Paid media and advertising operations", "/categories/paid-media/", "H07"),
    8: ("Ecommerce growth and merchandising software", "/categories/ecommerce-growth/", "H08"),
    9: ("Customer experience, retention and customer success", "/categories/customer-retention/", "H09"),
    10: ("Affiliate, influencer and partnership growth", "/categories/affiliate-partnerships/", "H10"),
    11: ("Website experience and conversion infrastructure", "/categories/website-experience/", "H11"),
    12: ("Data, research and revenue operations", "/categories/data-revops/", "H12"),
    13: ("Webinars, events, communities and demand generation", "/categories/webinars-demand-gen/", "H13"),
    14: ("Agency business operations and client delivery", "/categories/agency-operations/", "H14"),
    15: ("Product-led growth, product analytics and experimentation", "/categories/product-led-growth/", "H15"),
}
NEW_SLUG_TO_CLUSTER = {v[1].split("/")[2]: k for k, v in CLUSTERS.items() if k >= 6}
NEW_TYPES = {"best": "listicle", "guide": "guide", "comparison": "comparison", "alternatives": "alternatives",
             "pricing": "pricing-guide"}
NEW_WORDS = {"listicle": "1400-2000", "comparison": "1400-2100", "alternatives": "1400-2100",
             "pricing-guide": "1200-1800", "guide": "1200-1800"}
PILLARS = {1: "A001", 2: "A021", 3: "A041", 4: "A061", 5: "A081"}
HUBS = [
    {"id": "H00", "cluster_num": 0, "page_type": "topical-hub",
     "title": "The Growth Stack: How to Choose the Software Behind Acquisition, Content, Sales, and Measurement",
     "public_path": "/growth-stack/", "primary_keyword": "growth stack software"},
    {"id": "H01", "cluster_num": 1, "page_type": "category-hub", "title": "SEO Software: Tools for Planning, Executing, and Measuring Organic Growth",
     "public_path": "/categories/seo/", "primary_keyword": "seo software"},
    {"id": "H02", "cluster_num": 2, "page_type": "category-hub", "title": "AI Content Software: Writing, Creative, and Content Operations Tools for Marketing Teams",
     "public_path": "/categories/ai-content/", "primary_keyword": "ai content software"},
    {"id": "H03", "cluster_num": 3, "page_type": "category-hub", "title": "Email Marketing and Outreach Software: Campaigns, Lifecycle, and Responsible B2B Outbound",
     "public_path": "/categories/email-outreach/", "primary_keyword": "email marketing and outreach software"},
    {"id": "H04", "cluster_num": 4, "page_type": "category-hub", "title": "CRM and Lead Generation Software: From Prospect Data to Qualified Pipeline",
     "public_path": "/categories/crm-lead-gen/", "primary_keyword": "crm and lead generation software"},
    {"id": "H05", "cluster_num": 5, "page_type": "category-hub", "title": "Marketing Automation and Analytics Software: Workflows, Measurement, CRO, and Distribution",
     "public_path": "/categories/automation-analytics/", "primary_keyword": "marketing automation and analytics software"},
    {"id": "H06", "cluster_num": 6, "page_type": "category-hub", "title": "Content Operations Software: Planning, Workflow, Governance, and Distribution Tools",
     "public_path": "/categories/content-operations/", "primary_keyword": "content operations software"},
    {"id": "H07", "cluster_num": 7, "page_type": "category-hub", "title": "Paid Media Software: Tools for Running, Governing, and Measuring Ad Spend",
     "public_path": "/categories/paid-media/", "primary_keyword": "paid media software"},
    {"id": "H08", "cluster_num": 8, "page_type": "category-hub", "title": "Ecommerce Growth Software: Storefront, Merchandising, Checkout, and Retention Tools",
     "public_path": "/categories/ecommerce-growth/", "primary_keyword": "ecommerce growth software"},
    {"id": "H09", "cluster_num": 9, "page_type": "category-hub", "title": "Customer Retention Software: Onboarding, Support, Feedback, and Customer Success Tools",
     "public_path": "/categories/customer-retention/", "primary_keyword": "customer retention software"},
    {"id": "H10", "cluster_num": 10, "page_type": "category-hub", "title": "Partnership Growth Software: Affiliate, Influencer, Referral, and Channel Programs",
     "public_path": "/categories/affiliate-partnerships/", "primary_keyword": "affiliate and partnership software"},
    {"id": "H11", "cluster_num": 11, "page_type": "category-hub", "title": "Website Experience Software: Builders, CMS, Forms, Performance, and Conversion Infrastructure",
     "public_path": "/categories/website-experience/", "primary_keyword": "website experience software"},
    {"id": "H12", "cluster_num": 12, "page_type": "category-hub", "title": "Data and RevOps Software: Connecting Marketing Activity to Accounts and Revenue",
     "public_path": "/categories/data-revops/", "primary_keyword": "revops software"},
    {"id": "H13", "cluster_num": 13, "page_type": "category-hub", "title": "Webinar, Event, and Community Software for Demand Generation",
     "public_path": "/categories/webinars-demand-gen/", "primary_keyword": "webinar and event software"},
    {"id": "H14", "cluster_num": 14, "page_type": "category-hub", "title": "Agency Operations Software: Projects, Clients, Resourcing, Proposals, and Billing",
     "public_path": "/categories/agency-operations/", "primary_keyword": "agency management software"},
    {"id": "H15", "cluster_num": 15, "page_type": "category-hub", "title": "Product-Led Growth Software: Product Analytics, Onboarding, and Experimentation Tools",
     "public_path": "/categories/product-led-growth/", "primary_keyword": "product-led growth software"},
]
WORDS = {"listicle": "1200-1800", "pillar-listicle": "1500-2200", "comparison": "1400-2000",
         "alternatives": "1400-2000", "pricing-guide": "1200-1800", "guide": "1000-1500",
         "strategic-guide": "1500-2200", "category-hub": "800-1400", "topical-hub": "1000-1800"}


def classify(a):
    slug = a["slug"].strip("/")
    intent = a["intent"].lower()
    title = a["title"]
    if a["num"] == 99:
        return "strategic-guide", f"/guides/{slug}/"
    if " vs " in title and not title.startswith("Lead Scoring vs"):
        return "comparison", f"/compare/{slug}/"
    if intent.startswith("alternative"):
        return "alternatives", f"/alternatives/{slug.replace('-alternatives', '')}/"
    if intent.startswith("pricing"):
        topic = {"seo-software-pricing": "seo-software", "ai-content-tool-pricing": "ai-content-tools",
                 "cold-email-software-pricing": "cold-email-software", "crm-pricing": "crm",
                 "marketing-automation-pricing": "marketing-automation"}[slug]
        return "pricing-guide", f"/pricing/{topic}/"
    if title.startswith("How to") or intent.startswith("informational"):
        return "guide", f"/guides/{slug}/"
    pt = "pillar-listicle" if a["num"] in (1, 21, 41, 61, 81) else "listicle"
    return pt, f"/best/{re.sub(r'^best-', '', slug)}/"


def main():
    src = json.load(open(os.path.join(ROOT, ".tmp", "source-article-map.json")))
    man_path = os.path.join(ROOT, "strategy", "url-manifest.json")
    old = {}
    if os.path.exists(man_path):
        old = {p["id"]: p for p in json.load(open(man_path))["pages"]}
    pages = []
    for h in HUBS:
        h = dict(h, counted=False, cluster=CLUSTERS.get(h["cluster_num"], ("Umbrella: growth software",))[0],
                 parent_hub="" if h["id"] == "H00" else "/growth-stack/",
                 target_word_range=WORDS[h["page_type"]],
                 source_doc_reference="Section 3 (site map) and Section 10 (central topical hub)")
        pages.append(h)
    for a in src["articles"]:
        pid = f"A{a['num']:03d}"
        pt, path = classify(a)
        cname, hub, _ = CLUSTERS[a["cluster_num"]]
        pages.append({
            "id": pid, "counted": True, "cluster_num": a["cluster_num"], "cluster": cname,
            "title": a["title"], "page_type": pt, "public_path": path,
            "primary_keyword": a["query"], "search_intent": a["intent"],
            "source_slug": a["slug"], "angle": a["angle"], "brief": a["brief"],
            "source_link_notes": a["links"], "parent_hub": hub,
            "cluster_pillar": PILLARS[a["cluster_num"]] if pid != PILLARS[a["cluster_num"]] else "",
            "target_word_range": WORDS[pt],
            "source_doc_reference": f"Section 10, Cluster {a['cluster_num']}, item {a['num']:02d}",
        })
    extra = os.path.join(ROOT, "inputs", "additional-200-articles.csv")
    if not os.path.exists(extra):
        raise SystemExit("Missing inputs/additional-200-articles.csv (A101-A300). See inputs/README.md.")
    for i, r in enumerate(csv.DictReader(open(extra, encoding="utf-8-sig")), start=2):
        cn = NEW_SLUG_TO_CLUSTER[r["cluster_slug"]]
        cname, hub, _ = CLUSTERS[cn]
        pt = NEW_TYPES[r["page_type"]]
        pages.append({
            "id": r["id"], "counted": True, "cluster_num": cn, "cluster": cname, "title": r["title"],
            "page_type": pt, "public_path": r["url"], "primary_keyword": r["primary_query"],
            "search_intent": r["page_type"], "source_slug": r["slug"], "angle": r["angle"],
            "brief": r["writing_brief"], "source_link_notes": r["internal_link_targets"],
            "parent_hub": hub, "cluster_pillar": "", "target_word_range": NEW_WORDS[pt],
            "source_doc_reference": f"additional-200-articles.csv row {i}",
        })
    for p in pages:
        p["physical_file_path"] = "site" + p["public_path"] + "index.html"
        p["status"] = old.get(p["id"], {}).get("status", "planned")
        p["final_h1"] = old.get(p["id"], {}).get("final_h1", p["title"])
    paths = [p["public_path"] for p in pages]
    assert len(paths) == len(set(paths)), "duplicate public paths"
    ids = [p["id"] for p in pages if p["counted"]]
    assert ids == [f"A{n:03d}" for n in range(1, 301)], "article IDs must be exactly A001-A300 in order"
    titles = [p["title"].lower() for p in pages]
    assert len(titles) == len(set(titles)), "duplicate titles"
    json.dump({"pages": pages}, open(man_path, "w"), indent=1)

    with open(os.path.join(ROOT, "strategy", "master-300-article-map.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["article_id", "cluster", "article_title", "final_h1", "page_type", "primary_keyword",
                    "secondary_topics", "search_intent", "audience", "suggested_slug", "public_path",
                    "physical_file_path", "parent_hub", "cluster_pillar", "target_word_range", "status",
                    "source_doc_reference", "notes"])
        for p in pages:
            if not p["counted"]:
                continue
            w.writerow([p["id"], p["cluster"], p["title"], p["final_h1"], p["page_type"], p["primary_keyword"],
                        p["angle"], p["search_intent"],
                        "Agencies, founders, and lean marketing/sales teams",
                        p["source_slug"], p["public_path"], p["physical_file_path"], p["parent_hub"],
                        p["cluster_pillar"], p["target_word_range"], p["status"], p["source_doc_reference"],
                        "Source internal-link notes: " + p["source_link_notes"]])
    print(f"Manifest: {len(pages)} pages ({sum(p['counted'] for p in pages)} counted articles)")


if __name__ == "__main__":
    main()
