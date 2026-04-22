# Rosetta Brands Website - Claude Code Handoff Document

**Date:** 15 April 2026  
**Live URL:** https://feirl.github.io/rosetta-brands-website/  
**Repository:** https://github.com/feirl/rosetta-brands-website  
**Branch:** `main` (direct deploy via GitHub Pages)  
**Total commits to date:** 102

---

## 1. Project Overview

**What it is:** A multi-page static HTML marketing website for Rosetta Brands, a UK FMCG Amazon vendor partner. The site is hosted on GitHub Pages and deployed from the `main` branch root.

**Who it is for:** UK FMCG brand decision-makers considering Amazon Vendor as a growth channel. Secondary audiences include Amazon internal stakeholders, investors, and agency partners.

**What it does:** Sells Rosetta Brands' three-pillar service proposition - Vendor-as-a-Service (VaaS), Growth Marketing, and Platform - to different audience segments (existing Amazon Vendors, Sellers wanting to upgrade, brands new to Amazon, agencies, and FMCG brands organised by product category). It is a pure marketing and lead generation site. No CMS, no backend, no JavaScript framework.

**Core positioning:** "The UK's only Vendor-as-a-Service for FMCG brands on Amazon."

---

## 2. Current File Structure

```
/rosetta-brands-website/
│
├── HANDOFF.md                    ← this document
│
├── ── SOURCE TEMPLATES (not deployed directly) ──
├── _nav.html                     ← Navigation source. build.py inlines this into every page.
├── _footer.html                  ← Footer source. build.py inlines this into every page.
│
├── ── BUILD SCRIPTS ──
├── build.py                      ← Inlines _nav.html + _footer.html into all PAGES. Run before every push (automated via pre-push hook).
├── add_structured_data.py        ← Legacy script for adding JSON-LD to pages. No longer used - structured data is now hand-coded per page.
├── centralise_css.py             ← Legacy script. Not in active use.
│
├── ── JAVASCRIPT ──
├── nav-loader.js                 ← Handles: (1) FAQ accordion, (2) fade-in IntersectionObserver, (3) mega menu hover/close logic, (4) mobile hamburger, (5) active nav item highlighting. Loaded with `defer` in every page <head>. Do NOT add duplicate FAQ or fade-in scripts inline - they will conflict.
│
├── ── GLOBAL STYLESHEET ──
├── rosetta.css                   ← Global styles. Variables, reset, nav, footer, buttons, FAQ, metrics strip, cert strip, CTA section, related cards, section tags, fade-in animations. Page-specific styles are in each page's <style> block.
│
├── ── HOMEPAGE ──
├── index.html                    ← Homepage. Hero, three-pillar overview, solutions grid, stats, testimonials, FAQ.
│
├── ── SOLUTIONS - BY BRAND TYPE ──
├── amazon-vendors.html           ← Solutions for existing Amazon Vendors. Three-pillar service showcase with linked service sub-pages.
├── amazon-sellers.html           ← Solutions for Seller Central brands upgrading to Vendor. Comparison table, 5-step upgrade path.
├── new-to-amazon.html            ← Solutions for FMCG brands not yet on Amazon. Fears-vs-reality cards, full three-pillar What's Included section.
├── amazon-agencies.html          ← Solutions for Amazon agencies/consultants. Partnership model, Rosetta handles/You keep split section, non-compete promise block.
│
├── ── SOLUTIONS - BY FMCG CATEGORY ──
├── grocery-gourmet.html          ← Grocery & Gourmet. Hero brand showcase placeholder, HFSS/Subscribe & Save/case-pack focus. Pink accent.
├── beer-wine-spirits.html        ← Beer, Wine & Spirits. Compliance-heavy (licensing, age-gate, glass logistics, brand devaluation). Pink accent.
├── health-personal-care.html     ← Health & Personal Care. Claims compliance, cGMP, Subscribe & Save. Case study stats (+2430%, +706%). Pink accent.
├── pet-supplies.html             ← Pet Supplies. PIF endorsement section, pallet economics, S&S for pet food. +633% Q1 case study. Pink accent.
├── home-household.html           ← Home & Household. Low unit value economics argument, own-label competition, S&S, seasonal planning. Pink accent.
│
├── ── SERVICES - VENDOR-AS-A-SERVICE ──
├── vendor-access.html            ← VaaS: Vendor Access & Prime
├── fulfilment.html               ← VaaS: Fulfilment & Logistics
├── vendor-management-team.html   ← VaaS: Vendor Management Team
├── compliance-escalation.html    ← VaaS: Compliance & Escalation
├── international-expansion.html  ← VaaS: International Expansion
├── exclusive-amazon-programmes.html ← VaaS: Exclusive Amazon Programmes
│
├── ── SERVICES - GROWTH MARKETING ──
├── advertising.html              ← Growth Marketing: Advertising
├── brand-store.html              ← Growth Marketing: Brand Store
├── aplus-content.html            ← Growth Marketing: A+ Content
├── key-feature-images.html       ← Growth Marketing: Key Feature Images & Lifestyle
├── product-launch.html           ← Growth Marketing: Product Launch
│
├── ── SERVICES - PLATFORM ──
├── order-automation.html         ← Platform: Order Automation. Split hero layout (copy + automation pipeline visual).
├── client-portal.html            ← Platform: Client Portal. Split hero (copy + dark dashboard card).
├── listing-health.html           ← Platform: Listing Health & Optimisation. Split hero (copy + ASIN monitor table).
├── reporting-analytics.html      ← Platform: Reporting & Analytics. Split hero (copy + bar chart card).
│
├── ── UTILITY PAGES ──
├── pricing.html                  ← Pricing page. Partner Efficiencies model, success fee table, Growth Marketing pricing.
│
├── ── ASSETS ──
├── img/
│   ├── badges/                   ← Amazon certification badges (amazon-vendor-central.png, amazon-verified-partner.png, amazon-freight-badge.png)
│   ├── case-studies/             ← Case study images (if any)
│   └── logos/                    ← Brand logos (if any - most logo slots are currently placeholders)
│
└── logo-dark-2026.png            ← Dark version of Rosetta Brands logo (used in nav)
└── logo-light-2026.png           ← Light version (used in footer)
```

