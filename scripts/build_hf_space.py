#!/usr/bin/env python3
"""Turn a built site/ folder into a flat static Hugging Face Space folder.

Usage: python scripts/build_hf_space.py <site_dir> <output_dir>
Flat layout (the Space upload page takes plain files): index.html, design.html, literature.html, about.html,
style.css, literature.js, papers.json, README.md (front matter: sdk static, license mit).
"""
import pathlib
import sys

README = """---
title: Physical visual attacks on AV perception (PhD research)
emoji: 🚗
colorFrom: blue
colorTo: gray
sdk: static
pinned: false
license: mit
short_description: Lightweight, explainable detection of visual attacks on AVs
---

# PhD thesis research: physical visual attacks on object detection in autonomous vehicles

Static mirror of the project website. Work in progress, literature-mapping and design phase; no experimental results yet; nothing here is peer reviewed or independently audited.

- Source, catalogs and scripts: https://github.com/ilkimaydar/phdthesisproject
- Same site on GitHub Pages: https://ilkimaydar.github.io/phdthesisproject/
"""


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    site, out = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
    out.mkdir(parents=True, exist_ok=True)
    for page in ("index.html", "design.html", "literature.html", "about.html"):
        text = (site / page).read_text(encoding="utf-8")
        text = text.replace("assets/style.css", "style.css").replace("assets/literature.js", "literature.js")
        (out / page).write_text(text, encoding="utf-8", newline="\n")
    (out / "style.css").write_text((site / "assets" / "style.css").read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    js = (site / "assets" / "literature.js").read_text(encoding="utf-8").replace("data/papers.json", "papers.json")
    (out / "literature.js").write_text(js, encoding="utf-8", newline="\n")
    (out / "papers.json").write_text((site / "data" / "papers.json").read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
    (out / "README.md").write_text(README, encoding="utf-8", newline="\n")
    print("files: " + ", ".join(f"{p.name} {p.stat().st_size}" for p in sorted(out.iterdir())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
