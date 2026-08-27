# Competitor Hero-Video Research — Definitive Edition (39 files)

**Project:** Vocal Image homepage hero (vocalimage.app)
**Audience:** Head of Creative Production; CEO; CTO
**Date:** 2026-08-07
**Supersedes:** the 2026-08-07 05:02 edition of this file (28 files) and the 04:32 draft (21 files). Extends `phase-1-reference-library.md`.

**Governing constraint on every judgement below:** there will be **no filming**. No shoot day, no actors, no camera. Everything must be achievable with AI generation (Higgsfield / Kling / Veo-class), licensed stock, motion graphics, code-rendered canvas/SVG/DOM, and screen recordings of the real Vocal Image app.

**Placement:** the hero sits **above the existing interactive quiz**. Its job is to earn the scroll into the quiz — not to convert on its own.

### What changed since the 28-file edition

Eleven files were added, and they are not more language apps. They are a deliberately sampled **craft tier** — best-in-class web heroes from outside the category (Clay, Retool, Resend, Cartesia, Superhuman, Rive, Lovable, Granola, Warp) plus two voice-AI infrastructure brands (Vapi, Hume AI). Four findings moved materially as a result, and one previous finding was **wrong and is retracted** (§1.3).

### Evidence base

| | Count | Provenance |
|---|---|---|
| **Media files measured at file level** (ffprobe duration/resolution/codec/stream inventory; `volumedetect`; ffmpeg scene detection; frame extraction) | **39** | this dataset |
| Of those, placement-confirmed heroes (tier H) | 25 | this dataset |
| Hero-adjacent widgets / decorative loops (tier A) | 8 | this dataset |
| Confirmed **not** heroes (tier N) | 5 | this dataset |
| Placement unconfirmed (tier U) | 1 | this dataset |
| Files measured but confirmed not heroes and excluded from all statistics (Tandem `homepage_video.mp4`, Pimsleur `video2839`) | 2 | prior round |
| Homepages probed across all rounds | 117 | **prior round** — see §7.5 |
| Homepages serving **no** hero motion asset of any kind | 75 (64%) | **prior round** — see §7.5 |
| Homepages blocked / unverifiable | 17 (15%) | **prior round** — see §7.5 |
| Assets found this round with a hero but no measurable file | 1 (Superlist) | this dataset |

Every number below traces to one of those measurements. Inference is marked **[inferred]**. Numbers carried from an earlier round are marked **[prior round]**. Where the evidence is thin or self-contradictory, it says so in the sentence.

---

## 1. Executive summary — the eight findings that change what we build

### 1.1 The entire voice-and-speech category ships heroes you cannot hear — and nobody has claimed the opposite position *(most surprising)*

Across 39 measured files:

| Audio state | Files | Share |
|---|---|---|
| **No audio stream at all** (ffprobe returns zero audio streams — not a `muted` attribute) | 22 | 56% |
| Audio stream present but decodes to **digital silence** (−91 dBFS mean/max) | 11 | 28% |
| **Total carrying nothing audible** | **33** | **85%** |
| Real audio content | 6 | 15% |

The eleven dead containers are pure waste — AAC/Opus tracks muxed into the file carrying −91 dB across the whole runtime: Oratori, Vocal Image's own `website_cover.mp4` (verified sample-by-sample), Whoop, Speak, LanguaTalk, FluentU, Framer, Arc/Dia, Retool, Resend, Lovable.

The six with real audio: Ovation (119.9 s narrated trailer), Jumpspeak (228.97 s Wistia ad), Hume AI (144 s below-hero explainer), Lingopie (music bed only — Whisper returned almost no intelligible speech), **Speechify** (the audio *is* the product's own TTS output reading the on-screen document), **Bodyswaps** (4 s of the avatar's spoken question, then true −91 dB silence for the remaining 4.9 s).

Read that list again. In a category built entirely on **how people sound**, three of the six audible assets are long-form ads that are not heroes at all, one is a music bed, and the only two short-form pieces that keep sound are the two where **the sound is the demonstration**.

**Nobody in the set offers opt-in audio.** Not one hero ships a mute-toggle affordance inviting the visitor to hear the product. That is an unoccupied position on a homepage for a voice-coaching app, and it is free — an `<audio>` element and a button. See §6.4.

**Consequence:** ship the loop with **no audio stream at all** (the default), and add a single opt-in unmute control carrying 3 seconds of a real before/after voice. Do not commission narration or a music bed for the hero — that budget belongs to the paid-social and YouTube cuts.

### 1.2 Two thirds of this category ships no hero video at all, and four more craft-tier brands just confirmed it with fresh DOM evidence

75 of 117 homepages carried **zero** hero motion asset [prior round], each backed by per-brand grep evidence with byte offsets. That included Babbel (a preloaded 2304×1693 PNG), Duolingo (an inline SVG, mask id `splash/HeroImage`), Preply (1.21 MB of HTML, zero video bytes), Rosetta Stone, Busuu, Memrise, Lingoda, Mondly, Lingvist, HelloTalk, Speakly, Pimsleur, Calm, Headspace, BetterUp.

This round adds four independent confirmations, three of them from companies with excellent video craft:

| Brand | Hero mechanism | Evidence (this dataset) |
|---|---|---|
| **Speechify** | Static: headline + 4 trust badges (Apple Design Award, 1M+ 5-star reviews, Chrome Extension of the Year, 60M+ users) + a celebrity photo strip | Hero `<section>` spans byte 62365–96421 and contains **zero** `<video>`/`<canvas>` (6 `<img>` only). First `<video>` at byte 107932, in a later section. |
| **Warp** | Static screenshot (`hero-left-aligned-with-photo`) | The measured 48.21 s file is a **background loop inside a below-hero announcement section** (`backgroundMode:true`, 45% dark overlay) |
| **Hume AI** | `<canvas>` strip over a CSS gradient, directly under the H1 | curl: zero `<video>`/`<source>`; only false-positive match on `manifest.webmanifest`. The measured 144 s asset is a below-hero YouTube embed. |
| **Spline** | Live WebGL canvas — `prod.spline.design/9951u9cumiw2Ehj8/scene.splinecode`, two-finger-orbitable | No video/mp4/webm/m3u8/YouTube asset of any kind |

Add **Blinkist** (three ~150 px Lottie-class loops orbiting a *static* PNG) and **Superlist** (a `<video>` shipped with an empty `src` that never resolves — see §7.3), and the pattern is unambiguous.

**Of 8 verified voice-AI brands, 7 ship no hero video** — Rime (5 canvases, `<canvas class="hero_canvas">` sits immediately *before* the H1), Hume, Wispr Flow (animated inline SVG `textPath` marquees), Deepgram, Sesame, Speechmatics, Camb.ai; Murf keeps its video below the fold [prior round]. The exception is ElevenLabs (HLS ladder) [prior round].

**Consequence:** the bar is not "beat RiseGuide's 88-second film." It is "be one of a handful of companies in this segment with a hero video that actually works." This is a differentiation play in a mostly empty field — and a static hero must be an arm in the test (§6.6), not an assumption we skip past.

### 1.3 RETRACTION: "every pure-footage hero needs a camera" was wrong. The constraint that bites is **specificity**, not filming

The 28-file edition stated: *"Every pure UI, pure motion-graphics, and pure AI-avatar hero in the set is fully no-shoot. Every pure-footage hero is not."* The second sentence does not survive the craft tier.

| Pure-footage hero | Duration | Shots | No-shoot verdict | Why |
|---|---|---|---|---|
| **Vapi** `hero-a.mp4` / `hero-b.mp4` | 11.01 / 13.01 s | 1 each | **YES** | Generic licensed stock ("man on phone call in glass office," "woman speaking into phone by a window"). Mirrored via CSS `-scale-x-100`, zero brand-specific content. Re-licensable from Pexels for $0, or generatable — no dialogue to lip-sync, no audio track to sell. |
| **Superhuman** `hero-background.mp4` | 26.58 s | 1 | **YES** | Golden-hour sky, pink-violet clouds, silhouetted grass. One Kling/Veo prompt or one Pexels download. Zero product, people, or brand mark. |
| Yousician | 15.0 s | 7 | NO | 5 instruments, 5 actors, close-up hand-to-fret/key contact |
| Oura | 6.37 s | 1 | NO | Uncut macro of a live ladybug on the real ring; correct-scale reflections off polished metal |
| Praktika | 17.68 s | 1 | NO | 17.68 s of one uncut naturalistic facial performance, no edit points to hide identity drift |
| **Granola** `sirine-call-512.mp4` | 10.0 s | 1 | **NO — strategically, not technically** | A tool could generate a similar idle webcam face. Doing so **forfeits the only thing the asset sells**: verifiable human authenticity as a trust signal. |

The corrected law: **AI/stock can replace footage that is generic; it cannot replace footage whose value is that it is specifically real.** Granola is the sharpest case in the whole sweep — 58 KB, 512×288, 10 seconds, no audio, no cuts, a real person faintly smiling on a webcam — and it is unremakeable *because faking it destroys the argument*.

Our constraint therefore costs us exactly one capability: **proof by a real, verifiable human**. Everything else — mood footage included — is on the table.

### 1.4 The real construction law is about **purity of material**, not about heroes

The Phase-1 claim ("5 of 8 heroes were a single unbroken shot") and the 28-file revision ("cutting requires footage to cut between") are both replaced by a cleaner correlation:

| Composition | Files | Shot counts | Single-shot rate |
|---|---|---|---|
| Pure UI screen recording | 7 | 1, 1, 1, 1, 1, 1, 5 | **6/7 (86%)** |
| Pure motion graphics / vector / 3D render | 9 | 1, 1, 1, 1, 1, 1, 3, 3, ~10 | **6/9 (67%)** |
| Pure real footage | 6 | 1, 1, 1, 1, 1, 7 | **5/6 (83%)** |
| Pure AI-avatar render | 2 | 1, 2 | 1/2 |
| **All pure compositions** | **24** | | **18/24 (75%)** |
| **Mixed** (two or more material types intercut) | **15** | 1, 1, 1, 1, 1, 2, 6, 7, 7, 9, 18, 18, 19, 72, 76 | **5/15 (33%)** |

Every montage over 5 shots in the entire set is a mixed composition. **Montage is what happens when a team has two kinds of material to intercut** — footage plus UI, live action plus CGI, stock plus screen capture. If the hero is made of one kind of thing, it is one shot 75% of the time regardless of what that thing is.

Across all 39 files: **23 single-shot (59%)**. Restricted to the 25 placement-confirmed heroes: **14 single-shot (56%)**.

**Consequence:** we will produce a single-shot hero — not because the category "rewards" it, but because a one-material build (real app screen recording plus type) is the only build our constraint cleanly supports, and one-material builds do not cut.

### 1.5 Only 25 of 39 measured files are actually in a hero slot, and several of the best-engineered assets sit below a static hero

| Tier | Files | Brands |
|---|---|---|
| **H** — placement-confirmed hero | 25 | BoldVoice, ELSA, Oratori, Loora, Final Round, Quantified, Exec, Cambly ×2, Yousician, Ovation, Oura, Whoop, Langotalk, Praktika, Lingopie, LanguaTalk, FluentU, Framer, Arc/Dia, Clay, Cartesia, Vapi, Superhuman, Lovable |
| **A** — hero-adjacent widget / decorative loop | 8 | Bodyswaps (540×410 CSS box), Blinkist (150 px accents), Speak ("Card Section" filename), TalkPal (~300–424 px widget), Pitch, Rive (ticker under the H1), Granola (tiles around the headline), Resend (225 px corner, mobile-only fallback) |
| **N** — confirmed not a hero | 5 | Speechify, Vocal Image, Jumpspeak, Warp, Hume AI |
| **U** — placement unconfirmed | 1 | Retool ("M4 Teaser Sample Loop" — filename and content both read as an internal teaser) |

Speechify, Warp and Hume all have genuinely good video craft **and all three chose a static hero anyway**, putting the video below the fold. That is three independent, deliberate decisions by well-resourced teams — the strongest form of the §1.2 evidence.

### 1.6 A hero with no moving human in it is the modal choice — 49% of files

