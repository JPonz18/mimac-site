#!/usr/bin/env python3
"""Generates the abstract macOS "desktop" scenes shown inside the SVG device
frame until real iPad captures exist. 1376x1032 points (4:3, same aspect as
the 13" iPad Pro at 2752x2064). Deliberately abstract: bars instead of text,
so nobody mistakes them for real screenshots.

Run:  python3 tools/make-scenes.py
"""
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1376, 1032
ACC = "#4FD1FF"
FONT = "-apple-system, 'SF Pro Text', Inter, system-ui, sans-serif"


def out(name, body):
    p = os.path.join(ROOT, "assets", "img", name)
    with open(p, "w") as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d">' % (W, H, W, H))
        f.write('<defs>'
                '<linearGradient id="wp" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#121A2A"/><stop offset="1" stop-color="#05070B"/></linearGradient>'
                '<radialGradient id="glow" cx="0.72" cy="0.2" r="0.6"><stop offset="0" stop-color="%s" stop-opacity="0.32"/><stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
                '<radialGradient id="glow2" cx="0.15" cy="0.95" r="0.5"><stop offset="0" stop-color="#2B5BFF" stop-opacity="0.22"/><stop offset="1" stop-color="#2B5BFF" stop-opacity="0"/></radialGradient>'
                '<filter id="sh" x="-10%%" y="-10%%" width="120%%" height="130%%"><feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="#000" flood-opacity="0.55"/></filter>'
                '<filter id="soft" x="-20%%" y="-20%%" width="140%%" height="140%%"><feGaussianBlur stdDeviation="14"/></filter>'
                '<linearGradient id="av" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="#2B5BFF"/></linearGradient>'
                '</defs>' % (ACC, ACC, ACC))
        f.write(body)
        f.write('</svg>\n')
    print("wrote", p, os.path.getsize(p), "bytes")


def rr(x, y, w, h, r, fill, extra=""):
    return '<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f" fill="%s"%s/>' % (x, y, w, h, r, fill, extra)


def wallpaper():
    return (rr(0, 0, W, H, 0, "url(#wp)") + rr(0, 0, W, H, 0, "url(#glow)") + rr(0, 0, W, H, 0, "url(#glow2)"))


def menubar(mic=False, dim=False):
    s = rr(0, 0, W, 28, 0, "#161A22", ' opacity="0.92"')
    # left: app name + menus as bars
    s += rr(20, 11, 14, 7, 3, "#C9CED8")  # stand-in for the menu-bar logo slot
    x = 52
    for wdt, col in ((54, "#E6E9EF"), (34, "#8B93A2"), (40, "#8B93A2"), (30, "#8B93A2"), (46, "#8B93A2"), (38, "#8B93A2")):
        s += rr(x, 11, wdt, 7, 3, col)
        x += wdt + 22
    # right: status items
    x = W - 24
    for wdt in (46, 12, 12, 16, 12):
        x -= wdt
        s += rr(x, 10, wdt, 8, 3, "#8B93A2")
        x -= 16
    if mic:
        s += '<circle cx="%d" cy="14" r="5" fill="%s"/>' % (x - 6, ACC)
    return s


