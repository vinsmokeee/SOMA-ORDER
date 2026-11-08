#!/usr/bin/env python3
"""Build the standalone SOMA website into docs/ (served by GitHub Pages).

index.html is written as a page fragment (that is how the Claude version publishes it).
This wraps it in a full HTML document, adds the Firebase library, the app manifest and
offline support, and copies the files the site needs.

Run:  python3 build.py
"""
import hashlib, pathlib, re, shutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "docs"
FIREBASE = "10.12.2"

src = (ROOT / "index.html").read_text(encoding="utf-8")
# The fragment starts with <title>, <meta>, <link> and <style>; those belong in <head>.
split = src.index('<div class="wrap">')
head_part, body_part = src[:split].strip(), src[split:].strip()

sdk = "\n".join(
    f'<script src="https://www.gstatic.com/firebasejs/{FIREBASE}/firebase-{m}-compat.js"></script>'
    for m in ("app", "auth", "firestore")
)
page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#f4f5f6" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b0c0e" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="SOMA">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" href="assets/icon-192.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
{head_part}
{sdk}
<script src="firebase-config.js"></script>
<script>if ("serviceWorker" in navigator) addEventListener("load", () => navigator.serviceWorker.register("sw.js"));</script>
</head>
<body>
{body_part}
</body>
</html>
"""

if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "assets").mkdir(parents=True)
(OUT / "index.html").write_text(page, encoding="utf-8")
for f in (ROOT / "assets").iterdir():
    shutil.copy(f, OUT / "assets" / f.name)
for name in ("manifest.webmanifest", "firebase-config.js"):
    shutil.copy(ROOT / "web" / name, OUT / name)
# New cache name whenever the app changes, so phones pick up updates
stamp = hashlib.sha1((page + (ROOT / "web/firebase-config.js").read_text()).encode()).hexdigest()[:10]
(OUT / "sw.js").write_text((ROOT / "web/sw.js").read_text().replace("__BUILD__", stamp), encoding="utf-8")
(OUT / ".nojekyll").write_text("")
print(f"Built {OUT}/ (cache soma-{stamp})")
