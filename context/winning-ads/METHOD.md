# Winning-Ads Method — Vocal Image

**Version 0.1 · 2026-09-03 · Phase 1 deliverable (method, not yet a skill) · awaiting Ivan's review**

This document is the evidence-derived procedure a writer follows to produce a top-performing Vocal Image ad script, plus the pattern library that procedure leans on. It is built from three sources that are kept separate throughout, and every claim carries one of three confidence tags:

| tag | meaning | source |
|---|---|---|
| **[MEASURED]** | supported by Vocal Image's own purchase counts and CPA | Meta Ads MCP (iOS-01_main ad level, Web-01 campaign level) + the team's own numbers in the TST_IVAN_04 script doc |
| **[OBSERVED]** | supported only by longevity / rank / duplication in Spiral | Spiral `brand_winners`, `meta_page_ads` sorted by duration, `ad_creative_analysis`, transcripts |
| **[ASSUMED]** | craft judgement, no data yet | nothing — treat as a hypothesis to test |

Raw pulls live in `context/winning-ads/evidence/`. Nothing in this document is a number that is not in that folder.

---

## 0. What "winner" means in each source (read before trusting any pattern)

- **Meta iOS-01_main (app installs):** in-app purchases and CPA, ad level, 2026-01-01 → 2026-09-03, top 25 by spend. Real conversion data. Video-completion fields are populated on only two rows.
- **Meta Web-01 (web funnel):** campaign level only. Ad-level requests timed out six times at every size tried. Per-creative web numbers therefore come from the team's own doc, where Ivan wrote purchases and CPA into each rework's "NEW TARGET" line at rework time. They are real, but they are snapshots.
- **Spiral:** `winning_score` = page rank + active days + duplicate count. It rewards ads that stay live and get re-uploaded. That correlates with performance in a disciplined account, but a generic brand ad ran 14 months on the app page (c5dbf26b), so longevity can also be inertia. Never promote an [OBSERVED] pattern to a rule without a [MEASURED] confirmation.
- **Playbook / criteria / avatars:** prior knowledge, audited in §5. Several rules are contradicted by the winners.

One structural discovery changes how the corpus is read: the team's "Ref:" links in TST_IVAN_04 all point to ads on four persona pages (Charisma Academy, Michelle Lee, Anna Jones, Robert Smith; landing buildcharisma.com) that Spiral files under the brand "RiseGuide". One of those ads is word-for-word the produced KR_TST_59_A. These are Vocal Image's own web-funnel creatives. All of them went dark between 19 July and 8 August 2026, and the same scripts re-appeared on the "Vocal Image App" page from 17 July onward. **Ivan must confirm this reading** (§6, Q1) because it decides which pages the future skill polls.

---

## 1. Evidence base

| source | what was pulled | count |
|---|---|---|
| Spiral `brands_list` / `brands_search` | Vocal Image brand + 20 category brands | 2 calls |
| Spiral `brand_winners` | Vocal Image (×2 sorts), BoldVoice, Loora, Patter AI, Skillsta, Fluently, ELSA, LingoChatAI, RiseGuide | 10 calls |
| Spiral `meta_page_ads` sort=duration | Vocal Image App, Speak with Impact, 3rd VI page, Charisma Academy, Michelle Lee, Anna Jones, Robert Smith | 7 calls |
| Spiral `tiktok_page_ads` | Vocal Image TikTok page | 1 call |
| Spiral `transcribe_ads` | 10 VI app-page winners, 10 competitor winners, 10 persona-page web winners | 3 calls, 30 transcripts |
| Spiral `ad_creative_analysis` | 7 VI, 3 persona-page, 5 competitor ads | 15 calls |
| Spiral `collection_ads` | Ivan's "winners", "IN APP INSTALLS", "new web 17JUN" | 3 calls |
| Spiral `ads_details` | the 3 "Ref:" ads from the doc | 1 call |
| Meta Ads MCP | accounts list, field catalog, iOS-01_main ad level (25 rows), Web-01 campaign level (10 rows); 6 failed ad-level web pulls | 4 successful calls |
| Google Drive | TST_IVAN_04 full text (200,930 chars): 30+ original scripts, 30 rework blocks with performance lines | 1 call |
| repo | playbook.md, criteria.md, avatars.md, script-format.md, ad-creative/hook-system.md, reworks, ad-script-pipeline, competitor-profiling, marketing-psychology | read |

