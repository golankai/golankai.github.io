"""
Generates assets/publications.pdf from _pages/publications.md, so the website page
is the single source of truth for the publications list.

Usage: python build_publications_pdf.py
"""
import html
import os
import re
from reportlab.lib.colors import HexColor, black
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

REPO = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD_PATH = os.path.join(REPO, "_pages", "publications.md")
OUT_PATH = os.path.join(REPO, "assets", "publications.pdf")
PHOTO_PATH = os.path.join(REPO, "assets", "kai.jpg")

SCHOLAR_URL = "https://scholar.google.com/citations?user=BvjFcjYAAAAJ"
PAGE_W, PAGE_H = 603, 850
MARGIN = 36
ACCENT = HexColor("#1a4b8c")
BAND = HexColor("#e8f3fa")
FONT, BOLD = "Helvetica", "Helvetica-Bold"
SIZE, LEADING = 9.5, 13.5


def parse(md):
    """Returns [(year, [(authors_html, title, url, venue), ...]), ...] in file order."""
    years = []
    for m in re.finditer(r'<h2 class="pub-year-heading">(\d{4})</h2>\s*<ul class="pub-list">(.*?)</ul>', md, re.S):
        items = []
        for li in re.findall(r"<li>(.*?)</li>", m.group(2), re.S):
            venue = re.search(r'class="pub-venue">(.*?)</div>', li, re.S).group(1)
            title_html = re.search(r'class="pub-title">(.*?)</div>', li, re.S).group(1)
            authors = re.search(r'class="pub-authors">(.*?)</div>', li, re.S).group(1)
            link = re.search(r'href="([^"]+)"', title_html)
            title = html.unescape(re.sub(r"<[^>]+>", "", title_html)).strip()
            items.append((authors, title, link.group(1) if link else None, html.unescape(venue).strip()))
        years.append((m.group(1), items))
    return years


def authors_runs(authors_html):
    """Splits the authors HTML into (text, bold) runs."""
    runs = []
    for part in re.split(r"(<strong>.*?</strong>)", html.unescape(authors_html)):
        if part.startswith("<strong>"):
            runs.append((re.sub(r"<[^>]+>", "", part), True))
        elif part:
            runs.append((part, False))
    return runs


def words(runs):
    """Flattens runs into (word, font, url, underline) tokens that keep their trailing space."""
    out = []
    for text, font, url in runs:
        for w in re.findall(r"\S+\s*", text):
            out.append((w, font, url))
    return out


def draw_header(c):
    c.setFillColor(BAND)
    c.rect(0, PAGE_H - 84, PAGE_W, 84, stroke=0, fill=1)
    c.saveState()
    p = c.beginPath()
    p.circle(MARGIN + 24, PAGE_H - 42, 24)
    c.clipPath(p, stroke=0)
    c.drawImage(PHOTO_PATH, MARGIN, PAGE_H - 66, 48, 48, preserveAspectRatio=True, anchor="c", mask="auto")
    c.restoreState()
    c.setFillColor(HexColor("#222222"))
    c.setFont(BOLD, 24)
    c.drawString(MARGIN + 66, PAGE_H - 50, "Publications")
    c.setFillColor(ACCENT)
    c.setFont(FONT, 8.5)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 34, "Google Scholar")
    c.setFont(BOLD, 8.5)
    label = SCHOLAR_URL.replace("https://", "")
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 48, label)
    w = stringWidth(label, BOLD, 8.5)
    c.linkURL(SCHOLAR_URL, (PAGE_W - MARGIN - w, PAGE_H - 52, PAGE_W - MARGIN, PAGE_H - 40), relative=0)


def main():
    with open(MD_PATH, encoding="utf-8") as f:
        years = parse(f.read())

    c = canvas.Canvas(OUT_PATH, pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Kai Golan Hashiloni - Publications")
    c.setAuthor("Kai Golan Hashiloni")
    draw_header(c)
    y = PAGE_H - 84 - 26
    indent = MARGIN + 14
    max_w = PAGE_W - MARGIN - indent

    for year, items in years:
        c.setFillColor(ACCENT)
        c.setFont(FONT, 15)
        c.drawString(MARGIN, y, year)
        y -= 20
        for authors, title, url, venue in items:
            runs = [(t, BOLD if b else FONT, None) for t, b in authors_runs(authors)]
            runs[-1:] = [(runs[-1][0].rstrip() + ". ", runs[-1][1], None)]
            runs.append((title, FONT, url))
            runs.append((". " + venue + ".", FONT, None))
            tokens = words(runs)

            lines, cur, cur_w = [], [], 0
            for tok in tokens:
                w = stringWidth(tok[0].rstrip(), tok[1], SIZE)
                if cur and cur_w + w > max_w:
                    lines.append(cur)
                    cur, cur_w = [], 0
                cur.append(tok)
                cur_w += stringWidth(tok[0], tok[1], SIZE)
            lines.append(cur)

            c.setFillColor(black)
            c.circle(MARGIN + 4, y + 3, 1.6, stroke=0, fill=1)
            for line in lines:
                x = indent
                span = None  # [link, x_start, x_end] of the link run being underlined
                for i, (text, font, link) in enumerate(line):
                    c.setFont(font, SIZE)
                    c.drawString(x, y, text)
                    x_end = x + stringWidth(text.rstrip(), font, SIZE)
                    if link and span and span[0] == link:
                        span[2] = x_end
                    elif link:
                        span = [link, x, x_end]
                    if span and (not link or i == len(line) - 1 or line[i + 1][2] != link):
                        c.setLineWidth(0.5)
                        c.line(span[1], y - 1.5, span[2], y - 1.5)
                        c.linkURL(span[0], (span[1], y - 3, span[2], y + SIZE), relative=0)
                        span = None
                    x += stringWidth(text, font, SIZE)
                y -= LEADING
            y -= 2.5
        y -= 8

    c.save()
    print(f"Wrote {OUT_PATH} ({sum(len(i) for _, i in years)} publications)")


if __name__ == "__main__":
    main()
