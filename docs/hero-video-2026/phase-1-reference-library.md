# Phase 1 — Hero Video Reference Library
**Vocal Image website hero video · research deliverable**

| | |
|---|---|
| Prepared for | Ivan Turapin (creative direction), Kirill Repin (motion execution) |
| Date | 2026-08-04 |
| Target ship date | 2026-09-01 (4 weeks) |
| Phase | 1 of 3 — research only. No concepts, scripts, or storyboards here. |
| Method | Every video in the "analyzed" tier was downloaded and taken apart locally (scene detection, keyframe extraction, keyframe reading, transcript where audio exists). Raw artifacts under `projects/website-hero-video/analysis/`. |

---

## 0. Read this first — four findings that change the brief

### 0.1 `website_cover.mp4` exists, but no visitor has ever seen it

The file is real: `https://static.vocalimage.net/videos/website_cover.mp4`, HTTP 200, 7.1 MB, 1080×1080, 24.4 s, with an audio track.

It appears on the homepage in exactly one place — an **`og:video` meta tag**. There are **zero `<video>` elements in the page**. It is a social-share preview asset, not a hero. Anyone landing on `vocalimage.app/en` sees the interactive quiz ("What brings you to Vocal Image?" → 5 journey options → *Continue*) and no video at all.

So the Phase 2 framing shifts: this is not "replace a weak hero video," it is **"there is no hero video, and a perfectly good 24-second asset is sitting unused in the meta tags."**

### 0.2 The dominant hero pattern in this category is a single unbroken loop — not a narrative

Scene detection across the analyzed set:

| Reference | Duration | Scenes | Avg cut |
|---|---|---|---|
| Speak | 5.5 s | **1** | — |
| Yoodli | 15.1 s | **1** | — |
| Praktika | 17.7 s | **1** | — |
| Descript | 25.5 s | **1** | — |
| Poised | 30.8 s | **1** | — |
| ElevenLabs | 13.8 s | 3 | 4.6 s |
| **Vocal Image (ours)** | 24.4 s | 3 | 8.1 s |
| RiseGuide | 88.1 s | 18 | 4.9 s |

Five of eight are **one continuous shot with no cuts at all**. The web hero in this category is an *ambient product loop*, not a story. RiseGuide is the outlier precisely because its hero is a repurposed YouTube ad.

This validates Ivan's instinct to commission **two deliverables** — but sharpens why: the homepage cut is not a shorter edit of the YouTube film. They are different species. One is an ambient loop optimized to be glanceable and re-enterable at any frame; the other is a narrative optimized to be watched once, to the end, with sound.

### 0.3 RiseGuide's hero is strong creative wrapped in a weak implementation

The creative is genuinely good and it *is* sound-off legible — the entire narration is duplicated as burned-in kinetic typography (verified by reading keyframes). But the implementation is the weakest part of the whole reference set, and it is the clearest opening we have. Details in §3.

### 0.4 Our real proof assets are stronger than the brief's "4M+ users" — and they're buried

The homepage already claims **8.4M+ accent tests taken**, 4M+ voice tests, **120+ accents detected**, **96% of users can't fool the AI accent detector**, 4.8 rating, plus Forbes / TIME / TechCrunch / Yahoo Finance / TechRadar. The accent test is the single biggest owned asset in the business and it sits below the fold. No competitor in this set has a comparable number.

---

## 1. Master reference table — analyzed tier

All figures measured locally, not taken from marketing pages.

### 1.1 RiseGuide — the direct benchmark
| | |
|---|---|
| Source | `youtube.com/watch?v=jzkoouRNhWk` (channel "RiseGuide: Expert Insights", uploaded 2026-01-09, 577K views) |
| Native | 1920×1080, 16:9, 30 fps, AV1 + AAC, 88.1 s |
| Placement | YouTube **iframe** in hero, rendered 723×448 (ratio 1.612) at `pageTop 127`, above the fold, inside a `overflow:hidden` / `border-radius:24px` wrapper |
| Embed params | `autoplay=1` `mute=1` `loop=1` `playlist=jzkoouRNhWk` `controls=0` `playsinline=1` `rel=0` `modestbranding=1` |
| Composition | Kinetic typography (dominant) + angled phone mockups with app UI + dark abstract gradient plates + light stock B-roll |
| Cut rhythm | 18 scenes / 88 s ≈ 4.9 s per cut; longest hold 10.0 s |
| Sound-off legible | **Yes** — narration fully duplicated as on-screen type |
| 9:16 survivable | Partially — typography is centred and would survive; the angled phone mockups and wide gradient plates would not |

