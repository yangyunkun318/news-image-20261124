#!/usr/bin/env python3
"""Render the 24 November 2026 world-news front page (1024x1024 PNG).

Stories are all first reported on Tuesday 24 November 2026 (UTC), taken
from the day's wire reporting. Drawn with Pillow only: flat vector
illustrations + real text, so every word is legible and nothing is garbled.
Deterministic: same input -> same bytes.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 232)
INK = (18, 30, 58)
NAVY = (16, 32, 66)
RED = (178, 28, 28)
GOLD = (180, 83, 9)
TEAL = (14, 74, 92)
GREY = (90, 96, 110)
LIGHT = (233, 228, 214)

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, width, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.18)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def sun(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def sea(draw, box, deep, shallow):
    vgrad(draw, box, shallow, deep)


def tanker(draw, x, y, s, hull=(30, 41, 59), deck=(178, 28, 28)):
    # simple flat tanker silhouette, length ~ 3.2*s
    draw.polygon([(x, y), (x + 3.2 * s, y), (x + 2.9 * s, y + 0.55 * s),
                  (x + 0.3 * s, y + 0.55 * s)], fill=hull)
    draw.rectangle([x + 0.5 * s, y - 0.55 * s, x + 1.1 * s, y], fill=deck)
    draw.rectangle([x + 1.4 * s, y - 0.4 * s, x + 2.2 * s, y], fill=(233, 228, 214))
    draw.rectangle([x + 2.4 * s, y - 0.7 * s, x + 2.6 * s, y], fill=(90, 96, 110))


def mine(draw, cx, cy, r, color=(20, 20, 26)):
    for k in range(8):
        a = math.pi * k / 4
        x2, y2 = cx + math.cos(a) * r * 1.7, cy + math.sin(a) * r * 1.7
        draw.line([(cx, cy), (x2, y2)], fill=color, width=3)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def burst(draw, cx, cy, r, color):
    pts = []
    for k in range(16):
        a = math.pi * k / 8
        rr = r if k % 2 == 0 else r * 0.45
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    draw.polygon(pts, fill=color)


def skyline(draw, x0, y_base, x1, color, seed=0):
    import random
    rnd = random.Random(seed)
    x = x0
    while x < x1:
        w = rnd.randint(22, 46)
        h = rnd.randint(18, 46)
        draw.rectangle([x, y_base - h, x + w, y_base], fill=color)
        x += w + rnd.randint(4, 10)


def columns(draw, x0, y0, x1, y1, color):
    draw.rectangle([x0, y0, x1, y0 + 10], fill=color)
    n = 5
    step = (x1 - x0) / n
    for i in range(n):
        cx = x0 + step * i + step / 2
        draw.rectangle([cx - 7, y0 + 10, cx + 7, y1 - 10], fill=color)
    draw.rectangle([x0, y1 - 10, x1, y1], fill=color)


# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# masthead
d.rectangle([0, 0, W, 128], fill=NAVY)
d.text((28, 18), "THE WORLD", font=font(SERIF_B, 92), fill=(248, 244, 232))
d.text((620, 30), "TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 24),
       fill=(248, 244, 232))
d.rectangle([620, 72, 996, 76], fill=(180, 83, 9))
d.text((620, 86), "ONE DAY  ·  SIX STORIES", font=font(SANS, 20),
       fill=(200, 205, 220))
d.rectangle([0, 128, W, 134], fill=RED)

# ------------------------------------------------------------- hero image
hx0, hy0, hx1, hy1 = 28, 152, 560, 470
sea(d, (hx0, hy0, hx1, hy1), (10, 42, 74), (24, 96, 122))
sun(d, 470, 205, 34, (232, 164, 66))
# strait cliffs
d.polygon([(hx0, hy1), (hx0, 330), (180, 300), (240, hy1)], fill=(30, 52, 84))
d.polygon([(hx1, hy1), (hx1, 350), (430, 320), (380, hy1)], fill=(24, 44, 72))
tanker(d, 90, 400, 62, hull=(64, 84, 112), deck=(178, 28, 28))
burst(d, 430, 380, 46, (232, 120, 40))
burst(d, 430, 380, 26, (248, 200, 90))
mine(d, 300, 440, 13)
mine(d, 180, 452, 10)
# waves
for yy in (430, 452):
    for xx in range(hx0 + 10, hx1 - 10, 46):
        d.arc([xx, yy, xx + 34, yy + 16], 0, 180, fill=(160, 200, 220), width=3)
d.rectangle([hx0, hy1 - 4, hx1, hy1], fill=(18, 30, 58))

# hero text
tx = 584
d.text((tx, 158), "STRAIT OF HORMUZ", font=font(SANS_B, 26), fill=RED)
y = text_block(d, (tx, 192), "FOUR TANKERS HIT MINES IN HORMUZ",
               font(SANS_B, 46), INK, 412, leading=52)
y += 8
text_block(d, (tx, y),
           "Iran says mines hit four tankers in the strait. Its army chief "
           "orders it closed further until Washington meets Tehran's terms.",
           font(SANS, 22), (40, 52, 84), 412, leading=29)

d.rectangle([28, 486, W - 28, 490], fill=INK)

# ------------------------------------------------------------- grid
cells = [
    ("THE HAGUE", "MYANMAR GUILTY OF GENOCIDE",
     "The UN court rules the 2017 crackdown on the Rohingya was genocide — "
     "a first for any state.", "court"),
    ("GAZA", "ISRAEL KILLS HAMAS SECURITY CHIEF",
     "Brig. Gen. Naeem Abu Mohammed Nahel dies in a strike, despite the "
     "October ceasefire.", "city"),
    ("COLOMBIA", "CAR BOMB HURTS 23",
     "Blast outside regional offices in Villavicencio; the president blames "
     "narcoterrorism.", "blast"),
    ("MEXICO", "EL CHAPO ISIDRO CAPTURED",
     "A U.S. drone helped Mexican forces seize cartel boss Fausto Isidro "
     "Meza Flores; 20 die in the raid.", "desert"),
    ("UKRAINE", "RUSSIAN STRIKE KILLS 2",
     "Zaporizhzhia hit; 44 wounded, four of them children. Moscow says it "
     "downed ~700 drones.", "night"),
    ("NATO", "NATO VOWS SPACE DEFENCE",
     "Rutte vows space defence, as Russia is reported ready to launch a "
     "nuclear-armed satellite.", "sat"),
]
cw, ch = 312, 200
gx0, gy0 = 28, 504
for i, (kicker, head, body, kind) in enumerate(cells):
    cx = gx0 + (i % 3) * (cw + 16)
    cy = gy0 + (i // 3) * (ch + 14)
    # illustration strip
    ix0, iy0, ix1, iy1 = cx, cy, cx + cw, cy + 64
    if kind == "court":
        vgrad(d, (ix0, iy0, ix1, iy1), (38, 64, 110), (16, 32, 66))
        columns(d, ix0 + 70, iy0 + 14, ix1 - 70, iy1 - 8, (233, 228, 214))
        sun(d, ix0 + 40, iy0 + 26, 12, (232, 200, 120))
    elif kind == "city":
        vgrad(d, (ix0, iy0, ix1, iy1), (96, 62, 52), (40, 30, 44))
        skyline(d, ix0 + 8, iy1 - 6, ix1 - 8, (22, 18, 28), seed=i)
        burst(d, ix1 - 60, iy0 + 30, 20, (232, 120, 40))
    elif kind == "blast":
        vgrad(d, (ix0, iy0, ix1, iy1), (120, 74, 40), (52, 40, 30))
        skyline(d, ix0 + 8, iy1 - 6, ix1 - 8, (30, 26, 34), seed=i + 3)
        burst(d, cx + cw // 2, iy0 + 38, 30, (248, 200, 90))
        burst(d, cx + cw // 2, iy0 + 38, 16, (232, 120, 40))
    elif kind == "desert":
        vgrad(d, (ix0, iy0, ix1, iy1), (200, 150, 90), (120, 82, 52))
        sun(d, ix1 - 46, iy0 + 26, 18, (248, 236, 200))
        d.polygon([(ix0, iy1), (ix0 + 90, iy0 + 52), (ix0 + 190, iy1)], fill=(96, 66, 44))
        d.polygon([(ix0 + 130, iy1), (ix0 + 220, iy0 + 44), (ix1, iy1)], fill=(78, 54, 38))
        # helicopter silhouette
        d.ellipse([cx + 130, iy0 + 26, cx + 200, iy0 + 44], fill=(30, 30, 36))
        d.rectangle([cx + 160, iy0 + 18, cx + 164, iy0 + 28], fill=(30, 30, 36))
        d.line([(cx + 120, iy0 + 24), (cx + 210, iy0 + 24)], fill=(30, 30, 36), width=3)
    elif kind == "night":
        vgrad(d, (ix0, iy0, ix1, iy1), (12, 24, 52), (6, 12, 30))
        for sx, sy in [(40, 18), (120, 30), (210, 14), (270, 34), (90, 44)]:
            d.ellipse([ix0 + sx, iy0 + sy, ix0 + sx + 4, iy0 + sy + 4],
                      fill=(240, 240, 220))
        skyline(d, ix0 + 8, iy1 - 6, ix1 - 8, (16, 20, 34), seed=i + 7)
        burst(d, ix1 - 70, iy0 + 34, 18, (232, 120, 40))
    else:  # sat
        vgrad(d, (ix0, iy0, ix1, iy1), (8, 16, 40), (4, 8, 22))
        for sx, sy in [(30, 20), (90, 12), (180, 26), (250, 16), (140, 40)]:
            d.ellipse([ix0 + sx, iy0 + sy, ix0 + sx + 3, iy0 + sy + 3],
                      fill=(240, 240, 220))
        # earth arc segment, kept inside the strip
        pts = [(ix0, iy1 - 4)]
        for k in range(33):
            t = k / 32
            x = ix0 + t * (ix1 - ix0)
            y = iy1 - 4 - 26 * math.sin(math.pi * t)
            pts.append((x, y))
        pts.append((ix1, iy1 - 4))
        d.polygon(pts, fill=(24, 96, 122))
        # satellite
        d.rectangle([cx + 130, iy0 + 10, cx + 158, iy0 + 30], fill=(200, 205, 220))
        d.rectangle([cx + 108, iy0 + 16, cx + 130, iy0 + 26], fill=(60, 110, 180))
        d.rectangle([cx + 158, iy0 + 16, cx + 180, iy0 + 26], fill=(60, 110, 180))
        burst(d, cx + 200, iy0 + 40, 10, (232, 164, 66))
    d.rectangle([ix0, iy1 - 3, ix1, iy1], fill=RED)
    d.text((cx, cy + 70), kicker, font=font(SANS_B, 16), fill=RED)
    y = text_block(d, (cx, cy + 92), head, font(SANS_B, 22), INK, cw, leading=24)
    text_block(d, (cx, y + 3), body, font(SANS, 16), (52, 60, 80), cw, leading=19)

# footer ticker
d.rectangle([0, 924, W, 928], fill=INK)
d.rectangle([0, 928, W, H], fill=NAVY)
d.text((28, 942), "ALSO:  UK sanctions Yemen's Houthis  ·  Iraq takes control of Kurdish "
       "oilfields  ·  Hasina plans Dec 16 return  ·  Hanoi blast kills six",
       font=font(SANS, 16), fill=(220, 224, 232))
d.text((28, 972), "TUESDAY 24 NOVEMBER 2026  ·  SIX STORIES FROM FIVE REGIONS",
       font=font(SANS_B, 16), fill=(180, 190, 205))

img.save("entry.png", optimize=True)
print("saved entry.png")
from PIL import Image as _I
_im = _I.open("entry.png")
print(_im.size, _im.format, len(open("entry.png", "rb").read()), "bytes")
