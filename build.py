#!/usr/bin/env python3
"""
Build script for the music theory catalog site.

What it does:
  1. Reads every markdown file in content/entries/
  2. Parses the front matter (composer, piece, tags, ...)
  3. Renders a page for each entry (this is the "piece" page)
  4. Automatically groups entries by composer -> generates composer pages
  5. Automatically groups entries by tag -> generates tag pages
  6. Renders an index page, a tag directory, and a composer directory
  7. Copies static/ (css, images you add) into the output folder

You never hand-edit tag or composer pages. Add/edit a file in
content/entries/, push, and everything downstream regenerates.

Run locally with:  python build.py
Output goes to:     _site/
"""

import shutil
from pathlib import Path
from datetime import datetime

import frontmatter
import markdown as md
import yaml
from jinja2 import Environment, FileSystemLoader
from slugify import slugify

ROOT = Path(__file__).parent
CONTENT_DIR = ROOT / "content" / "entries"
STATIC_DIR = ROOT / "static"
TEMPLATES_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "_site"
CONFIG_PATH = ROOT / "site_config.yml"

with open(CONFIG_PATH, encoding="utf-8") as f:
    SITE = yaml.safe_load(f)

BASE_URL = SITE.get("base_url", "/")
if not BASE_URL.endswith("/"):
    BASE_URL += "/"

env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
env.globals["site"] = SITE


def relurl(path: str) -> str:
    """Prefix a site-root-relative path with the configured base_url,
    e.g. '/tags/' -> '/my-repo/tags/' when publishing under a repo subpath."""
    return BASE_URL.rstrip("/") + path if path != "/" else BASE_URL


env.filters["relurl"] = relurl


def load_entries():
    """Read every markdown file in content/entries and return a list of dicts."""
    entries = []
    for path in sorted(CONTENT_DIR.glob("*.md")):
        post = frontmatter.load(path)

        composer = post.get("composer")
        piece = post.get("piece")
        tags = post.get("tags") or []

        if not composer or not piece:
            print(f"  ! skipping {path.name}: missing 'composer' or 'piece' in front matter")
            continue

        # normalize tags to a clean list of strings
        tags = [str(t).strip() for t in tags if str(t).strip()]

        slug = post.get("slug") or slugify(path.stem)
        html_body = md.markdown(
            post.content,
            extensions=["extra", "sane_lists", "toc"],
        )

        entries.append(
            {
                "slug": slug,
                "composer": composer,
                "composer_slug": slugify(composer),
                "piece": piece,
                "tags": tags,
                "tag_slugs": [slugify(t) for t in tags],
                "key": post.get("key"),
                "year": post.get("year"),
                "form": post.get("form"),
                "date_added": post.get("date_added"),
                "body": html_body,
                "source_file": path.name,
            }
        )
    return entries


def group_by(entries, field, slug_field):
    """Group entries by a field, returning {name: {"slug": ..., "entries": [...]}}."""
    groups = {}
    for e in entries:
        name = e[field]
        slug = e[slug_field] if isinstance(e[slug_field], str) else e[slug_field]
        if name not in groups:
            groups[name] = {"name": name, "slug": e[slug_field], "entries": []}
        groups[name]["entries"].append(e)
    return groups


def group_by_tags(entries):
    tags = {}
    for e in entries:
        for tag, tag_slug in zip(e["tags"], e["tag_slugs"]):
            if tag not in tags:
                tags[tag] = {"name": tag, "slug": tag_slug, "entries": []}
            tags[tag]["entries"].append(e)
    return tags


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build():
    print("Loading entries...")
    entries = load_entries()
    print(f"  found {len(entries)} entr{'y' if len(entries) == 1 else 'ies'}")

    composers = group_by(entries, "composer", "composer_slug")
    tags = group_by_tags(entries)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # sort helpers
    entries_sorted = sorted(entries, key=lambda e: (e["composer"], e["piece"]))
    composer_list = sorted(composers.values(), key=lambda c: c["name"])
    tag_list = sorted(tags.values(), key=lambda t: t["name"])

    # --- homepage ---
    tmpl = env.get_template("index.html")
    write(
        OUTPUT_DIR / "index.html",
        tmpl.render(
            entries=entries_sorted,
            composers=composer_list,
            tags=tag_list,
            built_at=datetime.now().strftime("%Y-%m-%d"),
        ),
    )

    # --- one page per entry (the "piece" page) ---
    tmpl = env.get_template("entry.html")
    for e in entries:
        write(
            OUTPUT_DIR / "entries" / e["slug"] / "index.html",
            tmpl.render(entry=e),
        )

    # --- composer directory + one page per composer ---
    tmpl_list = env.get_template("list.html")
    write(
        OUTPUT_DIR / "composers" / "index.html",
        tmpl_list.render(
            title="Composers",
            kind="composer",
            items=composer_list,
        ),
    )
    tmpl_composer = env.get_template("composer.html")
    for c in composer_list:
        c_entries = sorted(c["entries"], key=lambda e: e["piece"])
        write(
            OUTPUT_DIR / "composers" / c["slug"] / "index.html",
            tmpl_composer.render(composer=c["name"], entries=c_entries),
        )

    # --- tag directory + one page per tag ---
    write(
        OUTPUT_DIR / "tags" / "index.html",
        tmpl_list.render(
            title="Tags",
            kind="tag",
            items=tag_list,
        ),
    )
    tmpl_tag = env.get_template("tag.html")
    for t in tag_list:
        t_entries = sorted(t["entries"], key=lambda e: (e["composer"], e["piece"]))
        write(
            OUTPUT_DIR / "tags" / t["slug"] / "index.html",
            tmpl_tag.render(tag=t["name"], entries=t_entries),
        )

    # --- static assets (css, any images you drop in static/) ---
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, OUTPUT_DIR / "static", dirs_exist_ok=True)

    # GitHub Pages: tell it not to run its own Jekyll processing over our output
    write(OUTPUT_DIR / ".nojekyll", "")

    print(f"Built {len(entries)} entries, {len(composer_list)} composers, {len(tag_list)} tags -> {OUTPUT_DIR}")


if __name__ == "__main__":
    build()
