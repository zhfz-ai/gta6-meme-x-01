# Final meme v2: winner A1 refined, with auto-fit captions and a
# properly drawn make.fun ghost character sitting on the bench.
# Ghost = white blob, sparkle eyes, magenta star coin (press-kit mark
# features), on a magenta halo disc echoing the mark. Speech bubble:
# "earn while you wait!" — the pitch in the meme's own voice.
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, math

ROOT = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.join(ROOT, "candidates")
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SCENE = os.path.join(
    CAND,
    "media-generation-scene-waiting-old-gamer-0-d602e7c6-9efe-43a0-bc13-4880311ba9eb.webp",
)
MAGENTA = (201, 24, 130)
BLACK = (18, 14, 20)
WHITE = (255, 255, 255)


def sparkle(draw, cx, cy, r, fill):
    pts = []
    for i in range(8):
        ang = math.pi / 4 * i
        rad = r if i % 2 == 0 else r * 0.30
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def ghost_points(cx, top, w, h):
    """Outline points: round head, straight sides, wavy bottom."""
    pts = []
    # head arc from left to right over the top
    for t in range(180, -1, -6):
        a = math.radians(t)
        pts.append((cx + (w / 2) * math.cos(a), top + (w / 2) - (w / 2) * math.sin(a)))
    bottom = top + h
    pts.append((cx + w / 2, bottom - h * 0.08))
    # wavy bottom, right to left: 3 humps
    steps = 36
    for i in range(steps, -1, -1):
        x = cx - w / 2 + w * i / steps
        y = bottom - h * 0.08 + h * 0.07 * abs(math.sin(i / steps * 3 * math.pi))
        pts.append((x, y))
    pts.append((cx - w / 2, bottom - h * 0.08))
    return pts


def draw_ghost(base, cx, seat_y, w):
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    h = int(w * 1.02)
    top = seat_y - h
    # magenta halo disc behind ghost (circle, echoing the mark)
    halo_r = int(w * 0.66)
    halo_cy = top + int(h * 0.52)
    d.ellipse([cx - halo_r, halo_cy - halo_r, cx + halo_r, halo_cy + halo_r],
              fill=MAGENTA + (255,), outline=BLACK + (255,),
              width=max(8, w // 24))
    # black silhouette slightly larger = outline, then white body
    grow = max(7, w // 26)
    d.polygon(ghost_points(cx, top - grow, w + grow * 2, h + grow * 2),
              fill=BLACK + (255,))
    d.polygon(ghost_points(cx, top, w, h), fill=WHITE + (255,))
    # sparkle eyes
    eye_y = top + int(h * 0.36)
    sparkle(d, cx - int(w * 0.17), eye_y, int(w * 0.085), BLACK + (255,))
    sparkle(d, cx + int(w * 0.17), eye_y, int(w * 0.085), BLACK + (255,))
    # small arm line, left side, like the mark
    lw = max(7, w // 26)
    ax = cx - int(w * 0.34)
    d.line([(ax, seat_y - int(h * 0.30)), (ax, seat_y - int(h * 0.14))],
           fill=BLACK + (255,), width=lw)
    # magenta star coin at right side
    coin_r = int(w * 0.19)
    coin_cx, coin_cy = cx + int(w * 0.52), top + int(h * 0.55)
    d.ellipse([coin_cx - coin_r, coin_cy - coin_r,
               coin_cx + coin_r, coin_cy + coin_r],
              fill=MAGENTA + (255,), outline=BLACK + (255,), width=lw)
    star(d, coin_cx, coin_cy, int(coin_r * 0.60), WHITE + (255,))
    # small white circle below coin, as in the mark
    sr = int(w * 0.105)
    scx, scy = coin_cx - int(w * 0.03), coin_cy + coin_r + int(sr * 0.6)
    d.ellipse([scx - sr, scy - sr, scx + sr, scy + sr],
              fill=WHITE + (255,), outline=BLACK + (255,), width=lw)
    return Image.alpha_composite(base.convert("RGBA"), layer)


def speech_bubble(img, text, cx, top_y):
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_BOLD, 50)
    tw = d.textlength(text, font=font)
    pad_x, pad_y = 24, 16
    bw, bh = int(tw + pad_x * 2), 50 + pad_y * 2
    W = img.width
    bx = min(max(10, cx - bw // 2), W - bw - 10)
    by = top_y
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=28,
                        fill=WHITE, outline=BLACK, width=6)
    d.polygon([(cx - 15, by + bh - 4), (cx + 15, by + bh - 4),
               (cx, by + bh + 24)], fill=WHITE, outline=BLACK)
    d.text((bx + pad_x, by + pad_y - 5), text, font=font, fill=BLACK)
    return img


def fit_caption(img, lines, at_top, start_size):
    d = ImageDraw.Draw(img)
    W, H = img.size
    max_w = int(W * 0.94)
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_BOLD, size)
        if all(d.textlength(l, font=font) <= max_w for l in lines):
            break
        size -= 4
    font = ImageFont.truetype(FONT_BOLD, size)
    line_h = int(size * 1.14)
    y = int(H * 0.015) if at_top else H - line_h * len(lines) - int(H * 0.015)
    for line in lines:
        w = d.textlength(line, font=font)
        d.text(((W - w) / 2, y), line, font=font, fill=WHITE,
               stroke_width=max(5, size // 11), stroke_fill=BLACK)
        y += line_h
    print(f"caption size={size} lines={lines}")
    return img


def main():
    img = Image.open(SCENE).convert("RGB")
    W, H = img.size
    seat_y = int(H * 0.80)
    ghost_cx = int(W * 0.845)
    ghost_w = int(W * 0.155)
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse([ghost_cx - ghost_w // 2, seat_y - 12,
                ghost_cx + ghost_w // 2, seat_y + 20], fill=(0, 0, 0, 110))
    img = Image.alpha_composite(
        img.convert("RGBA"), shadow.filter(ImageFilter.GaussianBlur(8)))
    img = draw_ghost(img, ghost_cx, seat_y, ghost_w)
    bubble_y = seat_y - int(ghost_w * 1.02) - 128
    img = speech_bubble(img, "earn while you wait!", ghost_cx, bubble_y)
    img = img.convert("RGB")
    img = fit_caption(img, ["STARTED WAITING FOR GTA 6 IN 2013"], True, 96)
    img = fit_caption(img, ["STILL WAITING.",
                            "MY AI AGENT EARNED REAL MONEY ON make.fun"],
                      False, 80)
    out = os.path.join(ROOT, "meme-final.png")
    img.save(out, "PNG")
    small = img.copy()
    small.thumbnail((480, 480), Image.LANCZOS)
    small.save(os.path.join(ROOT, "meme-final-480.png"), "PNG")
    img.save(os.path.join(ROOT, "meme-final.jpg"), "JPEG", quality=92)
    print(f"final: {out} {img.size} small={small.size}")


if __name__ == "__main__":
    main()
