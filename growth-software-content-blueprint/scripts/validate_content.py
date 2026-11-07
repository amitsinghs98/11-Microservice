#!/usr/bin/env python3
"""Validate article HTML files against the manifest and the HTML spec.

Usage:
  python3 scripts/validate_content.py              # all pages, writes QA reports
  python3 scripts/validate_content.py A001 A002    # only these IDs, prints to stdout only

The HTML well-formedness check is HEURISTIC (stdlib html.parser tag balancing);
it is not a W3C conformance check. Exit code 1 if any page has errors.
"""
import csv, json, os, re, sys
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
FORBIDDEN_TAGS = {"style", "img", "iframe", "font"}
MARKER = "[YOUR EXPERIENCE HERE — the skill will not invent this]"
BAD_SCHEMA = re.compile(r'"@type"\s*:\s*"(Review|AggregateRating|Product|Rating)"')
PLACEHOLDERS = re.compile(r"\b(TODO|TBD|LOREM|INSERT TEXT|YOUR LINK HERE|AFFILIATE_URL_PENDING|FIXME|XXX)\b", re.I)
BANNED = re.compile(r"\b(we tested|our testing|our tests|we've tested|hands-on testing showed|users rate|verified customer rating|game-changing|revolutionary|best-in-class|ultimate solution|in today's digital landscape)\b", re.I)
WORD_RANGES = {"1200-1800": (1000, 2600), "1500-2200": (1250, 3000), "1400-2000": (1150, 2800), "1000-1500": (850, 2300),
               "1400-2100": (1150, 2900), "800-1400": (750, 2200), "1000-1800": (850, 2600),
               "2000-3000": (1700, 3600), "1800-2800": (1500, 3400)}


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors, self.ids, self.hrefs, self.headings = [], [], [], [], []
        self.counts, self.text, self.title, self.meta_desc, self.canonical = {}, [], "", None, None
        self.doctype = False
        self.html_lang = None
        self.in_title = False
        self.cur_heading = None
        self.article_attrs = {}
        self.in_body = False
        self.inline_style = False
        self.in_script = False
        self.scripts = []
        self.h1_text_index = None

    def handle_decl(self, decl):
        if decl.lower().startswith("doctype html"):
            self.doctype = True

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.counts[tag] = self.counts.get(tag, 0) + 1
        if "style" in a or "class" in a:
            self.inline_style = True
        if tag in FORBIDDEN_TAGS:
            self.errors.append(f"forbidden <{tag}>")
        if tag == "script":
            if a.get("type") != "application/ld+json":
                self.errors.append("forbidden non-JSON-LD <script>")
            self.in_script = True
            self.scripts.append("")
        if tag == "html":
            self.html_lang = a.get("lang")
        if tag == "body":
            self.in_body = True
        if tag == "title":
            self.in_title = True
        if tag == "meta" and a.get("name") == "description":
            self.meta_desc = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical = a.get("href")
        if tag == "article":
            self.article_attrs = a
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "a" and "href" in a:
            self.hrefs.append(a)
        if re.fullmatch(r"h[1-6]", tag):
            self.cur_heading = [int(tag[1]), ""]
        if tag not in VOID:
            self.stack.append((tag, self.getpos()[0]))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID and self.stack and self.stack[-1][0] == tag:
            self.stack.pop()

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if tag == "title":
            self.in_title = False
        if tag == "script":
            self.in_script = False
        if tag == "h1":
            self.h1_text_index = len(self.text)
        if re.fullmatch(r"h[1-6]", tag) and self.cur_heading:
            self.headings.append(tuple(self.cur_heading))
            self.cur_heading = None
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
            return
        # implicit closes allowed for p/li per HTML rules
        while self.stack and self.stack[-1][0] in ("p", "li", "td", "th", "tr", "dt", "dd") and self.stack[-1][0] != tag:
            self.stack.pop()
        if self.stack and self.stack[-1][0] == tag:
            self.stack.pop()
        else:
            self.errors.append(f"unexpected </{tag}> at line {self.getpos()[0]}")

    def handle_data(self, data):
        if self.in_script:
            self.scripts[-1] += data
            return
        if self.in_title:
            self.title += data
        if self.cur_heading is not None:
            self.cur_heading[1] += data
        if self.in_body:
            self.text.append(data)