| Human presence | Files | Share |
|---|---|---|
| **No human likeness of any kind** | 14 | 36% |
| Human present only as a **static** asset (UI thumbnail, still photo plate, illustrated portrait) | +5 | **49% cumulative** |
| Fully synthetic performing human (AI avatar / 3D render) | 3 | 8% |
| Hybrid (synthetic or stock face inset into a UI build) | 2 | 5% |
| Filmed real humans as primary subject | 15 | 38% |

The 14 with no human at all: ELSA (illustrated blob mascot), Oratori, Oura, Whoop, Blinkist, Pitch, Arc/Dia, Clay, Cartesia, Resend, Retool, Lovable, Superhuman, Rive.
The 5 static-only: Loora (profile thumbnail), Speechify ("Gwyneth" headshot chip), Framer (stock CMS headshots), Speak (one café photograph that never moves), TalkPal (four 224×224 illustrated character PNGs).

### 1.7 There is a third hero architecture we had not named: **the video carries no information and the DOM does all the arguing**

Five measured heroes deliberately separate the layers. The video is cheap, generic and swappable; the value proposition lives in HTML on top of it.

| Brand | Video content | Where the argument actually lives |
|---|---|---|
| **Vapi** | Two stock clips of people on phone calls, 1 shot each, no audio, no text, no product | H1 "Speak human to every customer" + a **live interactive widget** that places a real phone call to a working Vapi voice agent |
| **Superhuman** | Golden-hour sky and grass, 0 cuts, no audio, no text | HTML-overlaid headline copy and UI screenshots elsewhere on the page (DOM class `hero-background-video_videoContainer`) |
| **Cartesia** | 5.83 s procedural black-and-white ordered-dither blob, 209 KB | Page copy entirely |
| **Clay** | 17.14 s CG clay diorama, ball-run automation metaphor, 2:1 with ~50% dead space reserved for text | The reserved text region |
| **Resend** | 400×400 tumbling faceted cube, 654 KB, **mobile-only** (`md:hidden`) fallback for a desktop interactive WebGL element | Page copy entirely |

Two adjacent engineering facts from the same batch:

- **Vapi's "second clip" is not an edit.** ffmpeg scene detection at thresholds 0.3, 0.05 and 0.05 again found **zero** scene changes in either file. The page stacks two `<video>` elements and cross-fades them with a CSS opacity transition. You can build a multi-clip hero with zero encoded cuts and swap either clip without re-rendering anything.
- **Exec** does the same trick vertically: one long screen-recording pass with two independently-looping small clips (`ai-vid.mp4`, `participant.mp4`) absolutely-positioned on top at fixed screen coordinates as separate `<video>` tags.

**Consequence for us:** this is the cheapest, most iterable hero architecture in the entire sweep, and it is directly relevant because our page already has an interactive element below the fold. §6.2 argues against adopting it wholesale — but §5.2 ranks DOM-layer compositing highly as a *technique* regardless.

### 1.8 Vocal Image's own existing asset remains the worst-matched file in the entire measured set, on every axis

`https://static.vocalimage.net/videos/website_cover.mp4` — 1080×1080, 24.448 s, **18 shots**, 6.78 MB, H.264, AAC stream present but verified silent sample-by-sample.

- **Highest cut rate of all 39 files: 0.695 cuts/second** (17 cuts / 24.448 s), ahead of FluentU (0.680), Ovation's two-minute trailer (0.626) and Hume's 144 s explainer (0.493).
- Square 1:1, against our 9:16 default.
- Opens on an out-of-focus rack-focus pan that reads as an editing accident — a fatal first frame for poster or thumbnail use.
- Its one product-revealing shot type — a real hand holding a real phone showing real app UI, repeated across 5–6 people — is precisely the shot our constraint forbids and AI generation renders worst (hand grip, screen glare, skin-vs-plastic realism).
- **It has never been embedded on the homepage.** It exists only as an `og:video` meta tag.

The company with no hero video cuts faster than every company that has one. It is a paid-social cutdown wearing a hero's URL.

---

## 2. Master table — all 39 measured references

**Shot-count normalisation.** Measuring agents used two conventions for `cutCount`: some reported ffmpeg scene-detector output (unbroken take = `0`), others reported shot count (unbroken take = `1`). Cross-checking each entry's prose against its number confirms both mean **one unbroken shot** — Oura is `cutCount: 1` but its analysis says "zero cuts to hide any seam"; Loora was measured twice and returned `0` and `1` for the same file; Vapi is `cutCount: 1` with an explicit note that scene detection found zero changes. **Shots = max(cutCount, 1)**, each value verified against its descriptive text. **Cuts = shots − 1.**

**Segments.** `CAT` = speech/language/communication coaching (the actual competitive set). `VAI` = voice-AI infrastructure (adjacent). `CRAFT` = deliberately sampled best-in-class heroes from outside the category.

**Tiers.** `H` hero-confirmed · `A` hero-adjacent · `N` confirmed not a hero · `U` placement unconfirmed.

| # | Brand | Seg | Media URL | Resolution / aspect | Dur (s) | Shots | Cuts | MB | MB/s | Codec | Audio | Composition | Sound-off | No-shoot | Tier |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BoldVoice | CAT | `boldvoice.com/videos/homepage.mp4` | 390×740 · 0.527 | 6.57 | 1 | 0 | 0.27 | 0.041 | H.264 | none | mixed — filmed talking head + MG mouth-anatomy overlay | by-UI | **PARTIAL** | H |
| 2 | ELSA Speak | CAT | `cms-asset.elsanow.io/…ELSA_Speak_full_V2_720p….webm` | 720×720 · 1:1 | 49.73 | 1 | 0 | 2.07 | 0.042 | VP9 | none | motion graphics (mascot + UI mockups) | by-typography | **YES** | H |
| 3 | Oratori | CAT | `oratori.app/assets/video/oratori-app-preview.mp4` | 886×1920 · 0.461 | 30.00 | 1 | 0 | 3.50 | 0.117 | H.264 + AAC | −91 dB | UI screen recording (real iOS capture, sped up) | by-UI | **YES** | H |
| 4 | Loora | CAT | `loora.ai/legacy/hero_vdo.webm` (H.264 twin `.mp4`) | 412×720 · 0.572 | 32.07 | 1 | 0 | **0.54** | **0.017** | **AV1** (twin: H.264, 1.04 MB) | none | UI screen recording | by-UI | **YES** | H |
| 5 | Speechify | CAT | `website.cdn.speechify.com/platform-web-app-1.mp4` | 1610×1008 · 1.597 | 19.54 | 1 | 0 | 0.68 | 0.035 | H.264 + AAC | **real** (product TTS) | UI screen recording | by-UI | **YES** | **N** |
| 6 | Final Round AI | CAT | `d12araoe7z5xxk.cloudfront.net/…FinalRound_UI01_16x9.mp4` | 960×540 · 16:9 | 14.00 | 1 | 0 | 0.51 | 0.036 | H.264 | none | UI screen recording + 2 static call tiles | by-UI | **YES** | H |
| 7 | Quantified.ai | CAT | `…6a277d7de2380af8415cfbf7_HomepageLoop_mp4.mp4` | 1278×720 · 1.775 | 9.87 | 2 | 1 | 0.64 | 0.065 | H.264 (VP8 twin 2.83 MB) | none | AI-avatar footage only, 2 personas | **no** | **YES** | H |
| 8 | Exec | CAT | `res.cloudinary.com/…homepage-hero4k_gro4gw.mp4` | 1250×750 · 5:3 | 20.37 | 1 | 0 | 0.63 | 0.031 | **VP9** in .mp4 container | none | screen rec + AI-avatar inset + real webcam inset (separate `<video>` tags) | by-UI | **PARTIAL** | H |
| 9 | Cambly (02) | CAT | `camblycdnimages…/1600x600-Video_02_v02_241024.mp4` | 1600×600 · 8:3 | 20.05 | 7 | 6 | 2.72 | 0.136 | H.264 | none | real footage + app screen composited into devices | by-expression | **NO** | H |
| 10 | Cambly (03) | CAT | `camblycdnimages…/1600x600-Video_03_241026.mp4` | 1600×600 · 8:3 | 20.05 | 6 | 5 | 2.34 | 0.117 | H.264 | none | 5 filmed shots + 1 overhead real-UI shot | by-expression | **PARTIAL** | H |
| 11 | Bodyswaps | CAT | `bodyswaps.co/hubfs/Nova speaking…mp4` | 3840×2160 (displayed 540×410) | 8.88 | 1 | 0 | 9.39 | 1.057 | H.264 + AAC | **real** 0–4 s, then −91 dB | 3D game-engine avatar inside hand-coded HTML/CSS chrome | by-typography | **YES** | **A** |
| 12 | Yousician | CAT | `assets.yousician.com/…all_instruments_being_played.mp4` | 1280×720 · 16:9 | 15.00 | 7 | 6 | 3.84 | 0.256 | H.264 | none | real footage | by-imagery | **NO** | H |
| 13 | Ovation | CAT | `d1syj4d8txnu77…/Ovation_Trailer_Website_Captions2.mp4` | 854×480 · 16:9 | 119.90 | **76** | 75 | 16.63 | 0.139 | H.264 + AAC | **real** VO | mixed — live action + VR capture + UI + hardsubs | by-typography | **PARTIAL** | H |
| 14 | **Vocal Image** | CAT | `static.vocalimage.net/videos/website_cover.mp4` | 1080×1080 · 1:1 | 24.45 | 18 | 17 | 6.78 | 0.277 | H.264 + AAC | verified silent | mixed — stock B-roll + UGC phone-in-hand + UI inserts | by-UI | **PARTIAL** | **N** |
| 15 | Langotalk | CAT | `langotalk.org/langavideo/idle.mp4` | 1440×1440 · 1:1 | 5.08 | 1 | 0 | 5.45 | 1.073 | H.264 | none | 3D CGI avatar idle loop (1 of 3 layered videos) | **no** | **YES** | H |
| 16 | Praktika | CAT | `praktika.ai/assets/intro-BBoGofYM.mp4` | 358×636 · 0.5629 | 17.68 | 1 | 0 | 3.12 | 0.176 | H.264 | none | real footage — one uncut talking head | by-expression* | **NO** | H |
| 17 | Lingopie | CAT | `d1ndg56vpa7k9f…/homepage/landingvideo.mp4` | 852×480 · 16:9 | 42.28 | 9 | 8 | 3.71 | 0.088 | H.264 + AAC | music, no VO | mixed — lifestyle footage + real app capture + licensed TV + kinetic type | by-typography | **PARTIAL** | H |
| 18 | LanguaTalk | CAT | `res.cloudinary.com/chatterlang/…lesson_final_zbvmrq.mp4` | 1280×772 · 1.658 | 29.36 | 2 | 1 | 1.57 | 0.053 | H.264 + AAC | −91 dB | real webcam call + screen-share in a laptop mockup, B&W | by-UI | **PARTIAL** | H |
| 19 | TalkPal | CAT | `cdn.lottielab.com/l/999tpU9R4J8q40.json` | 461×461 vector · 1:1 | 3.30 | 1 | 0 | 0.18 | — | **Lottie JSON** | n/a | vector MG + 4 embedded 3D character PNGs | by-UI | **YES** | **A** |
| 20 | Jumpspeak | CAT | `embed-ssl.wistia.com/deliveries/ecbce66…bin` | 1920×1080 · 16:9 | 228.97 | 19 | 18 | 72.51 | 0.317 | H.264 + AAC | **real** VO | mixed — founder monologue + UGC testimonials + app capture | partial | **NO** | **N** |
| 21 | FluentU | CAT | `player.vimeo.com/video/933909025` | 1920×1080 · 16:9 | 25.00 | 18 | 17 | 8.98 | 0.359 | H.264 + AAC | −91 dB | mixed — licensed film/TV + real app capture + type cards | by-typography | **YES** | H |
| 22 | Speak | CAT | `s3.usespeak.com/…Summer Release Card Section Hero.mp4` | 660×780 · 0.846 | 32.10 | 1 | 0 | **15.18** | **0.473** | H.264 + AAC | −91 dB | one static photo plate + animated UI card overlay | by-typography | **YES** | **A** |
| 23 | **Vapi** | VAI | `vapi.ai/airfoil/hero/hero-a.mp4` (+ `hero-b`, 13.01 s) | 1280×720 · 16:9 | 11.01 | 1 | 0 | 1.97 mp4 / **0.65 webm** | 0.059 (webm) | **HEVC (hvc1) + VP9 — no H.264 at all** | none | real footage (licensed stock), DOM-crossfaded with a 2nd clip | by-DOM-overlay | **YES** | H |
| 24 | Hume AI | VAI | `youtube.com/embed/c5W7w2eYuYc` | 1920×1080 · 16:9 | 144.00 | 72 | 71 | 21.10 | 0.147 | AV1 + Opus | **real** VO | mixed — stock live action + UI comp + kinetic type + particle viz | partial | **YES** | **N** |
| 25 | Cartesia | VAI | `cartesia.ai/hero/dither.mp4` | 1920×1400 · 1.371 | 5.83 | 1 | 0 | **0.21** | 0.036 | H.264 | none | procedural motion graphics (ordered-dither shader loop) | **no** | **YES** | H |
| 26 | Oura | CRAFT | `ourahealth.imgix.net/cooper-home-hero-1920.mp4` | 1920×1080 · 16:9 | 6.37 | 1 | 0 | 1.39 | 0.218 | H.264 | none | real footage (macro, live insect) | by-metaphor | **NO** | H |
| 27 | Whoop | CRAFT | `videos.ctfassets.net/…HomepageHero_JanJump_16x9_Final.mp4` | 1920×1080 · 16:9 | 9.69 | 3 | 2 | 2.89 | 0.298 | H.264 + AAC | −91 dB | 3D CGI product render | **no** | **YES** | H |
| 28 | Blinkist | CRAFT | `static.blinkist.com/…/animation/ear.webm` (+ stars, glasses) | 194×160 / 150×150 | 5.00 | 1 | 0 | **0.015** | 0.003 | VP9 (+ HEVC .mov twins) | none | MG icon loops around a **static PNG hero** | by-UI | **YES** | **A** |
| 29 | Framer | CRAFT | `framerusercontent.com/assets/4RV4Erj59YHt6T06Ry7ab5tVI.mp4` | 2320×1300 · 1.784 | 21.03 | 5 | 4 | 3.78 | 0.180 | H.264 + AAC | −91 dB | UI screen recording + continuous virtual-camera moves | by-UI | **YES** | H |
| 30 | Pitch | CRAFT | `framerusercontent.com/assets/VwM40s9Ta5Cdfdl3djKPm57NAQ.mp4` | 1920×1080 · 16:9 | 8.77 | 1 | 0 | 0.37 | 0.042 | H.264 | none | UI screen recording | by-UI | **YES** | **A** |
| 31 | Arc / Dia | CRAFT | `arc.net/video/ArcDiaPLG_Video.mp4` | 3106×2160 · 1.438 | 6.70 | 1 | 0 | 4.65 | 0.694 | H.264 (+ VP9 webm) | −91 dB | UI screen recording (sidebar crop) | by-typography | **YES** | H |
| 32 | Clay | CRAFT | `assets.clayrun.dev/Hero 06-02 Lossy 0001-0240.mp4` | 3000×1500 · 2:1 | 17.14 | 1 | 0 | 12.35 | 0.720 | H.264, **14 fps** | none | motion graphics (CG clay-diorama ball run) | **no** | **YES** | H |
| 33 | Retool | CRAFT | `dqpcjghenxt8u.cloudfront.net/video/M4+Teaser+Sample+Loop.mp4` | 1920×1080 · 16:9 | 32.17 | ~10† | ~9† | 4.79 | 0.149 | H.264 + AAC | −91 dB | motion graphics — floating UI screenshots in 3D parallax | by-UI | **YES** | **U** |
| 34 | Resend | CRAFT | `resend.com/static/cube.mp4` | 400×400 · 1:1 | 10.00 | 1 | 0 | 0.64 | 0.064 | H.264 + AAC | −91 dB | 3D CGI object loop — **mobile-only** (`md:hidden`) fallback for a desktop WebGL element | **no** | **YES** | **A** |
| 35 | Superhuman | CRAFT | `superhumanstatic.com/…/shared/hero-background.mp4` | 3320×2160 coded (SAR 270:311) → ~415:311 | 26.58 | 1 | 0 | 2.65 | 0.100 | **HEVC Main10** (10-bit), ~60 fps VFR | none | real footage — ambient sky/grass stock loop | by-DOM-overlay | **YES** | H |
| 36 | Rive | CRAFT | `cdn.rive.app/framer/data_driven2.mp4` (+ `product_ui2`, 2.43 s) | 1066×600 · 16:9 | 3.37 | 1 | 0 | 0.44 | 0.132 | H.264, 59.94 fps | none | CGI device mockup + composited UI motion layer; **8-card horizontal ticker** | by-UI | **YES** | **A** |
| 37 | Lovable | CRAFT | `storage.googleapis.com/lovable-assets/videos/homepage/scene-1..3.webm` | 2000×1400 · 10:7 | 17.97 (3 files) | 3 | 2 | 7.35 | 0.409 | VP9, 24 fps (Opus −91 dB on 2 of 3) | −91 dB | motion graphics + UI screen recording | by-UI | **YES** | H |
| 38 | Granola | CRAFT | `granola.ai/homepageAssets/call-videos/sirine-call-512.mp4` (+ camilla) | 512×288 · 16:9 | 10.00 | 1 | 0 | **0.058** | **0.006** | H.264 | none | real footage — genuine webcam idle loop | **no** | **NO** | **A** |
| 39 | Warp | CRAFT | `cdn.sanity.io/files/…6103609f.mp4` | 1280×720 · 16:9 | 48.21 | 7 | 6 | 2.41 | 0.050 | H.264 Constrained Baseline, ~24 fps | none (deliberately stripped) | mixed — filmed CEO interview + caption cards + GitHub status chips | by-typography | **PARTIAL** | **N** |

