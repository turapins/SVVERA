---
name: winning-ads-script-writer
description: >
  Use when Ivan asks for a new Vocal Image ad script that has to perform, in Russian or English:
  "напиши winning скрипт", "новый креатив на этот угол", "нужен топ-перформер", "напиши скрипт
  под web funnel / под app installs", "write a top-performer script", "new creative for the
  accent / small-talk / meetings angle", or when he pastes a competitor ad (Spiral link, uuid,
  transcript, or description) and says "сделай нам такое сильнее" / "make ours stronger than
  this". Also use when asked which hook families are currently winning for Vocal Image before a
  batch is written. Not for hook-only reworks of an existing creative (use reworks), not for
  recreating a specific reference video end to end (use story-ad-from-reference), not for
  generating the video (use cinema-workflow).
---

# Winning-ads script writer — Vocal Image

Writes a Vocal Image ad script the way the measured winners are built, after checking what is
winning right now. Evidence and method: `context/winning-ads/METHOD.md`. Working references in
`references/` (load on demand, not all at once):

- `pattern-library.md` — the 16 patterns and 12 failure modes with tags and the honesty procedure
- `spiral-recipes.md` — exact Spiral/Meta calls, fixed uuids, parsing, quota reporting
- `hook-bank.md` — every measured hook line, competitor hooks, the hook matrix
- `output-template.md` — ELEMENTS skeleton, proven web body and install body, what stays out of the file

## 0. Hard rules and traps — read before anything else

These are the ways an agent without this skill got it wrong on the first test (2026-09-03), and
the ways live creatives have failed. Each has a measured reason in `pattern-library.md`.

| trap | rule |
|---|---|
| Writing from the playbook without looking at what is live | **No script before the research pull** (§1). The playbook's hook format, mechanism rule and length rule are contradicted by the winners. |
| Hook is a monologue to camera ("My accent isn't the problem…") | **Line 1 is said TO the character, or is their own stumble, in front of a witness.** Line 2 reframes to articulation by 6 s. (P1, P2) |
| Explaining breath, resonance, release, vocal cords | **Mechanism is one named practice with a dose and at most one sentence on what it trains:** "Articulation training. Nine minutes a day. It builds the reflexes that organize your thoughts before you speak." Resonance/release appears in 0 of 30 winning transcripts. If Ivan mandates it, it goes in Variant B only and is flagged. (P5) |
| A 30–45 s web script with one hook and a talking head | **Web funnel = 2+ hook blocks + the proven podcast body + Daily Plan VO + CTA card, 2–5 minutes.** Install = 15–45 s contrast/quiz piece. Length follows the funnel, not the playbook table. (P10, P4) |
| Repeating the hook at the end ("wrap") | Not in any winner. Drop it. |
| Reusing a live hook's lines verbatim as a "restaging" ("Your accent is strong." / "I know, but that wasn't the real problem.") | **A proven family is a shape, not a script.** Variant A takes the family's flinch type, reframe target and blocking, with new lines for a new moment. If the first two lines match a live family in the Recipe 1 pull, that is a rework, not a new creative; hand it to `reworks`. |
| Two variants that are the same script with a man and a woman | **Variant A = safest measured pattern. Variant B = one named deviation.** Casting is the multiplication step after Ivan picks; list three casts per variant in chat. |
| Inventing an offer or a number ("first session free", "93% of…", "81%…") | **Only numbers allowed: a character's age, routine and timeline, or a checkable product fact (4+ million users, 4.6).** Anything else gets `{VERIFY}` in chat and does not enter the script. The 93%/81% lines are the Mehrabian myth re-skinned; cut on sight. (P6, F4) |
| Notes, rationale, compliance block, metadata header inside the script file | **The file carries the script only.** Everything else goes to Ivan in chat, once. (`feedback_no_compliance_sections_in_scripts`) |
| Accent/nationality hook aimed at the US | US briefs reframe to a universal workplace pain (talked over, not heard, "does that make sense?"). Nationality lines are for Malaysia/SEA variants where they personalize. (P12, F6) |
| Brand name in the first 10 s; "Hi, I'm…" | Product enters after the reframe. Winners first say the brand at 14–67 s. (F9) |
| Health/cognition claims stated outright | Imply through a story ("my best friend started going quiet mid-sentence"); never name a condition. |
| Changing the body and the hook in one creative | The body is the fixed module. A new body is its own test creative and is said so. (P4, F1) |
| US register slips | US market = US spelling and vocabulary throughout. |
| Retyping `@C1` into a Higgsfield prompt | Script tags are not Elements IDs. After import, copy the real IDs. (script-format.md) |
| Spending credits | This skill spends zero generation credits. Research tools are read-only. |

## 1. Research before writing (every time)