def load_manifest():
    return json.load(open(os.path.join(ROOT, "strategy", "url-manifest.json")))["pages"]


def validate(page, domain):
    issues, warnings = [], []
    path = os.path.join(ROOT, page["physical_file_path"])
    if not os.path.exists(path):
        return {"exists": False, "errors": ["file missing"], "warnings": [], "words": 0, "internal_links": 0,
                "external_links": 0}
    raw = open(path, encoding="utf-8").read()
    p = Parser()
    p.feed(raw)
    p.close()
    if not p.doctype:
        issues.append("missing <!doctype html>")
    if not p.html_lang:
        issues.append("missing <html lang>")
    if not p.title.strip():
        issues.append("missing <title>")
    if not p.meta_desc:
        issues.append("missing meta description")
    elif not 70 <= len(p.meta_desc) <= 200:
        warnings.append(f"meta description length {len(p.meta_desc)}")
    exp_canon = domain + page["public_path"]
    if p.canonical != exp_canon:
        issues.append(f"canonical {p.canonical!r} != {exp_canon!r}")
    if p.counts.get("h1", 0) != 1:
        issues.append(f"{p.counts.get('h1', 0)} <h1> elements")
    if p.counts.get("article", 0) != 1:
        issues.append(f"{p.counts.get('article', 0)} <article> elements")
    if p.counts.get("main", 0) != 1:
        issues.append("missing <main>")
    if p.article_attrs.get("data-article-id") != page["id"]:
        issues.append(f"data-article-id {p.article_attrs.get('data-article-id')!r} != {page['id']}")
    if p.inline_style:
        issues.append("style= or class= attribute present")
    dup = sorted({i for i in p.ids if p.ids.count(i) > 1})
    if dup:
        issues.append(f"duplicate ids: {dup}")
    for a in p.hrefs:
        h = a["href"]
        if h.startswith("#") and h[1:] not in p.ids:
            issues.append(f"fragment {h} has no target")
        if h.startswith("http") and domain not in h:
            if a.get("target") == "_blank" and not {"noopener", "noreferrer"} <= set(a.get("rel", "").split()):
                issues.append(f"external link missing rel noopener noreferrer: {h}")
    # heading hierarchy
    prev = 1
    for lvl, _ in p.headings[1:]:
        if lvl > prev + 1:
            warnings.append(f"heading jump h{prev}->h{lvl}")
            break
        prev = lvl
    if p.headings and p.headings[0][0] != 1:
        issues.append("first heading is not h1")
    if p.stack:
        open_tags = [t for t, _ in p.stack if t not in ("p", "li")]
        if open_tags:
            issues.append(f"unclosed tags: {open_tags[:5]}")
    issues.extend(sorted(set(p.errors)))
    body = " ".join(p.text)
    if PLACEHOLDERS.search(body) or PLACEHOLDERS.search(raw.split("<body>")[-1]):
        issues.append(f"placeholder text: {PLACEHOLDERS.search(raw).group(0)}")
    m = BANNED.search(body)
    if m:
        issues.append(f"banned phrase: {m.group(0)!r}")
    is_hub = page["page_type"] in ("category-hub", "topical-hub")
    # --- seo-content-writer rules ---
    content_h2 = [t.strip() for lvl, t in p.headings if lvl == 2 and t.strip() != "On this page"]
    non_q = [t for t in content_h2 if not t.endswith("?")]
    if non_q:
        issues.append(f"{len(non_q)} H2s are not questions, e.g. {non_q[0]!r}")
    if any(re.search(r"\b(sources|references|bibliography)\b", t, re.I) for t in content_h2):
        issues.append("trailing sources/references section (links must be inline)")
    tables = p.counts.get("table", 0)
    if not is_hub and tables != 1:
        issues.append(f"{tables} tables (rule of one: exactly 1)")
    mk = raw.count(MARKER)
    if not is_hub and mk != 1:
        issues.append(f"experience marker present {mk} times (need exactly 1)")
    if is_hub and mk:
        issues.append("hubs must not carry the experience marker")
    after_h1 = " ".join(p.text[p.h1_text_index:]) if p.h1_text_index is not None else body
    first100 = " ".join(re.findall(r"[\w'’-]+", after_h1)[:100]).lower()
    kw = " ".join(re.findall(r"[\w'’-]+", page["primary_keyword"].lower()))
    if kw and kw not in first100:
        issues.append(f"primary keyword {page['primary_keyword']!r} not in first 100 words after H1")
    h1 = next((t for lvl, t in p.headings if lvl == 1), "")
    if kw and kw not in " ".join(re.findall(r"[\w'’-]+", h1.lower())):
        warnings.append("primary keyword not verbatim in H1 (H1 kept as source title)")
    tl = len(p.title.strip())
    if not 30 <= tl <= 75:
        warnings.append(f"title length {tl} (target 50-60 + ' | brand')")
    if p.meta_desc and not 110 <= len(p.meta_desc) <= 165:
        warnings.append(f"meta description length {len(p.meta_desc)} (target 120-160)")
    if len(p.scripts) != 1:
        issues.append(f"{len(p.scripts)} JSON-LD blocks (need exactly 1)")
    for js in p.scripts:
        try:
            data = json.loads(js)
        except ValueError as e:
            issues.append(f"JSON-LD does not parse: {e}")
            continue
        if BAD_SCHEMA.search(js):
            issues.append("forbidden Review/AggregateRating/Product schema")
        graph = data.get("@graph", [data]) if isinstance(data, dict) else data
        types = {g.get("@type") for g in graph if isinstance(g, dict)}
        if "BreadcrumbList" not in types:
            issues.append("JSON-LD missing BreadcrumbList")
        faq = next((g for g in graph if isinstance(g, dict) and g.get("@type") == "FAQPage"), None)
        if not is_hub and not faq:
            issues.append("JSON-LD missing FAQPage")
        if faq:
            qs = [q.get("name", "").strip() for q in faq.get("mainEntity", [])]
            visible = {t.strip() for lvl, t in p.headings if lvl == 3}
            missing = [q for q in qs if q not in visible]
            if missing or not qs:
                issues.append(f"FAQPage questions not matching visible H3s: {missing[:2] or 'none listed'}")
    words = len(re.findall(r"\b[\w'’-]+\b", body))
    lo, hi = WORD_RANGES.get(page["target_word_range"], (800, 3000))
    if not lo <= words <= hi:
        warnings.append(f"word count {words} outside review band {lo}-{hi}")
    internal = [a["href"] for a in p.hrefs if a["href"].startswith("/")]
    external = [a["href"] for a in p.hrefs if a["href"].startswith("http")]
    if page["id"] != "H00" and page.get("parent_hub") and page["parent_hub"] not in internal:
        issues.append(f"no link to parent hub {page['parent_hub']}")
    return {"exists": True, "errors": issues, "warnings": warnings, "words": words,
            "internal_links": len(internal), "external_links": len(external), "title": p.title.strip(),
            "meta": p.meta_desc}


