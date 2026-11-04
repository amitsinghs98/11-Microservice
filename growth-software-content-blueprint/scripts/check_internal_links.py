#!/usr/bin/env python3
"""Check every root-relative link in site/**/*.html against the manifest and the site/ tree.

Usage:
  python3 scripts/check_internal_links.py            # full audit, writes QA + strategy CSVs
  python3 scripts/check_internal_links.py --quiet A001 A002   # check only these source pages, no file output

Writes (full mode):
  qa/internal-link-audit.csv          every internal link, existence and relevance heuristic
  strategy/internal-linking-map.csv   source -> destination with anchor, context and relationship type
  strategy/anchor-text-map.csv        destination -> anchor variations and example context
  qa/external-link-inventory.csv      external links by page (not fetched)
Exit 1 if any internal link is broken or points outside the manifest.
"""
import csv, json, os, re, sys
from collections import defaultdict
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
NON_ARTICLE_OK = {"/", "/sitemap.xml", "/robots.txt"}


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.cur, self.section, self.ids, self.para = [], None, "", set(), ""
        self.block_text, self.in_heading = "", False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "section" and "id" in a:
            self.section = a["id"]
        if tag in ("p", "li", "td", "dd"):
            self.block_text = ""
        if tag == "a" and "href" in a:
            self.cur = {"href": a["href"], "anchor": "", "section": self.section, "rel": a.get("rel", ""),
                        "context_start": len(self.block_text)}

    def handle_endtag(self, tag):
        if tag == "a" and self.cur:
            self.cur["context"] = self.block_text
            self.links.append(self.cur)
            self.cur = None
        if tag in ("p", "li", "td", "dd"):
            for l in reversed(self.links):
                if l.get("final"):
                    break
                l["final"] = True
                l["context"] = self.block_text.strip()

    def handle_data(self, data):
        self.block_text += data
        if self.cur:
            self.cur["anchor"] += data


def rel_type(src, dst):
    if not dst:
        return "unplanned"
    if dst["page_type"] in ("category-hub", "topical-hub"):
        return "to-hub" if src["page_type"] not in ("category-hub", "topical-hub") else "hub-to-hub"
    if src["page_type"] in ("category-hub", "topical-hub"):
        return "hub-to-child"
    if src.get("cluster_num") == dst.get("cluster_num"):
        if src.get("cluster_pillar") == dst["id"]:
            return "to-pillar"
        return "same-cluster"
    return "cross-cluster"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    pages = json.load(open(os.path.join(ROOT, "strategy", "url-manifest.json")))["pages"]
    by_path = {p["public_path"]: p for p in pages}
    by_file = {os.path.normpath(os.path.join(ROOT, p["physical_file_path"])): p for p in pages}
    html_files = []
    for d, _, fs in os.walk(SITE):
        html_files += [os.path.join(d, f) for f in fs if f.endswith(".html")]
    rows, ext, broken = [], [], 0
    inbound = defaultdict(set)
    for fp in sorted(html_files):
        src = by_file.get(os.path.normpath(fp), {"id": "INDEX" if fp.endswith("site/index.html") else "UNKNOWN",
                                                    "page_type": "index", "public_path": "/"})
        if args and src["id"] not in args:
            continue
        lp = LinkParser()
        lp.feed(open(fp, encoding="utf-8").read())
        for l in lp.links:
            h = l["href"]
            if h.startswith(("http://", "https://")):
                ext.append([src["id"], h, l["anchor"].strip(), l["rel"]])
                continue
            if h.startswith(("#", "mailto:")):
                continue
            path, _, frag = h.partition("#")
            dst = by_path.get(path)
            exists_file = os.path.exists(os.path.join(SITE, path.lstrip("/"), "index.html")) if path.endswith("/") else os.path.exists(os.path.join(SITE, path.lstrip("/")))
            problem = ""
            if not path.startswith("/"):
                problem = "not root-relative"
            elif path in NON_ARTICLE_OK:
                pass
            elif not dst:
                problem = "not in manifest"
            elif not path.endswith("/"):
                problem = "missing trailing slash"
            elif not exists_file:
                problem = "destination file missing"
            if frag and dst and exists_file and not problem:
                tlp = LinkParser()
                tlp.feed(open(os.path.join(SITE, path.lstrip("/"), "index.html"), encoding="utf-8").read())
                if frag not in tlp.ids:
                    problem = f"fragment #{frag} not found"
            if dst and dst["id"] == src["id"]:
                problem = problem or "self-link"
            if problem and problem != "self-link":
                broken += 1
            if dst:
                inbound[dst["id"]].add(src["id"])
            anchor = re.sub(r"\s+", " ", l["anchor"]).strip()
            ctx = re.sub(r"\s+", " ", l.get("context", "")).strip()
            generic = anchor.lower() in ("click here", "read more", "here", "this", "learn more", "this guide")
            relevant = "review: generic anchor" if generic else ("contextual" if len(ctx) > len(anchor) + 20 else "list/directory")
            rows.append({"source_id": src["id"], "source_path": src["public_path"], "dest_id": dst["id"] if dst else "",
                         "dest_path": path, "anchor": anchor, "section": l["section"], "context": ctx[:240],
                         "relationship": rel_type(src, dst) if src.get("page_type") != "index" else "index-directory",
                         "exists": not problem or problem == "self-link", "problem": problem, "relevance": relevant})
    for r in rows:
        if r["problem"] and r["problem"] != "self-link":
            print(f"BROKEN {r['source_id']} -> {r['dest_path']} ({r['problem']}) anchor={r['anchor']!r}")
    orphans = [p["id"] for p in pages if os.path.exists(os.path.join(ROOT, p["physical_file_path"]))
               and not (inbound[p["id"]] - {"INDEX"})]
    print(f"Internal links: {len(rows)}; broken: {broken}; external links: {len(ext)}")
    if not args:
        print(f"Pages with no inbound links from other content pages: {orphans or 'none'}")
        write(rows, ext, pages, inbound, orphans)
    sys.exit(1 if broken else 0)


