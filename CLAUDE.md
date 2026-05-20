# Rosetta Brands Website

## What this project is
Static HTML website for Rosetta Brands (www.rosettabrands.com) — the UK's only Vendor-as-a-Service for FMCG brands on Amazon. Deployed on Vercel. No framework, no build tool except `build.py`.

Read `llms.txt` for a full map of every page on the site.

---

## Branching workflow

| Branch | Owner | Purpose |
|--------|-------|---------|
| `main` | **Production — www.rosettabrands.com** | Only push here after Brendan has reviewed the preview |
| `brendan` | Brendan | Brendan's preview branch |
| `sophie` | Sophie | Sophie's preview branch |

**Before starting any session**, sync with main first:
```
Fetch the latest from GitHub, switch to the [brendan/sophie] branch, and merge in the latest main before we start
```

### Deployment flow — every change, every time

1. Make changes (describe what you want to Claude)
2. **Push to the preview branch** (brendan or sophie)
3. **Review the preview URL before doing anything else:**
   - Brendan: `https://rosetta-brands-website-git-brendan-feirls-projects.vercel.app`
   - Sophie: `https://rosetta-brands-website-git-sophie-feirls-projects.vercel.app`
4. **Claude must always ask:** *"Please review the preview. Would you like to push this to main (production)?"*
5. Only push to main after receiving explicit confirmation

**Pushing to main = going live on www.rosettabrands.com immediately. Always confirm before doing this.**

### Sophie's workflow

Sophie works via the **Claude Code desktop app**. On a new machine, she needs to clone the repo first:
```
git clone https://feirl:PAT@github.com/feirl/rosetta-brands-website.git
```
Then open that folder in Claude Code. Ask Brendan for the PAT. Sophie pushes to her `sophie` branch, shares the preview URL with Brendan, and only pushes to `main` after Brendan confirms.

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
5. **Push workflow** — ALWAYS push to the preview branch first, share the preview URL, and explicitly ask Brendan "Would you like to push this to main (production)?" before pushing to main. Never push to main without this confirmation.

---

## Key files

| File | What it does |
|------|-------------|
| `index.html` | Homepage |
| `rosetta.css` | All shared CSS variables, typography, components |
| `build.py` | Pre-push build script — run this before every push |
| `llms.txt` | Structured site map with page descriptions for AI crawlers |
| `llms-full.txt` | Comprehensive single-document reference for AI crawlers |
| `pricing.md` | Machine-readable pricing model |
| `agents.md` | Agent discovery file — capabilities and resource URLs |
| `.well-known/agent-card.json` | A2A agent card |
| `vercel.json` | Clean URLs, redirects, cache headers, security headers |
| `cookie-consent.js` | GDPR cookie consent manager |
| `sitemap.xml` | Search engine sitemap (44 pages, www.rosettabrands.com) |

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
- **Live site** — www.rosettabrands.com
- **Vercel project** — rosetta-brands-website (Rosetta Brands team)
- **GitHub repo** — github.com/feirl/rosetta-brands-website