\* Praktika's `soundOffLegible` field was never reported by the measuring agent. Classification is **[inferred]** from two confirmed facts: no audio stream, and no on-screen text in any sampled frame.
† Retool's raw ffmpeg scene detector fired **16** times, but the measuring agent flagged that 8 of those fire within 12.3–13.3 s (roughly every 3 frames) as a single deliberate glitch-transition. Adjusted to ~9 real transitions / ~10 shots; raw value retained here for traceability.

**Measured but confirmed not heroes, excluded from all statistics** [prior round]:

| Brand | Asset | Measurement | Why excluded |
|---|---|---|---|
| Tandem | `homepage_video.mp4` | H.264, 414×896, 24 fps, 18.000 s, 3.60 MB, 0 scene cuts | Sits at 39.8% document depth vs H1 at 11.3%; Contentful labels it `"fallbackScreen"`; `_updatedAt` 2020-05-28 |
| Pimsleur | `video2839` | H.264, 1920×1080, 88.11 s, 39.67 MB | Belongs to a "Rave Reviews" testimonial carousel |

**Inherited from Phase 1, not re-measured — prior evidence only, excluded from every aggregate in §3:** RiseGuide (YouTube `jzkoouRNhWk`, 88 s, 18 cuts, iframe hero with the autoplay+mute+loop+playlist trick, no poster) · Yoodli (2880×2880, 15.1 s, one shot, pure UI motion graphics, zero people) · Descript (transparent WebM with alpha channel, 25.5 s, one shot) · ElevenLabs (HLS + 1080/720/480 ladder) · Poised (30.8 s, one shot) · Speak (720×720, 5.5 s, 92 KB).

---

## 3. Pattern analysis

*All percentages are over the 39 measured files unless stated. Where a statistic changes materially when restricted to the 25 placement-confirmed heroes (tier H), both numbers are given.*

### 3.1 Shot-count distribution

| Shots | Files | Share | Brands |
|---|---|---|---|
| **1 (single unbroken shot)** | **23** | **59%** | BoldVoice, ELSA, Oratori, Loora, Speechify, Final Round, Exec, Bodyswaps, Oura, Blinkist, Speak, Langotalk, Praktika, TalkPal, Pitch, Arc/Dia, Clay, Resend, Cartesia, Vapi, Superhuman, Rive, Granola |
| 2–3 | 4 | 10% | Quantified (2), LanguaTalk (2), Whoop (3), Lovable (3) |
| 5–10 | 7 | 18% | Framer (5), Cambly-03 (6), Cambly-02 (7), Yousician (7), Warp (7), Lingopie (9), Retool (~10) |
| 18–19 | 3 | 8% | Vocal Image (18), FluentU (18), Jumpspeak (19) |
| 72–76 | 2 | 5% | Hume (72), Ovation (76) |

**69% of all files run ≤3 shots. Tier H: 14 single-shot of 25 (56%).**

**Cut rate (cuts per second), highest first:** Vocal Image 0.695 · FluentU 0.680 · Ovation 0.626 · Hume 0.493 · Yousician 0.400 · Cambly-02 0.299 · Retool ~0.280 · Cambly-03 0.249 · Whoop 0.207 · Framer 0.190 · Lingopie 0.189 · Warp 0.124 · Lovable 0.111 · Quantified 0.101 · Jumpspeak 0.079 · LanguaTalk 0.034 · **all 23 remaining files: 0.000.**

### 3.2 Duration distribution

| Bucket | Files | Share |
|---|---|---|
| ≤10 s | 14 | 36% |
| 10–25 s | 13 | 33% |
| 25–50 s | 9 | 23% |
| >50 s | 3 | 8% |

| Cohort | n | Median | Mean |
|---|---|---|---|
| All measured files | 39 | **17.97 s** | 29.7 s (18.5 s excluding the three >100 s pieces) |
| Tier-H heroes | 25 | **17.97 s** | 23.2 s (19.1 s excluding Ovation) |
| Single-shot files | 23 | **10.00 s** | 15.2 s |
| **Single-shot tier-H heroes** | **14** | **15.57 s** | 18.1 s |
| Multi-shot files | 16 | 24.4 s | — |

**Nothing in the set argues for a hero longer than ~25 s.** The three long pieces (Jumpspeak 229.0 s, Hume 144.0 s, Ovation 119.9 s) are all narrated, cut-dense, sound-on ad grammar, and **all three are tier N** — none is a hero.

At the other end, the shortest workable loops cluster at 3–10 s: TalkPal 3.30, Rive 3.37, Blinkist 5.00, Langotalk 5.08, Cartesia 5.83, Oura 6.37, BoldVoice 6.57, Arc/Dia 6.70, Pitch 8.77, Bodyswaps 8.88, Whoop 9.69, Quantified 9.87, Resend 10.00, Granola 10.00. But BoldVoice's own teardown flags 6.57 s as *too* short — "risks feeling repetitive if watched more than a few seconds" — and Rive's 3.37 s card has a visible loop pop (§3.9).

The **15.57 s single-shot tier-H median** is the number to build to.

### 3.3 Aspect-ratio distribution

| Orientation | Files | Share | Brands |
|---|---|---|---|
| Vertical (<1.0) | 5 | 13% | Oratori 0.461, BoldVoice 0.527, Praktika 0.563, Loora 0.572, Speak 0.846 |
| Square (1:1) | 6 | 15% | ELSA 720², Vocal Image 1080², Langotalk 1440², TalkPal 461² vector, Blinkist ~150², Resend 400² |
| Landscape | 28 | 72% | everything else |

**16 of 39 (41%) sit on a ratio that matches no standard delivery spec:** BoldVoice 0.527, Oratori 0.461, Loora 0.572, Speak 0.846, Blinkist 1.213, Superhuman 1.334, Cartesia 1.371, Lovable 1.429, Arc/Dia 1.438, Speechify 1.597, LanguaTalk 1.658, Exec 1.667, Framer 1.784, Clay 2.000, Cambly ×2 at 2.667.

**Not one of the four vertical assets closest to 9:16 actually hits 0.5625.** Praktika 0.5629 (closest), Loora 0.5722, BoldVoice 0.5270, Oratori 0.4614. Every one is a crop of something else or a device-native screen-recording resolution shipped as-is.