Spiral quota: `usage` reports every call priced 0.0 and credits_charged 0, before and after. **Zero Spiral credits and zero generation credits spent.** About 42 Spiral calls were made.

Not reached: Kirill's KR_TASKS doc (view-only per memory; not attempted), scripts for KR_TST_76_A_1_2 / KR_TST_68 / IT_TST_71 / IT_TST_91 (codes appear in data but the scripts are not in TST_IVAN_04), any hook-rate or 3-second-view export (Ivan cites "63% hook rate" for IT_TST_61_C once; no dataset found).

---

## 2. The decision procedure

A writer follows these steps in order. Steps 1–3 are research; nothing is written before step 4.

**Step 1 — Fix the funnel, because everything downstream forks on it.**
App install (iOS/Android accounts, CTA button "Install now") or web funnel (Web-0x accounts, CTA "Learn more", lands on a quiz). The two have different lengths, different CTAs, different proof, and CPAs that differ by 5–8× (§3, P10, P9). Never compare a creative across funnels.

**Step 2 — Pull the current state before writing.**
Spiral `brand_winners` for Vocal Image (VIDEO, sort winning_score and sort active_days) and `meta_page_ads` sort=duration on the active page(s). Note which hook families are live and how many uploads each has. Then `brand_winners` for BoldVoice, Loora, Patter AI. Then the latest Meta pull for the target account, sorted by spend, top 15. Write down: top 3 live hook lines, top 3 body variants, the CPA band. Cache to `evidence/`.

**Step 3 — Pick avatar and situation from the measured winners, not from the ten-avatar list.**
Measured winners cluster on two avatars: the 47-year-old professional who is smart but goes quiet (Plateaued Professional + Anxious Speaker merged), and the fluent non-native professional judged by accent (Fluent But Invisible / Post-Language-App). The situation is always a specific social moment with a witness: interview waiting room, first meeting line, small talk at a party, "does that make sense?" in a call. Pick one moment. If you want a new avatar (founder, creator, HR), tag the script [ASSUMED] and ship it as a test, not as a bet.

**Step 4 — Write the hook block as dialogue that happens TO the character.**
The measured winners open on a line someone else says to the protagonist, or the protagonist's own verbal stumble, and the second line reframes it (P1, P2). Write three hook blocks per script (P14). Each block is 3–20 seconds, cut at 2–6 seconds (P3). The on-screen caption is the spoken line, word by word, centered (P16).

**Step 5 — Attach the proven body, don't rewrite it.**
The podcast Q&A ("How long does it take to articulate thoughts into words…", age 47, day 3/7/14, books-vs-training, no equipment) and the Daily Plan VO have run under every measured winner since spring (P4). Changing the body is a separate test with its own creative. Remove the "93%" and "81%" lines (Failure mode F4).

**Step 6 — Introduce the mechanism as a named daily practice with a dose, in a peer's mouth.**
"Articulation training. Nine minutes a day." plus one sentence on what it trains ("the reflexes that organize your thoughts before you speak"). No physiology. No lecture. (P5)

**Step 7 — Proof is a person with an age, a routine, an outcome and a date.**
"I'm 47, started four months ago, got promoted to VP last week, by May 28th you'll thank me." No third-party statistics anywhere in the script unless Ivan supplies the source; anything else is tagged {VERIFY} and will be cut. (P6)

**Step 8 — CTA by funnel.**
Web: spoken "Tap the screen, take the test, and start tomorrow", end card START SPEAKING CONFIDENTLY NOW with an arrow down, Meta button "Learn more". App install: spoken "Take the voice test" / "Do the voice test now", app-store badges, Meta button "Install now". The quiz/test is the verb in both. One CTA only. (P9)

**Step 9 — Length by funnel.**
Web: the master can be 2–5 minutes; it converts on the first 15 seconds and nobody finishes it. App install: a 10–20 second audio-contrast or quiz piece is what has survived a year on the app page, and the 131-second KR_TST_60_A_2 is currently the cheapest iOS purchase at €5.96, so long also works there when the hook family is proven. Default: web long, install short, and always ship one of each length as the two variants. (P10)

**Step 10 — Multiply by casting and geo, not by rewriting.**
One hook × three casts is the standard output. Malaysia is the top country on roughly 70% of winners; the US converts at 1.2–1.8× the Malaysian CPA and prefers hooks with no ESL framing (P12). Where the hook names a nationality, produce the personalization variants the rework pipeline already uses.

**Step 11 — Self-score against criteria.md, then against the failure modes in §4.** Fix, don't annotate. The script doc carries the script only.