def main():
    ids = set(sys.argv[1:])
    domain = json.load(open(os.path.join(ROOT, "site.config.json")))["domain"]
    pages = load_manifest()
    sel = [p for p in pages if not ids or p["id"] in ids]
    results, bad = {}, 0
    for p in sel:
        r = validate(p, domain)
        results[p["id"]] = r
        if r["errors"]:
            bad += 1
        flag = "FAIL" if r["errors"] else ("WARN" if r["warnings"] else "ok")
        print(f"{p['id']} {flag:4} words={r['words']:5} int={r['internal_links']:3} ext={r['external_links']:3} "
              + "; ".join(r["errors"] + r["warnings"]))
    counted = [p for p in pages if p["counted"]]
    print(f"\nManifest articles: {len(counted)} counted + {len(pages) - len(counted)} hubs; checked {len(sel)}; failing {bad}")
    if not ids:
        titles = [r.get("title") for r in results.values() if r.get("title")]
        metas = [r.get("meta") for r in results.values() if r.get("meta")]
        dt = sorted({t for t in titles if titles.count(t) > 1})
        dm = sorted({m for m in metas if metas.count(m) > 1})
        if dt or dm:
            bad += 1
            print("Duplicate titles:", dt, "\nDuplicate meta descriptions:", dm)
        write_reports(pages, results, dt, dm)
    sys.exit(1 if bad else 0)


