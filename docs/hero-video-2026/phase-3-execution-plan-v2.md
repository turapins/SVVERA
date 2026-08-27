# Phase 3 v2 — Execution Plan (No-Shoot)
**Vocal Image website hero video · fully digital production**

> **v2 supersedes v1.** v1 contained a shoot day on Fri 14 Aug. **There is no shoot.** Nothing is filmed. Everything is AI generation, stock, motion graphics, and screen recordings of the real app. If anyone is holding v1, discard it — it will send someone to book a crew.

| | |
|---|---|
| Today | Wed 5 Aug 2026 |
| Live on site | **Tue 1 Sept 2026** |
| Window | 27 calendar days · **20 working days** |
| Production | AI generation (Higgsfield / Kling / Veo-class) · stock · motion graphics · app screen recording |
| Post | DaVinci Resolve · Remotion |
| Deliverables | Homepage loop (1:1, 10–15 s, muted) + YouTube cut (16:9, 60–90 s, sound on) + 9:16 paid variant |

---

## 1. What removing the shoot actually changes

**It increases confidence in 1 September.** The shoot day was the only hard calendar dependency in v1 — a fixed date requiring a crew, talent, a location and a working camera, all on one morning, with a single pickup day as the entire contingency. Lose that day to illness or a bad location and the date was gone.

Generation has no such day. It runs continuously, retries cost almost nothing, and it can start before the storyboard is fully locked. **Float goes from effectively zero to roughly four working days.**

But the risk profile changes shape rather than disappearing:

| | Shoot | Generation |
|---|---|---|
| Failure mode | One bad day kills the schedule | Slow accumulation of near-misses |
| Retry cost | Very high — re-book everyone | Near zero |
| Real danger | Logistics | **Consistency and the uncanny look** |
| Timing | Fixed and knowable | Queue-dependent and unpredictable |
| Quality ceiling | Set on the day | Set by prompt iteration and reject discipline |

The thing that will actually bite us is **reject rate**. Nobody budgets for it, and then a week disappears into re-rolls. Budget it explicitly: assume **1 usable clip in 5** for anything with a human face, and **1 in 3** for abstract or environmental shots. If we need 12 hero clips, that is roughly 50 generations, not 12.

### 1.1 The dev/embed track still runs in parallel from week 1

Unchanged from v1, and still the top schedule risk. The video finishes Fri 28 Aug. If the embed is not already built and tested by then, 1 September slips and nobody notices until the final days.

File the ticket **this week** with a dummy 1:1 MP4 and placeholder poster. Mechanism live behind a flag by **Fri 21 Aug**. Swap the real asset in on 28 Aug.

Dev scope:
- `<video muted autoplay loop playsinline preload="none">` above the quiz, IntersectionObserver activation
- A real optimised `poster` — **the poster is the LCP element**
- `prefers-reduced-motion: reduce` → poster only, no playback
- AV1 primary, H.264 fallback, ordered `<source>` elements
- **The CTA block under the video** — see §2
- LCP measured before and after, mobile and desktop; no layout shift on the quiz below

---

## 2. The CTA — "Ready to upgrade your life? TAKE THE TEST"

Ivan's line, and it lands. But it goes in two different places, because the two deliverables have different physics.

**YouTube cut — burned into the video.** There is a real ending, so the card can hold on screen for the last 3–4 seconds. Wrap it back to the opening line.

**Homepage loop — NOT burned in.** A loop has no end. A CTA card in the last three seconds of a 12-second loop means a fifth of the loop is a static plate, and every visitor who arrives mid-cycle sees the ask before they have seen the product. This is precisely RiseGuide's failure: their keyframe at 81 s of 88 s is almost entirely black, and it replays forever.

Instead the line lives as **real HTML directly under the video**:

```
Ready to upgrade your life?
[ TAKE THE TEST ]     ← anchors to the quiz already on the page
```

