# What Higgsfield's own feature pipeline does — and what we take from it

Source: the ONEIRIC project brief, published read-only inside Cinema Studio
(`projectId=85a0f627-285b-4c8a-ac20-bcfd309d54c5`, "Project brief" in the left rail). ONEIRIC
is Higgsfield's own ~20-minute photoreal short — every frame generated, no footage, no sets.
The brief is written as a production breakdown: pipeline, tools, and the hacks they learned.

It is worth reading in full, because it is the only first-party document of its kind. This file
records what it changes for us.

**It is also the origin of the TIG skills.** The brief names them by filename —
`tig-scene-engine.skill`, `tig-acting-task.skill`, `tig-diagram.skill` — plus `CINEDANCE
HIGGSFIELD SKILL.skill`. All three TIG skills are installed in this repo as
`tig-scene-engine`, `tig-acting-task` and `tig-blocking-map`. They are not third-party
add-ons; they are the playbooks this film was made with.

## Scale, for estimating

41,118 assets for ~20 minutes. Per scene folder: COSMOS 5,397 · FAIRY TALE 3,743 · TROY 1,665 ·
the main LIVINGROOM split across seven folders totalling ~4,100 · a `regenerations` folder of
292. A one-room dialogue scene held across dozens of shots is described as *the hardest
technical task of the film* — harder than the space battle. Budget accordingly: continuity in
an ordinary room costs more than spectacle.

## 1. The diagram — the fix for the failure we documented all session

Our `dialogue-prompt.md` records, across three separate scenes, that a named screen side never
carries: the shoulder edge comes back mirrored, or the backgrounds swap instead. We concluded
"check the first frame, don't reword". Higgsfield's answer is better — **stop using words for
staging at all.**

> When a shot needs precise multi-character staging — who is where in the frame, in what pose,
> facing which way — words alone stop being enough. […] Win rate on staging-accurate takes goes
> up dramatically.

A schematic, colour-coded outline drawing is attached alongside the real references, and the
prompt binds each colour to a character tag. The full method is `tig-blocking-map`; the points
that explain *why* it is built the way it is:

- **Front view from the camera's side, never a top-down floor plan** — "video models think in
  frames, not blueprints."
- **Letters (A, B, C) exist in the prompt text only**, bound to figures through colour. A
  rendered letter bleeds into the shot.
- **The connector block is written in positive form only** and never names the map's graphic
  style even as a ban, because "no flat illustration" still injects the word *flat*.
- **The diagram is attached last**, after the location and character references, so the photos
  win the style vote.
- **Editing a diagram: name elements by colour, never by character** ("move the BLUE figure",
  not "move Rudy"), and always regenerate from the **original frame**, never from the previous
  diagram — feed a drawing back in and the model copies the drawing's flaws.
- Once a scene has a diagram, coverage becomes conversational: "give me the MCU on the blue",
  "now the POV of the green". The convention extends to trajectories (a dashed coloured path
  with start, path, end and trigger beat) and to camera moves (arrows declared camera-path-only
  in the legend).

**Use it whenever a shot has more than two people, or whenever a previous take flipped a
position.** This is the single biggest upgrade available to our workflow.

## 2. Move an unreliable instruction one step earlier, into the asset

Their anamorphic problem is our lens problem exactly:

> Ask Seedance for that look in a video prompt and it won't hold it reliably — the optics drift
> from shot to shot. The fix is to move the lens one step earlier in the pipeline: generate the
> location image with the anamorphic effect already in it. Seedance reads the optics straight
> off the asset and keeps them — **the plate itself becomes the lens.**

The optics block they append to the *location image* prompt:

```
STRONG anamorphic lens character: horizontal squeeze and compression, oval elliptical bokeh,
horizontally stretched highlights, curved barrel edge distortion, chromatic aberration toward
the edges. NO lens flares, NO light streaks, NO floating bokeh circles. 2.39:1.
```

Dosed with *subtle / gentle / moderate / strong / maximum*.

Generalise past anamorphic: **any look the video model keeps dropping — a grade, a lens
character, a texture, a time of day — belongs in the asset image, not in the video prompt.**
We learned the negative version of this the hard way when an evening prompt lost to a daylight
kitchen reference; the reference wins, so put the thing you want in the reference.

## 3. Where a negative is allowed, and where it summons

Their iron rule reads:

> Say what you want, not what you avoid — the words you write are the words you summon,
> including the ones inside a "no".