def window(x, y, w, h, kind, seed=1, active=True):
    rnd = random.Random(seed)
    s = '<g filter="url(#sh)">' + rr(x, y, w, h, 12, "#14171F") + '</g>'
    s += rr(x, y, w, 40, 12, "#1F232C") + rr(x, y + 28, w, 12, 0, "#1F232C")
    s += '<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="none" stroke="#FFFFFF" stroke-opacity="0.08"/>' % (x, y, w, h)
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        s += '<circle cx="%d" cy="%d" r="6" fill="%s"/>' % (x + 20 + i * 20, y + 20, c if active else "#3A3F4A")
    s += rr(x + w / 2 - 60, y + 16, 120, 8, 4, "#5A6170")
    bx, by, bw, bh = x, y + 40, w, h - 40
    if kind == "code":
        s += rr(bx, by, 190, bh, 0, "#0F1218")
        # file list
        for i in range(12):
            s += rr(bx + 22, by + 26 + i * 26, 60 + (i * 37) % 80, 8, 4, "#3C4350" if i != 3 else "#8B93A2")
        # code lines
        cols = [ACC, "#9AA4B2", "#E3B341", "#7EE787", "#C792EA"]
        for i in range(int((bh - 40) / 24)):
            s += rr(bx + 208, by + 24 + i * 24, 18, 8, 4, "#3C4350")
            xx = bx + 244 + (rnd.choice((0, 0, 24, 48, 72)))
            for j in range(rnd.randint(2, 6)):
                wdt = rnd.randint(30, 140)
                if xx + wdt > bx + bw - 40:
                    break
                col = rnd.choice(cols)
                s += rr(xx, by + 24 + i * 24, wdt, 8, 4, col, ' opacity="%.2f"' % (0.55 + rnd.random() * 0.4))
                xx += wdt + 14
    elif kind == "terminal":
        s += rr(bx, by, bw, bh, 0, "#0B0D12")
        s += rr(bx, by + bh - 12, bw, 12, 12, "#0B0D12")
        yy = by + 22
        for i in range(int((bh - 40) / 22)):
            if i % 5 == 0:
                s += rr(bx + 22, yy, 10, 8, 3, "#7EE787")
                s += rr(bx + 40, yy, rnd.randint(120, 300), 8, 4, "#C9CED8")
            else:
                s += rr(bx + 22, yy, rnd.randint(80, bw - 80), 8, 4, "#5A6170")
            yy += 22
        s += rr(bx + 22, yy, 10, 14, 2, ACC)
    elif kind == "canvas":
        s += rr(bx, by, 220, bh, 0, "#111419")
        s += rr(bx + bw - 240, by, 240, bh, 0, "#111419")
        for i in range(14):
            s += rr(bx + 24, by + 24 + i * 28, 40 + (i * 53) % 120, 8, 4, "#3C4350")
        for i in range(10):
            s += rr(bx + bw - 216, by + 24 + i * 40, 90, 8, 4, "#3C4350")
            s += rr(bx + bw - 110, by + 24 + i * 40, 70, 8, 4, "#2A2F3A")
        cx0, cy0 = bx + 220, by
        cw, ch = bw - 460, bh
        s += rr(cx0, cy0, cw, ch, 0, "#1B1F27")
        # frames on the canvas
        frames = [(60, 60, 300, 220), (420, 60, 260, 380), (60, 320, 300, 200), (420, 480, 260, 120)]
        for i, (fx, fy, fw, fh) in enumerate(frames):
            if fx + fw > cw - 30 or fy + fh > ch - 30:
                continue
            s += rr(cx0 + fx, cy0 + fy, fw, fh, 8, "#F2F4F8" if i == 0 else "#2A2F3A")
            s += rr(cx0 + fx + 20, cy0 + fy + 20, fw * 0.5, 10, 5, "#0B0D12" if i == 0 else "#4B5260")
            s += rr(cx0 + fx + 20, cy0 + fy + 44, fw * 0.7, 8, 4, "#9AA4B2" if i == 0 else "#3C4350")
            if i == 0:
                s += '<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="2"/>' % (cx0 + fx, cy0 + fy, fw, fh, ACC)
                for hx, hy in ((0, 0), (fw, 0), (0, fh), (fw, fh)):
                    s += rr(cx0 + fx + hx - 5, cy0 + fy + hy - 5, 10, 10, 2, "#fff", ' stroke="%s" stroke-width="2"' % ACC)
    elif kind == "chat":
        s += rr(bx, by, bw, bh, 0, "#14171F")
        yy = by + 24
        for i in range(5):
            mine = i % 2 == 1
            mw = rnd.randint(200, min(360, bw - 60))
            mh = 46 if i != 2 else 130
            xx = bx + bw - 24 - mw if mine else bx + 24
            s += rr(xx, yy, mw, mh, 14, "#2A2F3A" if not mine else "#1B3A4A")
            if i == 2:
                # a pasted screenshot thumbnail
                s += rr(xx + 14, yy + 14, mw - 28, 70, 6, "#0B0D12", ' stroke="%s" stroke-opacity="0.6"' % ACC)
                s += rr(xx + 26, yy + 26, (mw - 52) * 0.5, 6, 3, ACC, ' opacity="0.7"')
                s += rr(xx + 26, yy + 40, (mw - 52) * 0.8, 6, 3, "#5A6170")
                s += rr(xx + 26, yy + 54, (mw - 52) * 0.6, 6, 3, "#5A6170")
                s += rr(xx + 14, yy + 98, mw * 0.6, 8, 4, "#C9CED8")
            else:
                s += rr(xx + 16, yy + 14, mw * 0.7, 8, 4, "#C9CED8")
                s += rr(xx + 16, yy + 28, mw * 0.45, 8, 4, "#8B93A2")
            yy += mh + 16
        s += rr(bx + 24, by + bh - 60, bw - 48, 40, 20, "#1F232C", ' stroke="#FFFFFF" stroke-opacity="0.08"')
        s += rr(bx + 44, by + bh - 44, 120, 8, 4, "#5A6170")
    elif kind == "text":
        s += rr(bx, by, bw, bh, 0, "#F7F7F9")
        s += rr(bx, by + bh - 12, bw, 12, 12, "#F7F7F9")
        yy = by + 40
        s += rr(bx + 60, yy, 300, 14, 6, "#1B1E25")
        yy += 40
        for i in range(12):
            wdt = bw - 120 if i % 4 != 3 else (bw - 120) * 0.55
            s += rr(bx + 60, yy, wdt, 9, 4, "#8B93A2" if i < 9 else "#B4BAC6")
            yy += 24
    return s