def update_status(pages, results):
    """Status ladder: planned -> drafted -> QA-passed -> approved -> published.
    Automated QA can only move pages between planned/drafted/QA-passed; approved and
    published are set by a human editor and are never downgraded here except when the file is missing."""
    man_path = os.path.join(ROOT, "strategy", "url-manifest.json")
    for p in pages:
        r = results[p["id"]]
        if not r["exists"]:
            p["status"] = "planned"
        elif p["status"] not in ("approved", "published"):
            p["status"] = "drafted" if r["errors"] else "QA-passed"
    json.dump({"pages": pages}, open(man_path, "w"), indent=1)
    csv_path = os.path.join(ROOT, "strategy", "master-300-article-map.csv")
    rows = list(csv.reader(open(csv_path, encoding="utf-8")))
    idx = rows[0].index("status")
    st = {p["id"]: p["status"] for p in pages}
    for row in rows[1:]:
        row[idx] = st.get(row[0], row[idx])
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)


def write_reports(pages, results, dup_titles, dup_metas):
    update_status(pages, results)
    log = os.path.join(ROOT, "strategy", "research-source-log.csv")
    flagged = {}
    if os.path.exists(log):
        for row in csv.DictReader(open(log, encoding="utf-8")):
            if row["verification_status"] == "Needs verification":
                flagged[row["article_id"]] = flagged.get(row["article_id"], 0) + 1
    with open(os.path.join(ROOT, "qa", "article-status.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "public_path", "status", "file_exists", "word_count", "metadata_ok", "internal_links",
                    "external_links", "claims_needing_verification", "errors", "warnings"])
        for p in pages:
            r = results[p["id"]]
            meta_ok = r["exists"] and not any(k in e for e in r["errors"] for k in ("title", "meta", "canonical", "h1"))
            w.writerow([p["id"], p["public_path"], p["status"], r["exists"], r["words"], meta_ok,
                        r["internal_links"], r["external_links"], flagged.get(p["id"], 0),
                        " | ".join(r["errors"]), " | ".join(r["warnings"])])
    fails = {k: v for k, v in results.items() if v["errors"]}
    warns = {k: v for k, v in results.items() if v["warnings"]}
    with open(os.path.join(ROOT, "qa", "html-validation-summary.md"), "w", encoding="utf-8") as f:
        f.write("# HTML Validation Summary\n\nGenerated by `python3 scripts/validate_content.py`.\n\n")
        f.write("**Method:** heuristic checks with Python's standard-library `html.parser` (tag balance, required "
                "elements, IDs, fragments, metadata, forbidden markup, placeholder and banned-phrase scans, word "
                "count bands). This is **not** a W3C/Nu validator conformance result.\n\n")
        f.write(f"- Pages checked: {len(results)}\n- Pages with errors: {len(fails)}\n- Pages with warnings only: "
                f"{len([k for k in warns if k not in fails])}\n- Duplicate titles: {len(dup_titles)}\n"
                f"- Duplicate meta descriptions: {len(dup_metas)}\n")
        total = sum(r["words"] for r in results.values())
        f.write(f"- Total words (body text): {total:,}\n\n")
        if fails:
            f.write("## Errors\n\n" + "".join(f"- {k}: {'; '.join(v['errors'])}\n" for k, v in fails.items()) + "\n")
        if warns:
            f.write("## Warnings (manual review)\n\n" + "".join(f"- {k}: {'; '.join(v['warnings'])}\n" for k, v in warns.items()))


if __name__ == "__main__":
    main()
