#!/usr/bin/env python3
"""Build the canonical URL manifest from the extracted source map.

Inputs : .tmp/source-article-map.json (from scripts/extract_source_map.py)
Outputs: strategy/url-manifest.json   (machine-readable, used by all scripts)
         strategy/100-article-master-map.csv

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
}
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
]
WORDS = {"listicle": "1200-1800", "pillar-listicle": "1500-2200", "comparison": "1400-2000",
         "alternatives": "1400-2000", "pricing-guide": "1200-1800", "guide": "1000-1500",
         "strategic-guide": "1500-2200", "category-hub": "1500-2200", "topical-hub": "1500-2200"}


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
    for p in pages:
        p["physical_file_path"] = "site" + p["public_path"] + "index.html"
        p["status"] = old.get(p["id"], {}).get("status", "planned")
        p["final_h1"] = old.get(p["id"], {}).get("final_h1", p["title"])
    paths = [p["public_path"] for p in pages]
    assert len(paths) == len(set(paths)), "duplicate public paths"
    json.dump({"pages": pages}, open(man_path, "w"), indent=1)

    with open(os.path.join(ROOT, "strategy", "100-article-master-map.csv"), "w", newline="") as f:
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
