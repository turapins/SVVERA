# The shot allocator, and the four defects it exists to prevent

Each rule below was added after the defect appeared in a real cut of IT_MYS_06.

## 1. Reserve every primary before allocating any partner

Beat 4's partner took `E[0.00–4.33]`. Beat 8's primary was authored as `E@0.00` — its
reserve silently failed and it kept its in-point anyway, so the same 4.3 seconds of the
boy with the backpack played twice, once at 0:31 and once at 1:05. Same for `F` and `B`.

Reserve all primaries in one pass first, then let partners take from what is left.
A failed reserve must assert, not return quietly.

## 2. A source may not follow itself — across beat boundaries too

An early guard only compared against the previous shot *inside the current beat*, so
`A@3.00` → `A@16.50` and `B@5.40` → `B@20.00` went out as adjacent pairs. Worse, the pairs
ran backwards: the boy already working, then the parents still arguing at the counter.

Compare against the last emitted shot globally, and also exclude the *next* beat's source
so the beat boundary itself is not a repeat.

The exception is deliberate: the same character before and after, cut together on the
product turn, is a match cut. Author that as a partner preference, don't let it happen by
accident.

## 3. Phase lock

Every block carries both states. `B[0–20]` is the girl stuck; `B[20–30]` is the same girl
working calmly. Without a gate, the allocator put the laptop shot at 0:11 — the resolution
before the problem — and put "she gives up and switches off the lamp" under
*"A parent report every week"*.

```python
RESOLVED = {'A':(23.5,30.04), 'B':(20.0,30.04), 'C':(19.0,29.0), 'D':(18.0,30.04)}
```

- Before the product-turn beat, resolved ranges are held out of the pool entirely.
- At the product-turn beat they are released.
- One beat later, problem ranges are pruned from the pool.

`D` is in the table for a different reason: it is neutral (the father, alone, reading), so
it is never pruned — but it *is* rationed, because as the connective tissue between rooms
the early beats will otherwise consume all 30 seconds of it and the tail fragments into
1-second flashes.

## 4. Nothing under 2.5 seconds

When contiguous room runs out the allocator will happily emit 1.0s and 1.35s shots. Fold
any sub-2.5s shot into a neighbour: extend the previous shot if its source has room,
otherwise pull the next shot's in-point earlier.

## Reading the output

```
19 shots, 78.13s, avg 4.11s
 1  t=  0.00  A  in=  0.00  dur= 5.31
 2  t=  5.31  B  in=  0.00  dur= 5.05
```

Check three things before rendering: that the final beat is unbroken (author it as a
no-split special case — it is the emotional close), that no problem-state in-point appears
after the turn, and that the average is near the target. Doubling cut frequency means
halving the average, not adding shots to the end.
