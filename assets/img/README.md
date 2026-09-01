# Image and video slots

Everything in this folder that starts with `scene-` or `ipad-frame` is generated placeholder art
(`tools/make-scenes.py`, `tools/make-assets.py`). The scenes are deliberately abstract: bars instead of
text, so nobody mistakes them for real screenshots. They are shown inside the SVG iPad Pro + Magic Keyboard
frame (`ipad-frame.svg`) and are meant to be replaced by real captures from the physical iPad.

The frame's screen cutout is 4:3 (1376×1032 points, i.e. 2752×2064 pixels on the 13" iPad Pro). Any
capture at the iPad's native resolution drops in without cropping. The `.device-screen` element uses
`object-fit: cover`, so an 11" capture (2420×1668, also very close to 4:3) works too.

## How to swap in a real screenshot

1. Capture on the physical iPad while connected (Command+Shift+3 on the Magic Keyboard is the Mac's
   screenshot; for a capture of the iPad's screen use the iPad's own top button + volume up).
2. Export two versions: `name@2x.webp` (2752×2064, quality ~80) and `name@1x.jpg` (1376×1032, quality ~82).
   Keep each under ~350 KB; the home page budget is 300 KB before video, so use the 1x JPEG as the
   default and the WebP in a `<picture>`:

   ```html
   <picture>
     <source srcset="/assets/img/shots/desktop@2x.webp 2x, /assets/img/shots/desktop@1x.webp 1x" type="image/webp">
     <img class="device-screen" src="/assets/img/shots/desktop@1x.jpg" width="1376" height="1032" alt="…" loading="lazy">
   </picture>
   ```
3. Put the files in `assets/img/shots/` and change the `src` in the page. Keep `width`, `height` and `alt`.

## Screenshot slots (2752×2064, landscape, from the physical 13" iPad Pro)

| Filename (in `assets/img/shots/`) | Replaces | Used on | What it should show |
|---|---|---|---|
| `desktop@2x.webp` / `desktop@1x.jpg` | `scene-desktop.svg` | Home hero (poster for the video) | A real macOS desktop with a code editor, a terminal and a browser or chat window. Menu bar visible, dock visible. This is the first thing people see. |
| `switcher@2x.webp` / `switcher@1x.jpg` | `scene-switcher.svg` | Home "Built for iPad Pro"; Magic Keyboard shortcuts guide | The Option+Tab switcher open over the desktop, with 5–7 real app icons and one selected. |
| `pinch@2x.webp` / `pinch@1x.jpg` | `scene-pinch.svg` | Home "Feels like a MacBook" | Figma, Photoshop or Maps mid-pinch: content visibly zoomed, ideally with the two-finger touch indicators. |
| `dictation@2x.webp` / `dictation@1x.jpg` | `scene-dictation.svg` | Home "Sound and voice" | A dictation app (Wispr Flow, OpenWhispr or macOS dictation) receiving text, with System Settings → Sound → Input showing "Mimac Microphone" selected. |
| `agents@2x.webp` / `agents@1x.jpg` | `scene-agents.svg` | Home "Headless Mac minis"; AI agents guide | Claude Code or Cursor running in a terminal, a chat window, and the screenshot marquee mid-drag with the "Copied" confirmation. |
| `login@2x.webp` / `login@1x.jpg` | `scene-login.svg` | Headless Mac mini guide | The macOS login window as seen through Mimac before anyone has logged in (proves start-before-login). |
| `connect@2x.webp` / `connect@1x.jpg` | `scene-connect.svg` | /mac/ page | Mimac's connect screen listing a Mac discovered on the LAN, and the pairing-code prompt. |
| `tuning@2x.webp` / `tuning@1x.jpg` | (new slot, not yet placed) | Home "Thirty tuning controls" card, App Store | The tuning panel open, showing the range of controls. Add it as a `.device` next to the cards when available. |

Also produce the same eight at 2420×1668 from an 11" iPad Pro if one is available (App Store needs both
sizes; the site does not).

## Video slots (10–20 s each, screen-recorded on the iPad at 60 fps, no audio needed)

iPadOS records at 60 fps; captions on the site already say "captured at 60 fps, Mimac runs at 120".
Export each as HEVC `.mov` (Safari) and H.264 `.mp4` (everything else), 2752×2064 or 1376×1032,
target 6–10 Mbps. Poster is the matching screenshot above.

| Files (in `assets/video/`) | Used on | Content |
|---|---|---|
| `hero.mov`, `hero.mp4` | Home hero `<video>` (already wired up: autoplay, muted, loop, playsinline) | Scroll a long document with momentum, pinch in Figma or Maps, Option+Tab to another app. Loop-friendly start and end. |
| `gestures.mov`, `gestures.mp4` | Home "Feels like a MacBook" (swap the `<img>` for a `<video>`; markup comment is in `index.html`) | Two-finger scroll with a flick, then pinch in and out. |
| `switcher.mov`, `switcher.mp4` | Home "Built for iPad Pro" (optional; the screenshot also works) | Option+Tab held, cycling through apps, release. |
| `resume.mov`, `resume.mp4` | Home "Headless Mac minis" (swap the `<img>`; comment in `index.html`) | Command+Tab away to another iPad app, wait a few seconds, come back: the desktop is there instantly. |

## Other slots

| File | Used on | What |
|---|---|---|
| `assets/img/latency-chart.svg` | /press/ (comment marks the spot), and the home proof strip once a number exists | Bar chart from MEASURING.md: median glass-to-glass latency, Mimac vs the incumbent, LAN, with the ±4 ms quantum in the caption. Do not put a millisecond number anywhere on the site before this exists. |
| Official App Store badge | Every "Download on the App Store" button | The buttons are plain text today. Drop Apple's official badge SVG from developer.apple.com/app-store/marketing/guidelines into `assets/img/appstore-badge.svg` and replace the button contents. Do not redraw the badge. |
| `assets/press/screenshots/*.png` | /press/ downloads | The eight screenshots above, unmodified 2752×2064 PNGs, for journalists. |