**Beat map (timestamps from transcript + keyframes):**

| Time | Beat | On screen |
|---|---|---|
| 0:00 | **Hook** — "Stop scrolling, start growing." | Bright magenta→pink gradient type over a dark, defocused shot of hands holding a phone showing a feed |
| 0:00–0:04 | Name + category reframe: "your new smart scrolling experience" | — |
| 0:04–0:08 | **Differentiation by negation**: "This isn't just another summaries app" | — |
| 0:08–0:19 | Mechanism: daily practice, proven techniques of "the world's greatest role models" | Angled phone mockup, app lesson UI. At 0:09 the lesson on screen reads *"Have you ever been in a conversation where someone barely made eye contact with you?"* — flat-illustration characters |
| 0:19–0:32 | Value stack: "think sharper, **speak with confidence**, grow your influence" | White kinetic type on dark gradient |
| 0:32–0:45 | Friction removal: "7 minutes with your morning coffee, midday lunch, or evening wind-down" | — |
| 0:45–1:03 | Feature deep-dive: **SEEK** — "Search Engine for Expert Knowledge" | Per-word colour-reveal typography, blue/white on near-black |
| 1:03–1:12 | **Objection handling**: "No AI hallucinations, no basic info… from people who've done it before" | — |
| 1:16–1:22 | Close: "Your life gets better when you get better. Start rising one scroll at a time." | Logo resolve — near-black frame, very low luminance |

Narration: 250 words / 88 s = **2.84 words per second** (measured, unhurried).

**What works:** the hook is a behavioural command that names what the visitor is literally doing ("stop scrolling"); differentiation-by-negation lands the category distinction in four seconds; the objection-handling beat ("no AI hallucinations") is unusually mature for a hero; full sound-off legibility via burned-in type.

**What NOT to copy:** see §3 — the implementation, the 88-second length for a muted autoplay slot, and the dead final third.

### 1.2 Vocal Image — our own current asset (baseline)
| | |
|---|---|
| Source | `static.vocalimage.net/videos/website_cover.mp4` — reachable only via `og:video` |
| Native | **1080×1080 (1:1 square)**, 24.4 s, 24 fps, H.264 + AAC, 7.1 MB |
| Placement | **None.** Not embedded on any page. |
| Structure | 3 scenes: 0–3.75 s, 3.75–5.29 s, then a single **19.2-second continuous shot** to the end |
| Composition | Studio talent holding phones against a grey backdrop + one lifestyle shot; real app UI on the phone screens |

**Keyframe read:**
- **0.1 s** — a dim, defocused, empty interior: white wall, framed picture, pendant lights, a yellow lightning-bolt wall ornament. No people, no product, no text. As a poster frame this is the worst frame in the file.
- **3.9 s** — young man, curly hair, pink sweatshirt, grey studio backdrop, holding a phone showing the real Vocal Image home: "Hello, Nicki", a purple **Voice Test** card, "Start Your Day" lesson list with illustrated thumbnails. Heavy vignette.
- **10.1 s** — woman in a bathtub with candles, talking to her phone. Warm, dark, intimate lifestyle footage.
- **19.7 s** — woman, long reddish hair, beige sweatshirt, grey backdrop, holding a phone showing a **Voice Test results screen**: waveform, coloured metric bars, a "Pitch" section.

**Honest assessment.** The raw material is better than its packaging. It does the thing the playbook demands — real app screens are on camera, and the results screen with metric bars is exactly the "AI feedback" proof we need. Against that: the opening frame is an out-of-focus empty room; the grade is murky and the vignette is heavy enough to eat the corners; a 19.2-second unbroken shot in the back half has no rhythm; there is no on-screen type at all, so muted it communicates nothing verbally; and the bathtub shot reads as generic lifestyle rather than as communication coaching. Square 1:1, however, is a genuine asset — see §2.2.