---

## 3. What's Been Built - Complete or Substantially Complete

### Navigation & Footer
- **`_nav.html`** - Full mega-menu with three columns: Vendor-as-a-Service (orange), Growth Marketing (pink), Platform (purple). Solutions dropdown with "Solutions For…" and "Scaling FMCG on Amazon" sections. All 26 pages are linked in the nav. Mobile hamburger menu. Scrolled shadow on scroll.
- **`_footer.html`** - Full footer with logo, brand description, Ecologi badge, social links, all nav link columns. All FMCG category pages linked.
- **`build.py`** - Inlines nav + footer into 26 pages. Run automatically via pre-push hook. Detects `id="nav-placeholder"` and `id="footer-placeholder"` divs and replaces them.
- **`nav-loader.js`** - Handles FAQ accordion (with `data-faq-init` guard against duplicate binding), fade-in IntersectionObserver, mega-menu hover, hamburger, active page highlighting.

### Homepage
- **`index.html`** - Complete. Hero, three-pillar overview, solutions grid, stats strip, testimonial, FAQ.

### Solutions Pages - By Brand Type (4 pages)
| Page | Status | Notable features |
|---|---|---|
| `amazon-vendors.html` | Complete | Three-pillar service showcase with linked sub-pages |
| `amazon-sellers.html` | Complete | Comparison table (Seller Central vs Rosetta Vendor), 5-step HIW |
| `new-to-amazon.html` | Complete | Fears-vs-reality cards, three-pillar What's Included |
| `amazon-agencies.html` | Complete | Rosetta handles / You keep split, promise block |

### Solutions Pages - FMCG Categories (5 pages, all pink accent)
| Page | Status | Notable features |
|---|---|---|
| `grocery-gourmet.html` | Complete | Hero brand showcase placeholder, image placeholder in insight box |
| `beer-wine-spirits.html` | Complete | Compliance-heavy, brand devaluation narrative, 4 logo placeholders |
| `health-personal-care.html` | Complete | Two case study stat cards (+2430%, +706%), cGMP focus |
| `pet-supplies.html` | Complete | Dedicated PIF endorsement section, pallet economics |
| `home-household.html` | Complete | Economics argument as centrepiece, no named clients |

### VaaS Service Sub-pages (6 pages, orange accent)
All complete: `vendor-access.html`, `fulfilment.html`, `vendor-management-team.html`, `compliance-escalation.html`, `international-expansion.html`, `exclusive-amazon-programmes.html`

### Growth Marketing Sub-pages (5 pages, pink accent)
All complete: `advertising.html`, `brand-store.html`, `aplus-content.html`, `key-feature-images.html`, `product-launch.html`

### Platform Sub-pages (4 pages, purple accent)
All complete: `order-automation.html`, `client-portal.html`, `listing-health.html`, `reporting-analytics.html`