And in practice the bans (`NO lens flares, NO light streaks`) appear **only at the image
stage**; in video prompts "those words never appear at all — even as bans".

This looks like it contradicts our own finding that naming the three ways a model cheats an
approach (side door, frame edge, teleport) is what made the corridor scene work. Both are true,
and the line between them is what to write down:

| Kind of negative | Verdict |
|---|---|
| A renderable noun — *lens flare, grid, vector, flat illustration, letters* | Never write it, not even in a ban. The token summons the thing. |
| A blocking or action cheat — *do not enter from a side door, do not skip his approach, do not replace the hand raise with a glance* | Works, and often nothing else does. These name a behaviour, not an object the model can draw. |

## 4. Character sheets: two passes, and the base pixels are never re-run

Materially better than what our step 3 currently does:

1. **Soul Cinema makes the face, always in close-up** — "so the model captures identity at
   maximum detail — that close-up face is the anchor every other asset of the character is
   checked against."
2. **Soul 2.0 then builds the looks** — full-figure images with wardrobe, materials and
   silhouette matched to the locked face.
3. The two are assembled into the sheet in Seedream / Nano Banana / ChatGPT **with one hard
   condition: the original close-up portrait is preserved untouched. It never runs through a
   model again.** Changes between states — a scar, a haircut, dirt, a wound — are integrated
   point-by-point with masks, around the base. "The base image stays the same pixels, so the
   identity (and the skin texture that carries it) survives every new version."

That last rule is the one we did not have. Re-running a portrait through any model to make a
variant is how a character slowly stops being the same person.

## 5. A new state is a new asset, never an overwrite

> A character has as many assets as states he goes through: Alfie in the common room and Alfred
> in the lab bed are different assets of the same man.

Their tag convention, which our ID scheme already resembles:

```
@loc_ON_dorm_commonroom_front_s2    location + project + name + scene
@char_ON_Rudy_s2_v1                 character + project + scene + version
@prop_ON_pizza                      prop + project + name
```

The scene suffix ties an asset to where it lives; the version suffix appears when a state
changes. The stated reason for one convention across a team is duplicate control — "the same
couch living under three different names, and nobody knows which reference is the real one."

## 6. Voices live in a Voice Bible and are pasted verbatim

> A voice here is a written block — register, timbre, tempo, manner — decided once, stored in
> the Voice Bible, and pasted into every generation verbatim, **never even a synonym changed.**

```
BOB — voice: warm boisterous baritone, big dynamic range, theatrical comedic enthusiasm,
a gravelly edge; bursts loud then drops to a mock-confidential murmur, punches key words,
laughs mid-line. American.
```

Note this is for shots where the model generates the speech. A VO-driven piece still records
narration separately (our step 2).

## 7. Their CINEDANCE block order

```
SCENE CONTEXT · ACTIVE REFERENCES · LOCATION MAP · GAZE / EYELINES ·
FIRST FRAME AND BLOCKING · SEGMENTS (timed beats) · DIALOGUE · AUDIO ·
PHYSICS · LIGHTING · STYLE / FORMAT · POSITIVE LOCKS
```