Why this is better than burning it in: always on screen rather than 20% of the time · genuinely clickable · keyboard-accessible and screen-reader-legible · translatable without a re-render · indexable · and it survives any future re-cut of the loop. It also resolves the old v1 assumption that the homepage cut carries no CTA — **"TAKE THE TEST" is not a competing action, it is a signpost to the one action already on the page.** That was the actual concern, and this satisfies it.

**Beating RiseGuide here specifically.** Ivan likes their approach but wants better. Their CTA is inside a muted YouTube iframe with `controls=0` — invisible, unclickable, and a stray click drags the visitor off to YouTube mid-funnel. Ours is real DOM: visible, clickable, and it points *into* the funnel instead of out of it. Same intent, opposite outcome.

---

## 3. Owners

| Owner | Responsibility |
|---|---|
| **Ivan Turapin** | Creative direction · concept lock · script and storyboard approval · **generation QA — the accept/reject call on every clip** · final QA and go-live gate |
| **Kirill Repin** | Generation execution and prompt iteration · motion graphics · edit · grade · exports and variants |
| **Katti** | Brand and motion assets — type treatment, colour, logo animation, the CTA card design |
| **CTO / dev** | The embed track in §1.1, including the HTML CTA block. Not a creative task. |
| **Agent (me)** | Script drafts · storyboard · generation prompt drafts and reference-locking scheme · app screen-capture direction · QA checklist |

The accept/reject call on generated clips is **Ivan's**, and it needs to be fast. Generation QA is where this project will silently lose days if the decision sits.

---

## 4. Stages

### Stage 1 · Decisions & concept lock — Wed 5 → Fri 7 Aug
**Owner: Ivan**
- Confirm the CTA split in §2.
- Lock the direction from the Phase 2 v2 deck (in progress — waiting on the research now running).
- Name the dev owner and file the embed ticket.
- **Gate: concept locked Fri 7 Aug.**

### Stage 2 · Script — Mon 10 → Tue 11 Aug
**Owner: Agent drafts · Ivan approves**
- YouTube cut to the beat map: hook → voice test and mechanism → results screen and proof → CTA wrapped back to the hook.
- Homepage loop is a shot description plus on-screen type, not a shortened script.
- Every proof number verified or tagged `{VERIFY}`: 8.4M accent tests, 4M voice tests, 120+ accents, 96% detector figure.

### Stage 3 · App screen capture — Mon 10 → Wed 12 Aug
**Owner: Kirill · runs in parallel with Stage 2**

**This is now the most important production stage, and it is the one thing that cannot be generated.** Yoodli and Descript both built entire heroes from nothing but UI motion, with zero human beings on screen. Our results screen — waveform, coloured metric bars, pitch readout — is the strongest asset we own and the one thing no competitor can copy.

- Capture at native device resolution from a real device or a clean simulator. Never film a handset with a camera.
- Voice Test flow start to finish · results screen with metric bars · daily plan · accent test.
- Clean state: no debug builds, no placeholder copy, no test-account names, realistic data.
- Multiple takes of each interaction at different speeds — the edit will want the option.
- **Also capture the onboarding flow** *(pending: Ivan to move `vi_onboarding_ios.mov` out of `~/Downloads`, which macOS blocks from tooling — it is not yet analysed).*

### Stage 4 · Storyboard & generation prompts — Wed 12 → Fri 14 Aug
**Owner: Kirill · assets from Katti · approval from Ivan**
- Frame-by-frame board for both cuts, composed **1:1 with a 9:16 safe-area overlay** so the vertical variant is free.
- **Loop-seam design** — first and last frame must match. Storyboard the seam explicitly.
- **Reference and seed locking**: every recurring element gets a locked reference image and a recorded seed before batch generation starts. No reference sheet, no generation — escalate to Ivan instead of improvising.
- Katti delivers type system, colour, logo animation, CTA card.
- **Gate: storyboard locked Fri 14 Aug** at review R1.

