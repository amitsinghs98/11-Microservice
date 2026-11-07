#!/usr/bin/env python3
"""Tighten silos: keep at most MAX_CROSS cross-cluster destinations per article.

Extra cross-cluster links are unlinked (the <a> wrapper is removed, the anchor text stays),
so no sentence changes. Kept first: links to pillar pages and hubs, then reading order.
Stack-spanning guides (EXEMPT) keep all their links because spanning clusters is their job.
Usage: python3 scripts/limit_cross_links.py [--dry-run]
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_CROSS = 2
EXEMPT = {"A099", "A040", "A098"}

def main():
    dry = "--dry-run" in sys.argv
    pages = json.load(open(os.path.join(ROOT, "strategy", "url-manifest.json")))["pages"]
    by_path = {p["public_path"]: p for p in pages}
    removed = touched = 0
    for p in pages:
        if not p["counted"] or p["id"] in EXEMPT:
            continue
        fp = os.path.join(ROOT, p["physical_file_path"])
        s = open(fp, encoding="utf-8").read()
        a0, a1 = s.index("<article"), s.index("</article>")
        body = s[a0:a1]
        links = [(m.start(), m.group(1)) for m in re.finditer(r'<a href="(/[^"#]*)', body)]
        cross = []
        for _, href in links:
            d = by_path.get(href)
            if d and d["cluster_num"] not in (p["cluster_num"], 0) and href not in cross:
                cross.append(href)
        if len(cross) <= MAX_CROSS:
            continue
        rank = lambda h: (0 if by_path[h]["page_type"] in ("pillar-listicle", "category-hub") else 1, cross.index(h))
        keep = set(sorted(cross, key=rank)[:MAX_CROSS])
        drop = [h for h in cross if h not in keep]
        new = body
        for h in drop:
            new, n = re.subn(r'<a href="' + re.escape(h) + r'"[^>]*>(.*?)</a>', r"\1", new, flags=re.S)
            removed += n
        touched += 1
        if not dry:
            open(fp, "w", encoding="utf-8").write(s[:a0] + new + s[a1:])
    print(f"{'Would unlink' if dry else 'Unlinked'} {removed} cross-cluster links on {touched} articles (max {MAX_CROSS} per article; exempt {sorted(EXEMPT)})")

if __name__ == "__main__":
    main()
