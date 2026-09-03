# HELL GRIND — the origin brief, and what only it says

Source: `higgsfield.ai/original-series/hell-grind/episode-1` (note: `episode-1`, not
`full-film`). A 95-minute generated action-fantasy feature, screened at the Marché du Film in
Cannes 2026. 115,451 assets.

This is the earliest and most detailed of the four Higgsfield Studio briefs, and the one the
others are built on — Cully Hill's "what we took from the previous film" refers to this. Read
`cully-hill-pipeline.md` first for the current shape of the process; read this for the parts
that appear nowhere else, and for the reasons behind rules the later briefs only state.

## The production shape, for planning

95 minutes, **15 people**, budget under **$500K**, and — after the assets were prepared and
before post — **14 days of generation**. The team is a director group plus prompt engineers,
each owning their own block of scenes. Their own closing note: the pipeline does not need
fifteen people, it scales down to a team of one; what it needs is the rules followed.

Tool division, which is more specific than the later briefs:

| Job | Tool |
|---|---|
| Video and speech | Seedance |
| Faces and locations | Soul Cinema |
| Image edits | Nano Banana Pro, Seedream |
| Text in frame, props, reverse angles of locations | GPT Image |

## Keep the character sheet boring — the counterpoint to baking the look into the plate

> The cinema look does not live in the character sheet — it lives in the locations and in the
> video prompts.

Neutral grey, flat light, real skin with visible pores, no retouch. **Bake film grain or a
cinematic lens into a sheet and the character carries that look into every scene and stops
reacting to new light.**

Put beside ONEIRIC's anamorphic hack, this gives a clean two-part rule:

- **The look goes into the location plate.** That is where you want the model to read it off.
- **The look never goes into the character sheet.** A character carrying baked-in light stops
  responding to the light of the room he walks into.

## Choosing the face

Soul Cinema is a creative model — one prompt returns several different versions of a face.

- **Pick the most believable, not the most beautiful.** A beautiful-but-fake face shows its
  fakeness later, in video, when it is too late to fix.
- **Always check the eyes.** Even dark eyes need a small light reflection in the pupil. Without a
  catch-light the face reads dead, and no video model can act with a dead face.
- The sheets the model understands best carry a **large portrait in three-quarter view**.

## Why the base image is never re-run — stated properly

The later briefs say "never runs through a model again". This one gives the mechanism:

> Every extra pass destroys texture and drifts colour — after two passes the face turns
> symmetrical, plastic and lifeless, and that dead texture later hurts the acting in video.

The workflow for a variant: make the point change on the original sheet in an image model, then
bring it onto the original by hand with a mask in a graphics editor. The mask places only the
changed part — the jacket, the scar, the blood — over the original; everything else is untouched
pixels.

## Name the role of every reference

This is the mechanism behind the inheritance ban, and it appears only here:

> Name the role of each one right in the prompt — or the model decides by itself, and decides
> wrong: it copies the composition instead of the face, or the face instead of the colour
> palette.

```
@roco for character reference
@loc_cave_front for location reference — take only the space and the texture: do not use as a
starting frame, do not inherit the composition, the angle or the colour.
```

## Prompt length, and the real constraint

Their prompts ran **3,000–4,000 words**.

> Length is not the enemy; an overloaded beat is.

**Up to three sentences per beat** — overload one and the model smears it. Write in present
tense, short sentences, and put the camera inside the action rather than in a separate paragraph.

This is the answer to "should prompts be longer": yes, but the length comes from more beats and
more blocks, never from denser beats.

## Never write an age, in any language

> The content filter becomes much stricter the moment it reads a minor; instead of age, give the
> role, the clothes, the action.

We hit exactly this and lost generations to it. It is a straightforward rule: no ages anywhere in
a prompt, and a young character is described by role, wardrobe and behaviour.

## Keep a ban dictionary of words the model punishes

Per project, a list of words to substitute: *dark* becomes *low key*, *jolting* becomes *rapid
motion*. Worth starting one for Vocal Image and adding to it whenever a word demonstrably drags a
generation somewhere unwanted.

## The character-count header and the duplication bans

SCENE CONTEXT opens with a literal header:

```
EXACT 3 CHARACTERS — NO DUPLICATES: ROCO, JAX, REIN.
```

