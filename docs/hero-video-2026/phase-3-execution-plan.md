# Phase 3 — Execution Plan
**Vocal Image website hero video · production plan, owners, calendar**

| | |
|---|---|
| Kickoff | Tue 4 Aug 2026 |
| Live on site | **Tue 1 Sept 2026** |
| Window | 28 calendar days · **21 working days** |
| Deliverables | Homepage loop (1:1, 10–15 s, muted) + YouTube cut (16:9, 60–90 s, sound on) |
| Recommended direction | **A** for the YouTube cut, **C** for the homepage loop — one shoot day covers both |

---

## 1. The two things that will make or break this date

### 1.1 The dev track must start this week, not at the end

This is the single biggest schedule risk and it is not a creative one. The video is finished on **Fri 28 Aug**. If the `<video>` slot, poster plumbing and `preload="none"` behaviour are not already built and tested by then, 1 September slips — and nobody will have noticed until the last three days.

**The embed is a parallel track, not a final step.** File the dev ticket in Week 1 with a dummy 1:1 MP4 and a placeholder poster, get the whole mechanism live behind a flag by **Fri 21 Aug**, then swap in the real asset on 28 Aug. Swapping a file is a ten-minute job; building the mechanism is not.

Dev scope, so it can be estimated properly:
- A native `<video muted autoplay loop playsinline preload="none">` above the quiz, activated by IntersectionObserver
- A real `poster` image — **the poster is the LCP element**, so it must be optimised as such
- `prefers-reduced-motion: reduce` → poster only, no playback
- AV1 primary with H.264 fallback via multiple `<source>` elements
- LCP measured before and after, on mobile and desktop
- The quiz below must not shift (watch CLS)

### 1.2 Concept lock is due Thu 6 Aug

Every day concept lock slips comes straight out of post-production, because the shoot date cannot move later than 14 Aug without breaking the review cycles. There is no float in this plan. If a decision is going to take longer than 6 Aug, tell me now and I will re-plan against a compressed post schedule rather than discover it on 20 Aug.

---

## 2. Owners

| Owner | Responsibility |
|---|---|
| **Ivan Turapin** | Creative direction · concept lock · script and storyboard approval · final QA and the go-live gate |
| **Kirill Repin** | Production and motion execution · shoot · edit · motion graphics · exports and variants |
| **Katti** | Brand and motion assets — type treatment, colour, logo animation, lower-third system |
| **CTO / dev** | The embed track in §1.1. Owns the `<video>` element, poster, `preload`, and LCP measurement. **Not a creative task.** |
| **Agent (me)** | Script drafts · storyboard build · reference packs · app-screen capture direction · variant QA checklist · this plan's upkeep |

Anything touching the live site is dev-owned. Anything touching the timeline is Kirill-owned. Anything touching the decision is Ivan-owned.

---

## 3. Production plan, stage by stage

### Stage 1 · Decisions & concept lock — Tue 4 → Thu 6 Aug
**Owner: Ivan**
- Settle the seven items in Phase 2 §06. Four are already assumed (square master, typography over subtitles, no CTA on the loop, quiz-start guardrail) — confirm or correct.
- Two are genuinely open: the **interim-hero call** and **dev ownership**.
- Lock direction A + C, or override.
- **Gate: concept locked Thu 6 Aug.** Nothing downstream starts without it.

### Stage 2 · Script — Fri 7 → Mon 10 Aug
**Owner: Agent drafts · Ivan approves**
- YouTube cut script to the Phase 2 beat map: hook (name the private failure) → voice test + mechanism → results screen + proof numbers → single CTA wrapped back to the hook.
- Homepage loop is **not** a shortened script. It is a shot description plus one line of on-screen type.
- Playbook compliance pass: mechanism (release/resonance) present, no Mehrabian myth, every number verified or tagged `{VERIFY}`, one avatar only, hook is one sentence naming a specific situation.
- Proof numbers to legal//factcheck: 8.4M accent tests, 4M voice tests, 120+ accents, 96% detector figure.

### Stage 3 · Storyboard & pre-production — Tue 11 → Thu 13 Aug
**Owner: Kirill · assets from Katti · approval from Ivan**
- Frame-by-frame storyboard for both cuts, composed **1:1 with a 9:16 safe-area overlay** so the vertical re-cut is free rather than a rescue job.
- Loop-seam design: first and last frame must match. Storyboard the seam explicitly — this is the thing RiseGuide got wrong.
- Katti delivers type treatment, colour, logo animation, lower-third system.
- **App-screen captures**: clean screen recordings of the Voice Test flow and the results screen with metric bars. These are the money shot per Phase 2 — capture them properly at device resolution, not filmed off a handset.
- Casting, wardrobe, location confirmed. Talent must be able to deliver the same sentence twice with a real difference in delivery (direction C depends entirely on this).
- **Gate: storyboard locked Thu 13 Aug** at team review #1.