**Step 12 — Deliver two variants in the canonical ELEMENTS format** (`.claude/skills/cinema-workflow/references/script-format.md`) and stop for Ivan.

---

## 3. Pattern library

Each entry: claim → evidence → counter-examples → tag.

### P1. The hook is a line said TO the character, or the character's own stumble — a social flinch, not a statement about the product. [MEASURED]
Evidence: "Your accent is strong." (KR_TST_60_A_2: 65 web purchases at €37.83; iOS €5.96 on 286 purchases). "Long flight?" (KR_TST_59_A, 5-minute master, live on the brand page). "Never, and I mean never, say 'Does that make sense?'" (KR_TST_55_B: 77 purchases, the largest in the doc). "Tell me something interesting about yourself." / "You need to expand your vocabulary." (IT_TST_61_C: 48 Ukraine purchases at €23.17, Ivan notes 63% hook rate). "Never, and I mean never, open a meeting with 'How are you? Hope everyone's doing well.'" (IT_TST_87_B: 23 US purchases, one of two US-led winners). Competitors do the same: Loora's top ad opens "Sorry, my English is not good."; BoldVoice's opens with a mouth macro saying "Your tongue is holding you back."
Counter-examples: IT_TST_80_A opens on a headline statement ("People who lose their words mid-sentence — it's not ADHD, it's untrained communication skills") and still took 31 purchases at €37.68, so a statement works when it contains a denial or contrast. KR_TST_63_A opens on a compliment ("You 19? So deep voice.") and ran above €70 CPA.

### P2. Line two reframes the flinch away from what competitors sell (accent, vocabulary) toward articulation. [MEASURED]
Evidence: "I know, but that wasn't the real problem." → "That's not about your English level. That's untrained articulation." (60_A_2). "You don't have a confidence issue. You have a small talk problem." (61_C). "It's not ADHD, it's untrained communication skills." (80_A). "It's not your intelligence. It's how your thoughts come out." (86_A). The reframe lands inside 3–6 seconds in every case.
Counter-examples: none measured without it among the top performers. BoldVoice and Loora never reframe; they stay on pronunciation and fluency, which is their product.

### P3. First cut by 2–6 seconds to a second face or a reverse angle. [OBSERVED, weak MEASURED]
Evidence: every transcribed VI winner changes speaker or angle within 6 seconds (60_A_2 at 5 s, 59_A at 2 s, 88e79cf5 at 6 s, BASIC/PRO split at 3 s). The one outlier, 96ca3c74 (art gallery, first real cut at 18 s), carries the same body as 88e79cf5 and ranks lower (contender 57 vs strong 85) with a fifth of the EU reach.
Counter-examples: 0a2fb801 (before/after audio) holds one frame for 3.6 s and has run 168 days on the app page, so a held frame with an audio reveal works for short install pieces.

### P4. The body is a fixed module; only the hook is the variable. [MEASURED]
Evidence: the podcast Q&A ("How long does it take…", "How old are you? I'm 47", "isn't reading books better", "no equipment, just your phone", "day three / day seven / day fourteen") appears verbatim in KR_TST_55_B, 59_A, 60_A_2, 63_A, IT_TST_61_C, 80_A, 81_A, 86_A, 87_B, 88_B_F and in all ten transcribed persona-page ads. Reworks that changed only hook lines or casting were the team's whole optimization loop from June to August. Ivan's own note on 61_C: "the lever being tested is casting/appeal, not the pitch itself."
Counter-examples: the BASIC/PRO split-screen (7f418666) uses a different, 45-second body with a creator testimonial and app-store proof, and it is Spiral's #1 VI creative (168 days, 71 duplicates). So there are at least two proven bodies: the long podcast body for web, the short contrast body for install.

### P5. The mechanism is a named practice with a dose, never physiology. [MEASURED — contradicts playbook]
Evidence: every winner says "articulation training, nine/ten minutes a day" and at most one sentence of mechanism: "builds the reflexes that organize your thoughts before you speak" (55_B, 59_A body), "trains your brain to organize thoughts in real time" (59_A), "trains you to organize your thoughts, choose words quickly" (60_A_2). Resonance, breath, release, vocal cords, tension: zero occurrences in 30 winning transcripts.
Counter-examples: the short install pieces use "voice training" (0a2fb801, b8647637) without any mechanism at all and have run 6–14 months. Competitor Patter AI describes the mechanism through its scoring UI (fillers, hedging, uptalk, pacing) and ranks #1 on its page. See §5 for what this does to playbook.md.

