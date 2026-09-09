# Music Theory Examples

## File Organization

```text
/
├── _config.yml
├── index.md
│
├── _data/
│   ├── entries.yml   ← the ONLY file you edit day-to-day
│   ├── songs.yml     ← auto-generated
│   └── theory.yml    ← auto-generated
│
├── scripts/
│   └── generate.py   ← builds songs.yml + theory.yml from entries.yml
│
├── .github/workflows/
│   └── generate.yml  ← runs generate.py automatically on push
│
├── examples/
│   ├── shes-always-a-woman.md
│   └── ...
│
└── assets/
    └── css/
        └── main.scss
```

### Files

* **`_data/entries.yml`** — the single source of truth. One entry per song, listing every theory topic (and nested subcategory) it demonstrates.
* **`_data/songs.yml`** — auto-generated master list of songs. Don't hand-edit.
* **`_data/theory.yml`** — auto-generated theory categories (with nested subcategories) and which songs belong to them. Don't hand-edit.
* **`scripts/generate.py`** — regenerates `songs.yml`/`theory.yml` from `entries.yml`.
* **`examples/`** — individual pages containing detailed analysis.
* **`index.md`** — automatically displays the theory categories, subcategories, and examples.
* **`assets/css/main.scss`** — custom styling.
* **`_config.yml`** — Jekyll/Moonwalk configuration.

---

# Adding an Example

## 1. Add one entry to `_data/entries.yml`

This is the only file you need to type into. List the song once, with **every** topic it touches — including nested subcategories where useful (e.g. `Secondary Dominants` / `V/vi`):

```yaml
- id: shes-always-a-woman
  composer: Billy Joel
  title: "She's Always a Woman"
  page: /examples/shes-always-a-woman.html
  topics:
    - category: Mode Mixture
      techniques:
        - "I → i"
    - category: Secondary Dominants
      subcategory: "V/vi"
      techniques:
        - "V7/vi"
    - category: Sequences
      subcategory: "Descending Fifths"
      techniques:
        - "D5"
```

`subcategory` is optional — leave it out for categories that don't need nesting. You can repeat the same `category` with different `subcategory` values (e.g. `V/vi` and `V/ii`) and they'll both land under one "Secondary Dominants" heading, nested underneath it.

## 2. Create the song's example page

Create a Markdown file in `examples/`, e.g. `examples/shes-always-a-woman.md`. This is where the detailed analysis goes (unchanged from before).

## 3. Let the categorization happen automatically

Once `entries.yml` is committed/pushed, a GitHub Action regenerates `_data/songs.yml` and `_data/theory.yml` for you and commits them — that's the "sorted into all categories automatically" part. You don't touch either file by hand.

If you'd rather see the result immediately on your own machine before pushing (or you're working offline), run:

```bash
pip install -r requirements.txt
python3 scripts/generate.py
```

That regenerates both files locally so you can preview the site before committing.

---

# Adding Another Example to an Existing Song

Find that song's existing entry in `entries.yml` and add another item to its `topics` list — no need to repeat composer/title/page, and no need to touch `theory.yml` at all.

---

# Adding a Brand New Song

Add one new entry (with `id`, `composer`, `title`, `page`, and `topics`) to the bottom of `entries.yml`, then create its `examples/<id>.md` page. That's it — one file to type into instead of three.

---

## The Basic Principle

**`entries.yml` = What is the song, and what does it demonstrate?** (you write this)

**`songs.yml` + `theory.yml` = the same information, re-sorted for the site** (the script writes this)

**`examples/` = What's the detailed analysis?** (you still write this)
