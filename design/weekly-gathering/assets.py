#!/usr/bin/env python3
"""Lift the two supplied marks off their backgrounds and turn them into pure
   alpha masks, so the poster can paint them in its own metal."""
from PIL import Image, ImageFilter
import numpy as np, pathlib

HERE = pathlib.Path(__file__).parent
SRC  = pathlib.Path("/root/.claude/uploads/973b6c96-b51b-5a20-9967-a4a1762de681")

def crisp(mask, up=3):
    """Upscale the mask, then pull the edge back to a clean shoulder so the
       enlargement does not read as a blurred photocopy."""
    h, w = mask.shape
    im = Image.fromarray((mask*255).astype(np.uint8), "L")
    im = im.resize((w*up, h*up), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=up*0.8, percent=90, threshold=0))
    a = np.asarray(im).astype(float)/255.0
    # smoothstep either side of the 0.5 shoulder — vectorish edges from a raster
    lo, hi = 0.34, 0.68
    a = np.clip((a-lo)/(hi-lo), 0, 1)
    return a*a*(3-2*a)

def save_mask(a, path, target_w=None):
    if target_w and a.shape[1] != target_w:
        im = Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8), "L")
        h2 = round(im.height*target_w/im.width)
        a = np.asarray(im.resize((target_w, h2), Image.LANCZOS)).astype(float)/255.0
    h, w = a.shape
    rgba = np.zeros((h, w, 4), np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = (np.clip(a, 0, 1)*255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(path, optimize=True)
    print(path.name, (w, h))

# The ring carries the same name twice — English over the top, Arabic under.
# At poster size neither was legible, so the Latin half comes out and the
# Arabic keeps the ring to itself. The bullets at three and nine o'clock stay,
# capping the inscription; both circles that bound the band are untouched.
def strip_arc(m, a0, a1, r0=0.783, r1=0.952):
    h, w = m.shape
    cy, cx = (h-1)/2, (w-1)/2
    R = min(h, w)/2
    ys, xs = np.mgrid[0:h, 0:w]
    rad = np.hypot(xs-cx, ys-cy)/R
    ang = np.degrees(np.arctan2(xs-cx, -(ys-cy))) % 360      # 0 = twelve, clockwise
    within = (ang >= a0) if a0 > a1 else (ang >= a0) & (ang <= a1)
    if a0 > a1: within |= (ang <= a1)
    m[(rad >= r0) & (rad <= r1) & within] = 0.0
    return m

# ---- 1. the seal: gold on white ----------------------------------------
im = Image.open(SRC/"82803491-image.png").convert("RGB")
a  = np.asarray(im).astype(float)[681:1851]              # drop the black bars
d  = 255.0 - a.min(2)                                    # distance from white
d[d < 6] = 0
ys, xs = np.where(d > 14)
pad = 4
d = d[max(0, ys.min()-pad):ys.max()+pad, max(0, xs.min()-pad):xs.max()+pad]
seal = np.clip(d/np.percentile(d, 99.4), 0, 1)
seal = strip_arc(seal, 270.0, 96.0)
save_mask(crisp(seal, 2), HERE/"mask-seal.png", 1000)

# ---- 2. the calligraphy: gold on black ----------------------------------
im = Image.open(SRC/"c6183527-image.png").convert("RGB")
a  = np.asarray(im).astype(float)
band = a[1126:1320, 30:1120]                             # the Arabic line only
r, g, b = band[..., 0], band[..., 1], band[..., 2]
val  = band.max(2)/255.0
# gold reads yellow (G close to R); the rule and the diacritics read red.
goldness = g/(r + 1.0)
gold = val * np.clip((goldness - 0.44)/0.20, 0, 1)

# The red marks are the dots of the shin letters — orthography, not ornament,
# so they stay. The red *rule* underneath goes. They are told apart by run
# length: a rule runs the width of the line, a dot is a few pixels across.
red = (r > g + 22) & (r > b + 16) & (val > 0.30)
rule = np.zeros_like(red)
for y in range(red.shape[0]):
    row = red[y]; x = 0
    while x < len(row):
        if row[x]:
            x0 = x
            while x < len(row) and row[x]: x += 1
            if x - x0 > 55: rule[y, x0:x] = True     # a rule, not a dot
        else:
            x += 1
dots = red & ~rule
gold = np.maximum(gold, dots*0.92)          # the dots are solid marks, not shading

# the rule leaves a soft fringe the colour test cannot see; on its own rows,
# clear everything that is not a full-strength stroke of the script
rule_rows = np.where(rule.sum(1) > 55)[0]
for y in range(max(0, rule_rows.min()-2), min(gold.shape[0], rule_rows.max()+3)):
    gold[y][gold[y] < 0.46] = 0.0

# a last sweep: no row of this script covers three quarters of the line —
# any row that does is what remains of the rule
Wb = gold.shape[1]
for y in np.where((gold > 0.2).sum(1) > 0.70*Wb)[0]:
    gold[y][gold[y] < 0.80] = 0.0
print("  rule px:", int(rule.sum()), " dot px:", int(dots.sum()))

ys, xs = np.where(gold > 0.18)
y0, y1 = max(0, ys.min()-3), min(gold.shape[0], ys.max()+4)
x0, x1 = max(0, xs.min()-3), min(gold.shape[1], xs.max()+4)
print("  bbox:", (x0, y0, x1, y1))
gold = gold[y0:y1, x0:x1]
save_mask(crisp(gold, 3), HERE/"mask-wordmark.png", 2000)
