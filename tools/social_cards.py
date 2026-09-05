#!/usr/bin/env python3
"""Build self-contained 1200×630 share-card HTML for browser PNG export.

Run with --output PATH, serve PATH locally, capture each page with a 1200×630
viewport after document.fonts.ready, and save to assets/social/<slug>.png.
This is an occasional asset-authoring step, not part of the regular site build.
"""
import argparse
import base64
import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from build import PAGES


def data_image(name):
    return 'data:image/png;base64,' + base64.b64encode((ROOT / 'assets' / name).read_bytes()).decode()


def card(slug, title):
    headline = 'Deep roots.<br><em>Open doors.</em>' if slug == 'index' else html.escape(title)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<title>{html.escape(title)} — share card</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bitter:ital,wght@0,600;1,500&family=Nunito+Sans:wght@600;800&display=swap">
<style>*{{box-sizing:border-box}}html,body{{margin:0;width:1200px;height:630px;overflow:hidden}}body{{background:#3C5A45;color:#F5EFE3;font-family:'Nunito Sans',sans-serif;padding:55px 64px;position:relative}}body::before{{content:'';position:absolute;inset:22px;border:1px solid #81917d}}header{{display:flex;justify-content:space-between;align-items:center}}header img{{width:266px;height:auto}}header span{{font-size:12px;letter-spacing:2px;font-weight:800;text-align:right;line-height:1.65}}h1{{font:600 86px/1.07 Bitter,Georgia,serif;letter-spacing:-4px;max-width:850px;position:relative;margin:61px 0 0;text-wrap:balance}}h1 em{{font-weight:500}}.creek{{position:absolute;width:720px;height:auto;right:-440px;top:260px;opacity:.75}}footer{{position:absolute;left:64px;right:64px;bottom:48px;display:flex;justify-content:space-between;border-top:1px solid #81917d;padding-top:20px;font-size:13px;font-weight:800;letter-spacing:1.2px}}footer span:last-child{{font-weight:600;letter-spacing:0}}</style></head>
<body><header><img src="{data_image('logo-white.png')}" alt="Bluff Creek Baptist Church"><span>A COUNTRY CHURCH<br>CLINTON, LOUISIANA</span></header><img class="creek" src="{data_image('creek-gold.png')}" alt=""><h1>{headline}</h1><footer><span>ROOTED IN THE WORD. GROWING TOGETHER.</span><span>bluffcreekbaptistchurch.org</span></footer></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for slug, (title, _, _) in PAGES.items():
        if slug != '404':
            (args.output / (slug + '.html')).write_text(card(slug, title), encoding='utf-8')
    print('Wrote 11 share-card source pages to', args.output)


if __name__ == '__main__':
    main()