Two craft-tier oddities worth noting because they are *deliberate*, not sloppy:
- **Superhuman** codes 3320×2160 with SAR 270:311, yielding a ~415:311 display frame — a non-square-pixel encode, HandBrake 1.10.2, HEVC Main10, at only 0.100 MB/s. Someone tuned this.
- **Clay** reserves roughly half of its 2:1 canvas as empty grass for the headline. The aspect *is* the layout.
- [prior round] **Sonos** carries `width`/`height` on the hero `<video>` as an *aspect ratio* — 16/9 desktop, 4/5 mobile — an art-directed reframe rather than a CSS crop. The only deliberate multi-ratio hero encountered in any round.

### 3.4 Human presence

Tabulated in §1.6. Restated as the number that matters: **19 of 39 (49%) contain no moving human being.** Only 6 of 39 (15%) are pure real footage, and 2 of those 6 (Vapi, Superhuman) are generic stock that a prompt or a Pexels search reproduces.

### 3.5 Audio

Tabulated in §1.1. **33 of 39 (85%) carry nothing audible. 11 of 39 (28%) ship a dead −91 dB container track** — pure overhead with no fallback narration. Whoop's teardown calls its own out explicitly; Resend's does too ("dead silent audio track that only bloats file size for zero payoff").

One measured counter-example to the "silent by default" habit: **Rive's `product_ui2.mp4` carries a real, non-silent AAC track that is muted client-side by the `muted` attribute.** Its sibling `data_driven2.mp4` has no audio stream at all. Two files, one page, two different decisions — evidence that nobody is auditing this.

### 3.6 Sound-off legibility

| Mechanism | Files | Share | Brands |
|---|---|---|---|
| **Legible by product UI** | 15 | 38% | BoldVoice, Oratori, Loora, Speechify, Final Round, Exec, LanguaTalk, TalkPal, Pitch, Blinkist, Vocal Image, Framer, Retool, Lovable, Rive |
| **Legible by burned-in typography** | 8 | 21% | ELSA, Bodyswaps, Ovation, Speak, Lingopie, FluentU, Arc/Dia, Warp |
| **Legible only via HTML/DOM text overlaid on the page** (the file itself says nothing) | 2 | 5% | Vapi, Superhuman |
| "Legible" only because nothing verbal exists to lose — meaning rides on faces/mood | 6 | 15% | Cambly ×2, Yousician, Oura, Praktika*, Granola |
| **Not legible** — conveys no information at all | 6 | 15% | Quantified, Langotalk, Whoop, Clay, Cartesia, Resend |
| Partial | 2 | 5% | Jumpspeak (founder monologue uncaptioned), Hume (thesis is a spoken-audio beat) |

**23 of 39 (59%) carry their argument in the video file's own text or UI.** Add the two DOM-overlay heroes and 25 of 39 (64%) carry an argument *somewhere* on the page.

**Zero of 39 use a caption track (`.vtt`).** Every legible piece burns its text into the pixels, uses the product's own on-screen text, or renders HTML on top.

The correlation from the 28-file edition survives and strengthens: **of the 6 mood-only-by-faces pieces, 4 are NO on no-shoot and 1 is PARTIAL. Of the 6 that convey no information at all, all 6 are YES on no-shoot.** Information lives on screens; screens are free to produce. Faces cost a camera.

### 3.7 Composition

| Composition | Files | Share | No-shoot YES rate |
|---|---|---|---|
| Mixed (two or more material types) | 15 | 38% | 5/15 |
| Pure motion graphics / vector / 3D render | 9 | 23% | **9/9** |
| Pure UI screen recording | 7 | 18% | **7/7** |
| Pure real footage | 6 | 15% | 2/6 |
| Pure AI-avatar render | 2 | 5% | **2/2** |

**Every pure UI, pure motion-graphics and pure AI-avatar file in the set is fully no-shoot — 18 for 18.** Mixed compositions are where every PARTIAL verdict lives: they are exactly the pieces where one filmed insert holds an otherwise no-shoot build hostage (Exec's `participant.mp4` webcam inset; BoldVoice's talking-head plate; Vocal Image's phone-in-hand reveal; Warp's CEO interview).

### 3.8 No-shoot feasibility

| Verdict | Files | Share |
|---|---|---|
| **YES** — fully reproducible with zero filming | 25 | 64% |
| **PARTIAL** | 8 | 21% |
| **NO** | 6 | 15% |

Among the 25 tier-H heroes: **YES 15, PARTIAL 6, NO 4** (Cambly-02, Yousician, Oura, Praktika — Jumpspeak and Granola, the other two NOs, are tier N and tier A).

Among the 23 single-shot files: **18 YES, 2 PARTIAL, 3 NO (78% fully no-shoot).** Among the 16 multi-shot files: 7 YES, 6 PARTIAL, 3 NO. **Single-shot construction and no-shoot production are the same decision viewed from two angles.**

The complete **NO** list, all six, with the exact blocker:

| Brand | What blocks it |
|---|---|
| Cambly (02) | 6+ real actors, 6 real interiors, extreme facial close-ups, un-directable micro-expressions |
| Yousician | 5 instruments, 5 actors; close-up hand-to-fret/key contact — a known AI-generation failure mode |
| Oura | 6.4 s uncut macro of a live ladybug on the real ring; correct-scale reflections off polished metal |
| Praktika | 17.68 s of one uncut close-up naturalistic facial performance — no edit points to hide identity drift |
| Jumpspeak | ~90 s founder monologue + 4-person synced-sentence montage + real UGC webcam testimonials |
| **Granola** | Technically generatable; **strategically unremakeable** — its entire argument is that the person is verifiably real |

### 3.9 Delivery engineering

| Metric | Best measured | Worst measured | Median |
|---|---|---|---|
| MB per second | Blinkist 0.003 (icon loops) · **Granola 0.006** (real human, 512×288) · **Loora 0.017** (full 32 s product tour at 412×720) | Langotalk 1.073 · Bodyswaps 1.057 · Clay 0.720 · Arc/Dia 0.694 · Speak 0.473 · Lovable 0.409 | ~0.12 |
| Codec | AV1: 2 (Loora, Hume/YouTube) · HEVC: 2 (Superhuman Main10, Vapi hvc1) · VP9: 4 (ELSA, Exec, Blinkist, Lovable) · Lottie JSON: 1 (TalkPal) | **H.264: 30 of 39 (77%)** | — |
| Dual-encode cost | Blinkist's HEVC `.mov` Safari twins are **3–10× larger** than the VP9 `.webm` for identical content (`stars.mov` 622 KB vs `stars.webm` 87 KB) | Quantified's VP8 `.webm` twin is **4.4× larger than its own H.264** (2.83 MB vs 0.64 MB) | — |

**Loora remains the single best-engineered asset in the sweep:** 32.07 s of a full five-screen product tour at 412×720 in **553 KB** of AV1 — 0.017 MB/s. Its own H.264 twin is 88% larger for identical content. It is one of only two AV1 files in 39.

Individually notable delivery behaviours, each measured:

| Pattern | Brand | Detail |
|---|---|---|
| **Correct accessibility + LCP pattern** | Oura | Hero `<video>` wrapped in `<div class="motion-reduce:hidden">` **and** preceded by a `<picture>` with `fetchPriority="high" loading="eager"`. The still ships first; the video is the enhancement. The only correct instance in any round. |
| **Correct simple delivery** | Yousician | Plain self-hosted `<video poster="hero-guitar-1-scaled.jpg" autoplay muted loop playsinline>`. No YouTube iframe, no HLS ladder. The poster JPG is the real first impression and the real LCP element. |
| **Interactive hero with a canned mobile fallback** | Resend | The 400×400 cube MP4 is wrapped in `md:hidden` — it is the *mobile substitute* for a heavier draggable WebGL cube on desktop. Ship the cheap loop as the degradation path, not a degraded interactive. |
| **Multi-clip hero with zero encoded cuts** | Vapi | Two stacked `<video>` elements, CSS opacity cross-fade (`duration-cross`). Scene detection at 0.3/0.05 finds zero changes in either file. |
| **No H.264 fallback at all** | Vapi | `<source type="video/quicktime; codecs=hvc1">` (the mimetype hack that makes Safari pick HEVC) + `<source type="video/webm">` VP9. Combined preloaded webm weight ≈ 2.15 MB for 24.02 s across both clips. |
| **Missing `loop`** | Arc/Dia | `<video>` has no `loop` attribute — it freezes after 6.7 s on a dense wall of small body copy. A hero's resting frame is a design decision; theirs is an accident. |
| **Visible loop seam** | Rive | `data_driven2.mp4` hard-jumps from its expanded end state back to frame 1 every 3.37 s. Tolerable in a peripheral ticker card; fatal at a fixation point. |
| **Deliberate mid-action frame 1** | Quantified | "Engineered to look caught mid-conversation so wherever the loop restarts it never reads as a cold open." Also measured in Oratori, Loora, Pitch, Speechify, Cambly, Praktika, Arc/Dia, Final Round, Vapi. |
| **Boxed, not full-bleed** | ELSA | `class="hero-video … object-contain"`, a 720×720 square — on wide viewports it sits with empty space beside it. |
| **Massively over-encoded for the delivered size** | Bodyswaps | 3840×2160 at 8,615 kb/s, CSS-cropped into a 540×410 box via `object-fit: cover`. ~93% of delivered pixels discarded. |
| **Low frame rate as a bandwidth choice** | Clay | 14 fps for a CG loop (still 12.35 MB — the frame-rate saving was spent elsewhere). |

---

## 4. What each video is actually arguing

Seven recurring argument-types emerge from the 39 `coreMeaning` findings. Several pieces run two; the primary is listed first.

### Type 1 — Mechanism proof: "here is the loop, watch it run"

**Brands (13):** Oratori, Loora, ELSA, Arc/Dia, BoldVoice, Final Round, Speechify, Pitch, Framer, Lingopie, FluentU, Lovable, Retool.

Show input → processing → output as one continuous sequence, so the viewer infers the product works by watching it work.

The strongest executions attach the loop to a *specific, named* defect:

- **Oratori** is the purest in the set: a real transcript ("Um, I'm currently working with big company. Um. Um.") is scored across five pillars (Clarity 6.5, Structure 3.0, Pace 5.5, Language 2.0, Presence 2.5), a "Fix This / Try This" card shows the exact sentence rewritten tighter, and the closing screen shows Initial 3.9 → +21 plus a streak milestone.
- **Loora** does the same at phoneme resolution: 93% pronunciation, `/w/ Excellent, /aa/ Very good, /ch/ Sounded like s`.
- **Arc/Dia** compresses it to three beats: typed question → a "Read 6 tabs" row of named source chips → streamed answer with the verdict line bolded first.
- **Lovable** abstracts the moment of generation itself into a **skeleton-to-colour reveal** — grey placeholder shapes resolving into a finished coloured UI as a prompt is typed.

**Cost of this type:** it asks the viewer to read. Loora's own teardown flags the phoneme table as "nearly illegible at typical hero-video display sizes." Oratori's 886×1920 crop makes its score numbers soft. Retool's floating dashboard cards are dense. **This type dies at small sizes and low bitrates.**

### Type 2 — Measured progress / scoreboard

**Brands (5):** Loora, Oratori, ELSA, Exec, Ovation.

