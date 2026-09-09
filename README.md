# The Analysis Index

A static music-theory catalog. You write markdown files; a build
script sorts them by composer and by theory tag automatically.

## How it works

- Every piece is one file in `content/entries/`.
- Each file starts with a small YAML header (front matter) and then
  your normal markdown analysis below it.
- When you push to GitHub, a GitHub Action runs `build.py`, which:
  - turns each entry into its own page (`/entries/<slug>/`)
  - regenerates a page for every composer (`/composers/<name>/`)
  - regenerates a page for every tag (`/tags/<name>/`)
  - regenerates the homepage
- You never hand-write composer pages or tag pages — they're always
  derived from the entries. Add a new tag to an entry's front matter
  and its tag page appears automatically on the next push.

## Adding an entry

Create a new file in `content/entries/`, e.g.
`content/entries/schubert-erlkonig.md`:

```markdown
---
composer: Franz Schubert
piece: "Erlkönig, D. 328"
key: G minor
year: 1815
form: Through-composed
tags:
  - word painting
  - diminished seventh
  - through-composed
---

Write your analysis here in normal markdown. Headings, lists, images,
and blockquotes all work.
```

Front matter fields:

| field   | required? | notes                                              |
|---------|-----------|-----------------------------------------------------|
| composer| yes       | exact name you want displayed and grouped on        |
| piece   | yes       | display title of the piece                          |
| tags    | no        | a YAML list; each one becomes/joins a tag page       |
| key     | no        | shown in the meta line on the entry page             |
| year    | no        | shown in the meta line                               |
| form    | no        | shown in the meta line (e.g. "Sonata form", "Rondo") |
| slug    | no        | overrides the auto-generated URL slug for this entry |

The filename itself becomes the page's URL slug unless you set `slug`
explicitly, so name files descriptively
(`beethoven-sonata-op13-mvt1.md` → `/entries/beethoven-sonata-op13-mvt1/`).

**Tag names and composer names are matched by exact text**, so keep
spelling/capitalization consistent across entries (e.g. always
`mode mixture`, not sometimes `Mode Mixture`).

## Running it locally (optional)

You don't have to — GitHub Actions builds it for you on every push.
But if you want to preview locally before pushing:

```bash
pip install -r requirements.txt
python build.py
python -m http.server --directory _site 8000
```

Then open http://localhost:8000

## One-time setup on GitHub

1. Create a new GitHub repository and push this folder to it.
2. In the repo, go to **Settings → Pages**.
3. Under **Build and deployment → Source**, choose **GitHub Actions**.
   (You do *not* need to select a branch/folder — the included
   workflow at `.github/workflows/deploy.yml` handles building and
   deploying automatically on every push to `main`.)
4. If you're publishing at `https://<your-username>.github.io/<repo-name>/`
   (i.e. not a repo literally named `<your-username>.github.io`),
   open `site_config.yml` and set:
   ```yaml
   base_url: "/<repo-name>/"
   ```
   so internal links resolve correctly. If you're using a custom
   domain or the special `<username>.github.io` repo, leave it as `/`.
5. Push. Check the **Actions** tab for build progress; the site goes
   live at the URL shown in **Settings → Pages** a minute or two later.

## Adding images to an entry

Drop image files anywhere under `static/` (e.g.
`static/images/erlkonig-mm1-4.png`) and reference them in your
markdown with a path starting at `/static/...`:

```markdown
![First four measures](/static/images/erlkonig-mm1-4.png)
```

(If you set a non-root `base_url`, use the `site.base_url` prefix, or
just write the path relative to `/static/` as above — the build script
doesn't rewrite image paths inside your markdown, only the site's own
navigation links, so keep this in mind if you publish under a
subpath.)

## Project layout

```
content/entries/     ← you edit these (one file per piece)
site_config.yml       ← site title, description, base_url
templates/             ← Jinja2 HTML templates (edit to restyle)
static/style.css       ← the stylesheet
build.py                ← the generator — reads content/, writes _site/
.github/workflows/      ← the GitHub Action that builds + deploys
```
