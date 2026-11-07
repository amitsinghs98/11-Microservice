#!/usr/bin/env python3
"""Build strategy/keyword-map.csv (the seo-content-writer "01-keyword-map" input) from the manifest.

Primary keywords come from the source maps. Secondary topics are derived from each
brief's angle (comma/semicolon-separated dimensions). Search volumes are deliberately
left as "not measured": no keyword data source was used, and none may be invented.
"""
import csv, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def secondaries(angle):
    parts = re.split(r"[;,]| and |: ", angle)
    out = []
    for p in parts:
        p = re.sub(r"^(compare|assess|focus on|prioritize|explain|separate|make|distinguish|include|cover)\s+", "", p.strip(), flags=re.I)
        p = p.strip(" .—-").lower()
        if 3 <= len(p) <= 60 and p not in out:
            out.append(p)
    return out[:8]


def main():
    pages = json.load(open(os.path.join(ROOT, "strategy", "url-manifest.json")))["pages"]
    with open(os.path.join(ROOT, "strategy", "keyword-map.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "public_path", "role", "primary_keyword", "secondary_topics", "intent", "search_volume", "notes"])
        for p in pages:
            role = {"topical-hub": "umbrella hub", "category-hub": "cluster hub", "pillar-listicle": "cluster pillar"}.get(p["page_type"], "supporting")
            w.writerow([p["id"], p["public_path"], role, p["primary_keyword"], " | ".join(secondaries(p.get("angle", ""))),
                        p.get("search_intent", p["page_type"]), "not measured",
                        "Primary query is a search-intent hypothesis from the source map; validate the live SERP before publishing."])
    print("keyword-map.csv:", len(pages), "rows")


if __name__ == "__main__":
    main()