A sub-type of mechanism proof where **numbers** do the arguing rather than the interaction: radar charts, percentage scores, streak counters, vocabulary estimates (Loora's "18,921"), 5-pillar breakdowns, ELSA's animated pentagon (Pronunciation 75%, Fluency 82%, Vocabulary 62%, Grammar 75%, Intonation 62%), Exec's "96%" call score.

**Why it matters for us:** this is the only argument-type in the entire 39 that turns an *invisible* attribute into a *visible object*. It is the category's answer to our exact problem.

### Type 3 — Proof by demeanour: a real face's genuine reaction is the whole argument

**Brands (7):** Praktika, Cambly ×2, Yousician, Jumpspeak, **Granola**, Quantified.ai (synthetically).

Praktika is the extreme case: 17.68 s, one uncut medium shot, no UI, no logo, no text, no audio — a woman's visible delight, with the camera positioned behind the phone so the viewer occupies the AI's seat. Granola is the minimal case: 10 s, 58 KB, a real person idling on a webcam, doing nothing but existing.

**Verdict for us: closed.** Five of these seven are the "NO" list. Quantified.ai attempts it synthetically and its own teardown catches an **uncropped AI-generation watermark** (a four-point sparkle, bottom-right, male segment only) plus a subtly-too-smooth hairline in every frame. The moment a viewer notices, the argument inverts.

### Type 4 — Ambient mood / brand texture

**Brands (7):** Oura, Whoop, Langotalk, Clay, Cartesia, Resend, Superhuman. (Blinkist as accents.)

No information at all. Oura's ladybug and Whoop's floating band lineup are luxury-goods grammar. Clay's clay-diorama ball run argues "a complex multi-step process runs itself" without a single frame of product. Cartesia's 209 KB dither loop argues "we are a technical, signal-processing company with obsessive taste" and nothing else. Superhuman's sky argues calm.

This type splits into two sub-cases that matter enormously to us:

- **Object-anchored mood** (Oura, Whoop): needs a photogenic physical product. **Closed for us** — a voice has no surface. The synthetic attempt at this in our category, Langotalk's 3D avatar idle loop, is explicitly flagged as "zero product proof… real uncanny-valley risk."
- **Abstract/procedural mood** (Cartesia, Clay, Resend, Superhuman): needs no object at all, costs 0.2–2.7 MB, and is 100% no-shoot. **Open to us** — and Cartesia is the proof point, because a shader-generated dithered blob is about as close to "rendering a voice" as anything in the sweep.

Both sub-cases share the same measured weakness: a first-time visitor learns nothing about the product. Whoop's teardown says it plainly — "it only works as a hero if the audience already knows the brand."

### Type 5 — Capability / breadth flex: "look how much this does"

**Brands (7):** Final Round AI, Ovation, ELSA, FluentU, Framer, Jumpspeak, Retool.

Enumerate features, models, scenarios, content libraries. Final Round opens on a dropdown of five AI models. FluentU spends the first 9 s (36% of runtime) on borrowed Marvel/Friends/TED footage before showing a single frame of its own product. Retool cycles 5–6 disconnected app examples with no throughline.

**Cost: density.** Final Round's own teardown says the 960×540 multi-column form UI "would be illegible and cramped at a 9:16 mobile hero size." ELSA's 7-beat tour runs 49.7 s. **This type does not fit above a quiz.**

### Type 6 — Category reframe: arguing what *kind of thing* this is

**Brands (7):** Oura (jewellery, not a gadget), Whoop (a drop, not a tracker), Cambly ("FaceTiming a friend, not a lesson"), Speechify ("the voice quality *is* the product"), Bodyswaps ("you're the second half of this conversation"), Rive ("this isn't a design toy, it's already the UI inside cars and smart hubs"), Wispr Flow (*unmeasured — the mess of real human speech, given a body*).

**Bodyswaps deserves separate attention: it is the only reference in the entire sweep that breaks the fourth wall.** Its hero is not a video to watch — it is a staged live interaction. The avatar asks a real, on-topic question ("How are you preparing your learners for the world of work?"), goes silent, and the surrounding hand-coded DOM chrome invites the visitor to press START RECORDING and answer. The `<video>` is one beat inside a three-beat HTML/CSS/JS sequence (`haB2`/`haB3`/`haB4`); only one actual video tag exists across all three.

### Type 7 — Product-as-hero: the hero *is* an instance of the product, not a depiction *(new this round)*

**Brands (4):** Spline, Vapi, Bodyswaps, (Captions / OpusClip, unmeasured).

- **Spline** replaces the hero video with a live, two-finger-orbitable WebGL scene rendered by the exact engine it sells. "This is not a video of our product, this is our product."
- **Vapi** puts a **live "Initiate Call" widget** over its stock loop — press it and it places a real phone call to a working Vapi voice agent. The video is mood; the widget is the proof.
- **Bodyswaps** stages the interaction (above).
- [prior round] **Captions** and **OpusClip** have no hero video at all — their hero *is* the product's first input surface (a file-upload box, a "paste a video link" field). The hero doesn't demonstrate the product; it starts it.

Spline's own teardown supplies the honest caveat for us: this pattern works when your core capability has a "watch me do it in your browser" primitive. A 3D renderer does. A voice-coaching app's primitive would be *listening to you* — which means a microphone permission prompt above the fold. That is a real product decision, not a creative one.

### Which type fits an invisible product?

A voice has no visual form, no surface, no packaging. Ranked by fit, with the measured reason:

| Type | Fit | Reason |
|---|---|---|
| **2 — Measured progress / scoreboard** | **Best** | The only type in 39 files that gives an invisible attribute a body. A filler-word count, a pace meter, a clarity score, a rewritten sentence — these *are* the voice, rendered visible. Fully no-shoot: it's UI. |
| **1 — Mechanism proof** | **Best, as the container for Type 2** | The score means nothing without the input that produced it. Oratori's transcript → score → rewrite is the complete argument. Fully no-shoot: it's a screen recording. |
| **6 — Category reframe** | **Strong, if paired** | Vocal Image is not "a speaking app," it is "a mirror for how you actually sound." Wispr Flow's transcript-on-a-path proves this can be done in pure SVG. Alone it lacks product proof. |
| **4b — Abstract/procedural mood** | **Viable as a second arm** | Cartesia does a full-bleed hero for 209 KB with zero footage. If the "Um loop" slips, this is the same-week fallback. But it teaches nothing — pair it with copy that does the work (Vapi/Superhuman architecture). |
| **7 — Product-as-hero** | **Interesting, blocked on product** | Requires either a mic permission above the fold or an in-hero mini-interaction. The quiz below already occupies the "interactive" slot on our page. Revisit if the quiz moves. |
| 5 — Capability flex | Weak here | Above a quiz, density is the enemy. Measured failure mode in Final Round, ELSA and Retool. |
| 3 — Proof by demeanour | **Closed** | Needs a camera (5 of 7 measured NO) or a synthetic face (measured watermark and hairline failures) — and our product's subject *is* mouth and voice precision, exactly where AI faces are worst (BoldVoice's own flagged residual risk). |
| 4a — Object-anchored mood | **Closed** | Requires a photogenic object. We do not have one, and the one attempt to fake it in our category (Langotalk) has zero product proof. |

**Synthesis: Type 1 as the vessel, Type 2 as the payload, Type 6 as the tone.** Show one real cycle of the real app catching one real speech defect and fixing it, and let that reframe what kind of product this is.

---

## 5. No-shoot playbook

### 5.1 Which references are reproducible with zero filming, and exactly how

| Reference | Verdict | Exactly what it takes |
|---|---|---|
| Oratori | YES | Screen-record one real run of the real app, speed it up (their status-bar clock jumps 3:04 → 3:44 across 30 s), ship it. No editing beyond the speed ramp. |
| Loora | YES | One continuous virtual-camera pass down five real app screens (chat → feedback modal → score ring → celebration → stats dashboard), joined by slide-up card reveals so scene detection reads 0 cuts. |
| Pitch | YES | Cold-open screen recording of a live edit, with a second collaborator cursor drifting through frame. |
| Speechify | YES | Screen-record the product performing; its own TTS output becomes the audio track. No VO session. |
| Arc/Dia | YES | Three motion-graphic beats: typed-text reveal → source chips fading in → streamed paragraph with the first line bolded. Buildable in Remotion/HyperFrames or captured live. |
| Final Round | YES | Screen recording of real product chrome + two swappable persona tiles (stock or Higgsfield/Kling loops). |
| Framer | YES | One slow virtual camera trucking across a large composited canvas of several real app screens, with ~5 hard cuts between chapters. |
| Retool | YES | Flat UI screenshots composited as 2D layers with drop shadows, floated and rotated in simulated 3D via camera parallax. After Effects / C4D, or HTML/CSS 3D transforms (HyperFrames-native). |
| Lovable | YES | Real in-app screen capture or CSS-style skeleton loaders resolving to colour, a synthetic cursor, gradient blob morph, cross-fade joins. Arguably the easiest clone in the set. |
| ELSA | YES | 100% After Effects/Lottie-class: mascot orb, typography cards, recreated UI. Zero generation needed. |
| TalkPal | YES | Lottie JSON (69 KB) + four 224×224 character PNGs. ~180 KB total, resolution-independent, perfect infinite loop, zero video bytes. |
| Blinkist | YES | Static hero PNG + three 150 px icon loops. 15 KB total. |
| **Cartesia** | YES | A shader (WebGL/Shadertoy), After Effects (gradient + threshold/dither + animated noise), or a p5.js script. 209 KB output. No AI generation required at all. |
| **Clay** | YES | Fully CG (C4D/Blender with a stop-motion-look shader + grain pass). Already zero-filming in the original. Not a generative-video job — a 3D job. |
| **Resend** | YES | 3D render (Blender/C4D/Spline). Zero frames depict anything real. |
| **Superhuman** | YES | One Pexels/Artgrid download, or one Kling/Veo prompt: "static low-angle dusk sky, pink and violet clouds drifting, silhouetted tall grass, golden hour, seamless loop." |
| **Vapi** | YES | Two licensed stock clips ("person on phone call in office," "woman speaking into phone by window") or two i2v generations — no dialogue to lip-sync, no audio to sell. Then stack two `<video>` tags and cross-fade with CSS. |
| **Rive** | YES | Photoreal CGI or AI-generated device mockups with the real app UI composited into the screen, arranged as a horizontally-scrolling row of 2.5–3.5 s cards. **Fix the loop seam** (§3.9). |
| Whoop | YES *with a caveat* | Locked 3D asset in Blender/C4D, **not** generative video. The teardown is explicit that Kling/Veo-class i2v cannot hit exact product geometry, logo fidelity, or choreographed multi-object motion. Still zero filming. |
| Quantified.ai | YES | Two HeyGen/Higgsfield reference-image avatar renders, one hard cut. **Crop the watermark.** |
| Bodyswaps | YES | Avatar clip (HeyGen-class) + ElevenLabs line + hand-built HTML/CSS/JS chrome around it. |
| Langotalk | YES | Rigged 3D avatar or i2v idle loop, layered as one of several state videos (hello / idle / apploop). |
| Speak | YES | One licensed or generated still photo as the plate + an animated UI card cycling 4–6 variations over it. Nothing moves except the UI. |
| FluentU | YES | Licensed/stock B-roll for the borrowed-attention front third + real app screen recordings for the back two thirds + type cards. (The specific licensing — Marvel, Friends, TED — is a liability we cannot replicate.) |
| Hume AI | YES | Every segment is stock-licensable, screen-capturable, or motion graphics. Zero frames require a bespoke shoot — but it is 144 s of sound-on explainer, i.e. the wrong format entirely. |
| BoldVoice | **PARTIAL** | The mouth-anatomy diagram overlay is trivially remakeable motion graphics. The base plate — one continuous, well-lit, seamless-background shot of a person mid-sentence with a believable un-posed smile — is the hostage. Flagged residual risk: getting the mouth shape convincingly correct for the phoneme being taught is exactly where AI lip articulation looks approximate, **and this video's subject *is* mouth precision**. |
| Exec | **PARTIAL** | ~90% is plain screen recording; the AI-avatar inset is already synthetic; only `participant.mp4` (natural office bokeh, unforced gesture, webcam lighting) reads as genuinely filmed — routinely substitutable with licensed stock or an avatar. |
| LanguaTalk | **PARTIAL** | 6.7 s of screen-share is trivially no-shoot; the 22.6 s continuous two-person webcam call is not — simultaneous lip-synced, emotionally-reactive two-way dialogue for 22 s uncut is past current tooling. |
| Warp | **PARTIAL** | The Hacker News quote card, the "The Contribution Flow" title card and the GitHub status chips are pure motion graphics. The ~4 shots of the real, named CEO in a real coffee shop are the point and cannot be synthesised without destroying it. |
| Lingopie, Cambly-03, Ovation, Vocal Image | **PARTIAL** | Each is a no-shoot skeleton with filmed talent hung on it. |
| Cambly-02, Yousician, Oura, Praktika, Jumpspeak, Granola | **NO** | See §3.8. |

### 5.2 The techniques, ranked by value to us

Ranking criteria: (a) does it carry an argument sound-off, (b) does it work at mobile hero size, (c) cost to build and re-cut, (d) how badly it fails when done badly.

---

#### #1 — Real-app screen recording, one continuous pass