Run `references/spiral-recipes.md` Recipe 1 (Vocal Image state), Recipe 2 (BoldVoice, Loora,
Patter AI), and Recipe 5 (Meta, the target account). Cache under
`context/winning-ads/evidence/<YYYY-MM-DD>/`. If Spiral is unreachable (auth-expired symptom in
`reference_spiral_mcp` memory), stop and tell Ivan; do not write from memory of old winners.

Write down before touching the script:
- the live hook families on the target page (Meta `body` lines + first transcript line), with `active_days` and `duplicate_count`
- any body text you have not seen before (transcribe it; it may be a new family)
- top 3 competitor hooks in the `proven`/`strong` bands
- the current CPA band for the funnel from Meta
- one chat line: "Spiral: N calls, 0 credits. Meta: M calls. Cached at …"

If Ivan pasted a competitor ad: get its transcript and `ad_creative_analysis` (Recipe 3), extract
the moment, the flinch, the proof mechanism and the CTA. "Make ours stronger" means: same
moment, our reframe (P2), our proof (P6), our body — never a paraphrase of their lines.

## 2. Frame the brief

Fill this before generating hooks. Ask Ivan only for the funnel if it is not stated; everything
else defaults from the evidence.

| field | default from evidence | overrides |
|---|---|---|
| funnel | ask if absent | web (Learn more, quiz) / install (Install now, store) |
| avatar | 47-year-old professional who goes quiet · fluent non-native judged on accent | any other avatar = tag script [ASSUMED], say it is a test |
| awareness | problem-aware; the reframe does the education | solution-aware for install retargeting |
| formula | story-arc hook blocks + PAS body (what the winners actually are) | SF3 AIDA for install contrast pieces |
| market | Malaysia/SEA unless stated | US → no ESL line; UA/CIS → social/dating hooks have converted |
| moment | one social moment with a witness (hook-bank.md matrix) | — |

## 3. Generate and pressure-test hooks

Fill the matrix in `references/hook-bank.md` (moment × flinch × reframe × avatar × market):
6–9 cells. For each cell write line 1 and line 2 and the first cut. Then run every cell through
the checklist at the bottom of hook-bank.md. Discard anything whose first two lines match a live family
(compare against the Recipe 1 body lines and the first transcript lines), a compliment, a statement without contrast, or
unreadable in silence. Keep two: one in a proven family for Variant A, one for Variant B.

## 4. Assemble

Web: hook block(s) (2–4 scenes, 3–20 s each, first cut ≤ 6 s) → podcast Q&A body → Daily Plan
VO over lesson list → CTA card. Use the body text in `references/output-template.md` verbatim,
minus the cut lines, with relative deadlines.
Install: contrast or quiz hook → 1–2 more pairs → lesson list → optional one-line testimony →
badges + checkable facts. Spoken CTA "take the voice test".

## 5. Write both variants in the ELEMENTS format

Follow `references/output-template.md` exactly. One `## ELEMENTS` table, then `## SCENE n —
@LOCATION` blocks with Elements / Duration / Action / tag-prefixed dialogue. Save to
`context/scripts/<CODE>_A.md` and `<CODE>_B.md`. Nothing else in the file.

## 6. Self-score and revise

Score each variant on the six `skills/vocal-image/criteria.md` dimensions with these definitions
swapped in: **Hook Rate** = P1 flinch + P2 reframe by 6 s + readable in silence; **Message
Clarity** = one avatar, one moment, mechanism as named practice (P5), no lecture. All six ≥ 7 or
revise. Then walk the failure-mode table (F1–F12). Fix in the script; do not annotate the script.

## 7. Deliver and stop

In chat, once: the two file paths; which patterns each variant leans on and Variant B's
deviation; three casts per variant for the market; the self-score; any concern in one sentence;
the research call count. Then stop for Ivan's pick. Multiplication (casting × geo variants),
ClickUp tasks and generation belong to `reworks`, `addtask` and `cinema-workflow`.

## 8. Keeping this skill honest

A skill that froze the 2026-09 winners would be wrong by December. Two mechanisms:

1. **Step 1 is mandatory and dated.** The research pull is what makes the pattern library a
   prior, not a rule. If a live hook family is not in `hook-bank.md`, add it with its Spiral
   evidence before writing.
2. **Fold results back.** When a creative written with this skill reaches ≥10 purchases on one
   account, or is killed, run the six-step procedure at the bottom of `pattern-library.md`:
   pull, classify (confirms / contradicts / new), re-tag on Vocal Image data only, update
   `pattern-library.md` and `METHOD.md`, log the date, commit with the creative code. A
   [MEASURED] pattern with two measured counter-examples gets demoted and raised in chat.

Open decisions carried from Phase 1 (METHOD.md §6) that change this skill when answered:
whether resonance/release is a brand mandate, whether a hook-rate sheet exists, and where the
web-funnel ad-level Meta numbers live.
