#!/usr/bin/env python3
"""Generate site/sitemap.xml from the URL manifest.

Includes only pages whose file exists AND whose manifest status is publication-ready
("approved" = human editor has verified facts and signed off, or "published").
Status ladder: planned -> drafted -> QA-passed (automated checks) -> approved -> published.
Uses the domain from site.config.json (a placeholder until launch). No <lastmod>
is emitted: file modification times reflect drafting, not meaningful content
updates, so they would mislead crawlers. Add real lastmod values at publication.

Usage: python3 scripts/build_sitemap.py            # site/sitemap.xml (approved/published only)
       python3 scripts/build_sitemap.py --staging  # qa/sitemap-staging.xml (also QA-passed/drafted)
"""
import json, os, sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READY = {"approved", "published"}


def main():
    ready = set(READY)
    staging = "--staging" in sys.argv
    if staging:
        ready |= {"drafted", "researched", "edited", "QA-passed"}
    domain = json.load(open(os.path.join(ROOT, "site.config.json")))["domain"].rstrip("/")
    pages = json.load(open(os.path.join(ROOT, "strategy", "url-manifest.json")))["pages"]
    urls = [p["public_path"] for p in pages
            if p["status"] in ready and os.path.exists(os.path.join(ROOT, p["physical_file_path"]))]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines += [f"  <url><loc>{escape(domain + u)}</loc></url>" for u in urls]
    lines.append("</urlset>")
    out = os.path.join(ROOT, "qa", "sitemap-staging.xml") if staging else os.path.join(ROOT, "site", "sitemap.xml")
    open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"{os.path.relpath(out, ROOT)}: {len(urls)} URLs (statuses: {sorted(ready)}; domain {domain})")


if __name__ == "__main__":
    main()