**Evidence:** 7 pure instances measured, **7/7 YES on no-shoot, 6/7 single-shot.** Oratori, Loora, Pitch, Speechify, Final Round, Arc/Dia, Framer. Extend to near-pure and it covers Lovable and Retool too.
**Cost:** hours, not days. One person, one device, one scripted run. Re-cuts are free — you re-record.
**Needs:** a scripted run that reaches a moment worth showing within ~1 s, and a device capture at a resolution you can crop to 1080×1920 without upscaling. Oratori's 886×1920 is a downsized iOS capture and its numbers went soft — **record native, downscale once**.
**Done badly:** raw chrome nobody can parse. Pitch's own teardown is blunt: "a silent raw-UI screen recording risks reading as meaningless chrome unless it establishes within 1–2 seconds what problem is being solved." Final Round's 960×540 multi-column form is "illegible and cramped at 9:16." The failure mode is not ugliness — it is *unreadability*.

---

#### #2 — Kinetic typography / transcript-as-object

**Evidence:** 8 measured heroes carry their argument by burned-in typography (ELSA, Bodyswaps, Ovation, Speak, Lingopie, FluentU, Arc/Dia, Warp). Plus Wispr Flow's SVG `textPath` marquee [prior round] — unmeasured as a video because it isn't one.
**Cost:** the lowest of any technique that carries an argument. No generation, no capture, no licensing. Remotion/HyperFrames or raw SVG/CSS.
**Needs:** one sentence worth reading. The two most portable devices measured:
- **Ovation's "AI Prompt" chip** — a small coloured badge plus a bold black-on-white line popping in exactly when a condition is stated. Turns an abstract claim into a concrete, sound-off-legible beat.
- **FluentU's two-word hinge caption ("Look up.")** — marks the pivot from borrowed attention to product proof. And **Warp's** entire message survives as animated caption cards plus GitHub-style status chips after the audio was deliberately stripped.
**Done badly:** title cards that assert instead of demonstrate. ELSA's closing 3 s brand card spends the payoff moment on brand-name reinforcement. Type over nothing is a slide, not a hero.

---

#### #3 — Code-rendered hero: canvas / SVG / Lottie / DOM

**Evidence:** 14 sites [prior round], including Stripe (hand-written WebGL fragment shader — 67× `uniform`, 3× `gl_FragColor` in chunk `c62.js`), Raycast (`<canvas data-engine="three.js r167">` immediately after the H1), Attio (pixel-accurate fake app window in HTML/CSS, pinned sticky, scaled by scroll), Mintlify (6 canvases), Duolingo (inline animated SVG), and — critically — **Rime, Hume AI and Wispr Flow, three direct voice-AI competitors.** This round adds **Spline** (live orbitable WebGL scene as the entire hero). Measured file weights for the Lottie end: TalkPal 180 KB total, Blinkist 15 KB.
**Cost:** front-end engineering time instead of production time. Requires CTO buy-in, not creative budget.
**Needs:** a motif that survives being drawn rather than filmed. For a voice product the candidates are literally what the product outputs: a live waveform, a scrolling transcript on a path, a filler-word counter.
**Uniquely gives us:** resolution independence (no crop decision, ever), a perfect seamless loop with no restart artifact, zero video bytes, and instant iteration — change a constant, redeploy.
**Done badly:** decorative garnish mistaken for a hero. TalkPal's own weakness: "reads as a supporting UI embellishment, not a hero visual… implies 'the app is alive' far more than it demonstrates any actual feature." Blinkist's sparkles orbit a static PNG. **If the code doesn't carry the argument, it's a spinner.**

---

#### #4 — Data-visualisation as the hero