### 1.3 Yoodli
| | |
|---|---|
| Source | `yoodli.ai/assets/videos/hero-video.webm` |
| Native | **2880×2880 (1:1)**, 15.1 s, 30 fps, self-hosted WebM, 2.1 MB |
| Structure | **1 scene, no cuts** |
| Composition | Pure UI motion graphics. **No people at all.** |

Very light palette (pale blue-white ground), white rounded card, bold blue heading **"Cold call roleplay"**, fields reading "Agnes Beans, VP of Software at Hooli Inc" and "A cold call to sell Yoodli to Agnes. She has a busy day so you'll have to hit your talking points quickly!", decorated with purple four-point sparkles and yellow dots.

**Notable:** the exact tonal inverse of RiseGuide — bright, airy, optimistic where RiseGuide is dark and cinematic. 2880 px square is a deliberate retina-crisp UI choice: at 2× density the interface type stays razor sharp. Positioning is explicitly **B2B sales** (cold-call roleplay), which is a useful signal that Yoodli is not competing for our B2C confidence/accent audience. Sound-off legible because the UI itself carries the words.

### 1.4 Descript
| | |
|---|---|
| Source | `static-cdn.descript.com/descript-website/videos/home-hero-transparent.webm` |
| Native | 1920×1080, 25.5 s, 30 fps, **transparent WebM (alpha channel)**, 2.4 MB |
| Structure | **1 scene, no cuts** |
| Composition | Floating product-UI panels composited over page background |

A transcript/editor panel, a video thumbnail of a real person, and an "Underlord" AI-assistant panel with a legible conversation: *"Edit this for me"* → *"I see there are some repeated takes and long pauses. I'll remove those, and I'll enhance the audio quality."* → *"OK, all set. Want me to polish up the visuals?"*

**The single most transferable technique in the whole set.** Because the WebM carries an alpha channel, the video has no frame, no letterbox, and no container edge — the UI appears to float natively on the page, and the same file works against any background colour. For a product whose hero moment is *app UI plus AI feedback*, this is directly applicable. It also demonstrates AI value through a **legible conversation** rather than a narrator's claim.

### 1.5 ElevenLabs
| | |
|---|---|
| Source | `eleven-public-cdn.elevenlabs.io/payloadcms/video-derived/6a184b41ff464f65c08e32c1/` — `h264_1080.mp4`, `h264_720.mp4`, `h264_480.mp4`, **plus `master.m3u8`** |
| Native | 1920×1080, 13.8 s, 24 fps |
| Structure | 3 scenes, avg 4.6 s |
| Composition | Real footage — three men at a table with vintage microphones and buzzer buttons on a black stage, game-show/podcast staging |

**Notable:** the only reference serving **HLS adaptive streaming plus a three-rung ladder of pre-derived MP4s** (1080/720/480). That is the most technically mature delivery setup in the set and the right answer if a hero video must be both crisp on desktop and cheap on mobile. Creatively it is the least relevant to us — it reads as a customer-showcase reel rather than a product demo.

### 1.6 Praktika
| | |
|---|---|
| Source | `praktika.ai/assets/intro-BBoGofYM.mp4` |
| Native | **358×636 (9:16 vertical)**, 17.7 s, 24 fps |
| Structure | **1 scene, no cuts** |

The only **natively vertical** hero in the set, and served at a deliberately tiny 358 px wide — a mobile-first hero that treats the phone as the primary canvas and accepts softness on desktop. Named as a competitor in our own `avatars.md` (Avatar 8, Post-Language-App Graduate), so worth tracking, but the shot design does not survive a 16:9 crop.

### 1.7 Poised
| | |
|---|---|
| Source | Webflow CDN — `…65045120732df0df83136b2b_Poised - Website video-transcode.mp4` (+ `.webm`) |
| Native | 1038×720, 30.8 s |
| Structure | **1 scene, no cuts** |
| Placement | Self-hosted `<video autoplay loop>` with the poster supplied as a CSS `background-image` on the element |

The **longest single unbroken shot** in the set at 30.8 s. Standard Webflow hero pattern: dual `.mp4` + `.webm` sources, `data-wf-ignore`, and a background-image poster. Worth noting only as evidence of how far the "one long ambient shot" convention stretches.