### Stage 5 · Generation — Mon 17 → Thu 20 Aug
**Owner: Kirill · accept/reject by Ivan**
- Batch generate against locked references and seeds. Log model, prompt, seed and reference for every accepted clip — reproducibility matters when a note comes back at R2.
- **Budget the reject rate**: ~1 in 5 usable for faces, ~1 in 3 for abstract and environmental.
- Ivan reviews daily in batches, not clip by clip. A clip that needs a fourth attempt gets replaced with stock or motion graphics rather than a fifth.
- Stock is a first-class option, not a fallback — for anything ambient, stock is faster and safer than generation.
- **Hard rule: no synthetic human presenter.** For a product whose promise is an authentic human voice, a generated talking head is a specific credibility risk. Generation covers environments, abstractions, textures and graphics.

### Stage 6 · Post — Thu 20 → Mon 24 Aug
**Owner: Kirill**
- Grade must fix what the current asset got wrong: **lift the murk, kill the heavy vignette**, keep app screens legible.
- Kinetic typography pass — this carries the meaning with sound off, so it is structural, not decorative.
- Loop seam cut and tested by playing it twenty times consecutively. If the join is visible, it is not done.
- Poster frame chosen deliberately: must show the product, and read at thumbnail size.
- **Rough cut of both deliverables by Mon 24 Aug.**

### Stage 7 · Review — Mon 24 → Thu 27 Aug
See §5.

### Stage 8 · Exports & QA — Thu 27 → Fri 28 Aug
**Owner: Kirill produces · Agent QA · Ivan signs off**

| Deliverable | Spec |
|---|---|
| Homepage loop | 1:1, 10–15 s, **AV1 + H.264 fallback**, under 4 MB, CRF 23–28, no audio track, seamless loop, **no burned CTA** |
| Poster frame | Still from frame 1, optimised as the LCP element |
| YouTube cut | 16:9 1920×1080, H.264, AAC, sound on, burned subtitles, **CTA card on the tail** |
| 9:16 paid variant | 1080×1920 from the square master, subtitles on, single CTA |
| Archive | Both masters to Drive via `scripts/upload_to_archive.py` |

QA checklist: loops seamlessly · legible with sound off · legible at 390 px wide · poster reads at thumbnail size · no burned CTA on the loop · HTML CTA present and wired to the quiz · all numbers verified · under 4 MB.

- **Gate: final approval Fri 28 Aug.**

### Stage 9 · Publish — Mon 31 Aug → Tue 1 Sept
**Owner: dev · Ivan verifies**
- Swap real asset and poster into the pre-built embed. Measure LCP before and after.
- If LCP regresses past 2.5 s: drop to 720p or shorten the loop. Do not ship a regression.
- Ivan verifies on real devices. **Live Tue 1 Sept.**

---

## 5. Feedback checkpoints

Three gates, two time-boxed rounds. Unchanged in principle from v1 — this part worked.

| # | When | What | Who | How |
|---|---|---|---|---|
| **R1** | **Fri 14 Aug** | Storyboard + script + locked references, before batch generation | Ivan, Kirill, Katti | Comments on the board. **Closes EOD.** |
| **daily** | Mon 17 → Thu 20 | Generation accept/reject, in batches | Ivan | Same-day call. A stalled decision costs a day of queue time. |
| **R2** | **Mon 24 Aug** | Rough cut, both deliverables | Ivan, Kirill, + CEO/CTO invited | Timestamped comments, one ClickUp thread on 869edukr4. **Closes Tue 25 Aug 12:00.** |
| **R3** | **Thu 27 Aug** | Fine cut — confirmation only | Ivan | Approve, or one final round |
| **GATE** | **Fri 28 Aug** | Final approval and handoff | **Ivan** | Written go/no-go |

Rules: one thread, not DMs · video notes carry a timestamp · **R3 is confirmation, not fresh direction** — new direction there moves the date, and that is Ivan's explicit call · silence at a closing deadline reads as approval.

---

## 6. Calendar