def dock(dim=False):
    n = 10
    size, gap = 52, 14
    total = n * size + (n - 1) * gap + 60
    x0 = (W - total) / 2
    y = H - 84
    s = rr(x0, y - 14, total, size + 28, 22, "#1E222B", ' opacity="0.85" stroke="#FFFFFF" stroke-opacity="0.1"')
    cols = ["#2E9BFF", "#8B93A2", "#7EE787", "#FF7A59", "#C792EA", ACC, "#E3B341", "#4B5260", "#FF5F57", "#5A6170"]
    for i in range(n):
        x = x0 + 30 + i * (size + gap)
        s += rr(x, y, size, size, 13, cols[i])
        s += rr(x + 12, y + 12, size - 24, size - 24, 7, "#0B0D12", ' opacity="0.35"')
    return s


def scene_desktop():
    return wallpaper() + window(40, 60, 820, 700, "code", seed=3) + window(900, 60, 436, 420, "chat", seed=5) + window(620, 520, 716, 400, "terminal", seed=7) + dock() + menubar()


def scene_switcher():
    s = scene_desktop()
    s += rr(0, 0, W, H, 0, "#000", ' opacity="0.42"')
    pw, ph = 760, 190
    px, py = (W - pw) / 2, (H - ph) / 2 - 40
    s += '<g filter="url(#sh)">' + rr(px, py, pw, ph, 26, "#1E222B", ' opacity="0.97" stroke="#FFFFFF" stroke-opacity="0.12"') + '</g>'
    cols = ["#2E9BFF", "#7EE787", ACC, "#C792EA", "#E3B341", "#FF7A59"]
    n = 6
    size, gap = 84, 28
    x = px + (pw - (n * size + (n - 1) * gap)) / 2
    for i in range(n):
        if i == 2:
            s += rr(x - 14, py + 24, size + 28, 142, 18, "#FFFFFF", ' opacity="0.12"')
        s += rr(x, py + 40, size, size, 20, cols[i])
        s += rr(x + 20, py + 60, size - 40, size - 40, 10, "#0B0D12", ' opacity="0.35"')
        s += rr(x + size / 2 - 26, py + 140, 52, 8, 4, "#E6E9EF" if i == 2 else "#5A6170")
        x += size + gap
    return s