### 1.8 Speak
| | |
|---|---|
| Source | `speak-web.b-cdn.net/…_en-transcode.mp4`; additional localised films at `s3.usespeak.com/web-landing/` (`EN_FR_L1-3_Invitation_VL_v03.mp4`, `EN_KR_L1_fourpeople_VL.mp4`, `XX_EN_UC_L2-bs_tiredafraid_VL_1.mp4`) |
| Native | **720×720 (1:1)**, 5.5 s, 30 fps, 92 KB |
| Structure | **1 scene** |

**The shortest and lightest hero in the set — 5.5 seconds, 92 kilobytes.** Speak treats the hero as a *texture*, not a message. The filenames are the more valuable find: `EN_FR`, `EN_KR`, `XX_EN` prefixes reveal a **per-locale hero-video matrix**, which is a direct precedent for the `ESP_` / `FR_` / `DE_` language-variant convention already in our playbook.

---

## 2. Narrative-craft tier — hook and retention mechanics

Per the brief, these are mined for *why do I want to keep watching*, not for visual style. Analyzed at transcript level; each was downloaded and its opening captured verbatim.

### 2.1 Julian Treasure, "How to Speak So That People Want to Listen" (TED)
Verbatim opening: *"the human voice — it's the instrument we all play. it's the most powerful sound in the world, probably. it's the only one that can start a war or say I love you. And yet many people have the experience that when they speak, people don't listen to them. Why is that? How can we speak powerfully to make change in the world?"* → then promises *"seven deadly sins of speaking."*

**Mechanic — four moves in about twenty seconds:**
1. **Elevate the mundane into a universal** — "the instrument we all play"
2. **Establish dramatic range** — "start a war or say I love you"
3. **Name the listener's private failure** — "when they speak, people don't listen to them"
4. **Ask the question the video will answer**, then open a *countable* loop — "seven deadly sins"

This is the most directly transferable hook in the entire research set, and it is about our exact subject. "The instrument we all play" reframes voice from a fixed trait into something practised — which is precisely the practice-not-content differentiator in our playbook. The countable list ("seven") is what converts a hook into watch-through: the viewer now has a reason to stay for a known quantity of payoff.

### 2.2 Vox, "Kanye, deconstructed: The human voice as the ultimate instrument"
Verbatim opening: *"In 2002 Kanye West, known at the time mostly for his contributions to hip hop as a producer, recorded 'Through the Wire'… just a few weeks after his infamous car accident, while his jaw was completely wired shut."*

**Mechanic: concrete anomaly first, thesis second.** No claim, no promise, no framing — just one strange, specific, verifiable fact that generates the question on its own. The thesis arrives only afterwards: *"not many artists would record their debut single in that condition, but Kanye did — and that decision illustrates something very unique about his work."*

Applicable to us as the **statistic-as-anomaly** route: "96% of people can't fool our accent detector" or "8.4 million accent tests" are anomaly-shaped facts we already own.

### 2.3 Johnny Harris, "Why I Left The Mormon Church"
Verbatim opening: *"I grew up Mormon… I then left the Mormon church, and that is a whole story that I want to talk about today… my purpose in doing this is to share my perspective so that anyone who is questioning and wondering can have another perspective to lean on. I'm not looking to get into debates."*

**Mechanic: personal stake + explicit story promise + pre-emptive objection disarm.** The third move is the interesting one — naming what the video *is not* buys trust before any argument starts. RiseGuide uses the same move at 1:03 ("no AI hallucinations, no basic info"). For a category crowded with AI-slop scepticism, this is a strong tool.

---

## 3. RiseGuide production-pattern deep dive

### The exact embed, verbatim from their served HTML
```html
<iframe
  src="https://www.youtube.com/embed/jzkoouRNhWk?autoplay=1&mute=1&loop=1&playlist=jzkoouRNhWk&controls=0&playsinline=1&rel=0&modestbranding=1"
  title="RiseGuide hero video"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen>
</iframe>
```

Mechanics worth knowing:
- `loop=1` is inert on a YouTube embed **unless** `playlist=<same video id>` is also present. That pairing is the whole trick, and they use it.
- `mute=1` is mandatory — no browser will autoplay with sound.
- `controls=0` + `modestbranding=1` + `rel=0` strip the player chrome so it reads as a design element rather than an embed.
- `playsinline=1` stops iOS Safari hijacking it to fullscreen.