### Stage 4 · Production — Fri 14 Aug (one shoot day)
**Owner: Kirill**
- Single day covers both directions — shared talent, wardrobe, location.
- Shoot 1:1 framing with vertical safe area respected in-camera.
- Cover the results-screen insert generously; it carries the proof beat in both cuts.
- Generation (Higgsfield / Kling) is reserved for **environments and graphics only**. Real talent on camera — for a product promising authentic human voice, a synthetic presenter is a specific credibility risk. Any generated character requires its reference sheet; no reference, escalate to Ivan, do not improvise.
- Buffer: Mon 17 Aug is the pickup day if anything is unusable.

### Stage 5 · Post — Mon 17 → Thu 20 Aug
**Owner: Kirill**
- DaVinci Resolve as primary editor. Grade must fix what the current asset got wrong: **lift the murk, kill the heavy vignette**, keep the app screens legible.
- Motion graphics and kinetic typography pass — this is the sound-off carrier, so it is not decoration. Every claim the narration makes must also be readable.
- Loop seam cut and tested by looping it twenty times in a row. If you can see the join, it is not done.
- First frame chosen deliberately as the poster. It must show a person and the product, and read at thumbnail size.
- **Rough cut of both deliverables by Thu 20 Aug.**

### Stage 6 · Review cycles — Fri 21 → Thu 27 Aug
See §4. Two rounds, both time-boxed.

### Stage 7 · Exports & QA — Thu 27 → Fri 28 Aug
**Owner: Kirill produces · Agent QA · Ivan signs off**

Export matrix:

| Deliverable | Spec |
|---|---|
| Homepage loop | 1:1, 10–15 s, **AV1 primary + H.264 fallback**, under 4 MB, CRF 23–28, no audio track, seamless loop |
| Poster frame | Still from frame 1, optimised as the LCP element |
| YouTube cut | 16:9 1920×1080, H.264, AAC, sound on, burned subtitles |
| 9:16 paid variant | 1080×1920 from the square master, subtitles on, single CTA |
| Archive | Both masters to Drive archive via `scripts/upload_to_archive.py` |

QA checklist: loops seamlessly · legible with sound off · legible at 390 px wide · poster reads at thumbnail size · no CTA on the homepage cut · all numbers verified · playbook exceptions documented · file under 4 MB.

- **Gate: final approval Fri 28 Aug.** Ivan signs off, asset handed to dev.

### Stage 8 · Publish — Mon 31 Aug → Tue 1 Sept
**Owner: dev · Ivan verifies**
- Swap the real asset and poster into the already-built embed.
- Measure LCP before and after on mobile and desktop. If LCP regresses past 2.5 s, hold and drop to 720p or shorten the loop.
- Confirm the quiz below does not shift.
- Ivan verifies on real devices. **Live Tue 1 Sept.**

---

## 4. Team feedback checkpoints

Three gates and two review rounds. Both rounds are time-boxed to 24 hours, because an open-ended review is what actually breaks deadlines.

| # | When | What is reviewed | Who | How feedback is collected |
|---|---|---|---|---|
| **R1** | **Thu 13 Aug** | Storyboard + script, before a camera is touched | Ivan, Kirill, Katti | Comments on the storyboard doc. Ivan resolves conflicts same day. **Feedback closes end of day.** |
| **R2** | **Fri 21 Aug** | Rough cut, both deliverables | Ivan, Kirill, + CEO/CTO invited | Timestamped comments in one ClickUp thread on 869edukr4 — timestamp or it is not actionable. **Closes Mon 24 Aug 12:00.** |
| — | Mon 24 → Wed 26 Aug | Revisions from R2 | Kirill | — |
| **R3** | **Thu 27 Aug** | Fine cut — confirmation only, not fresh direction | Ivan | Approve, or one final round of notes |
| **GATE** | **Fri 28 Aug** | Final approval and handoff | **Ivan** | Written go/no-go in ClickUp |