> The model loves to add extra people and to clone furniture.

Only characters whose references are in the prompt exist in the frame, and set dressing gets its
own count lock — exactly one of a thing, never a second one. Their POSITIVE CONSTRAINTS block
counts everything: three people and no one else, one crystal arm on the right arm only, five
smashed mannequins never re-rendered intact and never multiplied, two trays and never more.

## The Style Prefix as a project constant

A single block, pasted word for word at the end of every prompt, covering style, cinematography,
lighting, colour ratio, camera, skin, acting, physics, composition, continuity, technical and
audio. It lives as a constant next to the descriptors, so one edit updates every shot in the
film at once.

Two lines from it that are policy rather than taste:

- `Colour: 60:30:10 — dominant / secondary / accent.` — the same ratio Cully Hill expands into
  its colour bible.
- `Audio: Environmental SFX only. No music. No subtitles.` — mandatory, because a generated
  soundtrack only fights the edit.

The prompt closes with technical tags: `Photoreal. NON-IP. [aspect ratio]. [duration]s. SFX only.
NO CGI. Cinematic.`

## GEO SPATIAL LAYOUT

Cully Hill's spatial map, named and with one clarification the later brief drops:

> GEO is only the map. The look of the place still comes from the location asset — its descriptor
> and reference go into the prompt next to the map.

Its content: the landmark objects, what is frame-left and frame-right, where the camera stands
and which line it never crosses, and the lighting direction — **no heroes and no action, only the
place**. Written once per scene, pasted into every shot of that scene unchanged.

## How a dialogue line is built

Always the same four parts, in order: **the voice and its emotion → the line in quotes → the
physical action → the facial reaction.**

And a hard separation that we have not been observing:

> Lines live only in the audio section of the prompt — not one word of speech inside the action.

Because Seedance adds its own filler — "uhms", chuckles, whole phrases — the prompt carries an
explicit block: everyone speaks **only** the quoted line; anyone without a line stays completely
silent; and a "half-laugh" written into the action is a facial expression **with no sound**.

Two more things in the audio block:

- **Write the mix.** Voices clean and close to the microphone, ambience underneath, ambience
  dipping when someone speaks.
- **Rare names get a phonetic transcription**, or the model mangles them.

Seam technique: **open every new generation with the line that closed the previous one** — the
emotion crosses the cut together with the text. (Same family as feeding the previous line's tail
into the opening wide.)

## Two staging problems and their fixes

**A transition between two spaces holds on a threshold.** Put both location assets in one prompt
and make the seam a doorway with a light contrast across it — a warm amber room, a cold blue
corridor beyond the arch. The contrast explains the palette change and forgives small geometry
mistakes.

**Anything much larger than a human needs two anchors at once**: a size comparison written out,
*and* a human figure in frame to measure against. With only one, the model quietly shrinks the
giant back toward human height. Their thirty-metre guardian carries the constraint in every shot
he appears in, and it ends the way their locks always do — a guardian that reads as a large man,
or fits comfortably in frame beside a standing human, is a failed shot.

**Crowds on medium shots take a stated number** — "20+" — or the model gives three people in one
take and a hundred in the next.

## Props split by what the shot needs

Their key artifact existed as three assets: a full one for close-ups, a small bloodied one for a
brief reveal in a palm, and a **"hidden" version for clenched-fist shots, where the prompt forbids
showing the crystal at all and allows only blue light between the fingers.** Splitting states is
cheaper than fighting the model — that applies to what a prop is *doing*, not only to what
condition it is in.

## Where the two feature briefs disagree

Both are worth knowing, and the later one wins:

| | HELL GRIND (earlier) | CULLY HILL (later) |
|---|---|---|
| Iterations before restructuring the shot | 10–15 | 15–20 |
| A failed stress test means | "the problem is your description, not the model" | fix the words first, but suspect the asset too — rebuild the sheet if it breaks again |

The second change is the meaningful one: after a feature's worth of experience they stopped
assuming the prompt was always at fault.

## Their own framing of the whole thing

HELL GRIND began as a short series and grew into a feature; the formula came together near the
end, and the brief is written as the version they would use from day one. Every rule in it exists
because a shot failed without it — which is exactly the standard we have been holding
`dialogue-prompt.md` to.