### Utility
- **`pricing.html`** - Complete.

---

## 4. What's In Progress

**Nothing is actively in an incomplete or broken state.** All 26 pages build and deploy cleanly.

However, several pages contain **placeholder content** that is intentionally left for real content to be inserted:

- **Brand logo placeholders** - Every FMCG category page has `<div class="client-logo-ph">` placeholder boxes where actual client logos will go. These are styled dashed grey boxes. The category pages have 4–6 of these.
- **Hero brand showcase placeholders** - Every FMCG category page has a right-column hero image section (`<div class="hero-brand-showcase">`) with 6 placeholder logo boxes and a label. These are dashed-border placeholder squares awaiting real brand logos or a designed image.
- **Image placeholders in insight boxes** - The Grocery and Beer/Wine/Spirits pages have `<div class="insight-img-ph">` in the dark insight box, awaiting a designer image.
- **Client names removed** - All category pages use anonymous attribution ("Head of E-commerce, Speciality Food Brand") for client quotes and generic logo placeholder boxes. Actual named clients and logos will be added when confidentiality is not a concern.

---

## 5. What's Not Started Yet

### Pages Not Built
These pages are in the nav and footer as links but the HTML files do not exist:

| Page | Nav link | Notes |
|---|---|---|
| `amazon-sellers.html` → wait, this exists | - | - |
| **Garden & Outdoor** | Footer only (`#`) | In the nav as `<div class="mega-item">` (non-clickable) - Garden & Outdoor sub-category mentioned in sitemap |
| **Why Rosetta Brands** | Nav (non-functional link) | Key page covering team, credentials, Invest NI, PIF endorsement, stats. High priority. |
| **Case Studies** | Nav Resources dropdown | Individual transformation stories. No template built. |
| **Insights & Blog** | Nav Resources dropdown | SEO content engine. No template or content. |
| **FAQ** | Nav Resources dropdown | General FAQ page (different from the per-page FAQ accordions). |
| **About / Contact** | Footer only | Contact/schedule a call page. |
| **D2C Brands** | - | Mentioned in sitemap as a Solutions For page. Not in current nav. |
| **amazon-sellers.html (D2C variant)** | - | Sitemap had D2C Brands as a solutions page. |

### Nav mega-items still as `<div>` (not yet linked)
These appear in the nav as non-clickable items because no page exists yet:
- **Garden & Outdoor** (in the FMCG scaling section)
- **Why Rosetta Brands** (in the main nav - currently renders as `<li>` with no link)
- **Case Studies**, **Insights & Blog**, **FAQ** (in Resources dropdown - all `<div class="mega-item">`)

### Missing Functionality
- **Contact form / Calendly embed** - The pricing.html and all CTAs link to `pricing.html` as a stand-in for scheduling. A real contact/schedule flow is not built.
- **Google Analytics / tracking** - No analytics code in any page.
- **sitemap.xml / robots.txt** - Not created. Would help SEO.
- **Favicon** - Not set in any page `<head>`.
- **Custom domain** - Currently on GitHub Pages default URL. The site references `rosettabrands.co.uk` in canonical tags and structured data but is live at `feirl.github.io/rosetta-brands-website/`.

---

## 6. Key Decisions Made - Stay Consistent

### Accent Colour System
The three service pillars each have a dedicated accent colour, enforced per page:
- **Vendor-as-a-Service** → **Orange** (`--orange: #f17d02`, `--orange-light: #fef3e6`)
- **Growth Marketing** → **Pink** (`--pink: #e15286`, `--pink-light: #fef0f4`)
- **Platform** → **Purple** (`--purple: #7f86c1`, `--purple-light: rgba(127,134,193,0.10)`)
- **FMCG Category Pages** → **Pink** (same as Growth Marketing - they sit under the Solutions nav column)
- **Solutions By Brand Type pages** → **Orange** (they use the VaaS/orange template)

Page-level accent overrides are applied in each page's `<style>` block (not in rosetta.css), including:
- `.metric-num span { color: var(--pink); }` - overrides the global orange for metrics strip spans
- `.btn-primary { background: var(--pink) !important; }` - overrides global orange for CTA buttons
- `.faq-q:hover, .faq-q[aria-expanded="true"] { color: var(--pink) !important; }`

### Build System
Every page **must** have:
```html
<div id="nav-placeholder"></div>
<!-- ... page content ... -->
<div id="footer-placeholder"></div>
```
`build.py` replaces these with the inlined nav and footer. After build, the divs get `data-inlined="true"` attributes.

