---
name: locals-translate
description: Localise Vocal Image creatives with HeyGen Video Translate — dub + lip-sync one or many videos into any target languages, always on the Precision engine with source quality/format preserved, driven through the browser UI with Google Drive links. Use when Ivan says "/locals_translate", "переведи эти крео", "translate these creatives to es fr it pl", "залей в heygen и переведи", names languages next to a list of creative codes, or drops a Drive folder / local files and asks for localised versions. For a human-corrected script pass instead of direct generation, use locals_profread.
---

# locals-translate

Batch localisation of Vocal Image performance ads through the HeyGen **Video Translate** web app. Produces dubbed, lip-synced versions in the requested languages.

Also triggers on the underscore spelling Ivan uses: `locals_translate`.

## Trigger

- `/locals_translate`, `locals_translate`
- "переведи эти крео на es fr it pl", "translate these to Spanish/French/Italian/Polish"
- A Drive folder link or local file paths + a language list
- Any request to localise / dub existing creatives (not to *create* new ones)

Use **locals_profread** instead when Ivan wants the script reviewed before generation.

## Inputs

1. **The videos** — a Drive folder link, individual Drive links, or local paths.
2. **The languages** — whatever he names (`es fr it pl`, `Russian`, `de`, …). If he names none, ask; never guess.

## Locked settings — never vary these

| Setting | Value | Where |
|---|---|---|
| Engine used | **Precision** | main row (shows a `Premium Engine` badge on the file card) |
| Keep source quality and format | **ON** | Advanced Settings |

Precision is required because these ads cut between speakers and camera angles; Speed only holds up on a single front-facing talking head. Everything else stays at HeyGen's default unless Ivan says otherwise — in particular leave `Adjust video length to fit speech` ON (its default) but **tell him** it means output duration drifts from the source, which matters for ad specs.

Use the plain language entries (`Spanish`, `French`, `Italian`, `Polish`), not regional variants, unless he asks for a specific market.

## Step 1 — make every file reachable by URL

HeyGen's URL field fetches **anonymously**, so the file must be `anyone with the link`. A named-user grant on a Shared Drive is invisible to it and produces `URL is invalid, please ensure that it's correct and has open access`.

- Already on Drive and public → use `https://drive.google.com/file/d/<ID>/view?usp=sharing`.
- Local file, or a Drive file that is not link-shared → `python3 scripts/drive_push.py FILE...`, which uploads, link-shares, and prints the URL.
- Uploading into someone else's Shared Drive folder can 403 even when you can read it; the helper falls back to My Drive root, which works fine for HeyGen.

Do **not** try to upload local files through the browser: the file-upload channel caps at 10 MB against 20–400 MB masters, and OS-level drag-and-drop is not available.

Verify access before blaming the UI:

```bash
curl -sL -r 0-511 -o /dev/null -w "%{http_code} %{content_type}\n" "https://drive.google.com/uc?export=download&id=<ID>"
```

`text/html` here is **not** a blocker — that is Google's virus-scan interstitial (or plain rate-limiting on repeated anonymous hits). HeyGen still imports such files, including 400 MB ones. Only the UI's own error message is authoritative.

## Step 2 — per-video UI recipe

Everything below fails **silently** — the page simply does not advance. Verify each stage instead of assuming.

Window size varies between sessions, so **never reuse hardcoded coordinates**. Compute the ratio once per page:

```js
const scale = <screenshotWidth> / window.innerWidth;   // e.g. 840/2160 = 0.3889
// screenshot coords = cssCoords * scale
```

1. **Load the video.** Click the URL field, `cmd+a`, then **type the whole URL as real keystrokes**. Do *not* set it with the native value setter — a synthetic set leaves React's state empty, the arrow stays inert, and you burn 3–6 blind retries. Real typing loads it first try. Then click the arrow once.
   - If it still does not advance after ~20 s, click the field, press `End`, and click the arrow again. Never put two arrow clicks in one `browser_batch` — they cancel each other.
   - Confirm by reading the file name off the card, not by assuming.

2. **Pick languages.** Click the `Translate it into` field for real (a trusted click renders the `Choose language` input and opens the list). Then per language: set the filter text via JS, wait ~1.1 s, and click the **first** checkbox — the plain name always sorts above regional variants.
   - The filter **resets after every selection**. Never click a fixed row coordinate twice; you will silently select Afrikaans.

3. **Engine → Precision.** Click the `Speed` control, then the `Precision` row.

4. **Advanced Settings → Keep source quality and format ON.** Toggle this **via JS** on the `[role=switch]` and assert `aria-checked === "true"`; coordinate clicks miss while the modal animates. Then `Done`.

5. **Verify before submitting.** `zoom` on the top row and read: all language chips present, `Precision`, correct file name, `Premium Engine` badge.

6. **Submit.** Press `Escape` first — the language dropdown stays open and silently swallows the click. Then click `Translate` with a **real coordinate click** — a JS `.click()` is ignored (trusted-event check).
   - Do not locate this button by text alone: `Translate` also matches the tab in the segmented control at the top of the page, and clicking that does nothing. Take the coordinates off a zoom.
   - Success = the URL becomes `…/projects?folder=<id>`. Check that rather than screenshotting.

## Step 3 — rename the project folder

A URL-imported job names the folder **and all its outputs** after the Drive URL, which breaks the universal naming rule (video name = script name = ClickUp task name). Rename the folder to the creative code; outputs keep their own `-Language` suffix, matching the team's existing `KR_TST_61_A_1_CLEAN-Italian-Polish` pattern.

Hover the tile to render its `…` button, then Rename. Automate it, but batch only **2–3 renames per JS call** — more exceeds the 45 s CDP timeout. The renames still land even when the call times out, so re-check state before retrying rather than redoing them.

## Cost

Roughly **5 generative credits per output-minute** (measured: 116 outputs ≈ 300 output-min ≈ 1520 credits). Multiply source duration × number of languages. Check the balance before a big batch:

```bash
cd ~/Desktop/OpenMontage-main && export $(grep '^HEYGEN_API_KEY=' .env | xargs) && \
curl -s https://api.heygen.com/v2/user/remaining_quota -H "X-Api-Key: $HEYGEN_API_KEY"
```

The API key itself has very few `api` credits and cannot drive this at scale — that is why this skill uses the web UI, which draws on the plan's generative credits.

## Report back

Per creative: name, duration, languages, and confirmation that Precision + keep-source were verified. Flag anything that needed a different variant than asked, and say plainly if a file's on-screen text is English (dubbing cannot touch burned-in pixels) — though for Vocal Image that is usually fine, since those segments get replaced at the edit stage.

Related: [[feedback_heygen_translate_ui_quirks]] in memory carries the same trap list.
