# Output template — two variants, ELEMENTS format, script only

The deliverable is one Markdown file per variant, written in the canonical import format from
`.claude/skills/cinema-workflow/references/script-format.md` so Cinema Studio's Import elements
extracts characters, locations and props. Both variants ship together. The file carries the
script and nothing else: no rationale, no compliance notes, no self-score, no "concerns" block.
Those go to Ivan in chat, once.

Save to `context/scripts/<CODE>_<A|B>.md`. Code follows the team convention
(`IT_TST_<n>_<A|B>`, or a rework code if Ivan gives one). Video name = script name = ClickUp task
name; the first line of the file is that name.

## Skeleton

````markdown
# PROJECT: IT_TST_<n>_A

## ELEMENTS

| Type | Tag | Name | Description |
|---|---|---|---|
| Character | @C1 | <Name>, <age> | <what they look like; wardrobe; nothing about plot> |
| Character | @C2 | <Name>, <age> | … |
| Character | @HOST | Podcast host, 45 | … |
| Location | @<LOC1> | <place>, <time of day> | <visual description> |
| Location | @STUDIO | Podcast studio | Wood panels, two mics, warm key light. |
| Prop | @<PROP> | <prop> | <look; who holds it> |

## SCENE 1 — @<LOC1>, day

**Elements:** @C1, @C2
**Duration:** 8s
**Action:** <one or two sentences of blocking; who is watching whom>
**Dialogue:**
@C2: "<line 1 — the flinch>"
@C1: "<line 2 — the reframe>"

## SCENE 2 — @<LOC1>, day
…hook block 2 (web only)…

## SCENE n — @STUDIO
**Elements:** @HOST, @C1
**Duration:** 70s
**Action:** Podcast Q&A. Host asks, @C1 answers. Word-by-word centered captions.
**Dialogue:**
@HOST: "How long does it take to articulate thoughts into words more clearly with Vocal Image?"
…

## SCENE n+1 — @STUDIO
**Elements:** @C1
**Duration:** 25s
**Action:** Daily Plan VO over lesson list "UNLOCK YOUR CONFIDENCE".
**Dialogue:**
@C1 (VO): "…"

## SCENE n+2 — CTA CARD
**Elements:** —
**Duration:** 3s
**Action:** Card: START SPEAKING CONFIDENTLY NOW, arrow down. <or: App Store / Google Play badges>
````

Rules from script-format.md that break the import if skipped: one `## ELEMENTS` table at the
top; `Type` is only Character / Location / Prop; every element has a short uppercase tag used
identically everywhere; every scene has an `**Elements:**` line with tags only; scene headings
carry the location tag; dialogue lines are prefixed with the speaker tag; every character in the
table even if introduced late. Descriptions are appearance, not plot.

## The two variants

| | Variant A | Variant B |
|---|---|---|
| purpose | closest to the measured winners; the safe bet | one deliberate deviation, named in chat and tagged [ASSUMED] or [OBSERVED] |
| hook | a new cell from the hook matrix in a proven family (P1+P2, proven blocking) | either a second matrix cell in a different family, or the same hook with the deviation below |
| body | proven module for the funnel (below), unchanged | proven module, or the deviation (e.g. live record → score → fix beat, P13; or a resonance/release line if Ivan mandates it) |
| casting | three casts listed in chat for the target market (P12) | same |

Never ship two variants that differ only in casting; casting is the multiplication step after
Ivan picks.

## Proven web body (use verbatim, minus the two cut lines)

Podcast Q&A (host + the hook character, or host + guest):
```
@HOST: "How long does it take to articulate thoughts into words more clearly with Vocal Image?"
@C1: "How old are you?"
@HOST: "I'm 47."
@C1: "Perfect. In 28 days you won't even recognize yourself."
@HOST: "But what if my mind literally goes blank in the middle of a presentation?"
@C1: "It's designed exactly for people like you. Professionals over 40 with untrained communication skills."
@HOST: "But isn't reading books better?"
@C1: "After 20, reading only keeps you busy. It doesn't train real-time responses. Articulation training builds the reflexes that organize your thoughts before you speak."
@HOST: "Do I need any equipment?"
@C1: "No. Just your phone and ten minutes a day. In three days you'll know how to practice communication in the most effective way. On day seven you'll sound more confident. On day fourteen you'll be the best speaker in any room."
@HOST: "So what's the first step?"
@C1: "Tap the screen, take the test, and start tomorrow."
```
Daily Plan VO (over the lesson list):
```
Most people think communication is just small talk. In reality, it's one of the most powerful skills you can develop. The way you speak reveals how you think, how confident you are, and how other people perceive you. Once you learn how to train it, you can strengthen your presence, express yourself clearly, and connect with anyone. Ready to become unrecognizable? Take the quick test now and get your personalized communication mastery plan. Just tap the screen to get started.
```
Cut on sight if they reappear in a source doc: "93% of how you're perceived comes from how you
communicate…" and "81% of how you're perceived…". Dated deadlines ("by the end of July") become
relative ("in 28 days") unless Ivan wants a monthly re-cut.

## Proven install body (short, 15–45 s)

Contrast + proof + test CTA:
```
SCENE 1 (3s): split screen BASIC | PRO — two deliveries of the same line (the flinch vs the trained version)
SCENE 2 (6–10s): two more pairs, different speakers
SCENE 3 (4s): lesson list "SPEAK ELOQUENTLY" over a boardroom still
SCENE 4 (15–20s, optional): one creator line to camera — age, routine, outcome ("I replaced scrolling with it… ten minutes a day")
SCENE 5 (3s): "START TODAY" · App Store / Google Play badges · checkable product facts only (e.g. "4+ million users", "4.6")
```
Spoken CTA for install: "Take the voice test." / "Do the voice test now." Button: Install now.

## What goes in chat, not in the file

- Which patterns each variant leans on, and the one deviation in Variant B.
- Three casting options per variant for the target market, as descriptions (Pinterest links if asked; never embeds).
- The criteria.md self-score (six dimensions, all ≥7) and what was changed to get there.
- Any concern (claim, compliance, market fit), stated once.
- Spiral/Meta call count and cache path.
