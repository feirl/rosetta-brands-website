#!/usr/bin/env python3
"""
build.py  —  Rosetta Brands static build script

Run before every git push:
  python3 build.py

What it does:
  1. Reads _nav.html and _footer.html (the source-of-truth fragments)
  2. For each HTML page, inlines them directly into #nav-placeholder and
     #footer-placeholder — eliminating the two fetch() network requests
     that nav-loader.js would otherwise make on every page load.
  3. Marks the inlined HTML with data-inlined="true" so nav-loader.js
     knows to skip fetching and jump straight to initNav().
  4. Adds a <link rel="preload"> hint for rosetta.css.
  5. Reports what was done.

Source files (with placeholders) are untouched — build.py edits in-place
but git diff will show the inlined content, which is intentional.
Revert with: git checkout -- *.html
"""

import re
import os


def replace_placeholder_div(html, div_id, replacement):
    """
    Find <div id="div_id" ...> and replace the *entire* element (including all
    nested children) with `replacement`.  Uses depth-counting so nested <div>s
    inside the placeholder don't confuse the match — unlike a lazy regex.
    """
    # Locate the opening tag
    m = re.search(r'<div\s+id="' + re.escape(div_id) + r'"[^>]*>', html)
    if not m:
        return html          # placeholder not found — nothing to do

    start = m.start()
    pos   = m.end()
    depth = 1

    while pos < len(html) and depth > 0:
        next_open  = html.find('<div',  pos)
        next_close = html.find('</div>', pos)

        if next_close == -1:
            break            # malformed HTML — bail out

        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4   # skip past '<div'
        else:
            depth -= 1
            end = next_close + 6  # len('</div>') = 6
            pos = end

    return html[:start] + replacement + html[end:]

PAGES = [
    'index.html',
    'amazon-vendors.html',
    'fulfilment.html',
    'pricing.html',
    'vendor-access.html',
    'vendor-management-team.html',
    'compliance-escalation.html',
    'international-expansion.html',
    'exclusive-amazon-programmes.html',
]

def strip_style_tags(fragment):
    """Remove <style>...</style> blocks from a fragment.
    Nav CSS travels via rosetta.css on each page; we don't want it duplicated
    inside the inlined HTML fragment."""
    return re.sub(r'<style>.*?</style>', '', fragment, flags=re.DOTALL).strip()

def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # ── Load fragments ─────────────────────────────────────────────────────
    nav_raw    = open('_nav.html',    encoding='utf-8').read()
    footer_raw = open('_footer.html', encoding='utf-8').read()

    # Keep the <style> block from _nav.html — it contains nav-specific CSS
    # that is NOT duplicated in rosetta.css (mega menu, nav bar, etc.)
    nav_fragment    = nav_raw.strip()
    footer_fragment = footer_raw.strip()

    # Wrap with the inlined marker so nav-loader.js can detect it
    nav_inlined    = f'<div id="nav-placeholder" data-inlined="true">\n{nav_fragment}\n</div>'
    footer_inlined = f'<div id="footer-placeholder" data-inlined="true">\n{footer_fragment}\n</div>'

    print(f'Nav fragment:    {len(nav_fragment):,} chars')
    print(f'Footer fragment: {len(footer_fragment):,} chars')
    print()

    for page in PAGES:
        if not os.path.exists(page):
            print(f'  SKIP {page} (not found)')
            continue

        html = open(page, encoding='utf-8').read()
        original_len = len(html)

        # 1. Replace nav placeholder (depth-aware — handles nested divs correctly)
        html = replace_placeholder_div(html, 'nav-placeholder', nav_inlined)

        # 2. Replace footer placeholder (depth-aware)
        html = replace_placeholder_div(html, 'footer-placeholder', footer_inlined)

        open(page, 'w', encoding='utf-8').write(html)
        delta = len(html) - original_len
        print(f'  ✓ {page}  (+{delta:,} chars inlined)')

    print()
    print('Build complete. Ready to push.')
    print()
    print('  git add -A && git commit -m "build: inline nav + footer" && git push origin main')

if __name__ == '__main__':
    main()
