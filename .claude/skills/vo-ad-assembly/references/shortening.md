# Making a short version

## Trim copy first, speed second

A 20% `atempo` on its own is audible: pauses compress along with the syllables and the
read flattens. On IT_MYS_06, removing 33s of restating copy and speeding the remainder by
**13%** hit the same 1:27 target with no perceptible change to the delivery.

Pick the cuts by what the line *adds*, not by length. The largest single cut was a
three-part atmospheric list — the folder that doesn't get opened, the homework at eleven at
night, the feeling attached to it — 10.7s that add nothing to the argument already made.

## Cut at silence, and drop the touched words

```python
prev = max((w["end"]   for w in words if w["end"]   <= a+0.05), default=a)
nxt  = min((w["start"] for w in words if w["start"] >= b-0.05), default=b)
span = (prev+0.06, nxt-0.06)
```

A word whose span merely overlaps a cut must be dropped from the caption list too:

```python
def clipped(w):
    return any(w["end"] > a+0.02 and w["start"] < b-0.02 for a,b in spans)
```

Without this the read keeps a 0.02s stub of "She" and the captions display it.

Rebuild the VO by concatenating the kept spans with a 0.03s fade-in on each part, then one
`atempo`.

## Re-time everything through one map

```python
def remap(t):
    off = 0.0
    for a,b in spans:
        if t >= b:  off += b-a
        elif t > a: t = a; break      # an edge inside a cut collapses to its start
    return (t-off)/TEMPO
```

Push the **beat edges** through this as well as the words. Beats re-time automatically, and
a beat that fell entirely inside a cut collapses to ~0.07s and drops out of the list —
which is the correct behaviour, its picture should go with its copy.

Re-run the allocator on the new grid. With a shorter piece, raise the split threshold so
only beats above ~6s get an inner cut: halving the runtime while keeping every split would
push the average shot to 3.2s, faster than intended.
