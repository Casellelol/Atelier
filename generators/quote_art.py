"""
Atelier — Quote Wall Art Generator
Generates printable quote art for Fiverr clients.
Usage: python3 quote_art.py --quote "Be still." --author "" --style ivory
"""

from PIL import Image, ImageDraw, ImageFont
import argparse, os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "portfolio", "prints")
os.makedirs(OUTPUT_DIR, exist_ok=True)

STYLES = {
    "ivory": {
        "bg": (250, 248, 244),
        "primary": (25, 23, 20),
        "accent": (180, 148, 90),
        "secondary": (140, 132, 120),
    },
    "dark": {
        "bg": (15, 15, 18),
        "primary": (235, 232, 225),
        "accent": (180, 148, 90),
        "secondary": (120, 116, 108),
    },
    "sage": {
        "bg": (228, 234, 224),
        "primary": (40, 52, 36),
        "accent": (110, 138, 96),
        "secondary": (100, 115, 88),
    },
    "navy": {
        "bg": (18, 26, 48),
        "primary": (232, 228, 218),
        "accent": (180, 148, 90),
        "secondary": (110, 124, 155),
    },
    "rose": {
        "bg": (248, 238, 238),
        "primary": (68, 42, 46),
        "accent": (172, 112, 112),
        "secondary": (155, 122, 122),
    },
}

def wrap_text(text, max_chars=20):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        if len(current) + len(word) + 1 <= max_chars:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def generate_quote_art(quote: str, author: str = "", style: str = "ivory", output_name: str = None):
    p = STYLES.get(style, STYLES["ivory"])
    W, H = 2400, 3000

    img = Image.new("RGB", (W, H), p["bg"])
    draw = ImageDraw.Draw(img)

    font_quote = ImageFont.load_default(size=int(W * 0.068))
    font_author = ImageFont.load_default(size=int(W * 0.028))
    font_deco = ImageFont.load_default(size=int(W * 0.022))

    cy = H // 2

    # Top accent line
    draw.line([(int(W*0.3), cy - int(H*0.22)),
               (int(W*0.7), cy - int(H*0.22))], fill=p["accent"], width=2)

    # Opening quotation mark
    draw.text((W//2, cy - int(H*0.17)), "“",
              fill=p["accent"], anchor="mm", font=ImageFont.load_default(size=int(W * 0.10)))

    # Quote lines
    lines = wrap_text(quote.upper(), max_chars=18)
    line_h = int(H * 0.085)
    total_h = len(lines) * line_h
    start_y = cy - total_h // 2

    for i, line in enumerate(lines):
        draw.text((W//2, start_y + i * line_h), line,
                  fill=p["primary"], anchor="mm", font=font_quote)

    # Author
    if author:
        draw.text((W//2, cy + int(H*0.18)), f"— {author.upper()} —",
                  fill=p["secondary"], anchor="mm", font=font_author)

    # Bottom accent line
    draw.line([(int(W*0.3), cy + int(H*0.24)),
               (int(W*0.7), cy + int(H*0.24))], fill=p["accent"], width=2)

    # Corner marks
    m = int(W * 0.04)
    pad = int(W * 0.05)
    for x, y, dx, dy in [(pad, pad, 1, 1), (W-pad, pad, -1, 1),
                          (pad, H-pad, 1, -1), (W-pad, H-pad, -1, -1)]:
        draw.line([(x, y), (x + dx*m, y)], fill=p["accent"], width=1)
        draw.line([(x, y), (x, y + dy*m)], fill=p["accent"], width=1)

    safe_quote = quote.lower().replace(" ", "-").replace(".", "")[:30]
    filename = output_name or f"quote-{safe_quote}-{style}.jpg"
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path, "JPEG", quality=97, dpi=(300, 300))
    print(f"✓ Quote art saved: {path}")
    return path

def generate_all_styles(quote: str, author: str = ""):
    paths = []
    for style in STYLES:
        paths.append(generate_quote_art(quote, author, style))
    print(f"\n✅ {len(paths)} variants generated")
    return paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quote", default="Be still.")
    parser.add_argument("--author", default="")
    parser.add_argument("--style", default="all")
    args = parser.parse_args()

    if args.style == "all":
        generate_all_styles(args.quote, args.author)
    else:
        generate_quote_art(args.quote, args.author, args.style)