### P6. Proof is one person, one age, one routine, one outcome, one date. [MEASURED]
Evidence: "I'm 47. I do articulation training for nine minutes a day. Now my thoughts come out clean and my boss asks me for advice." is in every long winner. The persona-page top ad (8a17dc31, 327k EU reach) opens on it: "6:30 a.m., training my articulation for nine minutes before the office. I'm 47, started four months ago, got promoted to VP last week. By May 28th, you'll thank me." "I'm 27, and my boss says I have the best articulation on the team… Nobody knows. That's my secret." (59_A).
Counter-examples: the two third-party statistics in the shared VO ("93% of how you're perceived comes from how you communicate", "81%…") are the only numeric claims, and they are the Mehrabian myth rephrased. They ride along in winners; nothing shows they help, and they are the one compliance and credibility hole in the corpus. The 45-second install winner uses "4+ million users, 4.6 out of 5" — real, checkable figures.

### P7. Objections are answered inside the ad, in Q&A form. [MEASURED]
Evidence: going blank mid-presentation, "isn't reading books better", "do I need equipment", "how old are you", "does it really work" are all asked and answered in the podcast body. 5ecf6660 goes further and pre-empts the scroll itself: "You're gonna hear me say articulation training, and your brain is gonna shut off. Too complicated, not for me, I'm too old for this."
Counter-examples: Loora does the same in 33 seconds with two objections (no partner, mistakes). BoldVoice answers none and wins on demo.

### P8. Daily dose plus a time box is category standard. [MEASURED + OBSERVED]
Evidence: VI "nine/ten minutes a day", "21 days" (61_C), "28 days" (59_A, 88_B_F, 87_B). Loora "five minutes a day is enough… ten minutes and you'll wonder why you waited". BoldVoice "10 minutes a day". Patter "three days and I've already seen drastic improvements".
Counter-examples: none. The number drifts between VI uploads (9/10/15 minutes, 21/28 days) with no visible penalty, so the presence of a dose matters more than the exact figure.

### P9. CTA verb is "take the test"; the button and the end card split by funnel. [MEASURED]
Evidence: web winners: spoken "Tap the screen, take the test, and start tomorrow", card START SPEAKING CONFIDENTLY NOW + arrow, button Learn more, quiz landing. Install winners: spoken "Take the voice test" / "Do the voice test now", app-store badges, button Install now; the 18 August uploads of 60_A_2 and 55_B on the app page switched the button to Install now with an empty primary text and became Spiral's #1 and #3 on that page within 30 days.
Counter-examples: competitors end soft ("Check it out", "try BoldVoice today", "Let's practice together every day"). No VI winner has a double CTA.

### P10. Length is a funnel property, and completion is not the KPI. [MEASURED]
Evidence: web masters are 130–317 seconds (60_A_2 131 s, 88e79cf5 152 s, 96ca3c74 207 s, 59_A 317 s, 4507e296 309 s). On iOS, KR_TST_60_A_2 converts at €5.96 with a 7-second average watch, 12.9% ThruPlay and 0.22% completion. KR_TST_76_A_1_2 converts at €5.81 with a 15-second average watch and 7.9% reaching the midpoint. The ads that have lived longest on the install page are 11–18 seconds (b8647637 voice-type quiz since October 2025 across re-uploads; 0a2fb801 before/after 168 days).
Counter-examples: the playbook's "UGC 15–60 s, web 30–60 s" is not what wins on web.

### P11. Layout and casting can kill a proven hook. [MEASURED]
Evidence: IT_TST_80_A (podcast stage, one speaker) 31 purchases; IT_TST_81_A (same headline, three women on a panel) 2 purchases, then 21 at €47.75 on a later dataset. Same words, different frame, order-of-magnitude difference.
Counter-examples: the same 59_A drama works in the India, China and male variants, so casting swaps inside a proven blocking are safe; changing the blocking is not.

### P12. Geo is a casting decision: Malaysia leads, the US pays more and rejects ESL framing. [MEASURED]
Evidence: Malaysia is the top country on 55_B (31 of 77), 60_A_2 (28 of 65), 80_A (12 of 31), 86_A (18), 88_B_F (20), 88_C_M, 91_B_F. US CPA vs Malaysia: 57.08 vs 32.42 (55_B), 31.06 vs 30.69 (60_A_2), 57.48 vs 44.86 (81_A). The two US-led creatives (87_B meeting opener, 68_A) have no accent line. Ivan's own rework note: the accent hook "is an ESL-specific angle — too niche for a general US audience".
Counter-examples: Ukraine on 61_C (48 at €23.17) is the cheapest CPA in the doc and came from a dating/poolside hook that no other creative uses. Canada led 64_C on 4 purchases (thin).

