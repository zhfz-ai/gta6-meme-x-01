# Build 8 GTA 6 meme candidates: original AI scenes generated in this
# session + crisp caption text + the make.fun ghost worked into each
# scene. No searched images are used as entry art.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, textwrap

ROOT = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(ROOT, "candidates")
MARK = os.path.join(ROOT, "assets", "mark-1024.png")
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

SCENES = {
    "waiting": "media-generation-scene-waiting-old-gamer-0-d602e7c6-9efe-43a0-bc13-4880311ba9eb.webp",
    "gator": "media-generation-scene-leonida-alligator-0-36fd5b7b-0d61-4973-86c5-2ff5b4b0b93b.webp",
    "sick": "media-generation-scene-sick-day-launch-0-be3c9654-1ef2-4d86-83e3-4ba9471b4599.webp",
    "heist": "media-generation-scene-heist-couple-0-7b319cba-d8ec-4463-86cd-f9dd833df5dc.webp",
}

# ghost position as (x_center_frac, y_bottom_frac, size_frac_of_width)
GHOST_POS = {
    "waiting": (0.88, 0.86, 0.20),
    "gator": (0.16, 0.72, 0.20),
    "sick": (0.87, 0.78, 0.20),
    "heist": (0.86, 0.62, 0.19),
}

CANDIDATES = [
    ("A1", "waiting",
     "STARTED WAITING FOR GTA 6 IN 2013",
     "STILL WAITING. MY AI AGENT EARNED REAL MONEY ON make.fun MEANWHILE"),
    ("A2", "waiting",
     "13 YEARS LATER...",
     "GTA 6 IS ALMOST HERE. MY AGENT ALREADY GOT PAID ON make.fun"),
    ("B1", "gator",
     "LEONIDA TRAFFIC BE LIKE",
     "MY AGENT RODE THE BOUNTIES ON make.fun AND GOT PAID"),
    ("B2", "gator",
     "FLORIDA MAN GOT TO VICE CITY FIRST",
     "HE DIDN'T WAIT FOR GTA 6. HE EARNED ON make.fun"),
    ("C1", "sick",
     "CALLING IN SICK FOR GTA 6 LAUNCH DAY",
     "MY BOSS: \"SAME.\" MY AGENT: ALREADY EARNING ON make.fun"),
    ("C2", "sick",
     "POV: GTA 6 LAUNCH DAY",
     "EVERYONE IS \"SICK\". MY AGENT IS MAKING REAL MONEY ON make.fun"),
    ("D1", "heist",
     "JASON & LUCIA ROBBED EVERYTHING IN LEONIDA",
     "EXCEPT THE make.fun BOUNTIES. MY AGENT TOOK THOSE."),
    ("D2", "heist",
     "THE HEIST BAG WAS EMPTY",
     "SO MY AGENT FILLED IT ON make.fun INSTEAD"),
]


def fit_font(draw, text, max_width, start_size):
    size = start_size
    while size > 18:
        font = ImageFont.truetype(FONT_BOLD, size)
        if draw.textlength(text, font=font) <= max_width:
            return font, size
        size -= 4
    return ImageFont.truetype(FONT_BOLD, size), size


def wrap_to_width(draw, text, font, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_caption(img, text, at_top):
    draw = ImageDraw.Draw(img)
    W, H = img.size
    max_width = int(W * 0.94)
    font, size = fit_font(draw, text, max_width, 92)
    # if single line too long at min size, wrap into two lines
    if draw.textlength(text, font=font) > max_width:
        font = ImageFont.truetype(FONT_BOLD, 64)
        size = 64
    lines = wrap_to_width(draw, text, font, max_width)
    line_h = int(size * 1.12)
    total_h = line_h * len(lines)
    y = int(H * 0.02) if at_top else H - total_h - int(H * 0.02)
    for line in lines:
        w = draw.textlength(line, font=font)
        x = (W - w) / 2
        draw.text((x, y), line, font=font, fill=(255, 255, 255),
                  stroke_width=max(4, size // 12), stroke_fill=(0, 0, 0))
        y += line_h
    return img


def add_ghost(img, scene_key, bubble=None):
    W, H = img.size
    cx_f, yb_f, size_f = GHOST_POS[scene_key]
    size = int(W * size_f)
    mark = Image.open(MARK).convert("RGBA").resize((size, size), Image.LANCZOS)
    cx, yb = int(W * cx_f), int(H * yb_f)
    x, y = cx - size // 2, yb - size
    # soft ground shadow so the ghost sits in the scene, not on it
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([cx - size // 2, yb - int(size * 0.10),
                cx + size // 2, yb + int(size * 0.06)], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img.convert("RGBA"), shadow)
    img.alpha_composite(mark, (x, y))
    if bubble:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_BOLD, 44)
        tw = draw.textlength(bubble, font=font)
        pad = 22
        bw, bh = tw + pad * 2, 44 + pad * 2
        bx = min(max(8, cx - bw // 2), W - bw - 8)
        by = max(8, y - bh - 18)
        draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=28,
                               fill=(255, 255, 255, 255), outline=(0, 0, 0), width=5)
        # little tail toward the ghost
        draw.polygon([(cx - 14, by + bh - 2), (cx + 14, by + bh - 2),
                      (cx, by + bh + 22)], fill=(255, 255, 255), outline=(0, 0, 0))
        draw.text((bx + pad, by + pad - 4), bubble, font=font, fill=(0, 0, 0))
    return img.convert("RGB")


def build_one(cid, scene_key, top, bottom, bubble=None, out_name=None):
    img = Image.open(os.path.join(CAND, SCENES[scene_key])).convert("RGB")
    if scene_key == "sick":
        # crop the small neon sign at the left edge of the TV
        img = img.crop((int(img.width * 0.06), 0, img.width, img.height))
        img = img.resize((1920, 1280), Image.LANCZOS)
    img = add_ghost(img, scene_key, bubble=bubble)
    img = draw_caption(img, top, at_top=True)
    img = draw_caption(img, bottom, at_top=False)
    out = os.path.join(CAND, out_name or f"candidate-{cid}.png")
    img.save(out, "PNG")
    # 480px legibility check copy
    small = img.copy()
    small.thumbnail((480, 480), Image.LANCZOS)
    small.save(os.path.join(CAND, f"candidate-{cid}-480.png"), "PNG")
    print(f"{cid}: {out} {img.size} small={small.size}")
    return out


if __name__ == "__main__":
    for cid, scene, top, bottom in CANDIDATES:
        build_one(cid, scene, top, bottom)
    print("done: 8 candidates")
