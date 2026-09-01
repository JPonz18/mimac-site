#!/usr/bin/env python3
"""Generates the favicons, Open Graph images, press-kit logo files and the
SVG device frame (iPad Pro 13" + Magic Keyboard) used as a placeholder while
real captures are pending.

Run from anywhere:  python3 tools/make-assets.py
Needs Pillow (pip install pillow). Uses the macOS system font for PNG text.
Everything it writes is committed, so the site itself has no build step.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG = (11, 13, 18)
BG2 = (17, 20, 27)
ACCENT = (79, 209, 255)
FG = (242, 244, 248)
FG2 = (168, 176, 190)
FONT = "/System/Library/Fonts/SFNS.ttf"


def font(size, weight="Bold"):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def out(path):
    p = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    return p


# ---------------------------------------------------------------- mark (the "M")
M_PTS = [(0.18, 0.80), (0.18, 0.22), (0.50, 0.57), (0.82, 0.22), (0.82, 0.80)]


def draw_mark(img, x, y, s, tile=True, color=ACCENT, bg=BG2):
    """Bold M stroke inside an s×s box at (x, y). Drawn 4× and downsampled by caller."""
    d = ImageDraw.Draw(img)
    if tile:
        d.rounded_rectangle([x, y, x + s, y + s], radius=s * 0.22, fill=bg)
    pts = [(x + px * s, y + py * s) for px, py in M_PTS]
    w = s * 0.15
    d.line(pts, fill=color, width=max(1, int(round(w))), joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=color)


def mark_png(size, tile=True, glow=False, bg=BG2):
    ss = 4
    img = Image.new("RGBA", (size * ss, size * ss), (0, 0, 0, 0))
    draw_mark(img, 0, 0, size * ss, tile=tile, bg=bg)
    if glow:
        g = Image.new("RGBA", img.size, (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        r = size * ss * 0.55
        cx, cy = size * ss * 0.5, size * ss * 0.42
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ACCENT + (70,))
        g = g.filter(ImageFilter.GaussianBlur(size * ss * 0.18))
        base = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(base).rounded_rectangle([0, 0, size * ss, size * ss], radius=size * ss * 0.22, fill=bg)
        base.alpha_composite(g)
        m = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw_mark(m, 0, 0, size * ss, tile=False)
        base.alpha_composite(m)
        img = base
    return img.resize((size, size), Image.LANCZOS)


MARK_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="100" height="100">'
    '<rect width="100" height="100" rx="22" fill="#11141B"/>'
    '<path d="M18 80V22L50 57 82 22V80" fill="none" stroke="#4FD1FF" stroke-width="15" '
    'stroke-linecap="round" stroke-linejoin="round"/></svg>\n'
)

LOGO_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 100" width="420" height="100" role="img" aria-label="Mimac">'
    '<title>Mimac</title>'
    '<rect width="100" height="100" rx="22" fill="#11141B"/>'
    '<path d="M18 80V22L50 57 82 22V80" fill="none" stroke="#4FD1FF" stroke-width="15" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<text x="124" y="72" font-family="-apple-system, \'SF Pro Display\', Inter, system-ui, sans-serif" '
    'font-size="66" font-weight="700" letter-spacing="-2" fill="#F2F4F8">Mimac</text></svg>\n'
)


def icons():
    with open(out("favicon.svg"), "w") as f:
        f.write(MARK_SVG)
    with open(out("assets/press/mimac-mark.svg"), "w") as f:
        f.write(MARK_SVG)
    with open(out("assets/press/mimac-logo.svg"), "w") as f:
        f.write(LOGO_SVG)
    # ICO with 16/32/48
    frames = [mark_png(s) for s in (16, 32, 48)]
    frames[0].save(out("favicon.ico"), format="ICO", sizes=[(16, 16), (32, 32), (48, 48)],
                   append_images=frames[1:])
    mark_png(180, glow=True).convert("RGB").save(out("apple-touch-icon.png"), optimize=True)
    mark_png(1024, glow=True).convert("RGB").save(out("assets/press/mimac-icon-1024.png"), optimize=True)
    mark_png(512, glow=True).convert("RGB").save(out("assets/press/mimac-icon-512.png"), optimize=True)
    # Wordmarks (transparent background): light-on-dark and dark-on-light, 2x
    for name, color, tile_bg in (("mimac-wordmark-on-dark.png", FG, BG2), ("mimac-wordmark-on-light.png", (11, 13, 18), (11, 13, 18))):
        ss = 2
        f = font(132 * ss, "Bold")
        tw = int(f.getlength("Mimac"))
        H = 200 * ss
        img = Image.new("RGBA", (H + 48 * ss + tw + 20 * ss, H), (0, 0, 0, 0))
        m = mark_png(H, glow=False, bg=tile_bg)
        img.alpha_composite(m, (0, 0))
        d = ImageDraw.Draw(img)
        d.text((H + 44 * ss, H * 0.5), "Mimac", font=f, fill=color, anchor="lm")
        img = img.resize((img.width // 2, img.height // 2), Image.LANCZOS)
        img.save(out("assets/press/" + name), optimize=True)


# ---------------------------------------------------------------- Open Graph images
def wrap(text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if f.getlength(t) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def og(name, title, subtitle):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), BG)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([700, -420, 1500, 380], fill=ACCENT + (46,))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = Image.alpha_composite(img.convert("RGBA"), glow)
    d = ImageDraw.Draw(img)
    d.line([(0, H - 1), (W, H - 1)], fill=(30, 34, 44), width=2)
    img.alpha_composite(mark_png(64), (72, 64))
    d = ImageDraw.Draw(img)
    d.text((156, 96), "Mimac", font=font(40, "Bold"), fill=FG, anchor="lm")
    tf = font(64, "Bold")
    lines = wrap(title, tf, 1000)[:3]
    y = 236
    for ln in lines:
        d.text((72, y), ln, font=tf, fill=FG)
        y += 78
    if subtitle:
        for ln in wrap(subtitle, font(30, "Regular"), 1000)[:2]:
            d.text((72, y + 14), ln, font=font(30, "Regular"), fill=FG2)
            y += 42
    d.text((W - 72, H - 64), "mimac.ai", font=font(28, "Semibold"), fill=FG2, anchor="rm")
    img = img.convert("RGB").quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.FLOYDSTEINBERG)
    img.save(out("assets/og/%s.png" % name), optimize=True)


OG_PAGES = [
    ("home", "Your Mac, at 120 fps, on the iPad Pro.", "Remote desktop rebuilt for iPad Pro + Magic Keyboard. One purchase, forever."),
    ("mac", "Mimac Connect for Mac", "The free menu-bar host app. Apple silicon, macOS 15 or later."),
    ("pricing", "Free to try. $49.99 once.", "No subscription, no account. Every future update included."),
    ("compare-jump-desktop", "Mimac vs Jump Desktop", "An honest side-by-side for iPad Pro users with a Mac."),
    ("compare-workbench", "Mimac vs Astropad Workbench", "An honest side-by-side for headless Mac minis."),
    ("compare-screens", "Mimac vs Screens 5", "An honest side-by-side for iPad-to-Mac remote access."),
    ("compare-luna-display", "Mimac vs Luna Display", "Remote desktop or second display? The honest answer."),
    ("compare-splashtop", "Mimac vs Splashtop Personal", "An honest side-by-side for iPad-to-Mac remote access."),
    ("guide-headless-mac-mini-ipad-pro", "Headless Mac mini with an iPad Pro", "Step-by-step setup, no monitor required."),
    ("guide-remote-mac-with-tailscale", "Reach your Mac from anywhere with Tailscale", "Off-LAN setup for Mimac, step by step."),
    ("guide-magic-keyboard-shortcuts", "Magic Keyboard shortcuts in Mimac", "Which chords go to the Mac and which stay on the iPad."),
    ("guide-mac-mini-for-ai-agents", "A Mac mini for AI agents, driven from an iPad", "Screenshots to clipboard, dictation, start before login."),
    ("support", "Mimac Support", "Requirements, FAQ, known limitations, and how to reach us."),
    ("privacy", "Mimac Privacy Policy", "No accounts, no servers, no analytics."),
    ("press", "Mimac Press Kit", "Logo, icon, descriptions and the build story."),
]


# ---------------------------------------------------------------- device frame (perspective)
CY = 24.0       # camera height above the keyboard deck, cm
F = 5000.0      # focal length, px
ZP = 100.0      # iPad glass plane distance, cm


def proj(x, y, z):
    return (F * x / z, -F * (y - CY) / z)


def rrect_path(x, y, w, h, r):
    return ("M%.1f %.1f H%.1f A%.1f %.1f 0 0 1 %.1f %.1f V%.1f A%.1f %.1f 0 0 1 %.1f %.1f H%.1f "
            "A%.1f %.1f 0 0 1 %.1f %.1f V%.1f A%.1f %.1f 0 0 1 %.1f %.1f Z" % (
                x + r, y, x + w - r, r, r, x + w, y + r, y + h - r, r, r, x + w - r, y + h,
                x + r, r, r, x, y + h - r, y + r, r, r, x + r, y))


def frame_svg():
    pad_w, pad_h = 28.16, 21.55
    pad_y0 = 2.4
    bezel = 0.84
    scr_w, scr_h = pad_w - 2 * bezel, pad_h - 2 * bezel
    base_w, base_d, base_t = 28.6, 22.0, 0.62
    z_rear, z_front = ZP + 2.2, ZP + 2.2 - base_d

    # projected iPad rectangle (front-facing plane => a true rectangle)
    (px0, py_top) = proj(-pad_w / 2, pad_y0 + pad_h, ZP)
    (px1, py_bot) = proj(pad_w / 2, pad_y0, ZP)
    # keyboard front edge
    (_, y_front) = proj(0, -base_t, z_front)
    margin = 40
    ox = 800.0
    oy = -py_top + margin
    W = 1600
    Hfull = int(y_front + oy + margin)
    # crop the front of the deck with a fade; keep the trackpad partly visible
    H = int(min(Hfull, (py_bot + oy) + 0.5 * (y_front - py_bot)))

    def P(x, y, z):
        X, Y = proj(x, y, z)
        return (X + ox, Y + oy)

    def poly(pts, fill, extra=""):
        return '<polygon points="%s" fill="%s"%s/>' % (
            " ".join("%.1f,%.1f" % p for p in pts), fill, extra)

    parts = []
    parts.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">' % (W, H, W, H))
    parts.append('<defs>'
                 '<linearGradient id="fade" gradientUnits="userSpaceOnUse" x1="0" y1="%.0f" x2="0" y2="%.0f">'
                 '<stop offset="0" stop-color="#fff"/><stop offset="0.62" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                 '<mask id="fm"><rect x="0" y="0" width="%d" height="%d" fill="url(#fade)"/></mask>'
                 '<linearGradient id="rim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3B404B"/><stop offset="1" stop-color="#1B1E25"/></linearGradient>'
                 '<linearGradient id="deck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2F333C"/><stop offset="1" stop-color="#1E2128"/></linearGradient>'
                 '<filter id="blur" x="-20%%" y="-50%%" width="140%%" height="200%%"><feGaussianBlur stdDeviation="22"/></filter>'
                 '</defs>' % (py_bot + oy, H, W, H))

    # --- keyboard deck (masked so it fades toward the viewer)
    kb = []
    deck_top = [P(-base_w / 2, 0, z_rear), P(base_w / 2, 0, z_rear), P(base_w / 2, 0, z_front), P(-base_w / 2, 0, z_front)]
    kb.append(poly(deck_top, "url(#deck)"))
    front_face = [P(-base_w / 2, 0, z_front), P(base_w / 2, 0, z_front), P(base_w / 2, -base_t, z_front), P(-base_w / 2, -base_t, z_front)]
    kb.append(poly(front_face, "#111318"))
    # shadow of the floating iPad on the deck
    sx0, sy0 = P(-pad_w / 2 + 1, 0, ZP - 0.5)
    sx1, sy1 = P(pad_w / 2 - 1, 0, ZP - 6)
    kb.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#000" opacity="0.55" filter="url(#blur)"/>' % (
        (sx0 + sx1) / 2, (sy0 + sy1) / 2, (sx1 - sx0) / 2, max(14, (sy1 - sy0) / 2)))
    # keys
    pitch = 26.6 / 14.5
    gap = 0.22
    rows = [
        (0.58, [1.036] * 14),
        (1.0, [1] * 13 + [1.5]),
        (1.0, [1.5] + [1] * 12 + [1]),
        (1.0, [1.75] + [1] * 11 + [1.75]),
        (1.0, [2.25] + [1] * 10 + [2.25]),
        (1.0, [1, 1, 1, 1.25, 5.0, 1.25, 1, 1, 1, 1]),
    ]
    z = z_rear - 1.7
    for hfrac, widths in rows:
        depth = pitch * hfrac
        x = -sum(widths) * pitch / 2
        for wu in widths:
            w = wu * pitch
            q = [P(x + gap / 2, 0.16, z), P(x + w - gap / 2, 0.16, z), P(x + w - gap / 2, 0.16, z - depth + gap), P(x + gap / 2, 0.16, z - depth + gap)]
            kb.append(poly(q, "#363A44"))
            x += w
        z -= depth
    # trackpad
    tz0 = z - 0.5
    tp = [P(-5.9, 0.05, tz0), P(5.9, 0.05, tz0), P(5.9, 0.05, tz0 - 6.2), P(-5.9, 0.05, tz0 - 6.2)]
    kb.append(poly(tp, "#282C35", ' stroke="#3A3E48" stroke-width="1"'))
    # hinge bar along the rear edge and the arm rising to the iPad
    hinge = [P(-13.9, 0, z_rear), P(13.9, 0, z_rear), P(13.9, 1.1, z_rear - 0.8), P(-13.9, 1.1, z_rear - 0.8)]
    kb.append(poly(hinge, "#1A1D23"))
    arm = [P(-13.4, 1.1, z_rear - 0.8), P(13.4, 1.1, z_rear - 0.8), P(13.4, pad_y0 + 0.2, ZP + 0.4), P(-13.4, pad_y0 + 0.2, ZP + 0.4)]
    kb.append(poly(arm, "#15181E"))
    parts.append('<g mask="url(#fm)">%s</g>' % "".join(kb))

    # --- iPad body with a transparent screen cutout
    bx, by = px0 + ox, py_top + oy
    bw, bh = px1 - px0, py_bot - py_top
    sx, sy = bx + bezel / pad_w * bw, by + bezel / pad_h * bh
    sw, sh = scr_w / pad_w * bw, scr_h / pad_h * bh
    parts.append('<path fill-rule="evenodd" fill="url(#rim)" d="%s %s"/>' % (
        rrect_path(bx - 6, by - 6, bw + 12, bh + 12, 92), rrect_path(bx, by, bw, bh, 86)))
    parts.append('<path fill-rule="evenodd" fill="#0A0B0E" d="%s %s"/>' % (
        rrect_path(bx, by, bw, bh, 86), rrect_path(sx, sy, sw, sh, 40)))
    # camera dot (landscape: on the long edge, top center)
    parts.append('<circle cx="%.0f" cy="%.0f" r="5" fill="#1C2029"/>' % (bx + bw / 2, by + (sy - by) / 2))
    parts.append('</svg>\n')
    with open(out("assets/img/ipad-frame.svg"), "w") as f:
        f.write("".join(parts))
    # Screen cutout as percentages of the frame box, for the CSS
    print("frame %dx%d  screen: left %.3f%% top %.3f%% width %.3f%% height %.3f%%  aspect %.4f" % (
        W, H, sx / W * 100, sy / H * 100, sw / W * 100, sh / H * 100, sw / sh))


if __name__ == "__main__":
    icons()
    for name, title, sub in OG_PAGES:
        og(name, title, sub)
    frame_svg()
    print("ok")
