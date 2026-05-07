"""
Atelier — Logo Generator
Generates minimalist logos for Fiverr clients.
Usage: python3 logo.py --name "Brand Name" --tagline "tagline" --style dark
"""

from PIL import Image, ImageDraw, ImageFont
import argparse, os, sys

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "portfolio", "logos")
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

def generate_logo(name: str, tagline: str = "", style: str = "ivory", output_name: str = None):
    p = STYLES.get(style, STYLES["ivory"])
    W, H = 2400, 1600

    img = Image.new("RGB", (W, H), p["bg"])
    draw = ImageDraw.Draw(img)

    name_upper = name.upper()
    tagline_upper = tagline.upper() if tagline else ""

    # Fonts
    font_name = ImageFont.load_default(size=int(W * 0.075))
    font_tag  = ImageFont.load_default(size=int(W * 0.026))
    font_deco = ImageFont.load_default(size=int(W * 0.018))

    cy = H // 2

    # Top decorative line
    draw.line([(int(W*0.32), cy - int(H*0.18)),
               (int(W*0.68), cy - int(H*0.18))], fill=p["accent"], width=2)

    # Brand name
    draw.text((W//2, cy - int(H*0.04)), name_upper,
              fill=p["primary"], anchor="mm", font=font_name)

    # Tagline
    if tagline_upper:
        draw.text((W//2, cy + int(H*0.10)), tagline_upper,
                  fill=p["secondary"], anchor="mm", font=font_tag)

    # Bottom decorative line
    draw.line([(int(W*0.32), cy + int(H*0.20)),
               (int(W*0.68), cy + int(H*0.20))], fill=p["accent"], width=2)

    # Corner marks (luxury detail)
    m = int(W * 0.04)
    pad = int(W * 0.06)
    for x, y, dx, dy in [(pad, pad, 1, 1), (W-pad, pad, -1, 1),
                          (pad, H-pad, 1, -1), (W-pad, H-pad, -1, -1)]:
        draw.line([(x, y), (x + dx*m, y)], fill=p["accent"], width=1)
        draw.line([(x, y), (x, y + dy*m)], fill=p["accent"], width=1)

    # Save
    safe_name = name.lower().replace(" ", "-")
    filename = output_name or f"logo-{safe_name}-{style}.jpg"
    path = os.path.join(OUTPUT_DIR, filename)
    img.save(path, "JPEG", quality=97, dpi=(300, 300))
    print(f"✓ Logo saved: {path}")
    return path

def generate_all_styles(name: str, tagline: str = ""):
    paths = []
    for style in STYLES:
        paths.append(generate_logo(name, tagline, style))
    print(f"\n✅ {len(paths)} logo variants generated for '{name}'")
    return paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default="Maison")
    parser.add_argument("--tagline", default="quiet luxury")
    parser.add_argument("--style", default="all")
    args = parser.parse_args()

    if args.style == "all":
        generate_all_styles(args.name, args.tagline)
    else:
        generate_logo(args.name, args.tagline, args.style)
