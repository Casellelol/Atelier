"""
Atelier — Order Delivery Script
Run this when a Fiverr order arrives.
Usage: python3 deliver.py --type logo --name "Brand Name" --tagline "tagline" --style all
       python3 deliver.py --type quote --quote "Be still." --author "" --style ivory
"""

import argparse, os, sys, shutil, zipfile
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

DELIVERY_DIR = os.path.join(os.path.dirname(__file__), "..", "deliveries")
os.makedirs(DELIVERY_DIR, exist_ok=True)

def deliver_logo(name, tagline, style):
    from logo import generate_logo, generate_all_styles, STYLES
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    safe = name.lower().replace(" ", "-")
    out_dir = os.path.join(DELIVERY_DIR, f"{ts}-logo-{safe}")
    os.makedirs(out_dir, exist_ok=True)

    if style == "all":
        for s in STYLES:
            path = generate_logo(name, tagline, s, output_name=f"logo-{safe}-{s}.jpg")
            shutil.copy(path, out_dir)
    else:
        path = generate_logo(name, tagline, style, output_name=f"logo-{safe}-{style}.jpg")
        shutil.copy(path, out_dir)

    zip_path = out_dir + ".zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for f in os.listdir(out_dir):
            zf.write(os.path.join(out_dir, f), f)
    print(f"\n✅ Delivery ready: {zip_path}")
    return zip_path

def deliver_quote(quote, author, style):
    from quote_art import generate_quote_art, generate_all_styles, STYLES
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    safe = quote.lower().replace(" ", "-").replace(".", "")[:25]
    out_dir = os.path.join(DELIVERY_DIR, f"{ts}-quote-{safe}")
    os.makedirs(out_dir, exist_ok=True)

    if style == "all":
        for s in STYLES:
            path = generate_quote_art(quote, author, s)
            shutil.copy(path, out_dir)
    else:
        path = generate_quote_art(quote, author, style)
        shutil.copy(path, out_dir)

    zip_path = out_dir + ".zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for f in os.listdir(out_dir):
            zf.write(os.path.join(out_dir, f), f)
    print(f"\n✅ Delivery ready: {zip_path}")
    return zip_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", choices=["logo", "quote"], required=True)
    parser.add_argument("--name", default="Brand")
    parser.add_argument("--tagline", default="")
    parser.add_argument("--quote", default="Be still.")
    parser.add_argument("--author", default="")
    parser.add_argument("--style", default="all")
    args = parser.parse_args()

    if args.type == "logo":
        deliver_logo(args.name, args.tagline, args.style)
    else:
        deliver_quote(args.quote, args.author, args.style)
