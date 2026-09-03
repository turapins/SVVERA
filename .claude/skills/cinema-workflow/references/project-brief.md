# Project Brief

Every Cinema Studio project carries a **Project Brief** panel with seven fixed sections:
Context, Narrative, Visuals, Production, Status, Resources, Notes. Fill it before the first
generation.

Whether Higgsfield's backend parses it is unconfirmed — the claim comes from a Google AI
Overview, not from Higgsfield documentation, so do not rely on it. Fill it anyway: it is the
only place where the constants true for **every scene** live. Without it those constants get
retyped into each prompt, drift between prompts, and the drift is what shows up as a
different grade or a different camera language three scenes in.

**The division of labour:**

| Where | What it holds |
|---|---|
| Project Brief | what is true for the whole project — look, camera, voice, model settings, casting rules |
| Script `.md` | the elements table and what happens in each scene |
| Scene prompt | only this scene — blocking, action, dialogue, camera |

A fact that belongs in the brief should never be repeated in a prompt. If a prompt is
restating the palette or the camera rules, the brief is not being used.

## Template

Copy-paste this into the panel and fill it.

````markdown
# <CODE>            ← project title = the creative code only, nothing else

<One line: what this is. Format, length, market.>

## ✨ Context

Client / product. Campaign and where it runs. What this creative is testing, and what it is
adapted from if it is an adaptation. Anything true for every scene in the project.

## 🎭 Narrative

Audience — who is watching and what they already believe.
Logline — one sentence.
Structure — the beat order, in one line each.
Message — the single thing the viewer should leave with.
Voice — VO or dialogue; language and register.

## 🎨 Visuals

Look — palette, light, grade, era.
Camera — handheld or locked, shot sizes, what the camera never does.
Casting rules — what people in this project look like as a class.
Do — the constants every shot must honour.
Don't — the failures this project keeps producing.
Format — aspect ratio, captions, end cards.

## 🎬 Production

Model and settings — generation model, resolution, per-prompt duration limit.
Locations — the location Elements this project uses.
Cast — the character Elements, with their tags.
Pipeline — where the scenes go after generation.

## 🚀 Status

Where it is now. What is blocking. What happens next.

## 🔗 Resources

Script doc — link.
Reference — link to the ad or film this is built from.
Elements — the imported element IDs, once the import has run.
Drive / project folder — link.

## 📝 Notes

Decisions taken and when. Anything that would otherwise be re-litigated later.
````

## Section notes

**Context** — includes what the creative is adapted from. An adaptation without its reference
named loses the reason its structure is shaped the way it is.

**Narrative** — the structure goes here as one line per beat. This is what the scene
breakdown in step 6 works against, and what tells you whether a scene is carrying its beat.

**Visuals** — carries a **Don't** list, and it is the section that earns its keep. Write the
failures this specific project keeps producing, not generic advice. Generic entries are
noise; "no legible content on any screen" is a rule that saves a regeneration.

**Production** — model, resolution, the per-prompt duration ceiling, and the location and
character Elements with their tags. This is the checklist for what must exist before a scene
can be generated.

**Status** — where it is, what is blocking, what is next. Keep it current; a stale Status is
worse than an empty one.

**Resources** — script doc, reference, Drive folder, and the **real element IDs after the
import has run**. Those IDs carry a prefix abbreviated from the document title, so they are
not the short tags written in the script — see `script-format.md`.

**Notes** — decisions and their date. This is what stops a settled question being reopened
three weeks later.

## Worked example

`project-brief-example.md` holds a filled brief for a real project (IT_MES_06 — a 3:14 VO
explainer). Read it to calibrate how specific each section should be.
