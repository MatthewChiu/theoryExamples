# Music Theory Examples

## File Organization

```text
/
├── _config.yml
├── index.md
│
├── _data/
│   ├── songs.yml
│   └── theory.yml
│
├── examples/
│   ├── shes-always-a-woman.md
│   └── ...
│
└── assets/
    └── css/
        └── custom.scss
```

### Files

* **`_data/songs.yml`** — master list of songs, with composer, title, and page
* **`_data/theory.yml`** — theory categories and which songs/examples belong to them
* **`examples/`** — individual pages containing detailed analysis
* **`index.md`** — automatically displays the theory categories and examples
* **`assets/css/custom.scss`** — custom styling
* **`_config.yml`** — Jekyll/Moonwalk configuration

---

# Adding an Example

## 1. Add the song to `songs.yml`

If the song isn't already there, add it to:

```text
_data/songs.yml
```

Give the song a unique ID:

```yaml
shes-always-a-woman:
  composer: Billy Joel
  title: "She's Always a Woman"
  page: /examples/shes-always-a-woman/
```

The **ID** (`shes-always-a-woman`) is what you'll use everywhere else to refer to the song.

---

## 2. Create the song's example page

Create a Markdown file in:

```text
examples/
```

For example:

```text
examples/shes-always-a-woman.md
```

This is where the detailed analysis goes.

---

## 3. Add the example to `theory.yml`

Open:

```text
_data/theory.yml
```

Add the appropriate theory category:

```yaml
- category: MODE MIXTURE
  examples:
    - song: shes-always-a-woman
      techniques:
        - "I → i"
        - "D5"
```

If the same song demonstrates another concept, add it separately:

```yaml
- category: SECONDARY DOMINANTS
  examples:
    - song: shes-always-a-woman
      techniques:
        - "V7/vi"
```

The song information is **not repeated** here. Just use the song's ID.

---

# Adding a New Song

For a completely new song:

1. Add the song to `_data/songs.yml`
2. Create its page in `examples/`
3. Add its theory examples to `_data/theory.yml`

For example:

```text
_data/songs.yml
    ↓
examples/new-song.md
    ↓
_data/theory.yml
```

---

# Adding Another Example to an Existing Song

You **do not** need to add the song to `songs.yml` again.

Just reference its existing ID in `theory.yml`:

```yaml
- category: CHROMATIC MEDIANTS
  examples:
    - song: shes-always-a-woman
      techniques:
        - "I → ♭VI"
```

---

# Quick Workflow

### New song

**1.** `songs.yml` → add song
**2.** `examples/` → create song page
**3.** `theory.yml` → add theory examples

### Existing song

**1.** `theory.yml` → add the new theory category/example
**2.** Edit the song's page in `examples/` if detailed analysis is needed

---

## The Basic Principle

**`songs.yml` = What is the song?**

**`theory.yml` = Why is the song here?**

**`examples/` = What's the detailed analysis?**
