#!/usr/bin/env python3
"""Generate launcher icons and splash logo for the Wholeness Android app."""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = "/home/claude/wholeness-android/app/src/main/res"

BG = (8, 10, 14, 255)
GOLD = (201, 168, 76, 255)
GOLD_DIM = (201, 168, 76, 60)
TEXT = (232, 234, 242, 255)

# Density buckets for ic_launcher.png (square) and ic_launcher_round.png
DENSITIES = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}

def find_serif_font(size):
    """Try to load a serif font (for the W). Falls back to default."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

def draw_w_emblem(size, square=True):
    """Draw a square or round launcher icon: dark bg, gold ring, gold W."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if square:
        # Slight rounded corner so it looks intentional even outside adaptive layer
        radius = int(size * 0.18)
        d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=BG)
    else:
        # Circular bg
        d.ellipse([0, 0, size - 1, size - 1], fill=BG)

    # Gold ring
    pad = int(size * 0.12)
    ring_w = max(1, int(size * 0.025))
    if square:
        d.rounded_rectangle(
            [pad, pad, size - 1 - pad, size - 1 - pad],
            radius=int(size * 0.10),
            outline=GOLD,
            width=ring_w,
        )
    else:
        d.ellipse(
            [pad, pad, size - 1 - pad, size - 1 - pad],
            outline=GOLD,
            width=ring_w,
        )

    # Centered W
    font_size = int(size * 0.55)
    font = find_serif_font(font_size)
    text = "W"
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1]
    d.text((tx, ty), text, fill=GOLD, font=font)

    # Tiny gold dot top-right (the brand's "header-logo-dot")
    dot_r = max(2, int(size * 0.025))
    cx = size - pad - dot_r * 3
    cy = pad + dot_r * 3
    d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=GOLD)

    return img

def write_icon_density(dpi, px):
    out_dir = os.path.join(ROOT, f"mipmap-{dpi}")
    os.makedirs(out_dir, exist_ok=True)
    sq = draw_w_emblem(px, square=True)
    rd = draw_w_emblem(px, square=False)
    sq.save(os.path.join(out_dir, "ic_launcher.png"))
    rd.save(os.path.join(out_dir, "ic_launcher_round.png"))
    # Adaptive icon foreground (108dp logical, 432px at xxxhdpi). For simplicity use 1.5x.
    fg_px = int(px * 1.5)
    fg_img = Image.new("RGBA", (fg_px, fg_px), (0, 0, 0, 0))
    fg_w = draw_w_emblem(int(fg_px * 0.66), square=False)
    # paste centered, no bg
    fg_no_bg = Image.new("RGBA", fg_w.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(fg_no_bg)
    s = fg_w.size[0]
    font = find_serif_font(int(s * 0.55))
    bbox = d.textbbox((0, 0), "W", font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(((s - tw) / 2 - bbox[0], (s - th) / 2 - bbox[1]), "W", fill=GOLD, font=font)
    paste_x = (fg_px - s) // 2
    paste_y = (fg_px - s) // 2
    fg_img.paste(fg_no_bg, (paste_x, paste_y), fg_no_bg)
    fg_img.save(os.path.join(out_dir, "ic_launcher_foreground.png"))


def write_splash_logo():
    """Splash logo: 'Wholeness' wordmark in serif, gold accent on 'ness'."""
    w, h = 720, 360
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Eyebrow
    eb_size = 22
    eb_font = find_serif_font(eb_size)
    eb_text = "T E A M  21  A C A D E M Y"
    bbox = d.textbbox((0, 0), eb_text, font=eb_font)
    d.text(((w - (bbox[2] - bbox[0])) / 2, 70), eb_text, fill=GOLD, font=eb_font)

    # Main wordmark (single text, then a separate 'ness' overlay in gold)
    main_size = 110
    main_font = find_serif_font(main_size)
    full = "Wholeness"
    bbox = d.textbbox((0, 0), full, font=main_font)
    fw = bbox[2] - bbox[0]
    fx = (w - fw) / 2 - bbox[0]
    fy = 130
    # 'Whole' in white
    d.text((fx, fy), "Whole", fill=TEXT, font=main_font)
    # measure 'Whole' to know x for 'ness'
    whole_bbox = d.textbbox((0, 0), "Whole", font=main_font)
    whole_w = whole_bbox[2] - whole_bbox[0]
    d.text((fx + whole_w, fy), "ness", fill=GOLD, font=main_font)

    # Thin gold rule
    line_y = fy + main_size + 30
    line_w = 80
    d.line(
        [((w - line_w) / 2, line_y), ((w + line_w) / 2, line_y)],
        fill=GOLD,
        width=2,
    )

    out = os.path.join(ROOT, "drawable", "splash_logo.png")
    img.save(out)
    print(f"  splash logo: {out}")


for dpi, px in DENSITIES.items():
    write_icon_density(dpi, px)
    print(f"  icons: mipmap-{dpi} ({px}px)")

write_splash_logo()
print("✓ All icons and splash assets generated")
