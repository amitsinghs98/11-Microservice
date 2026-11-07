#!/usr/bin/env python3
"""Apply launch values from site.config.json across every HTML file and robots.txt.

Replaces the placeholder domain (https://YOUR-DOMAIN.example) and brand (BRAND_NAME)
with the configured values. Run once when the real domain/brand are decided:

  1. Edit site.config.json: set "domain" and "brand_name".
  2. python3 scripts/apply_config.py --dry-run   # review counts
  3. python3 scripts/apply_config.py
  4. python3 scripts/build_sitemap.py && python3 scripts/validate_content.py

The script records what it replaced in site.config.json ("applied_from") so it can be re-run
from the new values if they change again.
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDER_DOMAIN = "https://YOUR-DOMAIN.example"
PLACEHOLDER_BRAND = "BRAND_NAME"


def main():
    dry = "--dry-run" in sys.argv
    cfg_path = os.path.join(ROOT, "site.config.json")
    cfg = json.load(open(cfg_path))
    prev = cfg.get("applied_from", {"domain": PLACEHOLDER_DOMAIN, "brand_name": PLACEHOLDER_BRAND})
    new_domain, new_brand = cfg["domain"].rstrip("/"), cfg["brand_name"]
    if (prev["domain"], prev["brand_name"]) == (new_domain, new_brand):
        sys.exit("Nothing to apply: site.config.json still holds the currently applied values.")
    changed = 0
    for d, _, fs in os.walk(os.path.join(ROOT, "site")):
        for f in fs:
            if not f.endswith((".html", ".txt", ".xml")):
                continue
            fp = os.path.join(d, f)
            s = open(fp, encoding="utf-8").read()
            t = s.replace(prev["domain"], new_domain).replace(prev["brand_name"], new_brand)
            if t != s:
                changed += 1
                if not dry:
                    open(fp, "w", encoding="utf-8").write(t)
    print(f"{'Would update' if dry else 'Updated'} {changed} files: {prev} -> domain={new_domain}, brand={new_brand}")
    if not dry:
        cfg["applied_from"] = {"domain": new_domain, "brand_name": new_brand}
        json.dump(cfg, open(cfg_path, "w"), indent=2)


if __name__ == "__main__":
    main()