### P13. Competitors prove with the product working live; Vocal Image proves with a lesson list. [OBSERVED]
Evidence: BoldVoice 8bd9ee3c shows the score go from 56% to 98% in-app; 15bb4a63 shows the app flag the missing "th" and then pass at 100%. Patter shows the confidence/hedging/uptalk/filler scores. VI winners show a static 15-lesson list; actual app UI appears only in the 11-second b8647637.
Counter-examples: VI's long body outperforms on longevity within its own category, so the lesson list is not failing. The gap is untested, not proven. [ASSUMED]: a live "record → score → fix" beat inside the podcast body is the most promising unmade test in the corpus.

### P14. Multiple hook blocks form a mini-drama; one hook is the exception. [MEASURED]
Evidence: 59_A has four hook blocks (bias → interview → confrontation → solo reveal) before the body. 61_C has two (poolside, podcast). 55_B has three. 88_B_F has two. Single-hook long ads (80_A) score lower than multi-hook ones from the same period.
Counter-examples: the install-length winners have exactly one hook by construction.

### P15. Persona pages, not the brand page, carried the web funnel until August. [OBSERVED — needs confirmation]
Evidence: see `evidence/vocal-image-spiral/persona_pages_web_funnel.md`. Longest-running web ads had 310–327k EU reach on "Michelle Lee" and "Robert Smith" pages with the body "😱 Read this if you want to improve your communication skills 👇". All ended 19 July – 8 August. Same scripts reappeared on the brand page from 17 July with "Learn more", then from 18 August with "Install now".
Counter-examples: none; this is a fact about distribution, not creative. It matters because the future skill must poll the right page.

### P16. Word-by-word centered captions on every winner, ours and theirs. [OBSERVED]
Evidence: all 15 creative analyses report synchronized word-by-word captions, center or lower-center. The hook must read as text in silence.
Counter-examples: none.

---

## 4. Failure modes, with the real example

- **F1. Layout swap on a proven hook.** IT_TST_81_A panel: 2 purchases against 80_A's 31 with the identical headline. Test blocking separately from words.
- **F2. Compliment hook.** KR_TST_63_A "You 19? So deep voice" — the flinch became flattery; blended CPA above €70. The hook must cost the character something.
- **F3. Visual-only, no dialogue.** IT_TST_64_C elevator shortdrama: 20 purchases at €49.51, middling. Sound-off viewers get a caption; silent viewers get nothing.
- **F4. Recycled statistics.** "93% of how you're perceived comes from how you communicate" (59_A body, live in 88e79cf5 and 96ca3c74) and "81%…" (61_C body). Mehrabian, rephrased. Forbidden by playbook.md and criteria.md, and live in two top-ten ads. Cut on the next re-upload.
- **F5. Dated deadlines that go stale.** "By May 28th you'll thank me" ran until 7 August; "by the end of July" and "by September first" both live now. Either re-cut monthly or write a relative deadline ("in 28 days").
- **F6. ESL hook pointed at the US.** Ivan's own RW2 note on 60_A_2. US winners carry no accent line.
- **F7. Targeting on a thin sample.** 81_A was sent to Malaysia on 2 purchases "to stay consistent with the cross-creative pattern". Ivan later wrote the rule himself: trust real data over cross-creative assumption.
- **F8. Reading Spiral rank as conversion.** c5dbf26b, a generic "Discover the power of your voice" install ad, ran 14 months. Longevity is evidence of not being killed, not of winning.
- **F9. Product name in the first 10 seconds.** No winner does it; brand is first spoken at 14–67 s. Confirms the playbook.
- **F10. Lecturing the mechanism.** No winner explains breath or resonance. The moment a line sounds like a coach, the winners cut to a question instead.
- **F11. Two CTAs, or a CTA that names the wrong funnel** ("download" on a web ad). Not observed in winners; observed in the playbook's loser list and kept.
- **F12. Retyping short element tags into generation prompts.** Not a script failure but the production trap documented in script-format.md; the skill must carry it because the script is the source of the tags.

---

## 5. Prior knowledge audit: playbook.md / criteria.md / avatars.md against the evidence