**Never add FAQ or fade-in JavaScript inline in page `<script>` tags.** `nav-loader.js` handles both globally, with a `data-faq-init` guard to prevent double-binding. This bug was fixed on the Solutions pages - adding inline scripts on new pages will reintroduce it.

### Naming Conventions
- **Filenames:** kebab-case, no underscores (e.g. `home-household.html`, `beer-wine-spirits.html`)
- **FMCG category pages:** Always include the full category name in the `<title>` tag with "Amazon UK" and "Rosetta Brands" for SEO
- **Section tags:** Use `.section-tag.orange`, `.section-tag.pink`, or `.section-tag.purple` for the pill labels above section headings - these are defined in rosetta.css
- **Breadcrumbs on VaaS/GM/Platform pages:** `Services > [Pillar]` format (e.g. "Services > Platform") with pill showing the current page name
- **Breadcrumbs on FMCG category pages:** `Scaling FMCG on Amazon > [Category]` in the hero-b-label

### Copy Rules (enforced from the Beer, Wine & Spirits page onwards)
1. **Always "Rosetta Brands"** - never just "Rosetta". Use `sed -i "s/Rosetta's/Rosetta Brands'/g"` etc. if batch-fixing.
2. **No em dashes** - Replace ` - ` with `, ` or restructure the sentence. Remove `-` and ` - ` characters.
3. **No artificial line breaks in headings** - No `<br>` inside `<h1>` or `<h2>` tags.
4. **FAQ tone** - Questions should sound like a real person asking, not a content checklist (e.g. "Our products are heavy. Does Vendor fix that?" not "How does Rosetta handle heavy product fulfilment?")
5. **Client confidentiality** - No named clients in FMCG category pages. Use generic attribution: "Commercial Director, UK FMCG Brand". Logo slots are placeholder `<div>` boxes.

### Hero Layout Patterns
- **Solutions by brand type** (amazon-vendors, amazon-sellers etc.) → centred `page-hero-b` template with `hero-b-inner`, `hero-b-stats` strip at bottom
- **FMCG category pages** → two-column `hero-cat-layout` grid (copy left, brand showcase placeholder right), stats strip below the grid
- **Platform sub-pages** (order-automation etc.) → two-column grid with dark card/visual on the right (specific to each page)
- **VaaS/GM sub-pages** → centred hero with left-aligned layout (varies by page)

### Related Cards in Platform Pages
All Platform sub-pages cross-link to each other. All four Platform pages are now live with working `<a href>` links (no more "coming soon" cards in the Platform section). If you add a fifth Platform page, update the related cards on the other four.

### The Pre-Push Hook
`.git/hooks/pre-push` runs `build.py` automatically before every push and stages the built HTML files. When adding a new page:
1. Add it to `PAGES` list in `build.py`
2. Add it to the `git add` line in `.git/hooks/pre-push`
3. Add the nav mega-item link in `_nav.html`
4. Add the footer link in `_footer.html`
5. Run `python3 build.py` and push

---

## 7. Known Issues / Tech Debt

### Minor Bugs / Inconsistencies
1. **`add_structured_data.py` and `centralise_css.py`** - Legacy scripts from early development. Not harmful, just clutter. Can be deleted.
2. **`grocery-gourmet.html` still has one `orange-bg` class** reference in the nav HTML section (the mega-item icon for the Solutions dropdown). This is correct - it is the nav's VaaS column styling, not a page-level error.
3. **The pre-push hook `git add` list has `grocery-gourmet.html` duplicated** (appears twice). Not breaking - git add of the same file twice is harmless - but should be cleaned up.
4. **CTA buttons throughout** - Most pages use `pricing.html` as the href for both "Get a Free Review" and "Schedule a Call". These should eventually point to a proper contact/booking page. This is a known placeholder.
5. **`amazon-sellers.html` and other Solutions pages** - The "Scaling FMCG" section cards in their related grids still link to `amazon-vendors.html` as a fallback for categories not yet built (Garden & Outdoor etc.). Update these when those pages are built.
6. **The `index.html` and older pages** may still have standalone `Rosetta` references (not "Rosetta Brands"). The batch replacement was only applied to the Grocery and subsequent category pages. A global find-and-replace pass across all pages would be worthwhile.
7. **Em dashes** - Same as above. The ` - ` removal was applied to the FMCG category pages but may persist in older pages (VaaS sub-pages, Growth Marketing sub-pages, etc.).