def scene_pinch():
    s = wallpaper() + window(30, 50, W - 60, H - 130, "canvas", seed=11) + dock() + menubar()
    # two touch points spreading apart
    for cx, cy, dx in ((560, 520, -1), (760, 440, 1)):
        s += '<circle cx="%d" cy="%d" r="34" fill="%s" fill-opacity="0.16" stroke="%s" stroke-opacity="0.9" stroke-width="3"/>' % (cx, cy, ACC, ACC)
        s += '<circle cx="%d" cy="%d" r="8" fill="%s"/>' % (cx, cy, ACC)
        ax = cx + dx * 60
        s += '<path d="M%d %d L%d %d" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-opacity="0.8"/>' % (cx + dx * 44, cy - dx * 18, ax + dx * 30, cy - dx * 40, ACC)
    return s


def scene_login():
    s = wallpaper()
    s += '<circle cx="%d" cy="%d" r="330" fill="%s" fill-opacity="0.10" filter="url(#soft)"/>' % (W / 2, H / 2 - 40, ACC)
    # clock
    s += rr(W / 2 - 90, 90, 180, 34, 10, "#E6E9EF", ' opacity="0.9"')
    s += rr(W / 2 - 40, 140, 80, 10, 5, "#8B93A2")
    # avatar
    s += '<clipPath id="avc"><circle cx="%d" cy="%d" r="72"/></clipPath>' % (W / 2, H / 2 - 40)
    s += '<circle cx="%d" cy="%d" r="72" fill="url(#av)"/>' % (W / 2, H / 2 - 40)
    s += '<g clip-path="url(#avc)" fill="#0B0D12" opacity="0.45"><circle cx="%d" cy="%d" r="26"/><ellipse cx="%d" cy="%d" rx="52" ry="44"/></g>' % (W / 2, H / 2 - 62, W / 2, H / 2 + 24)
    s += rr(W / 2 - 60, H / 2 + 52, 120, 12, 6, "#E6E9EF")
    # password pill
    s += rr(W / 2 - 150, H / 2 + 92, 300, 44, 22, "#FFFFFF", ' opacity="0.14" stroke="#FFFFFF" stroke-opacity="0.2"')
    for i in range(6):
        s += '<circle cx="%d" cy="%d" r="4" fill="#E6E9EF"/>' % (W / 2 - 110 + i * 16, H / 2 + 114)
    s += '<circle cx="%d" cy="%d" r="14" fill="#FFFFFF" opacity="0.25"/>' % (W / 2 + 120, H / 2 + 114)
    # footer buttons
    for i in range(3):
        s += '<circle cx="%d" cy="%d" r="18" fill="#FFFFFF" opacity="0.12"/>' % (W / 2 - 80 + i * 80, H - 90)
        s += rr(W / 2 - 100 + i * 80, H - 58, 40, 7, 3, "#8B93A2")
    return s


def scene_dictation():
    s = wallpaper() + window(80, 70, 900, 800, "text", seed=21) + dock() + menubar(mic=True)
    # caret + live waveform pill near the current line
    s += rr(80 + 60 + 300, 70 + 40 + 40 + 9 * 24 - 4, 3, 18, 1, ACC)
    px, py = 80 + 60 + 320, 70 + 40 + 40 + 9 * 24 - 30
    s += '<g filter="url(#sh)">' + rr(px, py, 190, 44, 22, "#1E222B", ' stroke="#FFFFFF" stroke-opacity="0.12"') + '</g>'
    s += '<circle cx="%d" cy="%d" r="7" fill="%s"/>' % (px + 24, py + 22, ACC)
    rnd = random.Random(4)
    for i in range(22):
        h = rnd.randint(6, 26)
        s += rr(px + 46 + i * 6, py + 22 - h / 2, 3, h, 1.5, ACC, ' opacity="0.85"')
    # small "Sound input" panel with the Mimac Microphone row selected
    wx, wy, ww = 1000, 560, 336
    s += '<g filter="url(#sh)">' + rr(wx, wy, ww, 240, 14, "#1E222B", ' stroke="#FFFFFF" stroke-opacity="0.1"') + '</g>'
    s += '<text x="%d" y="%d" font-family="%s" font-size="13" font-weight="600" fill="#9AA4B2">Input</text>' % (wx + 18, wy + 30, FONT)
    rows = ("iPad Pro Microphone", "Mimac Microphone", "Studio Display Microphone")
    for i, name in enumerate(rows):
        ry = wy + 48 + i * 56
        if i == 1:
            s += rr(wx + 10, ry - 6, ww - 20, 48, 10, ACC, ' opacity="0.16"')
        s += '<circle cx="%d" cy="%d" r="12" fill="%s"/>' % (wx + 34, ry + 18, ACC if i == 1 else "#3C4350")
        s += '<text x="%d" y="%d" font-family="%s" font-size="15" font-weight="%s" fill="%s">%s</text>' % (
            wx + 58, ry + 23, FONT, "600" if i == 1 else "400", "#F2F4F8" if i == 1 else "#8B93A2", name)
    return s