### Measured layout
- Rendered **723×448** at `pageTop 127`, above the fold (viewport 1267 px). Wrapper is `overflow:hidden`, `border-radius:24px`, transparent background.
- Rendered ratio is **1.612, not 1.778** — the 16:9 source does not match its container, so the wrapper is cropping or letterboxing it.
- DOM order top→down: **CTA (16) → H1 (109) → VIDEO (127)** — a side-by-side hero at desktop width, not full-bleed.
- `pointer-events: auto` — the iframe is live, so a click lands on the YouTube player.

### Four things to take, four to reject

**Take:**
1. Duplicating the narration as burned-in kinetic typography, so the piece is fully legible muted.
2. The behavioural hook that names what the visitor is doing right now.
3. Differentiation by negation inside the first five seconds.
4. An explicit objection-handling beat ("no AI hallucinations") before the close.

**Reject:**
1. **A YouTube iframe as a hero.** No poster frame, no `loading` attribute, eager-loaded third-party player. Current guidance is blunt about this: *"autoplay hero videos are the #1 cause of LCP failures on visually-rich websites"* and *"the poster is the LCP element. Always."* RiseGuide has no poster at all, so there is nothing to paint early — the hero slot stays empty until YouTube's player boots. Self-hosting a `<video>` with `poster` + `preload="none"` is strictly better and needs zero JavaScript.
2. **88 seconds in a muted autoplay slot.** The same guidance: autoplay loops are for mood; *"for explanations or storytelling, a traditional play button is usually the better choice."* RiseGuide's film is explanatory storytelling, so the format fights the content.
3. **The dead final third.** The keyframe at 81.3 s of 88 s is almost entirely black — the logo is barely discernible. Roughly the last 12 s carries near-zero information, and because it loops, that dead air replays forever. Any loop we build must earn every second.
4. **A clickable iframe.** With `controls=0` the click target is invisible but live, so a stray click can pull the visitor to YouTube — off our site, mid-funnel.

### Head-to-head: their voice analyzer vs our accent test
Reviewers of RiseGuide specifically praise its **AI voice analyzer**, so the feature overlap is real, and their value stack literally includes *"speak with confidence."* At 0:09 their in-app lesson reads *"Have you ever been in a conversation where someone barely made eye contact with you?"* — squarely our territory.

Where we are unambiguously stronger: their app is lessons *about* communication delivered as bite-sized content ("7 minutes with your morning coffee"), which is exactly the **content-based** model our playbook defines itself against. Our differentiator — *practice-based, trains how you sound, daily vocal exercises with AI feedback* — is a real distinction, and their own positioning hands us the contrast. Their proof is "864K learning hours / 400K MAU / 1M downloads." Ours is **8.4M accent tests and 120+ accents detected.** We win the numbers comparison outright if we put it on screen.

---

## 4. 2026–27 hero-video practice (sourced)