**Rules that keep this on rails**
- Feedback goes in **one thread**, not DMs. Anything sent by DM gets pasted into the thread or it does not exist.
- Video notes carry a timestamp.
- R3 is confirmation, not a new creative round. New direction at R3 means the date moves — that is Ivan's call to make explicitly, not a drift.
- Silence at a closing deadline reads as approval. Nobody gets to reopen a closed round.
- CEO/CTO see the Phase 2 deck now and the rough cut at R2. They are not in the daily loop.

---

## 5. Calendar

```
WEEK 1  Aug 4–9      Decisions, concept lock, script
  Tue 4   Phase 2 deck circulated · decisions open        Ivan
  Wed 5   Dev ticket filed for the embed track            Ivan → CTO
  Thu 6   ▲ GATE — concept locked                          Ivan
  Fri 7   Script draft 1                                   Agent

WEEK 2  Aug 10–16    Storyboard, pre-pro, shoot
  Mon 10  Script approved · numbers to factcheck           Ivan
  Tue 11  Storyboard build · Katti brief issued            Kirill / Katti
  Wed 12  App-screen captures · casting, wardrobe, location Kirill
  Thu 13  ▲ R1 — storyboard + script review, closes EOD    all
  Fri 14  ★ SHOOT DAY                                       Kirill

WEEK 3  Aug 17–23    Post
  Mon 17  Pickup day if needed · edit starts               Kirill
  Tue 18  Grade · motion graphics pass                     Kirill
  Wed 19  Kinetic typography · loop seam                   Kirill
  Thu 20  Rough cut, both deliverables                     Kirill
  Fri 21  ▲ R2 — rough cut review · CEO/CTO invited        all
          ▲ Embed mechanism live behind a flag             dev

WEEK 4  Aug 24–30    Revisions, exports, sign-off
  Mon 24  R2 feedback closes 12:00 · revisions start       Kirill
  Tue 25  Revisions                                        Kirill
  Wed 26  Revisions complete                               Kirill
  Thu 27  ▲ R3 — fine cut · export matrix begins          Ivan / Kirill
  Fri 28  ▲ GATE — final approval · handoff to dev        Ivan → dev

WEEK 5  Aug 31–Sep 1  Publish
  Mon 31  Asset + poster swapped in · LCP measured         dev
  Tue 1   ★ LIVE · Ivan verifies on real devices           Ivan
```

**Float: effectively zero.** Mon 17 Aug doubles as the shoot pickup day and the first edit day — that is the only slack in the plan, and it is single-use. The brief's own estimate was 2–3 weeks for a polished hero video; this is 3 weeks of production inside a 4-week window, with the fourth week spent on review and publishing. It fits. It does not fit if concept lock slips past 6 Aug.

---

## 6. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| **Dev work starts late** and the embed isn't ready on 28 Aug | High if not filed this week | File the ticket Wed 5 Aug. Mechanism live behind a flag by 21 Aug with a dummy asset. |
| Concept lock slips past 6 Aug | Medium | Four of seven decisions already assumed; only two are genuinely open. Escalate on 6 Aug if unresolved. |
| Talent can't deliver the before/after in direction C | Medium | Screen for it in casting. Direction A is the fallback for the loop as well as the YouTube cut. |
| LCP regresses and blocks go-live | Medium | Measure at 21 Aug on the dummy asset, not on 31 Aug. Fallback: 720p, or shorten the loop. |
| R2 opens fresh creative direction | Medium | R3 is explicitly confirmation-only. Reopening moves the date, and that is Ivan's explicit call. |
| A proof number fails factcheck | Low | Factcheck at Stage 2, before it is in a storyboard. Anything unverified is tagged `{VERIFY}` and cut. |
| Shoot day lost to illness/location | Low | Mon 17 Aug pickup day. Beyond that the date is at risk — escalate immediately. |

---

## 7. Still open

1. **Interim hero** — re-cut the existing `website_cover.mp4` as a stopgap now? Roughly one day of Kirill's time, and it starts collecting baseline LCP and engagement data three weeks before the real asset lands. Recommend yes, since it also de-risks the dev track by forcing the embed to exist early.
2. **Dev owner named** — who on the CTO's side owns §1.1, and can they commit to 21 Aug?
3. **Katti's availability** in Week 2 — the brand/motion assets are on the critical path for the typography pass.
4. **Performance data** — still nothing quantitative available. `context/scripts/` does not exist on disk. If hook-rate or retention figures exist in Drive or ClickUp, they would sharpen the concept choice before 6 Aug.

---
*Phase 1 reference library: `docs/hero-video-2026/phase-1-reference-library.md` · Phase 2 deck: ClickUp 869edukr4 · Evidence: 11 videos torn down, 44 keyframes.*