**Evidence:** the Type-2 cluster — Loora's phoneme breakdown and radar chart, Oratori's 5-pillar scores and 3.9 → +21 climb, ELSA's animated pentagon (five named skills, five numbers), Exec's 96% call score, Hume's emotion-cluster particle visualisation.
**Cost:** design time. Can be delivered either as a real screen recording (#1) or as a rebuild (#2).
**Needs:** real numbers from the real product. **Every measured instance uses plausible in-product values, not lorem ipsum.** This is the technique that turns a voice into an object.
**Done badly:** too many numbers, too small. Loora's phoneme table is flagged as near-illegible at hero size; Oratori's five score cards plus a transcript block plus a feedback card ask "more sustained attention than the single-glance UI loops in this category." **One number, big, beats five numbers, small.**

---

#### #5 — DOM-layer compositing *(new this round; highest cost-to-value ratio in the set)*

**Evidence:** Vapi (two stacked `<video>` tags cross-faded by CSS opacity — a two-clip hero with zero encoded cuts), Exec (`ai-vid.mp4` and `participant.mp4` absolutely-positioned over one long screen-recording pass at fixed coordinates), Bodyswaps (one `<video>` inside a three-beat hand-coded HTML/CSS/JS sequence; only one video tag exists across all three beats), Superhuman and Vapi again (the entire message is HTML text over the video, never baked in).
**Cost:** near-zero incremental. Each layer is independently swappable without re-rendering anything.
**Needs:** discipline about which layer owns which job. Superhuman's DOM class name says it out loud: `hero-background-video_videoContainer`. The video is a *background*.
**Why it matters for us specifically:** we will iterate this hero. Baking the headline, the score, and the transcript into one MP4 means every copy change is a re-render. Baking only the *motion* into the MP4 and rendering the *words* in HTML means copy changes are a deploy, and A/B tests are free.
**Done badly:** Vapi's own weakness — "swap the headline out and it becomes an ad for payroll software." If the video layer is fully generic, the page carries 100% of the burden, and a screenshot of the hero conveys nothing.

---

#### #6 — Static plate + animated UI overlay

**Evidence:** Speak (one café photograph, never moving, with a translation card cycling six languages over it), Blinkist (static PNG + icon loops), Liveblocks (two 1120×630 JPGs cross-faded) [prior round], Speechify (a fully static hero carried by trust badges), Yoodli and Descript [prior round].
**Cost:** near-zero. One licensed or generated still + motion graphics.
**Needs:** a photograph that establishes stakes without needing to move. For us: a job interview, a stand-up, a sales call, a first date.
**Done badly:** Speak's file is **15.18 MB for 32.1 s at 660×780** — 0.473 MB/s for content that is ~95% static. If the plate doesn't move, the encoder should know it.

---

#### #7 — 3D / abstract object render

**Evidence:** Whoop (wide → macro → reveal in 9.69 s, zero text, zero people), Clay (CG clay diorama, 4–5 independent small mechanisms looping inside one locked-off shot), Resend (tumbling faceted cube, 654 KB), Cartesia (procedural dither loop, 209 KB).
**Cost:** high for photoreal product CG (a 3D pipeline, not a prompt); **very low for abstract/procedural** — Cartesia's is a shader, Resend's is a primitive.
**Needs:** an object, or an invented abstract one. We don't have a physical object. We could invent one: a voice ring, a waveform solid, a dithered blob that breathes.
**The transferable structures:**
- **Whoop's 3-beat whip:** context → texture proof → reveal, in under 3 s. Works with UI screens as well as objects.
- **Clay's locked diorama:** one static composition in which 4–5 independent loops run simultaneously. Gives perpetual-motion energy with no narrative, no cuts, no UI. For us: several coaching mechanisms visibly ticking inside one frame.
**Done badly:** Whoop's own weakness applies doubly to us — "it will not communicate anything about what the product actually does to a first-time visitor; it only works as a hero if the audience already knows the brand." Resend's teardown is harsher: as a hero it "would give a visitor nothing to understand about the product before the quiz." That sentence was written about a different company and describes our exact risk.

---

#### #8 — AI-avatar talking head

**Evidence:** Quantified.ai (2 avatars, 1 cut, fully synthetic), Bodyswaps (3D game-engine avatar), Langotalk (3D idle loop), Exec (avatar inset), Final Round (two static-looking call tiles).
**Cost:** cheap per render, expensive per *acceptable* render. Already in our stack (HeyGen, Higgsfield reference-image control).
**Needs:** a reason for a face to exist. Quantified has one — their moat *is* believable synthetic humans. We do not have that excuse.
**Done badly, with measured evidence:** Quantified.ai shipped with an **uncropped generator watermark** (four-point sparkle, bottom-right, male segment only) and a subtly-too-smooth hairline in every frame; its single cut is "hard, unmotivated… reads as two stitched clips" (different lighting, framing and room). Langotalk's has "real uncanny-valley risk." And BoldVoice's teardown names the exact trap for us: **a product about mouth mechanics cannot afford approximate mouth mechanics.**
**Recommendation: do not put a synthetic face in the hero.** Use avatars in paid social, where the format tolerates it and the audience is scrolling.

---

#### #9 — Generated environments / AI-video B-roll

**Evidence — now positive but thin, and the change matters.** In the 28-file edition this technique had *no* supporting reference. The craft tier supplies two: **Vapi** (two single-shot stock clips of people on phone calls) and **Superhuman** (a golden-hour sky loop) are both explicitly assessed as reproducible via i2v generation *or* a stock download, precisely because they have no dialogue, no lip-sync, no audio and no product in frame.
**Cost:** a Pexels/Pixabay search is $0 and takes minutes. A Kling/Veo generation costs credits and iterations.
**Needs:** the shot must be generic enough that identity, hands and lip-sync never matter. Vapi's clips pass because nobody speaks a line; Superhuman's passes because nobody is in it.
**Verdict:** **if a shot can be licensed from Pexels for $0, generating it is the worse trade** — same generic value, more artifact risk, more iteration cost. Generation earns its place only where stock cannot deliver a specific composition (a specific device, a specific brand-coloured environment). Use stock first.
**Done badly:** Vapi's own weakness — "generic, overused corporate-stock iconography… instantly recognisable as licensed stock rather than anything shot for Vapi," and "the link to voice AI is purely associative." Also: Vocal Image's own asset already does this (chess, boardroom, graduation confetti, beach run) and its teardown says those segments are "trivially replaceable with licensed stock." We have already proven we can produce a forgettable version of this.

---

#### #10 — Transparent-alpha WebM

**Evidence: thin, and one measurement actively complicates it.** The only alpha-channel hero in any round is **Descript** [prior round, 25.5 s, one shot — not re-measured]. In this round, Blinkist's three layered loops were checked for alpha and **neither the VP9 `.webm` nor the HEVC `.mov` twin has an alpha channel**, despite being composited over other content.
**Measured cost of the Safari path:** Blinkist's HEVC `.mov` twins run **3–10× larger** than the VP9 `.webm` for identical content (`stars.mov` 622 KB vs `stars.webm` 87 KB). You ship two encodes and the Safari one is the fat one. Vapi's HEVC/VP9 pairing shows the same shape: 1.97 MB HEVC vs 0.65 MB VP9 for hero-a.
**Verdict:** technically appealing (composite motion directly onto the page background, no letterbox, no crop) but **the category evidence is one asset deep across 39+ files.** If we want a hero element that floats on the page background with no box, the code-rendered route (#3) delivers the same result with no dual-encode, no alpha support matrix, and zero bytes. **Prefer #3. Do not spend a sprint on alpha WebM on the strength of one reference.**

---

### 5.3 Delivery checklist, derived only from measured behaviour

| Do | Because |
|---|---|
| Self-host `<video autoplay muted loop playsinline>` with a `poster` | Yousician's hero pattern; the poster JPG is the real first impression and the real LCP element |
| Ship a `fetchPriority="high" loading="eager"` `<picture>` **before** the video, and wrap the video in a `motion-reduce:hidden` container | Oura — the only correct accessibility + LCP pattern found in any round |
| **Always set `loop`** | Arc/Dia freezes on a wall of small body copy after 6.7 s |
| **Test the loop seam explicitly** | Rive's card hard-jumps back to frame 1 every 3.37 s — a visible pop. Quantified engineers the opposite: frame 1 is already mid-sentence so the restart never reads as a cold open |
| Ship AV1 or VP9 with an H.264 fallback | Loora's AV1 is 88% smaller than its own H.264 twin at identical content. Note two counter-examples: Quantified's VP8 twin is **larger** than its H.264 (2.83 vs 0.64 MB), and Vapi ships **no** H.264 at all |
| Ship **no audio stream at all** | 11 of 39 carry a dead −91 dB track; pure container overhead. Audit both files if you ship a pair — Rive's two sibling clips disagree with each other |
| Encode at the delivered size | Bodyswaps discards ~93% of its 4K pixels inside a 540×410 CSS box |
| Keep the words in the DOM, not in the pixels | Vapi and Superhuman — copy changes become deploys, not re-renders; A/B tests become free |
| Design frame 1 to be mid-action | 10 measured heroes open already mid-state (Oratori, Loora, Pitch, Speechify, Quantified, Cambly, Praktika, Arc/Dia, Final Round, Vapi) |
| If you build an interactive hero, ship a canned loop as the *mobile* path | Resend's `md:hidden` MP4 substitutes for the desktop WebGL cube — degrade to a video, not to a degraded interactive |
| Consider an art-directed aspect swap rather than a CSS crop | Sonos carries `width`/`height` as aspect ratio: 16/9 desktop, 4/5 mobile [prior round] |
| Avoid | YouTube iframe heroes (RiseGuide [prior round] — needs the autoplay+mute+loop+playlist hack and ships no poster) and HLS ladders (ElevenLabs [prior round]) for a sub-20 s loop |

---

## 6. How to be the best in this category

### 6.1 The gap, stated precisely

No measured reference in 39 files does all four of these at once:

1. **Shows the actual product** — 22 of 39 do (7 pure UI + 9 MG/UI rebuild + 6 mixed with real UI inserts).
2. **Shows a specific, named defect being caught and fixed** — **2** do well: Oratori and Loora.
3. **Is legible in one glance at mobile hero size** — the two that do #2 both fail this. Oratori's numbers are soft in an 886×1920 downsized capture; Loora's phoneme table is flagged near-illegible at hero size.
4. **Costs nothing to iterate** — the screen-recording and DOM-layered ones do; the mixed-footage ones don't.

Wispr Flow achieves #3 and #4 brilliantly and shows no product at all. Cartesia achieves #3 and #4 for 209 KB and argues nothing. Oratori achieves #1 and #2 and loses them to a soft crop.

**The unoccupied position is a piece that does all four.**

### 6.2 The counter-argument, taken seriously and rejected

Vapi's architecture is structurally identical to ours: an ambient loop above an interactive element, with the video carrying no proof. If Vapi can ship stock footage and let the widget prove the product, why can't we ship a cheap mood loop and let the quiz prove it?

**Because our interactive element is not the product.** Vapi's widget places a real call to a real voice agent — pressing it *is* using Vapi. Our quiz is a segmentation and lead-capture funnel; completing it demonstrates nothing about whether Vocal Image can hear a filler word. The proof burden does not transfer. It stays with the hero.

Second-order check: does the hero need to prove anything at all if its only job is "earn the scroll"? Superhuman, Clay and Cartesia say no. But all three are brands whose visitors arrive already knowing what the product is — Whoop's teardown states the dependency explicitly. Vocal Image's homepage traffic is largely cold, quiz-first, paid. A hero that argues nothing hands a cold visitor no reason to start a five-minute quiz.

### 6.3 The recommendation

**Build one 15-second, silent, single-shot vertical loop whose entire content is a real Vocal Image session catching and fixing one real speech defect. Call it the "Um" loop.**

Three beats, no cuts, one continuous virtual camera move across a composited canvas of real app screen recordings (Framer's technique) with the transcript rendered as kinetic type over it (Wispr Flow's technique) and the headline living in the DOM, not in the pixels (Vapi/Superhuman's technique):

| Beat | ~Duration | Content | Borrowed from |
|---|---|---|---|
| 1 | 0–5 s | A live transcript types itself in real Vocal Image chrome. Filler words are flagged **inline as they land** — `um`, `like`, `you know` catching a coloured chip the instant they appear. Frame 1 is already mid-sentence. | Oratori's real transcript; Ovation's AI-Prompt chip; Quantified's mid-sentence frame 1 |
| 2 | 5–10 s | Camera pushes to **one** number. Not five. It climbs. | Loora's score ring and Oratori's 3.9 → +21, with their measured density mistake corrected |
| 3 | 10–15 s | The same sentence, rewritten and tight, replaces the messy one **in place** — a skeleton-to-resolved reveal. Loop restarts mid-sentence so the seam is invisible. | Oratori's "Fix This / Try This"; Lovable's skeleton-to-colour reveal; Quantified's seamless-restart discipline |

Hard specs, each justified by a measurement:

| Spec | Value | Justification |
|---|---|---|
| Duration | **15 s** | Single-shot tier-H median is **15.57 s** (n=14). BoldVoice's 6.57 s is flagged as too repetitive; ELSA's 49.7 s is flagged as too long above a fold |
| Shots | **1** | 6 of 7 pure UI-screen-recording files are single-shot; pure compositions are single-shot 75% of the time; there is nothing to cut to |
| Aspect | **1080×1920, true 9:16** | Not one of 39 measured vertical assets actually hits 0.5625. Being the only one that does is free |
| Audio | **no stream at all** | 85% carry nothing audible; 11 of 39 ship a dead track as pure overhead |
| Faces | **zero** | 49% of measured files contain no moving human; every synthetic-face attempt in the set has a named, measured defect |
| Weight | **<500 KB** — AV1 primary, VP9 + H.264 fallbacks | Loora does 32 s at 412×720 in **553 KB** of AV1. At 15 s we should beat it |
| Words | **in the DOM, not baked in** | Vapi and Superhuman — makes copy iteration a deploy and A/B tests free |
| Text size | every number and word legible at **375 px wide** | The measured failure mode of this exact argument-type in Loora, Oratori, Retool and Final Round |
| Delivery | poster `<picture>` first, `motion-reduce` wrapper, `loop` set, loop seam QA'd | Oura + Yousician + Arc/Dia's mistake + Rive's mistake |

**Why this beats the table.** It is the only piece that would show a viewer *their own problem* — the filler words they know they have — being caught and fixed, in fifteen seconds, without a face, a voice, or a camera. Cambly's warmth needs six actors. Oura's elegance needs an object. Granola's authenticity needs a real person who is really real. Quantified's polish needs a face that survives inspection. Oratori has the right argument and lost it to a soft 886×1920 crop. We have the argument, the app, and no legacy asset worth protecting.

### 6.4 The unclaimed position: be the only hero in this category you can hear

33 of 39 files carry nothing audible. Not one of the 39 offers the visitor a way to *choose* sound.

Ship the loop silent — then put a single small speaker toggle in the corner. Pressing it plays **3 seconds of a real before/after**: the same sentence, hedged and mumbled, then delivered. No narration, no music, no VO session. Just the product's subject matter, audible on demand.

Measured support:
- The only two short-form heroes in 39 that keep sound are **Speechify** and **Bodyswaps** — and in both, **the sound is the demonstration**, not the score. Ours would be too.
- Autoplay audio is correctly universal-off; this is opt-in, so it violates nothing.
- Cost: an `<audio>` element, a button, and one clean voice pair. Hours.

For a company whose product is how people sound, being the only homepage in the category where you can press a button and hear the difference is a stronger differentiator than any frame we can render.

### 6.5 The parallel bet: a code-rendered hero

Run a second track, cheap, in parallel: **a canvas/SVG hero, no video file.**

The evidence is now four voice-AI brands deep — **Rime, Hume AI, Wispr Flow** [prior round] and **Spline** — plus Stripe, Raycast, Attio, Mintlify and Duolingo. Wispr Flow's `textPath` marquee is the closest existing execution to the "Um" loop's beat 1: a real, messy, human transcript crawling along two SVG curves, costing zero media bytes, resolution-independent, seamless, changeable by editing a string.

Two candidate builds:
- **Transcript-on-a-path** (Wispr Flow's mechanic, our content): disfluencies scroll past on a curve and get struck out and replaced in place.
- **Live waveform that resolves**: a jagged, hesitant waveform smooths into a confident one across the loop — the Type-6 category reframe, drawn rather than filmed.

Ship it as the `motion-reduce` / low-bandwidth path at minimum. Follow Resend's inverse pattern if it wins: interactive on desktop, a canned sub-500 KB loop on mobile. If it tests better than the video, it becomes the hero and we stop paying for encoding forever.

### 6.6 Three things to stop doing

1. **Do not resurrect `website_cover.mp4`.** Highest cut rate of all 39 measured files (0.695/s), wrong aspect, broken first frame, and its one product shot is the one we cannot produce.
2. **Do not commission narration or a music bed for the hero.** 85% of the set ships nothing audible; the only two short heroes with sound use the sound *as the product* — which is what §6.4 proposes instead.
3. **Do not put an AI avatar in the hero.** Every measured synthetic-face hero has a named defect, and ours would be a product about vocal precision fronted by approximate lip articulation.

### 6.7 What to measure

The hero's job is scroll-through into the quiz. Instrument exactly that: **quiz-start rate among visitors who reach the fold**, split four ways:

| Arm | What it tests | Precedent in the data |
|---|---|---|
| A — the "Um" loop | Mechanism proof + scoreboard | Oratori, Loora |
| B — code-rendered transcript/waveform | Category reframe, zero media | Wispr Flow, Rime, Hume, Spline |
| C — static poster frame, no motion at all | Does motion earn its cost? | **75 of 117 competitors bet on this** [prior round]; Speechify, Warp, Hume and Blinkist all chose it deliberately |
| D — arm A plus the opt-in audio toggle | Does hearing the product beat seeing it? | Unoccupied — 0 of 39 |

Arm C is not a strawman. It is the modal choice of this category and it deserves to be in the test, not assumed away.

---

## 7. Coverage and limits

### 7.1 What was verified

- **39 media files** measured at file level: `ffprobe` for duration/resolution/codec/stream inventory, `ffmpeg volumedetect` for audio content (the −91 dBFS readings), `ffmpeg` scene detection (project-standard threshold 0.3, with 0.05/0.15/0.2/0.4 cross-checks on several assets) for cuts, and frame extraction for composition analysis. Every duration, resolution, byte count, codec, frame rate and audio measurement in this document comes from those runs.
- Several delivery claims come from **served HTML/markup inspection**, not from the media files: Speechify's byte offsets (hero section 62365–96421; first `<video>` at 107932), Vapi's `<source type="video/quicktime; codecs=hvc1">` and `duration-cross` opacity classes, Superhuman's `hero-background-video_videoContainer` / `page_heroBackgroundVideo` DOM classes, Resend's `md:hidden` wrapper, Oura's `motion-reduce:hidden` + `fetchPriority="high"` `<picture>`, Arc/Dia's missing `loop` attribute, ELSA's `object-contain`, Bodyswaps' `haB2`/`haB3`/`haB4` beat sequence, TalkPal's Lottie JSON layer inspection (all 64 layers `ip=0`/`op=331`), Spline's `.splinecode` URL, Warp's `backgroundMode:true`, Hume's zero `<video>` tags.
- **75 homepages** verified to carry no hero motion asset [prior round], each with reproducible `curl` + `grep` evidence and, in most cases, a byte-offset comparison between the `<h1>` and the first media element.
- Several absences were re-verified in a real browser after `curl` returned a JS shell or a 403 [prior round]: Calm, BetterUp, Duolingo, Headspace, Stripe, Raycast, Mintlify, Attio, Linear, Vercel, Cursor, Cal.com, Liveblocks, Notion Calendar.
- Several apparent media hits were checked and **rejected as false positives** [prior round]: `/site.webmanifest` clipped to `.webm` (Teenage Engineering, RankedSpeak, Vercel, Cursor, Sesame, Granola, Kling) and Mondly's `https://stream.mux.com/${t}.m3u8`, an unresolved JS template literal with no playback id. Hume AI produced the same `manifest.webmanifest` false positive in this round and was correctly rejected.

### 7.2 Inconsistencies inside the source data — and how they were resolved

The measuring agents reported **zero disputed findings**. The following are inconsistencies I found and reconciled while aggregating; they are not agent disputes, and each resolution is stated so it can be overturned.

| Inconsistency | Resolution |
|---|---|
| **`cutCount` semantics differ across agents.** Some report scene-detector output (unbroken take = `0`), others report shot count (unbroken take = `1`). Proof: Oura is `cutCount: 1` while its prose says "zero cuts to hide any seam"; Praktika is `cutCount: 1` and described as a single continuous take; Cambly's `cutCount: 7` is explicitly "7 shots, avg ~2.9 s each"; Vapi is `cutCount: 1` with an explicit note that detection found **zero** scene changes. | Normalised to **shots = max(cutCount, 1)**, each value cross-checked against its entry's prose. **This is the single largest methodological caveat in the document.** |
| **Loora measured twice**, returning `cutCount: 0` and `cutCount: 1` for the same asset. | Both mean one unbroken shot. The second notes "the only motion blip at 20.5 s is a card sliding up to reveal the next screen, not an edit." Recorded as 1 shot / 0 cuts. |
| **ELSA appears twice** with near-identical measurements from two agents (one calls sound-off legibility "by-UI/typography," the other "by-typography"; one reports 0 hard cuts with one soft dissolve at ~32.6 s at threshold 0.15). | Deduplicated; counted once as 1 shot. |
| **Vapi appears twice**, once with `hasAudioTrack: false` and once with the same value plus fuller codec detail. | Deduplicated; the fuller entry used. |
| **Speechify appears twice** — once as a measured media file, once as a "hero has NO video" finding. | Both are true and consistent: the file exists **below** the hero. Tiered **N**; retained in the file statistics, excluded from tier-H statistics. |
| **Retool's cut count is internally contradicted by its own agent**: raw detector 16, with 8 of those firing within a 1-second window flagged as one glitch transition. | Recorded as ~10 shots / ~9 cuts, raw 16 preserved in the table footnote. Retool is multi-shot under either reading, so no aggregate changes. |
| **Loora's human presence**: one measurement notes "a static profile-photo thumbnail inside the UI," another says "no human face anywhere." | Classified as *no moving human, static UI asset present*. |
| **Rive's two sibling files disagree on audio**: `data_driven2.mp4` has no audio stream; `product_ui2.mp4` has a real AAC track muted client-side. | Both reported. Row 36 measures `data_driven2`. |

### 7.3 Unmeasured, unreported, or inferred

- **Superlist — measured as far as possible, then blocked.** Its hero `<video>` ships with an **empty `src`**; the real mp4/webm URL appears nowhere in the static HTML and nowhere in the site's main JS bundle (`script_main.mjs` was fetched and searched). There is no `og:video` either. Only the 2000×1616 poster PNG is provable. Duration, cut count, codec and true resolution are **unmeasurable** without a headless browser with scroll-triggered network capture. Its content is described from the poster + surrounding copy only. **Excluded from every statistic.**
- **Praktika's `soundOffLegible` was never reported.** Its classification is **[inferred]** from two confirmed facts: no audio stream, and no on-screen text in any sampled frame.
- **Lovable's placement is [inferred]** from its asset path (`/videos/homepage/scene-1..3.webm`). Above-the-fold position was not confirmed by DOM offset. If it is not a hero, tier-H counts drop by one and the tier-H single-shot rate rises slightly (14/24 = 58%).
- **Retool's placement is unconfirmed** (tier U). The filename is literally `M4+Teaser+Sample+Loop.mp4` and its own agent calls it "an internal product-team teaser rather than a polished homepage hero." It is included in the 39-file statistics and excluded from tier-H.
- **Wispr Flow, Rime, Stripe, Raycast, Attio, Mintlify, Spline** — hero mechanisms documented from markup and JS-chunk evidence only. **Nothing about them was measured with ffprobe, because there is no media file to probe.** Any claim about their visual quality is observational, not measured. §6.5 proposes copying Wispr Flow's mechanic on the strength of markup evidence alone.
- **Blinkist's live page could not be fetched** (Cloudflare bot challenge). The hero structure was reconstructed from a Wayback Machine snapshot; the measuring agent reported this as BLOCKED rather than guessing. The three `.webm` files themselves were measured directly.
- **Phase 1 assets were not re-measured:** RiseGuide, Yoodli, Descript, ElevenLabs, Poised, and the 5.5 s Speak asset. Cited as prior evidence only; excluded from every aggregate in §3.
- **No brand's performance data was obtained.** Not one number in this document says a hero *worked*. Everything here is craft and construction analysis. The only performance evidence that will matter is our own test (§6.7).

### 7.4 Placement caveats — the "hero" set is not homogeneous

Of 39 measured files, 25 are placement-confirmed heroes. The other 14:

**Confirmed NOT heroes (5), excluded from tier-H statistics:**
- **Speechify** — hero section byte 62365–96421 contains zero `<video>`; first `<video>` at 107932. The homepage hero is text + trust badges + a celebrity photo strip.
- **Warp** — hero is `hero-left-aligned-with-photo`, a static screenshot. The measured file is a below-hero announcement background (Feb 2024, tied to a one-off open-source launch).
- **Hume AI** — hero is a `<canvas>`; the measured 144 s file is a below-hero YouTube embed.
- **Jumpspeak** — 228.97 s served from Wistia; YouTube-ad grammar (founder monologue, UGC testimonials, sound-on).
- **Vocal Image** — exists only as an `og:video` meta tag; never embedded.

**Hero-adjacent (8):**
- **Bodyswaps** — CSS-cropped into a 540×410 widget; one beat inside a 3-beat DOM sequence.
- **Blinkist** — three ~150 px decorative loops around a *static* PNG hero.
- **TalkPal** — a ~300–424 px square widget beside the headline; its own teardown says it "can't do the stop-the-scroll job a full-bleed hero video does."
- **Speak** — the filename says "Card Section," and the agent explicitly flagged that its comparability as a homepage hero is uncertain.
- **Pitch** — flagged as "likely embedded as a small inline product-screenshot demo."
- **Rive** — one card in a horizontally-scrolling ticker of ~8, placed under the H1.
- **Granola** — one of a set of small looping tiles surrounding the hero headline (path: `homepageAssets/call-videos/`, plural, multiple named individuals).
- **Resend** — 225×225 CSS px, absolutely positioned as a corner decoration, and **mobile-only** (`md:hidden`).

**Placement unconfirmed (1):** Retool.

Also flagged among tier H: **ELSA** is a boxed `object-contain` 720×720 square, not full-bleed. **Arc/Dia** is a crop of just the Dia sidebar panel, with content occupying well under half the 3106×2160 canvas. **Clay** reserves ~50% of its 2:1 frame as empty space for overlaid text.

One possible content error was flagged and left unresolved: in **Speak**, one sampled frame (the Chinese-language card) showed an English caption reading as a different phrase than the visible target-language text — either a genuine QA slip in their asset or a frame-sampling artifact on a crossfade. **Do not cite it as a finding.**

### 7.5 Absences and blocks — and the honest state of that evidence

**The absence data in this round's payload arrived truncated.** The `absentOrBlocked` array is cut off mid-entry (the Sanako record is incomplete). The brands with complete, quotable no-hero-video evidence **in this round** are ten:

| Brand | Verdict | Evidence |
|---|---|---|
| Orai | static-image hero | HTTP 200, 25,899 B; zero `<video>`/`<source>`; zero mp4/webm/m3u8; zero wistia/vimeo/mux/lottie/rive; 7 `<img>`; server-rendered (no `__NEXT_DATA__` shell) |
| Speeko | static-image hero | HTTP 200, 271,591 B; zero video tokens of any kind; 37 `<img>` |
| Speakio | static-image hero | HTTP 200, 511,699 B (Framer); zero video, zero youtube/vimeo, zero `og:video`; 4 `<img>` |
| Huru | static-image hero (screenshot carousel) | HTTP 200, 1,053,550 B; **zero matches** for wistia\|vimeo\|mux\|videodelivery\|b-cdn\|vidyard\|loom\|m3u8\|mp4\|webm\|`<video`\|lottie\|rive across the whole 1 MB document; 161 `<img>` |
| TalkPal | no `<video>` element — Lottie only | HTTP 200, 788,750 B; `20 lottie` and nothing else; 1,086 `<img>` |
| Pronounce (getpronounce.com) | static-image hero | HTTP 200, 86,907 B; zero matches; 82 `<img>` (Webflow) |
| Tandem | static-image hero (`homepage_hero_bg2.png`) | zero `<video>` tags; the mp4 exists only inside a Contentful JSON blob at 39.8% document depth, labelled `"fallbackScreen"` |
| Preply | static-image hero | HTTP 200, 1,213,224 B; zero video bytes of any kind |
| italki | static-image hero | zero `<video>` tags; 5 mp4s and 3 YouTube embeds all at **94.1% document depth** (h1 at 331,091 of 463,513; first media at 436,030) |
| VirtualSpeech | static-image hero | one YouTube iframe (`ANkgQnJukwI`) at byte 55,482 vs h1 at 36,919, with four distinct copy sections between them — mid-page, not hero |

The wider **117 probed / 75 no-hero / 17 blocked** figures are carried forward from the prior round and are **not re-derivable from this round's payload.** They are cited as [prior round] throughout. The 17 blocked brands from that round: Ummo (HTTP 526), TalkTune (404 at root), TalkMe (2,148-byte JS shell), Vocable (2,761-byte SPA shell, and a different product), Voloco (1,396-byte shell), TalkMeUp (JS redirect to a parked stub), Rhetoric (HTTP 000, dead DNS), Height (HTTP 000), OpenAI / Perplexity / Midjourney / Ideogram (403 bot shells), LOVO (HTTP 402 from the edge), PlayAI (HTTP 000), **Sonos** and **Bang & Olufsen** (hero `<video>` present, `src` JS-injected — video confirmed to exist, file unmeasurable), and **Oura** (hero `<video>` with zero `<source>` children; the measured file was recovered via the imgix CDN path).

**The residual risk this creates matters and should not be papered over:** absence of a URL in server-rendered HTML is not absence of a hero video. Three of the most design-led brands in the sweep inject their hero `src` at runtime. Any brand in the 75-strong list whose evidence rests only on `curl` + `grep` carries that risk. The 14 re-verified in a real browser do not. **Superlist, found this round, is a live example of exactly this failure mode.**

### 7.6 What was left out, and what the sample is not

- **The craft tier is a convenience sample, not a population.** The 14 non-category files (Oura, Whoop, Blinkist, Framer, Pitch, Arc/Dia, Clay, Retool, Resend, Superhuman, Rive, Lovable, Granola, Warp) were chosen because they are well-known, well-designed sites — not by any sampling frame. Statistics that mix them with the category set describe "39 files we looked at," not "the state of web heroes." Where a finding depends on them, it says so. The two findings most exposed to this bias are §1.3 (retraction, driven entirely by Vapi and Superhuman) and §1.7 (the DOM-overlay architecture, 4 of 5 instances from the craft tier).
- **No teardown exists at this depth for Yoodli, Descript, Poised, ElevenLabs or RiseGuide** — Phase 1 assets were measured at file level only. **Descript's alpha-channel WebM is the single most consequential un-toredown asset**, because it is the only alpha reference in any round and §5.2 rates that technique on one data point.
- **No teardown of the code-rendered heroes.** Wispr Flow, Rime, Stripe, Attio, Mintlify and Spline were documented from markup only. Given that §6.5 proposes copying Wispr Flow's mechanic, **a frame-by-frame teardown of that SVG animation is the highest-value next research task.**
- **Nothing was measured on mobile viewports.** Every measurement is of the source file, not of what a phone renders. The aspect-ratio criticism in §3.3 is about the file, not the delivered crop.
- **No hero was measured over time.** Every asset is a single snapshot from 2026-08-07. We do not know which are current bets and which are old furniture — except Tandem (`_updatedAt` 2020-05-28) and Warp (Feb 2024 announcement).
- **The 75 absences were never sub-classified by recency or traffic.** "Babbel ships a static hero" and "Natulang ships a static hero" carry very different weight; this document treats them as one row each.
- **Every "done badly" example in §5.2 is a defect the measuring agents observed, not a defect we tested.** No user saw any of these heroes in a controlled setting. The claim "this fails at 375 px" is a reading of the asset, not a measurement of a viewer.

---

*Compiled 2026-08-07 from file-level measurements by parallel research agents across three rounds. Numbers marked as measured are reproducible with ffprobe/ffmpeg against the URLs in §2. Numbers marked [inferred] are not. Numbers marked [prior round] were not re-derived from this round's payload.*