**Performance is now the binding constraint, not aesthetics.**
- LCP ↔ conversion: ~1 s LCP correlates with conversion as high as 40%; slipping to 3 s drops it to ~29%. ([The Fix](https://blog.thefix.it.com/what-is-a-good-lcp-time-the-definitive-2026-performance-guide/))
- Autoplay hero videos are the **#1 cause of LCP failures** on visually-rich sites. ([Mintec](https://mintec.co/blog/video-lcp-hero-performance-2026/))
- The architectural rule: **the poster image is the LCP element; the video is progressive enhancement.** Use `preload="none"` and activate via IntersectionObserver, with a native `<video>` — no JS framework needed for hero autoplay. ([Aaron T. Grogg](https://aarontgrogg.com/blog/2026/01/06/improving-lcp-for-video-hero-components/), [Mintec](https://mintec.co/blog/video-lcp-hero-performance-2026/))

**The current baseline recipe.** Muted + autoplay + loop + playsinline; ≤ 4 MB; 1920×1080; H.264; a bottom mask-gradient; and a poster fallback honouring `prefers-reduced-motion: reduce`. ([SitesPlaced](https://sitesplaced.com/blog/cinematic-landing-pages-with-video-backgrounds))

**Codecs and sizing.** AV1 primary with HEVC then H.264 as ordered fallbacks. 720p is generally sufficient for an autoplay loop; reserve 1080p for front-and-centre. Compress at CRF 23–28. ([Mux](https://www.mux.com/articles/add-background-video-website-hls-performance), [Cloudinary](https://cloudinary.com/guides/video-effects/video-autoplay-in-html))

**Sound-off is the design default, not a constraint.** All modern browsers block autoplay with sound, and `playsinline` is mandatory on iOS or Safari goes fullscreen and breaks autoplay outright. ([Ignite](https://www.ignite.video/en/articles/basics/autoplay-videos), [MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/video))

**Format choice follows intent.** Autoplay loops set mood in headers; explanation and storytelling belong behind a play button. ([Ignite](https://www.ignite.video/en/articles/basics/autoplay-videos)) — This is the single strongest external argument for Ivan's two-deliverable split.

**AI avatars crossed the credibility line in 2026.** Synthesia, HeyGen and Synthesys now produce avatars that pass casual viewing, with the market expected to exceed $2B by 2027 and entry pricing around $20/month. ([GenMediaLab](https://www.genmedialab.com/news/ai-video-trends-2026/)) Practical read for us: an AI presenter is no longer an automatic tell — but it is also no longer a differentiator, and for a product whose entire promise is *authentic human voice*, a synthetic presenter carries a specific credibility risk worth weighing deliberately in Phase 2.

**Landing-page direction.** 2026 SaaS design is trending toward personality, interactivity and conversion-focused storytelling, with narrative headlines and supporting visuals telling a story in seconds. ([SaaSFrame](https://www.saasframe.io/blog/10-saas-landing-page-trends-for-2026-with-real-examples))

---

## 5. Synthesis — what great hero videos share

1. **They are loops, not stories.** Five of eight analyzed heroes are a single unbroken shot; the median is ~17 s. The hero's job is to be enterable at any frame, because a visitor arrives at a random point in the loop. Narrative structure assumes a beginning; a loop cannot.
2. **They are legible with the sound off — by construction, not by captioning.** RiseGuide duplicates narration as kinetic type. Yoodli and Descript let the product UI carry the words. Nobody relies on a voice nobody will hear. *Our current cover has no on-screen text at all — muted, it says nothing.*
3. **The product is the visual.** Yoodli and Descript show only interface. Our own asset already does this well — real Voice Test screens and a results view with metric bars — and that is the strongest thing in it.
4. **The first frame is a design decision, because it is the poster and therefore the LCP element.** Every strong reference has a deliberate opening frame. Ours is a defocused empty room.
5. **Length is set by placement, not ambition.** 5.5 s (Speak) to 30.8 s (Poised) for genuine web heroes. The one 88-second hero in the set is the one that was repurposed rather than designed, and it pays for it with a dead final third.
6. **The best hooks name the viewer's private failure before naming the product.** Treasure: "when they speak, people don't listen to them." RiseGuide: "stop scrolling." Both describe the viewer, not the company. Neither opens with a brand introduction — which is also exactly what our playbook's loser list forbids.
7. **Trust is built by saying what the thing is not.** "No AI hallucinations" (RiseGuide), "I'm not looking to get into debates" (Harris). In an AI-sceptical category, the negation beat does more than another benefit claim.

---

## 6. What this means for a video that sits *above a quiz*

No reference in this set shares our constraint, so this is reasoning rather than observation — flagged as such.

The quiz is the conversion mechanism and it already works. Therefore the video's job is **not** to convert, and not to explain the whole product. Its job is to make the visitor believe the quiz is worth starting, in about five seconds, and then get out of the way.

Consequences:
- **The video must not compete with the quiz for the click.** A hard CTA inside the video creates two competing actions in one viewport — which our own playbook already names as a loser pattern.
- **Watch-through has a ceiling here, and that is fine.** Ivan's success metric is watch-through, but a hero above a functioning quiz *should* leak viewers into the quiz early. Measuring watch-through alone would score a video that hijacks attention as a success. Recommend pairing it with **quiz-start rate** as a guardrail metric so we can tell the difference between a video that earns the scroll and one that steals it. This is the one place where I would push back on the brief's stated metric.
- **Short and loopable beats long and narrative** for the homepage cut. The 88-second RiseGuide approach is the wrong model for this slot even though it is our direct competitor.
- **The YouTube version can be everything the hero cannot** — narrated, 60–90 s, sound-on, play button, full hook→value→proof→CTA arc. That is where the Treasure-style structure belongs.

---

## 7. Playbook exception — needs Ivan's explicit sign-off

`skills/vocal-image/playbook.md` is written for paid social. Three of its hard rules break on a web hero, and I am flagging rather than silently deviating:

| Playbook rule | Hero-video reality | Proposed exception |
|---|---|---|
| "9:16 vertical default always" | Desktop hero is landscape or square; the analyzed set is 5× square/landscape to 1× vertical | **Master at 1:1 square.** Square is the crop-efficient centre — it fills a desktop side-by-side slot, survives a mobile crop, and re-cuts to 9:16 for paid social. Yoodli, Speak and *our own existing cover* all already chose square. |
| "Subtitles in every final export" | Burned-in subtitles under an ambient muted loop look like an error | **Replace subtitles with designed on-screen typography** as the sound-off carrier. Keeps the intent (legible muted) and drops the mechanism. Real subtitles stay mandatory on the YouTube cut. |
| "CTA cards rendered separately and composited" / single CTA | The page's CTA is the quiz; a second CTA competes with it | **Homepage cut carries no CTA.** The YouTube cut keeps the standard single CTA. |

Unchanged and still binding: reference-image control for any generated character, no Mehrabian myth, no invented statistics (tag anything unverified `{VERIFY}`), mechanism (release/resonance) present, app screens on camera.

---

## 8. Coverage — honest accounting

The plan called for deep teardowns of 15. **The pool did not yield 15 live hero videos.** Reporting rather than padding:

**Analyzed at frame level (8)** — RiseGuide, Vocal Image (baseline), Yoodli, Descript, ElevenLabs, Praktika, Poised, Speak. Each has a local artifact directory under `projects/website-hero-video/analysis/<slug>/` containing `video_analysis_brief.json`, `scenes.json` and extracted keyframes.

**Analyzed at transcript level (3)** — Julian Treasure / TED, Vox, Johnny Harris. Narrative-craft tier; per the brief these were mined for hook mechanics, so transcript depth is the appropriate depth. First 100 s of each downloaded.

**Verified absent — checked, no hero video found (5)**
| Site | Finding |
|---|---|
| Orai (`orai.com`) | Site **live** (product copy intact), but no `<video>`, no embed, no media references. Static hero. |
| Speeko (`speeko.co`) | 272 KB page, zero video or embed references. |
| Headspace (`headspace.com`) | 557 KB page, zero video or embed references. |
| Duolingo (`duolingo.com`) | 11 KB JS shell; nothing in served HTML. |
| BetterUp (`betterup.com`) | `vimeo-id` / `vimeo-hash` attributes present but **empty** — JS-populated at runtime, no ID retrievable statically. |

**Blocked — could not be analyzed (4)**
| Site | Reason |
|---|---|
| Calm, Whoop, Blinkist | HTTP **403** — bot protection rejected automated fetches. |
| Oura (`ouraring.com`) | Media URLs found (`/pop/gen4/craft-film-final.mp4`, `/sizing/Oura_Sizing_240918_en.mp4`) but the download returned an error page rather than video. |

**Two limitations worth stating plainly.** (1) The 403 and JS-populated sites are reachable with a real browser session — if Ivan wants Calm, Whoop, Blinkist, BetterUp or Duolingo genuinely covered, that is another pass, not a dead end. (2) There is still **no quantitative performance data** behind any of this — the repo has none, `context/scripts/` does not exist, and none of the competitor numbers are ours to verify. Every craft judgement here is reasoned from construction, not from measured retention. If hook-rate or retention figures exist in Drive or ClickUp, folding them in would materially upgrade Phase 2.

---

## 9. Open questions for Ivan before Phase 2

1. **Guardrail metric** — do you accept pairing watch-through with quiz-start rate? (§6)
2. **Playbook exceptions** — sign off on the three in §7, especially mastering at 1:1 square rather than 9:16.
3. **Existing asset** — do we re-cut `website_cover.mp4` as an interim hero (its app-UI shots are genuinely usable) while the new one is produced, or leave the slot empty until 1 September?
4. **AI presenter** — worth deciding early given the credibility tension in §4 for a product about authentic human voice.
5. **Second research pass** — want the 403/JS-blocked five properly covered?