| prior claim | verdict | evidence |
|---|---|---|
| Hook names a specific situation in the first 2 s; no "Hi I'm", no brand first | **Confirmed** | P1, F9 |
| The proven hook format is "Why do/don't [situation]?" | **Not supported** | no measured winner opens on a why-question; "Why am I so awkward at small talk?" appears only as line 3–4 of a body |
| Mechanism (resonance/release/breath) must be present in every script | **Falsified as written** | 0 of 30 winning transcripts mention it; winners use "articulation training… reflexes that organize your thoughts" (P5). Decide whether this is a brand mandate or a hypothesis (Q3) |
| Repeat the hook at the end (wrap structure) | **Not observed** | no winner does it |
| UGC 15–60 s; web funnel 30–60 s; app installs 15–30 s | **Web falsified, install confirmed** | P10 |
| Podcast format 30–90 s, Aria + Nick | **Partially confirmed** | the podcast Q&A is the workhorse body, but it is 60–90 s inside a 130 s+ ad and is played by generated actors, not Aria/Nick |
| App screen must appear | **Partially confirmed** | a lesson list appears; actual UI is rare; competitors show UI working (P13) |
| Never use Mehrabian 93% | **Rule confirmed, practice violated** | F4 |
| One avatar per ad; ten avatars available | **Two avatars carry everything** | 47-year-old professional who goes quiet; fluent non-native judged on accent. Founder, HR, Creator, Toastmasters: no winner, untested |
| Awareness × sophistication × 8 script formulas | **Untested** | no script in the doc is labelled with them; measured winners are a story-arc hook + PAS body hybrid |
| Winners: clean audio, calm Aria voice, app screen | **Not what wins** | winners are dialogue dramas with actors, not calm presenter narration |
| criteria.md six-dimension rubric | **Usable as a gate**, but Hook Rate and Message Clarity need the P1/P2/P5 definitions swapped in (flinch + reframe + named practice, not "why-question + resonance") |

---

## 6. What we still don't know (questions for Ivan)

1. **Persona pages.** Are Charisma Academy / Michelle Lee / Anna Jones / Robert Smith (buildcharisma.com) Vocal Image's own web funnel? Why did all of them stop between 19 July and 8 August, and is "Speak with Impact" or the brand page the replacement? This decides what the skill polls.
2. **Web-funnel ad-level numbers.** Meta ad-level on Web-01 and Web-02 timed out six times. Is there a CSV export or a dashboard, or should it be retried at a quieter hour? Without it the web side stays at doc-snapshot fidelity.
3. **Resonance/release.** Brand mandate, or hypothesis? No winner uses it. If it is a mandate, the skill will write it in; if a hypothesis, the skill will propose one test creative.
4. **Hook rate.** You cite 63% for 61_C. Is there a hook-rate / 3-second-view sheet for all creatives? That is the single most valuable dataset missing; it would let P1–P3 move from purchase-inferred to directly measured.
5. **KR_TST_76_A_1_2.** Best hold metrics in the account (15 s average watch, 7.9% to midpoint, €5.81). Its script is not in TST_IVAN_04. Where is it?
6. **The 93% / 81% lines.** Remove from the shared body VO on the next upload? They are live in two top-ten ads.
7. **Losers.** Only 81_A, 63_A and 64_C can be inferred as weak from the doc. Which creatives were killed, and for what reason? A short list of 5–10 dead ones with the reason would double the value of §4.
8. **Other script docs.** KR_TASKS (view-only), the Andrei docs, and wherever KR_TST_68 / IT_TST_71 / IT_TST_91 live. Access or paste.
9. **Install vs web body.** Should the skill treat the 45-second BASIC/PRO contrast body as the default install body and the podcast body as the default web body, or is that a coincidence of what was uploaded where?
10. **Live product demo.** P13's untested gap: do you want the skill to propose a "record → score → fix" beat as one of the two variants by default?

---

## 7. Provenance and quota

- Spiral: about 42 read-only calls, all priced 0.0, `available_credits` 0 → 0. All results are in `evidence/`, including raw JSON for transcripts and collections. Repeat `ad_creative_analysis` calls return cached results, so re-running the analysis is free.
- Meta Ads MCP: 4 successful calls, 6 timeouts on Web-01/Web-02 ad level. Conversation id kept constant.
- Google Drive: 1 read (TST_IVAN_04). No writes to any doc.
- No image or video generation. No commits made; `context/winning-ads/` and `context/scripts/` are new, untracked, and not gitignored.
