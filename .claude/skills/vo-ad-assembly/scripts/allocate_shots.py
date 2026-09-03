#!/usr/bin/env python3
"""Allocate shots for a VO-driven ad cut.

Edit CONFIG, run, read the printed table, then render with render_shots.py.
Every rule here exists because its absence produced a real defect — see
references/shot-allocator.md before loosening any of them.
"""
import json, sys

# ── CONFIG ────────────────────────────────────────────────────────────────────
SRC_LEN = {'A':30.04,'B':30.04,'C':29.0,'D':30.04,'E':11.04,'F':11.05}

# (block, in-point, beat length). Lengths come from the voice-over, not the footage.
BEATS = [('A',0.0,6.000),('B',0.0,10.792),('C',0.0,9.708),('D',0.0,8.667),
         ('A',6.0,10.625),('B',10.5,9.750),('C',9.5,9.500),('E',0.0,10.708),
         ('A',16.5,7.292),('C',19.0,10.208),('B',20.0,9.667),('F',0.0,12.042),
         ('A',23.5,6.583)]
# preferred blocks for each beat's inner cut, best first
PARTNERS = [['D','C'],['C','D'],['A','D'],['E','D'],['D','C'],['C','D'],['F','D'],
            ['D','C'],['B','D'],['D','B'],['C','D'],['B','D'],['C','B']]

# range of each block that shows the resolved state (or, for a neutral block, the part
# held back so the tail does not run out of material)
RESOLVED = {'A':(23.5,30.04),'B':(20.0,30.04),'C':(19.0,29.0),'D':(18.0,30.04)}
NEUTRAL  = {'D'}                # released on schedule but never pruned as problem-state
TURN     = 8                    # beat index where the ad turns to the product
SPLIT_MIN = 0.0                 # beats shorter than this play as one shot
MIN_SHOT  = 2.5
OUT = "shots.json"
# ──────────────────────────────────────────────────────────────────────────────

free = {k:[(0.0,v)] for k,v in SRC_LEN.items()}
def biggest(s): return max((b-a for a,b in free.get(s,[])), default=0.0)

def take(s, dur):
    iv = free.get(s) or []
    if not iv: return None
    i = max(range(len(iv)), key=lambda k: iv[k][1]-iv[k][0]); a,b = iv[i]
    if b-a < dur-0.01: return None
    iv[i] = (a+dur, b)
    if iv[i][1]-iv[i][0] < 0.4: iv.pop(i)
    return round(a,3)

def reserve(s, st, dur):
    e = st+dur; iv = free[s]
    for i,(a,b) in enumerate(iv):
        if a <= st+0.01 and e <= b+0.01:
            new = []
            if st-a > 0.4: new.append((a,st))
            if b-e  > 0.4: new.append((e,b))
            free[s] = iv[:i]+new+iv[i+1:]; return True
    return False

# rule 1 — every primary is reserved before any partner is allocated
prim = []
for (s,i,d) in BEATS:
    half = round(d/2,3) if d >= SPLIT_MIN else round(d,3)
    if not reserve(s,i,half):
        sys.exit(f"primary {s}@{i} for {half}s does not fit — check BEATS against SRC_LEN")
    prim.append((s,i,half))

# rule 3 — hold the resolved state out of the pool until the product turn
held = {}
for k,(lo,_) in RESOLVED.items():
    held[k] = [(max(a,lo),b) for a,b in free[k] if b > lo+0.01]
    free[k] = [(a,b) for a,b in free[k] if b <= lo+0.01]

LAST = len(BEATS)-1
shots = []
for n,((s,i,d),pref) in enumerate(zip(BEATS,PARTNERS)):
    if n == TURN:
        for k,v in held.items(): free[k] = free.get(k,[])+v
    if n == TURN+1:
        for k,(lo,_) in RESOLVED.items():
            if k in NEUTRAL: continue
            free[k] = [(a,b) for a,b in free.get(k,[]) if a >= lo-0.01]
    if n == LAST or d < SPLIT_MIN:          # the closing beat plays unbroken
        shots.append((s,i,round(d,3))); continue

    primary = prim[n]; shots.append(primary)
    need = round(d-primary[2],3); part = []; guard = 0
    while need > 0.35 and guard < 10:
        guard += 1
        prev = part[-1][0] if part else primary[0]
        nxt  = BEATS[n+1][0] if n+1 < len(BEATS) else None
        pool = pref + ['D','C','B','A','F','E']
        # rule 2 — a block may not follow itself, and may not collide with the next beat
        order = [q for q in pool if q != prev and q != nxt] or [q for q in pool if q != prev]
        cand  = [q for q in order if biggest(q) >= need-0.01]
        p     = cand[0] if cand else max(set(order), key=biggest)
        room  = biggest(p); chunk = round(min(need,room),3)
        # rule 4 — never leave a remainder too short to read
        if 0.01 < need-chunk < MIN_SHOT: chunk = round(need-MIN_SHOT,3)
        if chunk < MIN_SHOT: chunk = round(min(need,room),3)
        if chunk < 0.35: break
        st = take(p,chunk)
        if st is None: break
        part.append((p,st,chunk)); need = round(need-chunk,3)
    if need > 0.35 and part:
        a,b,c = part[-1]; part[-1] = (a,b,round(c+need,3))
    shots += part

# rule 4 — fold away any flash frame that survived
changed = True
while changed:
    changed = False
    for k,(s,i,d) in enumerate(shots):
        if d >= MIN_SHOT: continue
        if k > 0 and shots[k-1][1]+shots[k-1][2]+d <= SRC_LEN[shots[k-1][0]]+0.01:
            a,b,c = shots[k-1]; shots[k-1] = (a,b,round(c+d,3))
        else:
            j = k+1 if k+1 < len(shots) else k-1
            a,b,c = shots[j]; shots[j] = (a,b,round(c+d,3))
        shots.pop(k); changed = True; break

tot = sum(s[2] for s in shots)
print(f"{len(shots)} shots, {tot:.2f}s, avg {tot/len(shots):.2f}s\n")
t = 0.0
for n,(s,i,d) in enumerate(shots,1):
    print(f"{n:2d}  t={t:6.2f}  {s}  in={i:6.2f}  dur={d:5.2f}"); t += d
json.dump(shots, open(OUT,"w"))
print(f"\n-> {OUT}")
