#!/usr/bin/env python3
"""Merge the author's first-hand experience and approvals from progress/david-experience-intake.md.

For each block with text, the page's experience marker is replaced with the author's paragraphs
(<p data-experience="filled">). 'Approved: yes' sets the page status to approved, which puts it in
site/sitemap.xml. Never fill these blocks with anything other than the author's own words.
Usage: python3 scripts/apply_experience.py [--dry-run]
"""
import html, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARKER_P = "<p><mark>[YOUR EXPERIENCE HERE — the skill will not invent this]</mark></p>"

def main():
    dry = "--dry-run" in sys.argv
    src = open(os.path.join(ROOT, "progress", "david-experience-intake.md"), encoding="utf-8").read()
    man_path = os.path.join(ROOT, "strategy", "url-manifest.json")
    man = json.load(open(man_path)); by = {p["id"]: p for p in man["pages"]}
    filled = approved = 0
    for m in re.finditer(r"^## (A\d{3}) .*?\n<<<\n(.*?)\n>>>\nApproved: (\w+)", src, re.S | re.M):
        pid, text, ok = m.group(1), m.group(2).strip(), m.group(3).lower() == "yes"
        p = by[pid]; fp = os.path.join(ROOT, p["physical_file_path"])
        page = open(fp, encoding="utf-8").read()
        if text and MARKER_P in page:
            paras = [html.escape(x.strip()) for x in re.split(r"\n\s*\n", text) if x.strip()]
            block = "\n        ".join(f'<p data-experience="filled">{x}</p>' for x in paras)
            page = page.replace(MARKER_P, block)
            filled += 1
            if not dry:
                open(fp, "w", encoding="utf-8").write(page)
        if ok:
            if MARKER_P in page:
                print(f"{pid}: not approved, experience section still empty")
                continue
            p["status"] = "approved"; approved += 1
    if not dry:
        json.dump(man, open(man_path, "w"), indent=1)
    print(f"{'Would fill' if dry else 'Filled'} {filled} experience sections; approved {approved} pages."
          " Next: python3 scripts/validate_content.py && python3 scripts/build_sitemap.py")

if __name__ == "__main__":
    main()