def scene_agents():
    s = wallpaper() + window(40, 60, 640, 860, "terminal", seed=31) + window(720, 60, 616, 500, "chat", seed=33) + window(720, 600, 616, 320, "terminal", seed=35) + dock() + menubar()
    # screenshot marquee being dragged over the terminal
    s += '<rect x="90" y="300" width="500" height="260" fill="%s" fill-opacity="0.10" stroke="%s" stroke-width="2" stroke-dasharray="8 6"/>' % (ACC, ACC)
    for hx, hy in ((90, 300), (590, 300), (90, 560), (590, 560)):
        s += rr(hx - 5, hy - 5, 10, 10, 2, "#fff", ' stroke="%s" stroke-width="2"' % ACC)
    s += rr(600, 566, 160, 30, 15, "#1E222B", ' stroke="#FFFFFF" stroke-opacity="0.12"')
    s += '<text x="%d" y="%d" font-family="%s" font-size="13" fill="#E6E9EF">1000 × 520 · Copied</text>' % (614, 586, FONT)
    return s


def scene_connect():
    """The Mimac connect screen: host list and a pairing code prompt."""
    s = wallpaper()
    s += '<circle cx="%d" cy="%d" r="380" fill="%s" fill-opacity="0.12" filter="url(#soft)"/>' % (W / 2, H / 2, ACC)
    px, py, pw, ph = W / 2 - 250, H / 2 - 180, 500, 360
    s += '<g filter="url(#sh)">' + rr(px, py, pw, ph, 28, "#1E222B", ' opacity="0.97" stroke="#FFFFFF" stroke-opacity="0.12"') + '</g>'
    s += rr(px + 40, py + 40, 200, 14, 7, "#E6E9EF")
    s += rr(px + 40, py + 70, 300, 9, 4, "#5A6170")
    for i in range(2):
        ry = py + 110 + i * 70
        s += rr(px + 40, ry, pw - 80, 56, 14, "#FFFFFF", ' opacity="%s"' % ("0.10" if i == 0 else "0.05"))
        s += '<circle cx="%d" cy="%d" r="6" fill="%s"/>' % (px + 64, ry + 28, "#7EE787" if i == 0 else "#5A6170")
        s += rr(px + 84, ry + 18, 140 - i * 30, 9, 4, "#E6E9EF")
        s += rr(px + 84, ry + 34, 180 - i * 40, 7, 3, "#8B93A2")
    s += rr(px + 40, py + ph - 76, pw - 80, 48, 24, ACC)
    s += rr(px + pw / 2 - 40, py + ph - 57, 80, 10, 5, "#052433")
    return s


if __name__ == "__main__":
    out("scene-desktop.svg", scene_desktop())
    out("scene-switcher.svg", scene_switcher())
    out("scene-pinch.svg", scene_pinch())
    out("scene-login.svg", scene_login())
    out("scene-dictation.svg", scene_dictation())
    out("scene-agents.svg", scene_agents())
    out("scene-connect.svg", scene_connect())