def write(rows, ext, pages, inbound, orphans):
    with open(os.path.join(ROOT, "qa", "internal-link-audit.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source_id", "source_file", "dest_path", "dest_id", "destination_exists", "problem",
                    "contextual_relevance", "anchor_text"])
        for r in rows:
            w.writerow([r["source_id"], "site" + r["source_path"] + "index.html", r["dest_path"], r["dest_id"],
                        r["exists"], r["problem"], r["relevance"], r["anchor"]])
    with open(os.path.join(ROOT, "strategy", "internal-linking-map.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source_id", "source_path", "dest_id", "dest_path", "anchor_text", "link_location",
                    "context", "relationship_type", "validation_status"])
        for r in rows:
            if r["source_id"] == "INDEX":
                continue
            w.writerow([r["source_id"], r["source_path"], r["dest_id"], r["dest_path"], r["anchor"],
                        "section#" + r["section"] if r["section"] else "body", r["context"], r["relationship"],
                        "ok" if not r["problem"] else r["problem"]])
    anchors = defaultdict(list)
    for r in rows:
        if r["dest_id"] and r["source_id"] != "INDEX":
            anchors[r["dest_path"]].append(r)
    titles = {p["public_path"]: p["title"] for p in pages}
    with open(os.path.join(ROOT, "strategy", "anchor-text-map.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["dest_path", "dest_title", "inbound_link_count", "distinct_anchor_count",
                    "anchor_variations", "most_repeated_anchor", "example_context"])
        for path in sorted(titles):
            rs = anchors.get(path, [])
            al = [r["anchor"] for r in rs]
            distinct = sorted(set(al), key=str.lower)
            top = max(distinct, key=al.count) if distinct else ""
            ex = next((r["context"] for r in rs if r["relevance"] == "contextual"), "")
            w.writerow([path, titles[path], len(rs), len(distinct), " | ".join(distinct[:15]),
                        f"{top} (x{al.count(top)})" if top else "", ex[:200]])
    with open(os.path.join(ROOT, "qa", "external-link-inventory.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source_id", "url", "anchor_text", "rel"])
        w.writerows(ext)


if __name__ == "__main__":
    main()
