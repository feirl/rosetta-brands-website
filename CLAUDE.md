# Rosetta Brands Website

## What this project is
Static HTML website for Rosetta Brands (rosettabrands.co.uk) — the UK's only Vendor-as-a-Service for FMCG brands on Amazon. Deployed on Vercel. No framework, no build tool except `build.py`.

Read `llms.txt` for a full map of every page on the site.

---

## Branching workflow

| Branch | Owner | Purpose |
|--------|-------|---------|
| `main` | Live site | Never push directly — only merge via pull request |
| `brendan` | Brendan | Brendan's working branch |
| `sophie` | Sophie | Sophie's working branch |

**Before starting any session**, make sure you're on the right branch:
```
git checkout sophie   # or brendan
git pull origin main  # get latest changes
```

**When changes are ready to go live:**
```
Run build.py, then open a pull request to main
```
Claude will handle the PR. Brendan reviews and merges it. Vercel deploys automatically.

---

## How the site is built

- All pages are plain `.html` files at the root
- `rosetta.css` — global stylesheet (all shared styles live here)
- `_nav.html` — navigation source fragment
- `_footer.html` — footer source fragment (includes cookie consent)
- `build.py` — inlines `_nav.html` and `_footer.html` into every page before push

**Always run `build.py` before committing and pushing:**
```
python3 build.py
```
This also checks for em dashes and will warn you if any are found.

---

## House rules

1. **No em dashes** (`—` or `&mdash;`). Use ` - ` or `:` instead. build.py will catch them.
2. **Edit `_nav.html` and `_footer.html`** for nav/footer changes — not the individual page files. Then run build.py.
3. **Images** go in `img/`. Pillar graphics are in `img/pillars/`.
4. **Clean URLs** — no `.html` in any internal links. `/contact` not `/contact.html`.
5. **Never push to `main` directly** — always open a pull request.

---

## Key files

| File | What it does |
|------|-------------|
| `index.html` | Homepage |
| `rosetta.css` | All shared CSS variables, typography, components |
| `build.py` | Pre-push build script — run this before every push |
| `llms.txt` | Full site map (37 pages) — read this first |
| `vercel.json` | Clean URLs, cache headers, security headers |
| `cookie-consent.js` | GDPR cookie consent manager |
| `sitemap.xml` | Search engine sitemap |

---

## Colours & brand

| Token | Hex | Use |
|-------|-----|-----|
| `--orange` | `#E8440A` | Primary CTA, accents |
| `--charcoal` | `#2D2933` | Headings, dark backgrounds |
| `--pink` | `#E8468A` | Growth Marketing accent |
| `--purple` | `#7C6BE8` | Platform accent |

---

## Pushing to GitHub

No SSH or credential helper is installed. Use a PAT:
```
git push https://USERNAME:PAT@github.com/feirl/rosetta-brands-website.git BRANCH
```
Ask Brendan for a PAT if you don't have one.

---

## Contacts

- **Brendan Hughes** — project lead, reviews and merges PRs
- **Sophie Smith** — Commercial Director, content and copy
- **Live site** — rosettabrands.co.uk
- **Vercel project** — rosetta-brands-website (Rosetta Brands team)
- **GitHub repo** — github.com/feirl/rosetta-brands-website
