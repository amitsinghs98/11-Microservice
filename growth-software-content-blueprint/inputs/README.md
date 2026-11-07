# Inputs

Put the source strategy document at `inputs/content-strategy.docx`.

- It is the source of truth for the 100-article topical map.
- It is **not committed**. `.gitignore` excludes `*.docx`.
- To regenerate the manifest after updating it:

```bash
python3 scripts/extract_source_map.py
python3 scripts/build_manifest.py
```

Pandoc must be installed for extraction.
