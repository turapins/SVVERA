#!/usr/bin/env python3
"""Render burned-in captions as PNGs plus a single alpha overlay track.

Needed because this ffmpeg build has no drawtext/subtitles/ass filter.
Input: stt.json from ElevenLabs Scribe (timestamps_granularity=word).
Output: subs/*.png, caps.txt — then
    ffmpeg -f concat -safe 0 -i caps.txt -c:v png -pix_fmt rgba -r 24 caps.mov
"""
import json, os
from PIL import Image, ImageDraw, ImageFont

# ── CONFIG ────────────────────────────────────────────────────────────────────
STT   = "stt.json"
OUTD  = "subs"
W, H  = 480, 854
FONT  = os.path.expanduser("~/Library/Fonts/Montserrat-ExtraBold.ttf")
SIZE  = 29                       # ≈6% of frame width
FILL  = (250,186,32,255)         # amber; (255,255,255,255) with PILL for the neutral look
OUTLINE = (20,16,0,255)
PILL  = None                     # or (0,0,0,200) when captions sit over a busy banner
BASE_Y, GAP, MAXW = 612, 5, W-70
PAD_X, PAD_Y = 18, 11
GAPLESS = True                   # hold each caption until the next one starts
# ──────────────────────────────────────────────────────────────────────────────

f = ImageFont.truetype(FONT, SIZE)
os.makedirs(OUTD, exist_ok=True)
words = [w for w in json.load(open(STT))["words"] if w.get("type") == "word"]

DANGLING = {"and","or","but","so","that","who","which","what","when","where","while",
  "the","a","an","to","of","in","on","at","for","with","from","by","as","if","into",
  "it","is","was","are","were","be","been","has","have","had","will","would","can",
  "could","should","he","she","they","we","you","i","her","his","their","its","my",
  "your","this","these","those","not","just","back","then","because","every","any",
  "some","no","up","out","off","down","one","more","very","like"}

groups, cur = [], []
for w in words:
    cur.append(w)
    raw  = w["text"].strip()
    span = cur[-1]["end"] - cur[0]["start"]
    hard    = raw.endswith((".","!","?"))          # a sentence ends: always break
    ceiling = len(cur) >= 7 or span >= 2.8         # never let a caption run long
    comma   = raw.endswith(",") and len(cur) >= 2
    full    = len(cur) >= 5 or span >= 2.0
    if hard or ceiling or ((comma or full) and raw.rstrip(".,!?").lower() not in DANGLING):
        groups.append(cur); cur = []
if cur: groups.append(cur)

merged = []                                        # fold away anything too short to read
for g in groups:
    dur = g[-1]["end"] - g[0]["start"]
    if merged and (dur < 0.62 or len(g) < 2) \
       and g[-1]["end"]-merged[-1][0]["start"] <= 3.4 and len(merged[-1])+len(g) <= 9:
        merged[-1] = merged[-1] + g
    else:
        merged.append(g)
groups = merged

def wrap(text):
    out, line = [], ""
    for w in text.split():
        t = (line+" "+w).strip()
        if f.getbbox(t)[2]-f.getbbox(t)[0] > MAXW and line:
            out.append(line); line = w
        else: line = t
    if line: out.append(line)
    return out[:2]

Image.new("RGBA",(W,H),(0,0,0,0)).save(f"{OUTD}/_blank.png")
entries = []
for n,g in enumerate(groups):
    lines = wrap(" ".join(x["text"] for x in g).strip().replace("  "," ").upper())
    im = Image.new("RGBA",(W,H),(0,0,0,0)); dr = ImageDraw.Draw(im)
    hs = [f.getbbox(l)[3]-f.getbbox(l)[1] for l in lines]
    ws = [f.getbbox(l)[2]-f.getbbox(l)[0] for l in lines]
    block_h = sum(hs)+GAP*(len(lines)-1); top = BASE_Y-block_h//2
    if PILL:
        bw = max(ws)+PAD_X*2
        dr.rounded_rectangle([(W-bw)//2, top-PAD_Y, (W+bw)//2, top+block_h+PAD_Y],
                             radius=13, fill=PILL)
    y = top
    for l,hh,ww in zip(lines,hs,ws):
        x, yy = (W-ww)//2, y-f.getbbox(l)[1]
        dr.text((x+2,yy+2), l, font=f, fill=(0,0,0,120), stroke_width=3,
                stroke_fill=(0,0,0,120))
        dr.text((x,yy), l, font=f, fill=FILL, stroke_width=3, stroke_fill=OUTLINE)
        y += hh+GAP
    p = f"{OUTD}/c{n:03d}.png"; im.save(p)
    entries.append([g[0]["start"], g[-1]["end"], p])

if GAPLESS:
    for i in range(len(entries)-1):
        entries[i][1] = entries[i+1][0]

lines, t = [], 0.0
for st,en,p in entries:
    st = max(st,t); en = max(en, st+0.4)
    if st-t > 0.02:
        lines += [f"file '{OUTD}/_blank.png'", f"duration {st-t:.3f}"]
    lines += [f"file '{p}'", f"duration {en-st:.3f}"]
    t = en
lines += [f"file '{OUTD}/_blank.png'", "duration 6.0", f"file '{OUTD}/_blank.png'"]
open("caps.txt","w").write("\n".join(lines)+"\n")
print(f"{len(entries)} captions, last ends {t:.2f}s -> caps.txt")