### Structural Tech Debt
1. **No component reuse** - Every page duplicates the CSS for its accent colour, hero layout, challenge cards, approach features etc. This was intentional (static site, no build tool), but means any design change requires updating multiple files.
2. **Inline CSS in some pages** - Some sections use inline `style=""` attributes (particularly in the Opportunity section dark panels) rather than named classes. These work but are harder to maintain.
3. **All pages fully self-contained after build** - After `build.py` runs, every page contains the full nav and footer HTML inlined. This means the deployed files are large (85–120KB each) but have zero network fetches for nav/footer.

---

## 8. Exact Next Steps - Priority Order

### Immediate (next Claude Code session)

1. **Build `why-rosetta-brands.html`** - This is the most strategically important unbuilt page. It should cover: Top 20 vendor account credential, team (Nick Comer, Sophie Smith), Invest NI, Pet Industry Federation, 958+ brands / £100M+ / 100+ Best Sellers stats, the five reasons to choose Rosetta Brands. Uses orange accent (it's a core brand page). Nav item is currently non-functional.

2. **Build a contact/scheduling page** - Currently all CTAs link to `pricing.html`. A proper contact page with Calendly embed or equivalent is needed. Suggested URL: `contact.html`. Update all CTA hrefs across the site once built.

3. **Fix the duplicate `grocery-gourmet.html` in pre-push hook** - One-line fix in `.git/hooks/pre-push`.

4. **Global "Rosetta" → "Rosetta Brands" pass** - Run across all VaaS sub-pages and Growth Marketing pages (built before the convention was established). Use: `for f in vendor-access.html fulfilment.html vendor-management-team.html compliance-escalation.html international-expansion.html exclusive-amazon-programmes.html advertising.html brand-store.html aplus-content.html key-feature-images.html product-launch.html index.html pricing.html amazon-vendors.html amazon-sellers.html new-to-amazon.html amazon-agencies.html; do sed -i "s/Rosetta's/Rosetta Brands'/g; s/Rosetta Brands/RBPH/g; s/Rosetta/Rosetta Brands/g; s/RBPH/Rosetta Brands/g" $f; done` - then rebuild.

5. **Em dash removal pass** - Same set of older pages. Use `sed -i 's/ - /, /g'` and check results manually.

6. **Add favicon** - Add `<link rel="icon" ...>` to every page. Add to `_nav.html` in the `<head>` section... wait, nav is inlined into body. Add favicon to each page's `<head>` directly or create a consistent favicon snippet.

7. **sitemap.xml** - Create a basic XML sitemap listing all 26+ pages. Helps SEO once the domain is set up.

### Medium Priority

8. **`garden-outdoor.html`** - The sixth FMCG category page. Nav slot exists as a non-clickable `<div>`. Same pink accent template as other category pages.

9. **Case Studies section** - Build at least 2–3 individual case study pages using the anonymised data from the case study PDFs in the Rosetta folder. The brand stories (Health & Beauty +2430%, Health Food +361%, Pet Supplement +633%, Water Brand +388%, Seller-to-Vendor protein bar +550% S&S) are all available as PDFs.

10. **Replace CTA button hrefs** - Once `contact.html` is built, do a global find-and-replace of `href="pricing.html"` in CTA button elements to the correct scheduling/contact URL.

### Lower Priority

11. **Custom domain setup** - Point `rosettabrands.co.uk` to GitHub Pages. Update canonical tags and structured data URLs throughout (currently they reference `rosettabrands.co.uk` but live at `feirl.github.io/rosetta-brands-website/`).
12. **Google Analytics** - Add GA4 tag to all pages via `_nav.html` (it gets inlined everywhere).
13. **Garden & Outdoor** - Lower priority than other FMCG pages; less client evidence available.
14. **FAQ page** - A dedicated global FAQ page (`faq.html`). Some pages reference `faq.html` in their FAQ subtitles already.

---

## 9. How to Run the Project Locally

### Prerequisites
- Python 3 (any recent version - used to run `build.py`)
- Git
- A local HTTP server (optional but recommended for testing nav-loader.js in non-inlined mode)

### Setup
```bash
# Clone the repo
git clone https://github.com/feirl/rosetta-brands-website.git
cd rosetta-brands-website

# Verify the pre-push hook is executable
ls -la .git/hooks/pre-push
# Should show -rwxr-xr-x. If not: chmod +x .git/hooks/pre-push
```

### Making Changes and Deploying
```bash
# 1. Edit source files (_nav.html, _footer.html, any .html page)

# 2. Run build to inline nav + footer into all pages
python3 build.py

# 3. Stage your changed files (build.py re-stages built files automatically on push)
git add your-changed-file.html

# 4. Commit
git commit -m "feat: description of change"

# 5. Push - the pre-push hook runs build.py again automatically and stages all built HTML
git push origin main
```

### Adding a New Page
```bash
# 1. Create the page file with nav and footer placeholders:
#    <div id="nav-placeholder"></div>
#    ... page content ...
#    <div id="footer-placeholder"></div>

# 2. Add to build.py PAGES list:
#    'your-new-page.html',

# 3. Add to pre-push hook git add line:
#    your-new-page.html \

# 4. Add <a href="your-new-page.html"> in _nav.html (replacing <div class="mega-item">)

# 5. Add <a href="your-new-page.html"> in _footer.html

# 6. Run build.py and push
python3 build.py && git add your-new-page.html _nav.html _footer.html build.py && git commit -m "feat: add page" && git push origin main
```

### Viewing Locally
Open any `.html` file directly in a browser - nav and footer are inlined so the pages are self-contained. If you want to test the fetch-based fallback mode (for nav/footer before build.py runs), serve with:
```bash
python3 -m http.server 8000
# Then open http://localhost:8000
```

### Key Files to Know
| File | What it controls |
|---|---|
| `rosetta.css` | All global styles. Edit here for sitewide changes. |
| `_nav.html` | Navigation HTML + all nav CSS. Changes here apply everywhere after next build. |
| `_footer.html` | Footer HTML. Same - changes apply everywhere after next build. |
| `build.py` | Inlining script. Add new pages to `PAGES` list here. |
| `nav-loader.js` | FAQ accordion, fade-in, mega menu, hamburger. Never duplicate this logic in pages. |
| `.git/hooks/pre-push` | Auto-runs build before every push. Add new pages to `git add` line here. |

---

## Appendix: Full Page Inventory

| File | Section | Accent | Status |
|---|---|---|---|
| `index.html` | Homepage | Orange | ✅ Complete |
| `pricing.html` | Utility | Orange | ✅ Complete |
| `amazon-vendors.html` | Solutions / Brand Type | Orange | ✅ Complete |
| `amazon-sellers.html` | Solutions / Brand Type | Orange | ✅ Complete |
| `new-to-amazon.html` | Solutions / Brand Type | Orange | ✅ Complete |
| `amazon-agencies.html` | Solutions / Brand Type | Orange | ✅ Complete |
| `grocery-gourmet.html` | Solutions / FMCG | Pink | ✅ Complete |
| `beer-wine-spirits.html` | Solutions / FMCG | Pink | ✅ Complete |
| `health-personal-care.html` | Solutions / FMCG | Pink | ✅ Complete |
| `pet-supplies.html` | Solutions / FMCG | Pink | ✅ Complete |
| `home-household.html` | Solutions / FMCG | Pink | ✅ Complete |
| `vendor-access.html` | VaaS | Orange | ✅ Complete |
| `fulfilment.html` | VaaS | Orange | ✅ Complete |
| `vendor-management-team.html` | VaaS | Orange | ✅ Complete |
| `compliance-escalation.html` | VaaS | Orange | ✅ Complete |
| `international-expansion.html` | VaaS | Orange | ✅ Complete |
| `exclusive-amazon-programmes.html` | VaaS | Orange | ✅ Complete |
| `advertising.html` | Growth Marketing | Pink | ✅ Complete |
| `brand-store.html` | Growth Marketing | Pink | ✅ Complete |
| `aplus-content.html` | Growth Marketing | Pink | ✅ Complete |
| `key-feature-images.html` | Growth Marketing | Pink | ✅ Complete |
| `product-launch.html` | Growth Marketing | Pink | ✅ Complete |
| `order-automation.html` | Platform | Purple | ✅ Complete |
| `client-portal.html` | Platform | Purple | ✅ Complete |
| `listing-health.html` | Platform | Purple | ✅ Complete |
| `reporting-analytics.html` | Platform | Purple | ✅ Complete |
| `why-rosetta-brands.html` | Core Brand | Orange | ❌ Not built |
| `contact.html` | Utility | Orange | ❌ Not built |
| `garden-outdoor.html` | Solutions / FMCG | Pink | ❌ Not built |
| `faq.html` | Resources | Orange | ❌ Not built |
| Case study pages | Resources | Orange | ❌ Not built |
| Blog/Insights pages | Resources | Orange | ❌ Not built |
