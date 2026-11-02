import io, re, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
LATIN = ["/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"]
TELUGU = ["/System/Library/Fonts/KohinoorTelugu.ttc", "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"]

def get_font(size, telugu=False):
    for p in (TELUGU if telugu else LATIN):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    return ImageFont.load_default()

def clean(text):
    # Pillow lo emojis render avvavu, so teesestam
    return "".join(c for c in text if ord(c) < 0x2600 or 0x0C00 <= ord(c) <= 0x0C7F).strip()

def wrap(draw, text, font, max_w):
    lines, line = [], ""
    for word in text.split():
        test = f"{line} {word}".strip()
        if draw.textlength(test, font=font) <= max_w:
            line = test
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def make_card(name, wish):
    wish = clean(wish)
    telugu = bool(re.search("[\u0C00-\u0C7F]", wish))
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top, bottom = (45, 10, 80), (230, 90, 20)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))

    # sparkles
    import random
    random.seed(len(name) + len(wish))
    for _ in range(60):
        x, y, r = random.randint(0, W), random.randint(0, int(H * 0.6)), random.randint(1, 4)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 220, 130))

    cream, gold = (255, 244, 214), (255, 196, 64)
    title = get_font(96)
    d.text((W / 2, 150), "Happy Diwali", font=title, fill=gold, anchor="mm")
    d.text((W / 2, 250), f"{name}", font=get_font(64, telugu and False), fill=cream, anchor="mm")

    # diya
    cx, cy = W // 2, 520
    d.ellipse([cx - 90, cy - 230, cx + 90, cy - 20], fill=(255, 150, 40))      # glow
    d.polygon([(cx, cy - 200), (cx + 40, cy - 100), (cx, cy - 55), (cx - 40, cy - 100)], fill=(255, 235, 150))
    d.chord([cx - 170, cy - 90, cx + 170, cy + 110], 0, 180, fill=(190, 80, 20))
    d.ellipse([cx - 170, cy - 100, cx + 170, cy - 60], fill=(140, 55, 15))

    body = get_font(50, telugu)
    lines = wrap(d, wish, body, W - 160)
    y = 780
    for ln in lines:
        d.text((W / 2, y), ln, font=body, fill=cream, anchor="mm")
        y += 78

    d.text((W / 2, H - 70), "Shubh Deepavali", font=get_font(40), fill=gold, anchor="mm")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
