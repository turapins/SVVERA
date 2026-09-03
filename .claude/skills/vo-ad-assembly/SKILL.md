---
name: vo-ad-assembly
description: >
  Cut a voice-over-driven ad against its own voice-over with ffmpeg — beat grid from
  word-level alignment, a shot allocator that cannot break continuity, burned-in captions,
  brand banner/CTA/music, and a short version made by trimming copy rather than speeding
  the read. Use after Cinema Studio blocks are approved and the VO exists: "собери ролик",
  "смонтируй под закадр", "нарежь блоки", "добавь субтитры", "сделай версию на 30/60/90
  секунд", "сделай монтаж плотнее". Optional and one of several routes — Ivan picks the
  assembly tool per project and often cuts in DaVinci himself; ask before assuming this
  one. For a Resolve project use davinci-ad-assembly, and to generate the blocks in the
  first place use cinema-workflow.
---

# VO-driven ad assembly (ffmpeg)

## This route is a choice, not a default

Assembly is optional and the tool is Ivan's call per project — some pieces he cuts himself
in DaVinci, some go through ffmpeg here, some go to Remotion. Ask which before starting, the
same way the render runtime is asked. Nothing upstream depends on this skill: approved
480p blocks plus a voice-over are a complete handoff on their own.

What follows applies only once the ffmpeg route has actually been chosen.

## The spine

The input is a handful of long **location blocks** (one 30s generation per room, several
shots inside it) plus a **voice-over master**. The output is a cut where every shot change
lands on a line of the read.

Never cut picture first and fit the voice afterwards. The voice-over is the spine; the
picture is allocated against it.

## 0. Check the toolchain before planning anything

Two things are commonly missing and both are found out mid-render:

| Check | If missing |
|---|---|
| `ffmpeg -filters \| grep -E "drawtext\|subtitles\|ass"` | no text filter → captions and cards are PIL PNGs, see `references/captions.md` |
| `whisper --help` | broken numba/numpy → align with ElevenLabs Scribe, same file |

## 1. Align the voice-over to the word

POST the VO to ElevenLabs `/v1/speech-to-text` with `model_id=scribe_v1` and
`timestamps_granularity=word`. No reference text needed. This one file drives the beat
grid, the captions and every later re-time — keep it.

## 2. Build the beat grid

A **beat** is one thought in the read, 6–12s, ending at a sentence boundary. Ten to
fifteen beats for a two-minute piece. Each beat gets one primary source block chosen for
meaning, hand-authored once:

```
beats    = [('A',0.0,6.0), ('B',0.0,10.79), ('C',0.0,9.71), ...]   # source, in-point, length
partners = [['D','C'],     ['C','D'],       ['A','D'],      ...]   # preference for the inner cut
```

The beat lengths come from the VO, never from the footage. Their sum is the picture
length; whatever the VO runs past that plays over the end card.

## 3. Allocate the shots

Run `scripts/allocate_shots.py`. It splits each beat into a primary half at its authored
in-point plus one or more partner shots from other blocks, doubling the cut rate without
touching sync. Four rules, each of which caught a real defect — see
`references/shot-allocator.md`:

1. **Reserve every primary before allocating any partner**, or partners eat the in-points
   and two shots play the same seconds.
2. **A source may not follow itself**, across beat boundaries too.
3. **Phase lock.** Mark each block's resolved-state range. Resolved footage is absent from
   the pool before the product turn; problem-state footage is removed from it after.
4. **No shot under 2.5s.** Fold a remainder into a neighbour instead of emitting a flash
   frame.

Then read the printed table before rendering. It is short and it is where a wrong shot is
still cheap.

## 4. Captions

`scripts/build_captions.py`. Amber Montserrat ExtraBold, heavy black outline, no pill,
lower third — the format's proven look. Break at clause boundaries, not at word counts:
a full stop always breaks, a caption never ends on a preposition or a conjunction, hard
ceiling 7 words / 2.8s. Gapless — each caption holds until the next one starts.

76 captions is 76 PNGs and **one** overlay: assemble them into a single alpha `.mov`
through the concat demuxer. Details and the exact filter chain in `references/captions.md`.

## 5. Banner, CTA, music, delivery

- A full-screen semi-transparent banner is a **card, not a bed**. Three appearances of
  5–7s beat one block of 35s: a static hold over a quarter of the runtime is where
  retention breaks.
- Music sits under the VO with `sidechaincompress` keyed off the voice, not at a fixed
  low level — fixed level is either audible over the read or inaudible entirely.
- Deliver at **−15 LUFS, true peak ≤ −1 dBFS**. Measure with `ebur128`, correct with one
  `volume` pass plus `alimiter`.

## 6. A shorter version

Trim copy first, speed second. 20% `atempo` alone collapses the pauses along with the
syllables and the read starts to sound like an answering machine. Cutting the restating
lines buys the same seconds and leaves the speed change inaudible.

Cut at the silence between words, and drop any word that merely *touches* a cut or a
dangling syllable survives. Then push the old beat edges through the same
`(t − deleted_before_t) / tempo` map: beats re-time automatically and a beat that fell
inside a cut collapses to ~0 and drops out of the list. Recipe in
`references/shortening.md`.

## Rules that carry the cost

- Voice-over aligned to the word before any picture decision.
- Beat lengths from the read; shot lengths from the beats.
- Primaries reserved before partners.
- A source never follows itself; nothing under 2.5s.
- Resolved footage cannot appear before the product turn, problem footage cannot appear after.
- Captions break on clauses, hold gapless, and ship as one overlay.
- Banners appear in short blocks, never as a long static hold.
- Shorten by cutting copy, then by a speed change small enough not to hear.
- Check loudness before delivering, every time.
