#!/usr/bin/env python3
"""Extract the 100-article topical map from the strategy DOCX.

Usage: python3 scripts/extract_source_map.py [inputs/content-strategy.docx]

Converts the DOCX to Markdown with Pandoc (must be installed), parses section
"10. The 100-article topical map", and writes .tmp/source-article-map.json.
The DOCX itself is never modified.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIELDS = {
    "Suggested slug": "slug",
    "Primary query / topic": "query",
    "Intent / page type": "intent",
    "Distinct editorial angle": "angle",
    "Writing brief and required depth": "brief",
    "Internal links": "links",
}


def main():
    docx = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "inputs", "content-strategy.docx")
    if not os.path.exists(docx):
        sys.exit(f"Source DOCX not found: {docx}. See inputs/README.md.")
    md = subprocess.run(["pandoc", "-t", "markdown", "--wrap=none", docx],
                        check=True, capture_output=True, text=True).stdout
    articles, purpose, cluster, cur = [], {}, None, None
    for i, line in enumerate(md.split("\n"), 1):
        if line.startswith("# 11."):
            break
        m = re.match(r"^# Cluster (\d) --- (.*)", line)
        if m:
            cluster = (int(m.group(1)), m.group(2).strip())
            continue
        m = re.match(r"^## (\d\d|100)\. (.*)", line)
        if m:
            cur = {"num": int(m.group(1)), "title": m.group(2).strip(),
                   "cluster_num": cluster[0], "cluster": cluster[1], "source_line": i}
            articles.append(cur)
            continue
        m = re.match(r"^\*\*Cluster purpose:\*\* (.*)", line)
        if m and cluster:
            purpose[cluster[0]] = m.group(1)
        m = re.match(r"^\*\*(.+?):\*\* ?(.*)", line)
        if m and cur and m.group(1) in FIELDS:
            cur[FIELDS[m.group(1)]] = m.group(2).replace('\\"', '"').replace("\\'", "'").strip()
    out = os.path.join(ROOT, ".tmp", "source-article-map.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({"articles": articles, "cluster_purpose": purpose}, open(out, "w"), indent=1)
    print(f"Extracted {len(articles)} articles -> {out}")


if __name__ == "__main__":
    main()