```
W1  Aug 5–9      Decisions, concept, script
  Wed 5   dev ticket filed · decisions open              Ivan → CTO
  Fri 7   ▲ GATE — concept locked                         Ivan

W2  Aug 10–16    Script, screen capture, storyboard
  Mon 10  script draft · APP SCREEN CAPTURE starts        Agent / Kirill
  Tue 11  script approved · numbers to factcheck          Ivan
  Wed 12  capture complete · storyboard + prompts         Kirill
  Thu 13  reference sheets + seeds locked · Katti assets  Kirill / Katti
  Fri 14  ▲ R1 — storyboard + references, closes EOD      all

W3  Aug 17–23    Generation
  Mon 17  batch generation begins                         Kirill
  Tue 18  generation · daily accept/reject                Ivan
  Wed 19  generation · stock substitution where needed    Kirill
  Thu 20  generation complete · edit + grade begins       Kirill
  Fri 21  ▲ embed mechanism live behind a flag            dev

W4  Aug 24–30    Cut, review, export
  Mon 24  rough cut both deliverables · ▲ R2              all
  Tue 25  R2 feedback closes 12:00 · revisions            Kirill
  Wed 26  revisions                                       Kirill
  Thu 27  ▲ R3 fine cut · exports begin                   Ivan / Kirill
  Fri 28  ▲ GATE — final approval → handoff to dev        Ivan → dev

W5  Aug 31–Sep 1  Publish
  Mon 31  asset + poster swapped · LCP measured           dev
  Tue 1   ★ LIVE · Ivan verifies on real devices          Ivan
```

**Float: roughly 4 working days**, spread across the generation week rather than concentrated in one contingency day. Generation can start early and run late without breaking anything downstream — that flexibility is what removing the shoot bought us.

---

## 7. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| **Dev work starts late**, embed not ready 28 Aug | High if not filed this week | File now. Mechanism live behind a flag by 21 Aug on a dummy asset. |
| **Generation reject rate underestimated** | High | Budget 1-in-5 for faces, 1-in-3 for abstract, up front. Fourth attempt → switch to stock. |
| **Character/style inconsistency across clips** | High | Lock reference images and seeds before batch generation. No reference, no generation. |
| **Uncanny look undermines a credibility product** | Medium | No synthetic human presenter. Generation for environments and graphics only. |
| **Generation queues unpredictable** | Medium | Start Mon 17, four-day window for what should take two. Stock always available as substitute. |
| **App screen capture looks amateur** | Medium | Native resolution, clean state, multiple takes. This is the one asset we cannot regenerate. |
| **Accept/reject decisions stall** | Medium | Daily batch review, not clip-by-clip. Ivan's call, same day. |
| LCP regresses and blocks go-live | Medium | Measure 21 Aug on the dummy asset, not 31 Aug. Fallback: 720p or shorter loop. |
| R2 opens fresh creative direction | Medium | R3 is confirmation-only. Reopening moves the date — Ivan's explicit call. |
| A proof number fails factcheck | Low | Factcheck at Stage 2, before it reaches a storyboard. |

---

## 8. Open

1. **Named dev owner** — who owns §1.1, and can they commit to 21 Aug?
2. **Onboarding flow** — `vi_onboarding_ios.mov` is still unreadable from `~/Downloads` (macOS TCC). Move it into the project and it feeds Stage 3.
3. **Katti's Week 2 availability** — the type system and CTA card are on the critical path for the typography pass.
4. **Which generation provider leads** — Higgsfield, Kling, or Veo-class. Decide at Stage 4, based on which holds character reference best in a test batch.
5. **Performance data** — still nothing quantitative. If hook-rate or retention figures exist in Drive or ClickUp, they sharpen the concept choice before Fri 7 Aug.

---
*Supersedes `phase-3-execution-plan.md` (v1, contained a shoot day — discard). Phase 1 references: `phase-1-reference-library.md`. Expanded competitor research in progress.*