Two differences from ours: **GAZE / EYELINES is its own block**, placed before blocking; and
DIALOGUE and AUDIO are separated, AUDIO carrying voice identity only ("see DIALOGUE for
words").

And the framing rule behind all of it:

> Seedance sees only the text in front of it, so **every prompt is an island**: positions,
> poses, wardrobe, props, optics, light — spelled out from scratch, every time. "Same as the
> previous shot" is an instruction to a model that has no "before".

In their real Scene 2 fragment, note that the LENS description is repeated **inside every
segment**, not stated once at the top — for the same reason.

## 8. The script is stress-tested before anything is generated

> On an AI film a weak scene costs real money — you find out it doesn't work only after you've
> generated it.

Every scene runs through `tig-scene-engine` — Goal, Obstacle, Tactic, Reversal, Value Shift —
which returns a verdict per element, the single weakest point, and "what if" fixes from minimal
to clean rewrite. This is a step our workflow did not have at all, and it is the cheapest one
in the whole pipeline.

The same stage produces the **director's read**: for each scene, the one shared event every
character lives through, and each character's own physical channel for it. Their example — the
event is "the search for self-forgiveness"; one man relives it in a dream, one hides in
flawless procedure, one cares for a patient beyond the checklist; the surface (routine rounds)
is just terrain.

## 9. Acting: tasks, not emotions

> Write "sad" in a prompt and you get a caricature or a dead face.

`tig-acting-task` replaces emotion labels with an acting task — the character invested in a
tactic, with **the eye-work named as action**: checking both of the partner's eyes, registering
whether the point landed, stealing looks and snapping back.

> Dead, glassy eyes are never fixed with lighting — they're fixed by giving the eyes a job.

Short block form:

```
ACTING TASK — [NAME] (invested in his tactic; the work happens in his eyes):
SCENE DIRECTION (shared, unspoken): [one line]
MOTIVE / GOAL / OBSTACLE: [his fuel, his fight, what presses on it]
TACTIC, moment to moment:
— "[dialogue words]" — [verb at the partner + what the eyes check]
(Safety: gaze always engaged in the task; natural blink cadence.)
```

## 10. Post: five stages to picture lock

1. **Assembly** — all scenes in script order, no rhythm. Goal: see the whole thing, find sags
   and coverage holes.
2. **Rough cut** — rhythm, trims, rearrangements; the main list of shot re-orders forms here.
3. **Generation supervision** — a QC pass *after* the rough cut: re-generate broken shots, clean
   out AI slop, catch what doesn't work before the fine cut.
4. **Fine cut** — precise fitting, screenings with cold viewers.
5. **Picture lock** — after lock, no new generations except emergency fixes, with notice to
   colour and sound.

Stage 3 is the one worth stealing: regeneration is a scheduled pass at a fixed point, not a
running reaction to every take. And on grading:

> Every generation arrives with its own built-in grade, so the colorist's job here is
> unification — bringing neighbouring shots to one look.

## Their four closing rules, verbatim

- **Assets first** — not one shot until every character, location and prop is named, versioned
  and locked.
- **Describe everything, every time** — the model has no memory.
- **Say what you want, not what you avoid** — the words you write are the words you summon,
  including the ones inside a "no".
- **Direct, don't describe** — scene event, motive, goal, obstacle, tactic. "The director's
  craft is the one part the model can't invent for you yet."

---

# ADILIADA — the same pipeline again, plus two additions

`higgsfield.ai/original-series/adiliada/full-film` — a ~6-minute photoreal short built as a
series opening, 11,299 assets. Its brief restates ONEIRIC almost point for point: the same
two-pass character sheet with the untouched base portrait, the same twelve-block CINEDANCE
order with GAZE / EYELINES, the same five post stages, the same closing rules. That repetition
is itself useful — it means those parts are settled practice, not one film's experiment.

Two things are new.

## The depth map — a second geometry channel

Alongside the blocking diagram, they feed a **depth map**: a black-and-white image where light
areas are near and dark areas are far. The model reads it as the depth skeleton of the scene,
which buys correct composition, volume and proportion. Their stated failure without it is the
space drifting — a location that rearranges itself every few seconds.

So there are two separate non-textual controls, and they solve different problems: the
**blocking diagram** fixes *who is where in the frame*; the **depth map** fixes *how deep the
room is and how the bodies sit in that depth*. Reach for the depth map when a shot has real
foreground/background separation to hold, or when a space keeps reshaping between takes.

## Hold the face, change everything else

ADILIADA's hero exists in several universes, each version with its own look and personality, and
the production rule is stated as a law:

> A new universe is a new look, not a new person. The base is never touched.

Alternate versions are built from **the same base face pixels**; wardrobe, makeup, hair, scars
and damage all change around it. That is the same rule as "a new state is a new asset", pushed
further: it also covers casting variants, aged/de-aged versions, and a character appearing as
himself in a different register. Directly applicable to our v1/v2/v3 casting folders and to
reworks — a variant is a re-dress of a locked face, never a re-generation of it.

## And one independent confirmation

ADILIADA plants **visual anchors** in every scene and location for the same stated reason Cully
Hill gives — "the chair a character sits in, the window two of them talk by" — objects that hold
a scene consistent and keep characters in the same places across generations. Two of three
briefs name the anchor rule independently, so treat it as a law rather than a preference.

They also run a **unification pass over the location set before generating**: once the plates
exist they are edited for colour, light and saturation so the whole set matches in character.
Cheaper than discovering the mismatch in the grade.

Their development stage adds one line worth keeping: after the drama pass the project goes into
a step-by-step storyboard, because only on the storyboard does it become clear how good a scene
really is, as opposed to how good it was in your head.
