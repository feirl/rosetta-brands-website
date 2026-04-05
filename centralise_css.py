"""
centralise_css.py  —  v2

For each HTML page:
  1. Adds <link rel="stylesheet" href="rosetta.css"> to <head>
  2. Strips shared CSS sections (now in rosetta.css / _nav.html) from inline <style>
  3. Leaves only page-specific CSS inline

Strategy: split the style block ONLY on the decorative ═══ section headers.
Ordinary inline comments (/* Brand Colors */ etc.) are NOT treated as separators.
"""

import re
import os

PAGES = [
    'index.html',
    'amazon-vendors.html',
    'fulfilment.html',
    'pricing.html',
    'vendor-access.html',
    'vendor-management-team.html',
]

# These section labels are now covered by rosetta.css or _nav.html.
# Match against the text INSIDE the decorative header comment.
REMOVE_LABELS = [
    'DESIGN SYSTEM',
    'RESET',
    'NAVIGATION',
    'MEGA MENU',
    'BUTTONS',
    'SECTION SHARED',
    'FOOTER',
    'ANIMATION',
    'ACCESSIBILITY',
    'HAMBURGER',
    'CERT',          # CERTIFICATION STRIP / CERT STRIP
    'CTA SECTION',
    'RELATED',
    'METRICS',
    'FADE',
]

# Regex: a line that is a decorative section header — contains ═ (U+2550)
HEADER_RE = re.compile(r'/\*[^*]*═[^*]*\*/', re.DOTALL)


def label_to_remove(header_text):
    """Return True if this section header matches something in REMOVE_LABELS."""
    upper = header_text.upper()
    for label in REMOVE_LABELS:
        if label in upper:
            return True
    return False


def clean_style_block(css):
    """
    Split CSS into (header, body) pairs using ═══ headers as delimiters.
    Drop any section whose header label is in REMOVE_LABELS.
    Returns cleaned CSS string.
    """
    # Find all ═══ headers and their positions
    headers = [(m.start(), m.end(), m.group()) for m in HEADER_RE.finditer(css)]

    if not headers:
        # No section structure — return as-is (shouldn't happen for our pages)
        return css

    result = []

    # Text before the first header (usually empty or just a newline)
    preamble = css[:headers[0][0]]
    if preamble.strip():
        result.append(preamble)

    for i, (start, end, header) in enumerate(headers):
        # Body = text from end of this header to start of next header (or end of css)
        body_end = headers[i + 1][0] if i + 1 < len(headers) else len(css)
        body = css[end:body_end]

        if label_to_remove(header):
            continue  # drop header + body

        result.append(header)
        result.append(body)

    cleaned = ''.join(result)

    # Collapse excessive blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned).strip()
    return cleaned


def process_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # ─── 1. Add rosetta.css <link> tag ────────────────────────────────────
    if 'rosetta.css' not in html:
        # Insert immediately before the first <style> tag
        html = re.sub(
            r'(<style\b[^>]*>)',
            '<link rel="stylesheet" href="rosetta.css">\n\\1',
            html, count=1
        )
        print(f'  + Added rosetta.css link')
    else:
        print(f'  . rosetta.css already present')

    # ─── 2. Extract + clean inline <style> block ──────────────────────────
    style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    if not style_match:
        print(f'  ! No <style> block found')
        return

    original_css = style_match.group(1)
    cleaned_css  = clean_style_block(original_css)

    lines_before = original_css.count('\n')
    lines_after  = cleaned_css.count('\n')
    print(f'  CSS: {lines_before} → {lines_after} lines  (−{lines_before - lines_after})')

    # ─── 3. Write back ────────────────────────────────────────────────────
    new_style = '\n' + cleaned_css + '\n'
    html = html[:style_match.start(1)] + new_style + html[style_match.end(1):]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for page in PAGES:
        if os.path.exists(page):
            print(f'\n{page}')
            process_file(page)
        else:
            print(f'\n{page}  — NOT FOUND')
    print('\nDone.')
