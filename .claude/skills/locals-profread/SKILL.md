---
name: locals-profread
description: Open a HeyGen "<Language> Proofread" pass on Vocal Image creatives — transcribe and translate the script into the target language and stop there, so a human corrects it before any video is generated. Use when Ivan says "/locals_profread", "сделай профрид на русский", "open proofread for each video", "не генерь перевод, а открой профрид", or names a language and asks for a script-review pass rather than finished dubs. For direct dub + lip-sync generation instead, use locals-translate.
---

# locals-profread

Same pipeline as **locals-translate**, but it stops at the script stage: each video becomes a `<Language> Proofread` project that a human opens, corrects, and only then generates. Ivan's standing use for this is **Russian**, where machine translation needs a native pass before it can ship.

Also triggers on the underscore spelling Ivan uses: `locals_profread`.

## Trigger

- `/locals_profread`, `locals_profread`
- "сделай профрид на русский", "открой профрид каждому видосу"
- "не генерить перевод, а именно открыть proofread"
- Any request for a reviewable script pass instead of finished dubs

## Why it is separate from locals-translate

| | locals-translate | locals-profread |
|---|---|---|
| Final click | `Translate` | **`Review and edit script`** |
| Result | finished dubbed videos | a `<Language> Proofread` project |
| Generative credits | ~5 per output-minute | **0** |
| Human step | none | edit the script, then generate |

Because it costs nothing up front, a proofread pass is safe to run across a whole batch without checking the credit balance first. Credits are only spent later, when someone approves the corrected script and generates.

The state **persists** as its own project entry with a `Proofread` badge on the thumbnail — closing the tab does not lose it. The team already has such items in the account (`c4-are-you-awake-Russian` → `Russian Proofread`), so this matches existing practice.

## Inputs

1. **The videos** — Drive folder link, individual Drive links, or local paths.
2. **The language** — usually `Russian`; ask if unnamed. Multiple languages work too (one proofread per language).

## Locked settings — identical to locals-translate

| Setting | Value |
|---|---|
| Engine used | **Precision** |
| Keep source quality and format | **ON** |

Set these even though nothing generates yet: they are stored on the project and apply when the corrected script is finally rendered. Use plain language entries (`Russian`, not `Russian (Russia)`) unless Ivan asks otherwise.

## Recipe

Steps 1–5 are **exactly** locals-translate — read that skill for the full trap list (anonymous Drive access, the keystroke that commits the URL, the arrow needing 2–3 separate clicks, the language filter resetting after each pick, the JS-only Advanced-Settings toggle, the scale factor for coordinates). In brief:

1. Get every file reachable at a link-shared Drive URL — `python3 scripts/drive_push.py FILE...` for anything local.
2. Load the video: click the URL field, `cmd+a`, **type the full URL as real keystrokes** (a synthetic value set leaves React empty and the arrow inert), then click the arrow once. Retry in a *separate* call if the file name does not appear on the card.
3. Pick the language: real click on `Translate it into`, then JS-filter and click the **first** checkbox.
4. Engine → **Precision**.
5. Advanced Settings → **Keep source quality and format ON** via JS (`aria-checked === "true"`), then `Done`.
6. **Press `Escape`**, then click **`Review and edit script`** — a real coordinate click, to the right of `Advanced Settings` beneath the file card. The Escape matters: the language dropdown stays open over that row and eats the click, leaving you on the same page with no error. This is the whole action; **do not** touch `Translate`.
   - Success = the page navigates to `…/projects` and a new entry appears labelled `<Language> Proofread`, dated `just now`.

Then rename the project folder to the creative code, exactly as in locals-translate — the import still names everything after the Drive URL.

## Verify

- The new project reads `<Language> Proofread` (e.g. `Russian Proofread`), not just the language.
- Generative credits are **unchanged** before vs after. If they dropped, a `Translate` was fired by mistake — say so immediately.
- Count the proofread projects against the input list; report any creative that did not produce one.

## Report back

A table of creative → duration → `<Language> Proofread` created, plus the reminder that these are **awaiting human correction** and generate nothing until someone opens each one, fixes the script, and renders. State the credit balance as untouched.

Related: [[feedback_heygen_translate_ui_quirks]] in memory carries the shared trap list.
