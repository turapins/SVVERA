---
name: cinema-workflow
description: >
  Kirill's end-to-end process for producing one AI video scene in Higgsfield Cinema Studio:
  a script written in the Markdown ELEMENTS format so Import elements can extract characters,
  locations and props; a project whose Project Brief holds every constant; character sheets
  and locations generated first and pinned as tagged Elements (@C1, @LOCATION); scene
  direction built with
  CINEDANCE + tig-acting-task + Lira, a script stress-tested with tig-scene-engine before
  anything is generated, a tig-blocking-map diagram wherever staging past two characters
  matters, a short test generation before the full one, final
  generation at 480p, and an optional ByteDance upscale to 1080p at the very end. Use this whenever
  a scene or dialogue video is being generated in Cinema Studio — "сделай сцену", "generate
  this scene", "нужен character sheet", "собери промт для сцены", "сгенерь по процессу
  Кирилла" — or when a script or a Cinema Studio Project Brief needs writing ("в каком
  формате писать скрипт", "подготовь скрипт для импорта элементов", "заполни project brief"). Scene-level
  only: it stops at approved 1080p scene files handed to the edit. Not for editing, cutting
  or captioning (see davinci-ad-assembly, embedded-captions), and not for producing a whole
  ad from a reference (see story-ad-from-reference).
---

# Cinema Studio scene workflow

Kirill's process for producing one AI video scene in Higgsfield Cinema Studio, extended with
what running a whole piece through it taught us, and with the parts of Higgsfield's own feature
pipeline that are better than what we had.

**Read the two first-party pipeline files before a project of any size.** Higgsfield Studio
publishes full production briefs for its own generated films, and they are the only documents of
their kind:

| File | Source | Read it for |
|---|---|---|
| `references/oneiric-pipeline.md` | ONEIRIC (20 min) + ADILIADA (6 min) | the short-form pipeline, the two-pass character sheet, the blocking diagram, the depth map |
| `references/cully-hill-pipeline.md` | THE CULLY HILL BOYS (1h54m, 137 scenes, 473k generations) | everything operational — sheet construction, the video stress test, location kits, the master shot and spatial map, optics anchors, named locks, production discipline, music lip-sync |
| `references/hell-grind-pipeline.md` | HELL GRIND (95 min, 15 people, 14 days of generation, Cannes) | the origin brief — prompt length and the per-beat limit, naming the role of every reference, the age ban, the Style Prefix, how a dialogue line is built, scale anchors |

ONEIRIC is also where the `tig-scene-engine`, `tig-acting-task` and `tig-blocking-map` skills in
this repo come from: they are the playbooks those films were made with, not third-party add-ons.

Where the briefs repeat each other, treat it as settled practice. Where Cully Hill is more
specific, it is later and it wins.

Nine steps, in order. The order is the point: every step exists to stop a specific
inconsistency from reaching the final generation, and skipping one shows up as a changed
face, a changed room, or a broken screen axis three generations later.

```
stress-test the script (tig-scene-engine) → script in import format
       → project + brief → import elements
       → [voice-over first, if VO-driven: measure real scene timings]
       → character sheets → locations → props → Elements check
       → scene breakdown (CINEDANCE + tig-acting-task + Lira)
       → [blocking map, if 3+ characters or a previous take flipped a position]
       → group scenes into blocks
       → plan review → short test → full 480p → [upscale 1080p]
```

**Scope.** This skill covers one scene, from empty project to an approved 1080p file. It
does not cut, join, caption or sound-design — approved scenes are handed to the edit.

## 0a. Stress-test the script before anything is generated

The cheapest step in the pipeline, and the one we did not have. Higgsfield's reason for it:

> On an AI film a weak scene costs real money — you find out it doesn't work only after you've
> generated it.

Run every scene through **`tig-scene-engine`** — Goal, Obstacle, Tactic, Reversal, Value Shift,
with bespoke definitions that are not the textbook ones. It returns a verdict per element, the
single weakest point, and "what if" fixes from minimal to clean rewrite. A scene that fails the
Reversal or Value Shift test will still generate beautifully and still not work, which is the
most expensive way to find out.

The same pass produces the **director's read**: the one shared event every character in the
scene lives through, and each character's own physical channel for it. That read is what feeds
the acting task in step 6.

## 0b. Write the script in the import format

Cinema Studio can read the script and pull characters, locations and props straight into
Elements — **Import elements**, which accepts `.pdf`, `.xlsx`, `.csv`, `.docx`, `.txt` and
`.md`. Nothing is added until the extraction is reviewed.

That only works if the script is written for it. **All scripts are written in Markdown with
an `## ELEMENTS` table at the top and tagged scenes below** — the full spec, rules and a
fillable template are in `references/script-format.md`.

Short version:

```markdown
# PROJECT: VI_RAISE_01

## ELEMENTS

| Type | Tag | Name | Description |
|---|---|---|---|
| Character | @C1 | Anna, 32 | Marketing manager. Reserved. Casual office wear. |
| Location | @OFFICE | Open-plan office, day | Glass partitions, daylight from the left. |
| Prop | @CUP | Paper coffee cup | Plain white, no logo. |

## SCENE 1 — @OFFICE, day
**Elements:** @C1, @CUP
**Duration:** 24s
**Action:** …
**Dialogue:**
@C1: "…"
```

The import runs once the project exists (step 1), and it does most of step 2 and step 5
automatically. Review the extracted list before adding: check the count, duplicate
characters extracted under two names, props filed as locations, and whether the visual
descriptions survived. Fix the script and re-import rather than patching Elements by hand —
the script stays the source of truth.

**Keep "Include project name in element ID" checked.** Verified ID scheme:
`@<type>_<PROJECTTAG>_<name-slug>_s<N>_v<M>` — so `@P1` in a script titled `IT_MYS_06` comes
back as `@char_ITM_mother-38_s1_v1`. Name the document with the creative code and nothing
else, or that tag is unreadable.

`s<N>` is the first scene the element appears in, read from the per-scene `**Elements:**`
lines — which makes those lines load-bearing, not housekeeping.

The full ID is only knowable after the import, so **prompts must use the real ID copied from
Elements**. A prompt pointing at a tag that does not exist does not fail — it silently
invents the character. Full note in `references/script-format.md`.

## 1. One project in Cinema Studio

Create a separate Cinema Studio project per video (or per series of scenes). Everything
lives inside it: characters and their character sheets, locations, extra props and visual
elements, the prompts written, test generations, and final scene versions.

Prepared characters and locations go into that project's **Assets and Elements** so they
can be reused across scenes without re-uploading or re-creating them.

### Fill the Project Brief

The project carries a **Project Brief** panel — Context, Narrative, Visuals, Production,
Status, Resources, Notes. Fill it before the first generation. Template, section notes and a
worked example are in `references/project-brief.md`.

It is the only place the constants true for *every* scene live: the look and grade, the
camera language, the casting rules, the model and resolution, the project's own Don't list.
Anything that lands there is not retyped into prompts — and a prompt restating the palette or
the camera rules is a sign the brief is not being used.

### Two project constants that live next to the brief

Both are pasted into every prompt word for word, and both exist so that one edit updates every
shot at once:

- **A Style Prefix** — one block covering style, cinematography, lighting, the colour ratio,
  camera, skin, acting, physics, composition, continuity, technical and audio, closed with the
  technical tags (`Photoreal. NON-IP. <aspect>. <duration>s. SFX only. NO CGI. Cinematic.`).
  `SFX only. No music.` is mandatory in it: a generated soundtrack only fights the edit, and
  continuous ambience laid in post is what glues generated shots into one space.
- **A ban dictionary** — words this project has caught the model punishing, with their
  replacements: *dark* → *low key*, *jolting* → *rapid motion*. Add to it whenever a word
  demonstrably drags a generation somewhere unwanted.

Three layers, and a fact belongs to exactly one:

| Where | What it holds |
|---|---|
| Project Brief | true for the whole project |
| Script `.md` | the elements table and what happens per scene |
| Scene prompt | only this scene — blocking, action, dialogue, camera |

(Whether Cinema Studio's backend reads the brief is unconfirmed — that claim comes from a
Google AI Overview, not Higgsfield's documentation. Fill it for the human reason above
regardless.)

## 2. Analyse the script

Writing the script in the import format (step 0) is this analysis, done up front — the
`## ELEMENTS` table and the per-scene `**Elements:**` lines are exactly the list below.
Re-read the whole script anyway before generating, and confirm for each scene:

- which characters appear;
- the location;
- props and extra elements needed;
- the dialogue and rough duration;
- the key action, and the result the shot has to deliver.

### If the piece is voice-over driven, record the voice-over first

Scene durations written from reading a script are guesses, and they are wrong by a lot. On
IT_MYS_06 the scripted 194 seconds came back as a 126-second read — roughly 35% shorter. Had
the clips been generated against the scripted numbers, every one of them would have been cut
to fit or thrown away.

So for a VO piece the order inverts: **voice first, timings measured off it, picture cut to
those numbers.**

1. Generate the whole narration in one continuous pass, not per scene — a continuous read is
   what makes lines flow across cuts, which is the format's whole rhythm.
2. Use a timestamped endpoint (`/v1/text-to-speech/{voice}/with-timestamps` on ElevenLabs)
   and map each scene's text span onto the character alignment. That gives exact in/out
   points measured from the take that will actually be used, not from separate per-scene
   renders, which drift.
3. Rewrite the durations in the script and the brief before generating anything.

Two things that cost time when skipped: Voice Design previews read markedly slower than the
finished voice does at speed 1.0, so do not size scenes from a preview; and audio generated
inside a video clip cannot be replaced, so a VO piece generates its clips silent or ignores
their audio.

## 3. Prepare the characters

Source characters either from the winners database or generate them **inside Cinema
Studio** — characters born in-system are safer (fewer moderation blocks) and behave better
in downstream video generation.

Before any scene, build a **character sheet** for every character. This is the primary
visual reference and it locks: face and features, age and build, hair, clothing and
footwear, accessories, front and back view, and a close-up of the face.

In Cinema Studio this is a two-node graph — a prompt node feeding an image-generation node
that returns the three panels side by side.

### Build the face and the wardrobe in two separate passes

How ONEIRIC builds a character, and the rule we were missing:

1. **The face first, always in close-up** — generated so the model captures identity at maximum
   detail. That close-up is the anchor every other asset of the character is checked against.
2. **Then the looks** — full-figure images with wardrobe, materials and silhouette, matched to
   the locked face.
3. Assemble the sheet around them, **with the original close-up preserved untouched. It never
   runs through a model again.** Anything that changes between states — a scar, a haircut, dirt,
   a wound, a new jacket — is integrated point by point with masks, around the base.

> The base image stays the same pixels, so the identity (and the skin texture that carries it)
> survives every new version of the character.

Re-running a portrait through any model to make a variant is how a character quietly stops
being the same person three scenes later. ADILIADA states the extreme form of the rule: a new
universe is a new look, not a new person — even a character playing his own villain version is
the same face pixels in different wardrobe.

### Sheet construction rules that cost generations when skipped

From the feature brief, all of them the result of a shot failing:

- **Take the head off the full-body panels.** On a wide panel the face is small and soft, and
  that is exactly the face the model copies into a wide shot. Remove it and the close portrait
  becomes the only source of the face.
- **The close portrait is three-quarter**, so the model gets front and side at once.
- **Make two close-ups, smiling and not.** Otherwise the model invents the teeth and the jaw the
  first time the character laughs, and the smile arrives as someone else's mouth. Do this for
  every speaking character.
- **Never write "studio".** It draws an actual photo studio — stands, lights — into the frame,
  and bakes a studio key that then repeats in every video generation. Write `no studio, no
  equipment, no walls`. `Overhead key light` draws the lamp itself.
- **Rim light is banned.** A sheet with a beautiful edge glow drags that light into every scene
  and stops reacting to the real one.
- **Hands stay empty on the sheet.** Every object is its own asset — a prop born inside a sheet
  can never be dropped, thrown or taken away.

### Keep the sheet boring on purpose

The counterpoint to baking the look into the location plate:

> The cinema look does not live in the character sheet — it lives in the locations and in the
> video prompts.

Neutral grey, flat light, real skin with visible pores, no retouch. Bake film grain or a
cinematic lens into a sheet and the character carries that look into every scene and **stops
reacting to new light**. So: the look goes into the plate, never into the person.

When the model returns several versions of a face, **pick the most believable, not the most
beautiful** — a beautiful-but-fake face shows its fakeness later in video, when it is too late.
And check the eyes: even dark ones need a catch-light in the pupil, or the face reads dead and
no video model can act with it.

The reason the base is never re-run, stated properly: every extra pass destroys texture and
drifts colour, and after two passes a face turns symmetrical, plastic and lifeless — which then
shows up as bad acting in video.

### Stress-test the sheet with video, not with your eyes

A sheet that looks perfect proves nothing. Ten generations — different actions, shot sizes and
locations — and the character must be recognisable in ten out of ten. Run them as real prompts:
running, on the phone, crying, laughing, shouting. That is how you find out a face is only
stable while the character is calm.

Two conditions: **test the character and the location together** (the assets pull on each other,
so never test a hero before his location exists) and **test him in a two-shot**, because a hero
who holds up alone often breaks beside someone.

And when it falls apart, suspect the asset, not only the prompt. Fix the words first; if the
same thing breaks again, rebuild the sheet.

### A new state is a new asset, never an overwrite

A character has as many assets as states he goes through — the same man in the kitchen and in a
hospital bed are two assets, not one asset edited. The `_v<M>` suffix exists for exactly this.
Never overwrite a locked reference to make a variant.

### Model choice: AI Cast, not Soul 2.0 — verified 2026-09-01

Both accept a free-text prompt. The difference is what comes back:

| | AI Cast | Soul 2.0 |
|---|---|---|
| Returns | **the three-panel sheet directly** — full-body front, full-body back, close-up portrait, flat grey studio backdrop | a single photograph |
| Also driven by | UI parameters (Genre, Budget in millions, Era, Archetype, Identity, Physical Appearance, Details, Outfit) + Randomize | prompt only |
| Consistency | the sheet is the reference | Soul ID locks a face across generations |
| Observed price | 0.375 for 3 sheets at 2K | 0.25 for one image at 2K |

**Use AI Cast for character sheets.** One call produces exactly what step 3 needs, cheaper
per useful asset, and it reads age honestly — the same prompt in Soul 2.0 came back visibly
younger and more polished than asked for, which is wrong for ordinary-people casting.

Soul 2.0 earns its place later, when a locked face has to appear across many generations
(Soul ID), or when the sheet is being built by hand for full control.

### Attaching Elements to a generation

**Pasting a prompt that contains exact element IDs attaches them automatically.** Paste text
containing `@char_ITM_mother-38_s1_v1` and the UI resolves the tag and pulls that element in
by itself — the References counter fills without touching the picker. This is the fast path,
and it is why tags must be copied verbatim from Elements: one wrong character resolves to
nothing, silently.

**It has to be a real paste.** Typing the same characters keystroke by keystroke does not
trigger the resolver — the identical prompt left `References 0/50` when typed and jumped to
`5/50` when pasted. Automating this means putting the prompt on the system clipboard
(`pbcopy < prompt.txt` on macOS) and sending `cmd+v`, not synthesising keystrokes.

The manual route stays for anything untagged — the **`+` beside `References`** (typing `@`
opens the same picker), with **Uploads / Elements / Generations / Liked** tabs and
Characters / Locations / Props filters.

**Check the References counter before generating, either way.** It should equal the number of
distinct elements named in the prompt; a run at `0/50` invents every character.

**In the CLI none of this applies** — there are no project Elements, so tags bind to nothing.
References go in as `--image-references` file paths and the prompt describes people instead
of tagging them.

**Three layers, and all three are needed.** The tag in the prompt supplies the reference
pixels (or the UI attach, or `--image-references` in the CLI). The `ACTIVE REFERENCES` block near the top of the prompt sets, per element, how
strictly to follow it ("100% matches the reference") and — critically for a location — which
parts of it to use ("use for the bench, hedges, facade and daylight only"); without that
scoping the model also inherits the reference's camera angle and composition and fights the
shot description. The inline tags inside each shot bind an element to what it actually does.
Drop the attach and the model invents everyone; drop the block and the reference overreaches;
drop the inline tags and it knows the cast but not the action.

**Trap in the manual picker:** clicking the middle of an element tile opens a Status menu
(In progress / Needs review / Approved) instead of selecting it, and the picker dismisses.
Prefer the tag route and avoid the picker.

**Audio On or Off depends on the format, and it is not a rule.** The control sits in the
settings row beside the duration.

- **Dialogue spoken on camera** — audio **On**. The model generates the speech and the mouth
  movement together; Kirill's own two-hander example works this way.
- **Voice-over laid on at the edit** — audio can go **Off**, since a per-clip synthesised
  voice is unusable and cannot be stripped later. Leaving it On is also defensible: it costs
  nothing and may return usable room tone. The one risk to watch is that the model sometimes
  invents a line and animates lips to match it, which fights a "mouths stay closed"
  constraint — if lips move in a silent shot, this is the first thing to check.

### UI traps in this form

- **The Generate button is unclickable by coordinate** once the prompt is long: the form
  grows downward and the button lands under the window edge. Click it by element reference,
  which scrolls it into view first. A coordinate click on the clipped button does nothing and
  reports no error — it reads as "the model rejected my prompt" when it is a layout problem.
- **Duration is a slider, not a number field, and `Return` submits the form.** It looks like
  a text box showing `30s`. Typing into it puts the digits in the *prompt* instead, and
  pressing Return to commit fires the generation — twice over, that cost two unwanted
  30-second renders. Drive it as a slider: focus it, `Home` jumps to the 4-second minimum,
  then arrow keys step up. (Clicking the number and typing also works by hand.)
- **Switching the model can wipe or swap the prompt field.** AI Cast → Soul 2.0 cleared it;
  Soul 2.0 → AI Cast kept it; switching to Nano Banana Pro handed back a *different* form
  still holding an older prompt from earlier in the session. There is more than one
  generation form in the page and each keeps its own text. Choose the model first, then
  re-read the field before typing, and read it again before pressing Generate.
- **`cmd+a` selects the whole page unless the field truly has focus.** Click the field by
  element reference — a coordinate click often misses and the select-all then highlights the
  sidebar, so the typed prompt lands nowhere and the old one generates instead.
- **The form can carry another project's state** — a leftover reference image and leftover
  prompt text. Check `References` reads `0/50` before casting an invented face; a stray
  reference overrides the description silently.
- Aspect 9:16 crops the top of the head on a full-body casting frame. State that the whole
  head sits inside the frame, or use the sheet from AI Cast, which frames it correctly.

The prompt is in `references/character-sheet-prompt.md`. Use it verbatim, changing only the
"omitted element" clause. If the character has to be dressed differently from the reference,
narrow the preserve-list to the face and state the new wardrobe explicitly — that note is in
the same file.

## 4. Create the location

Generate the location on its own, with no characters in frame, using the **Cinematic
Locations** model (in the model list under Cinematic models). Generating it empty is what fixes the room design, furniture and
object placement, lighting, colour palette, atmosphere, and the spatial geography that
later shots have to respect.

### Generate the plate in three-quarter, and leave an anchor in it

Two location rules that both feature briefs state independently:

- **Wide or medium in three-quarter view, never frontal.** A frontal picture of a room is flat
  wallpaper — the model cannot read volume from it and invents new surroundings past the frame
  edges every time. Three-quarter gives depth and yields almost a full circle of angles from one
  plate.
- **Leave a visual anchor** — a column, a lamp, a sofa, a crooked chair — and tie all staging to
  it. "The hero at the lamp, facing the door" works; "the hero in the room" is a lottery. This is
  the single cheapest thing that stops characters wandering between takes.

Also: one light logic, one direction of shadows, never two suns. No people and no weapons in the
plate. Against the render look, write real surfaces — rust, cracks, tape, fingerprints, oil
stains, water marks.

**A dialogue location needs a kit, not a plate**: three-quarter, front, reverse, and a background
plate for each character in the scene. Build it from the one plate by generating a video of the
empty room with the camera walking slowly through it — the model draws the other sides
consistently with your plate — then screenshot the angle you need and clean its texture and
light in an image model. A pass-through location needs one angle.

Once the whole set exists, run a **unification pass** over it for colour, light and saturation,
so the plates match in character before any generation. Cheaper than finding the mismatch in the
grade.

### Bake into the location asset anything the video model keeps dropping

Higgsfield's anamorphic problem is our lens problem exactly: ask the video model for an optical
character in the prompt and it drifts from shot to shot. Their fix generalises far past
anamorphic —

> The fix is to move the lens one step earlier in the pipeline: generate the location image with
> the effect already in it. Seedance reads the optics straight off the asset and keeps them —
> **the plate itself becomes the lens.**

So: **a grade, a lens character, a texture, a time of day that the video model will not hold
belongs in the location image, not in the video prompt.** We learned the inverse of this the
hard way, when an evening prompt lost to a daylight kitchen reference — the reference wins, so
put the thing you want inside the reference.

Their optics block, appended to the *location image* prompt and dosed with
subtle / gentle / moderate / strong / maximum:

```
STRONG anamorphic lens character: horizontal squeeze and compression, oval elliptical bokeh,
horizontally stretched highlights, curved barrel edge distortion, chromatic aberration toward
the edges. NO lens flares, NO light streaks, NO floating bokeh circles. 2.39:1.
```

Note where the bans sit: at the **image** stage only. See the rule on negatives at the end.

## 5. Add characters and location to Elements

If the script was imported (step 0), the entries already exist with their names, tags and
descriptions — what they lack is visuals. Attach the generated character sheets and the
location image to them here.

**The attach path:** element card → **Add element image** → click the drop zone → a media
picker opens with three tabs, **Uploads / Generations / Liked**. Project generations live
under **Generations**, newest first, so the earliest characters are a long scroll down.
Click the sheet, then **Save** in the Edit element dialog.

Two things worth knowing:

- **An element holds more than one image** — a `+` appears beside the attached thumbnail. Use
  it for several angles of the same character rather than making duplicate elements.
- **Versions are a field, not a folder.** The Edit element dialog exposes `Version` (a chip,
  `v1`), and the Element ID is composed from Name + first Scene + Version. Folders in the
  Elements panel only group; a prompt addresses the element by ID, so two casting variants
  must differ in `Version` — otherwise both read as `_v1` and a prompt cannot tell them
  apart. Duplicate the element, change `Version` to `v2`, and the ID follows.
- `Scene` in that dialog lists **every** scene the element appears in (mother-38 shows
  1, 5, 9, 13) while the ID carries only the first.

Otherwise add each character sheet and the location to **Elements** by hand, with clear
names and individual tags:

- `@character_1`
- `@character_2`
- `@office_location`

With the project prefix on, these read back with a short tag abbreviated from the document
title. Copy the real IDs from Elements into prompts — never retype the short form from the
script.

From then on, never re-describe appearance, wardrobe or room design in a prompt. Attach the
Elements and reference their tags in the prompt text — the tag binds the instruction to the
reference. The prompt then only describes what *happens*: positions, actions, acting,
dialogue, angles and camera movement.

This is what keeps faces, clothes, architecture and style identical across every generation
in the project.

## 6. Break the scene down in chat

Give the chat the task, the specific scene's script, and the result wanted. Three skills do
the work:

- **CINEDANCE** (`cinedance`) — directs the scene: shot breakdown, shot sizes, positions
  and camera movement, the screen axis/action line, eyelines, character placement, and
  continuity between angles.
- **ACTING SYSTEM** (`acting-skill`) — the performance: objectives, obstacles, tactics,
  emotional beat changes, subtext, physical behaviour, pauses, reactions, eye movement,
  speech manner.
- **`tig-acting-task`** — the same level, from the ONEIRIC pipeline, and the sharper tool for
  writing the block that actually goes in the prompt. It replaces emotion labels with an acting
  task and names the eye-work as action. `acting-skill` is the theory; this is the block format.
- **Lira** (`lira-image-prompts`) — writes and repairs prompts for characters, locations,
  extra elements and first frames.

The output is a detailed scene plan: shot sequence, character actions, dialogue, acting and
camera work.

### Give the eyes a job — never write the emotion

> Write "sad" in a prompt and you get a caricature or a dead face. […] Dead, glassy eyes are
> never fixed with lighting — they're fixed by giving the eyes a job.

The ONEIRIC block form, short:

```
ACTING TASK — [NAME] (invested in his tactic; the work happens in his eyes):
SCENE DIRECTION (shared, unspoken): [one line]
MOTIVE / GOAL / OBSTACLE: [his fuel, his fight, what presses on it]
TACTIC, moment to moment:
— "[dialogue words]" — [verb at the partner + what the eyes check]
(Safety: gaze always engaged in the task; natural blink cadence.)
```

The SCENE DIRECTION line is the director's read from step 0a — the one event all the characters
share. Each character then gets his own motive and physical channel for it.

### Staging: use a blocking map, not words, past two characters

Our own record across three separate scenes (`references/dialogue-prompt.md`) is that a named
screen side never carries — the shoulder edge comes back mirrored, or the backgrounds swap
instead. Higgsfield reached the same conclusion and solved it properly:

> When a shot needs precise multi-character staging — who is where in the frame, in what pose,
> facing which way — words alone stop being enough. […] Win rate on staging-accurate takes goes
> up dramatically.

Use **`tig-blocking-map`**: a schematic colour-coded outline drawing attached alongside the real
references, with a connector block binding each colour to a character tag. Reach for it whenever
a shot has three or more people, or whenever a previous take flipped a position.

Four things that make it work, all counter-intuitive enough to be worth repeating here: the
diagram is a **front view from the camera's side, never a floor plan**; letters live in the
prompt text only and never on the drawing; the connector never names the map's graphic style
even as a ban; and the map is attached **last**, so the photo references win the style vote.
Full method in the skill, background in `references/oneiric-pipeline.md`.

### Open every scene with a master shot, then paste a spatial map into every prompt

The feature brief's answer to positions not holding — and the one we should adopt first, because
it costs almost nothing.

**A master shot**: a wide with fixed blocking, about a second long, no lines and no action. The
model photographs the arrangement — who is where, what lies where, where the light comes from —
and holds it through the following shots. Remove that second and the characters start swapping
places. Two hacks on it: let someone say one short word ("hm") and the model treats the wide as
a proper shot more readily; and if the scene answers a previous one, feed the tail of the
previous clip's line into that first second, so the performance answers the right thing and the
two clips glue at the seam.

**A spatial map** — a compass written once per scene and pasted into every shot of that scene
unchanged. It names the camera side and the line never crossed, puts the landmarks in frame
terms, ties each character to a landmark, and states the exact head count.

The rules that make it work are the ones we got wrong all session:

- **Positions come from what is visible in the plate, not from measurements.** Metres mean
  nothing to the model, and "to the left of the hero" means less than nothing, because it does
  not know where the hero is. Tie every body to something it can see — the lamp, the second chair
  row, the stage edge, the door — and use **frame-left / frame-right** for sides.
- **After every cut, name again who is where and where they look.**
- **Give a static dialogue a corner of the room, not the whole room** — less space, less choice.
- **When a generation contradicts the real location, re-read the reference, not the prompt.**

### Two non-textual controls: the blocking diagram and the depth map

They solve different problems and can be used together:

| Control | Fixes | Use when |
|---|---|---|
| Blocking diagram (`tig-blocking-map`) | who is where in the frame, facing which way | three or more characters, or a previous take flipped a position |
| Depth map — black-and-white, light = near, dark = far | how deep the room is and where bodies sit in that depth | real foreground/background separation to hold, or a space that keeps reshaping between takes |

### Optics: ten anchors, and a native zone

Degrees, never millimetres: **180 · 135 · 107 · 84 · 63 · 47 · 29 · 18 · 12 · 8**. The native
zone is **29–84°** and comes out reliably; outside it the risk starts. Three laws:

- **Content decides the lens.** The model does not obey the number — it infers the lens from
  what is in the frame, which is why fine detail on 135° collapses and a crowd on 8° collapses.
- **One lens per shot, declared**, or it slides to a comfortable middle — write it as a
  per-shot list with FOV changing only on the hard cuts.
- **A long lens needs its whole observation pattern** or it snaps back to normal: the degrees,
  the camera distance in metres, the background compressed to a colour wash, and mandatory
  foreground occlusion filling the lower third to half of frame.

### Never write an age, in any language

> The content filter becomes much stricter the moment it reads a minor; instead of age, give the
> role, the clothes, the action.

We lost generations to exactly this. No ages anywhere in a prompt or a sheet description — a
young character is described by role, wardrobe and behaviour.

### How long a prompt should be

Their feature prompts ran **3,000–4,000 words**, and the constraint is not length:

> Length is not the enemy; an overloaded beat is.

**Up to three sentences per beat.** Overload one and the model smears it. Present tense, short
sentences, camera written inside the action rather than in a paragraph of its own. So a prompt
gets longer by gaining more beats and more blocks — never by packing more into one beat.

### Name the role of every reference

Otherwise the model decides for itself and decides wrong — it copies the composition instead of
the face, or the face instead of the colour palette:

```
@char_… for character reference
@loc_… for location reference — take only the space and the texture: do not use as a starting
frame, do not inherit the composition, the angle or the colour.
```

### Three prompt rules that break generations more than anything else

1. **Every tag appears exactly once, inside ACTIVE REFERENCES.** A duplicated tag at the end of a
   prompt is named as the most common reason a generation refuses to launch.
2. **The location reference carries an explicit ban on inheritance** — it controls geometry,
   materials, light and atmosphere but never framing. Without that line the model hands back a
   near-copy of the plate.
3. **Reference budget per generation: 9 images, 3 videos, 3 audio.** That budget decides how many
   named characters can share a shot — build the shot list around it.

### Speech lives only in the audio block

A dialogue line is built in four parts, always in this order: **the voice and its emotion → the
line in quotes → the physical action → the facial reaction.** And the separation is hard:

> Lines live only in the audio section of the prompt — not one word of speech inside the action.

Because the model adds its own filler — "uhm", chuckles, whole invented phrases — the prompt
carries an explicit block: everyone speaks **only** the quoted line, anyone without a line stays
completely silent, and a half-laugh written into the action is a facial expression **with no
sound**. Write the mix as well — voices clean and close to the microphone, ambience underneath,
ambience dipping when someone speaks — and give rare names a phonetic transcription.

Seam technique: **open every new generation with the line that closed the previous one.** The
emotion crosses the cut along with the text.

### Count everything that can duplicate

SCENE CONTEXT opens with a literal header — `EXACT 3 CHARACTERS — NO DUPLICATES: …` — because the
model adds extra people and clones furniture. Only characters whose references are in the prompt
exist in the frame, and set dressing gets its own count lock: exactly one of a thing, never a
second. Props duplicate in motion, so counts are written frame by frame.

Anything much larger than a human needs **two** anchors at once — a written size comparison *and*
a human figure in frame to measure against. With only one, the model quietly shrinks it back
toward human height.

### Add a GAZE / EYELINES block

ONEIRIC's block order carries eyelines as their own section, before blocking:

```
SCENE CONTEXT · ACTIVE REFERENCES · LOCATION MAP · GAZE / EYELINES ·
FIRST FRAME AND BLOCKING · SEGMENTS (timed beats) · DIALOGUE · AUDIO ·
PHYSICS · LIGHTING · STYLE / FORMAT · POSITIVE LOCKS
```

They also split DIALOGUE from AUDIO, with AUDIO carrying voice identity only, and they repeat
the LENS description **inside every segment** rather than once at the top — because every prompt
is an island.

### CINEDANCE ships three reference files — open them, the head file is not enough

`cinedance/SKILL.md` is the method; the control detail lives in files it tells you to read
and which are easy to skip. Skipping them costs generations.

| File | Open it when |
|---|---|
| `references/optics.md` | any lens choice — which is every scene with a person in it |
| `references/blocking.md` | more than one subject, any multi-shot sequence, any scene with a screen axis |
| `references/physics-lighting.md` | handheld camera, any specific lighting, liquids, weather, weapons, vehicles |

What they add that the head file does not:

- **Lens is a required section, and it is written in degrees.** Diagonal field of view plus
  camera distance plus the visible optical outcome — `47°, camera 3 to 4 metres, natural
  human-eye perspective`. Millimetres, f-stops, ISO and lens brand names are listed as
  anti-patterns: the model reads outcomes, not metadata. Anchors are 8° · 18° · 29° · 47° ·
  84° · 107°, chosen by content type — 47° for documentary-style action, 29° or 18° for
  portraits and tight emotion, 84°–107° for environmental, 8° for distant observation.
- **A multi-shot sequence needs a lens lock**, or the model re-picks a lens per shot and the
  cuts refuse to match: `LENS IS 47° ACROSS ALL SHOTS. NOT NEGOTIABLE.` plus
  `LENS LOCK SHOT n = 47°` on each shot header.
- **Lighting needs the camera's side**, not just the source. Name the primary light, its
  direction, which side of the subject falls into shadow, and what the exposure is set for.
  Without it a described low key drifts to flat front light.
- **Continuity across cuts is a written block**: same cast, geography, screen direction,
  gaze targets, left/right, lighting direction, wardrobe and prop states — plus *action does
  not reset after a cut*, which is what stops a character starting an action over again on
  the other side of a hard cut.
- **Proximity must be measurable.** "near", "beside", "behind him" are called out as weak;
  use "within half a metre of the chair back", "hand on the handle".
- **Cuts are named and effects forbidden**: HARD CUT / SMASH / MATCH / INSERT / REVERSE /
  WHIP only, with no fade, crossfade or dissolve unless asked for.

### What ACTING SYSTEM actually requires

The performance layer is not mood adjectives. Every character in frame needs:

- **An objective as a verb aimed at another person** — "make him explain the paper without
  asking" — never a state like "be worried". Plus the obstacle and what failing costs.
- **Two to four beat changes, each visible in the body**: a pause, a change of posture, a
  tempo shift, a change of gaze. Behaviour unchanged for a whole shot reads as flat.
- **Business** — hands doing a real task, and the *interrupted action* as punctuation: the
  strongest accent in a scene is the moment a character stops what their hands were doing.
- **Eye life, written explicitly.** Dead eyes are the number-one tell of AI acting:
  micro-saccades, gaze targeting, realistic blink rate for the state, live catchlights, and
  eyes reaching the target a beat before the head turns.
- **The listener described too.** Reaction starts before the other person finishes; the
  reaction shot is worth more than the action.
- **States, not transitions** — write the character already mid-action, never the process of
  getting there.

In a silent piece this layer carries more weight, not less: with no dialogue, every beat has
to be physical. Self-check against the skill's own scale and rewrite anything that lands
below 4.

Shared skills folder:
https://drive.google.com/drive/folders/1b3ybyZE4TyX6xoPisdcyYvmLtfmkcBxK?usp=share_link

## 6b. Group scenes into generations by location and cast

Kirill's method is one generation per scene. When several scenes share a room and a cast,
they can go into **one generation as a multi-shot block** and be cut apart afterwards, up to
the single-prompt maximum.

This does not save money — video is billed by the second, so the same total length costs the
same either way. It buys something better: everything shot in that room comes out of one
pass, so the room, the light and the faces are identical across those scenes by construction
rather than by hoping the Elements hold.

**Group by location AND cast, never by position in the timeline.** Slicing the running order
into 30-second chunks puts a location change inside a generation, which is where the model
breaks. On IT_MYS_06 the fourteen scenes regrouped into six generations: kitchen (4 scenes,
one mother present throughout), bedroom (3, one girl), dining (3, one boy), and the living
room left as three separate single shots because each of its scenes has a *different* solo
character — one generation asked to produce three different people in sequence tends to morph
one into another.

Then write an edit-order table mapping each block's shots back to their timeline positions,
with the measured VO in/out points, so the editor never has to work it out.

What it costs: a failure now wastes the whole block rather than one scene. Test the hard
fragment first when the block has several casts or a light change in the middle.

## 7. Review the plan before generating

Read the proposed plan and fix anything that doesn't fit — in chat, before spending a single
generation.

The prompt structure that comes out of this is fixed. Its sections, in order:

`SCENE CONTEXT` · `ACTIVE REFERENCES` · `LOCATION MAP` · `FIRST FRAME AND SPATIAL BLOCKING`
· `FORMAT MODE` · `SHOT n — timecodes` · `PHYSICS` · `LIGHTING` · `AUDIO` ·
`POSITIVE CONSTRAINTS`

A complete worked 24-second two-character dialogue prompt is in
`references/scene-prompt-template.md`.

**For a scene with spoken dialogue, read `references/dialogue-prompt.md` as well.** A
two-hander needs several sections a silent block never does — identity bound to visible
anchors rather than tags alone, a speaker lock repeated inside every shot, a voice lock, a
named physical continuity, and a closing identity lock. It also documents `@LAST_FRAME`
chaining, which is how a conversation longer than the single-prompt maximum keeps continuity
across generations. Copy its skeleton; `@` is always replaced by a
location, character or prop tag.

That file now covers three proven patterns, analysed from Kirill's prompts against the
videos they produced: a **two-hander** shot-reverse-shot; a **one-speaker scene with every
other voice offscreen**, which avoids multi-character lip sync entirely and is the most
reliable way to get dialogue density; and a **three-hander argument across four camera
positions**, including the world-position-versus-screen-position clause that replaces the
action-line rule when a scene genuinely needs reverse angles. It also records the cost:
past three or four distinct camera setups in one generation, the location reference stops
binding and the room drifts.

The scene also gets a **first frame** — a generated still of the opening blocking, which is
what `FIRST FRAME AND SPATIAL BLOCKING` describes. Check the still before generating video:
if screen-left/screen-right is wrong there, it will be wrong in every shot.

## 8. Test before committing to the full scene

If the scene is long or technically hard, generate a shortened trial version first,
containing the most important or most difficult fragment.

There is deliberately **no fixed second-count that makes a scene "long"** — it is a
judgment call in the moment. And pick the test fragment for *difficulty*, not for
importance: testing a static two-shot proves the elements bound and nothing else. The
fragment worth 15 credits is the one with the hard cut, the second character entering, or
the light changing. When the test would only cover the easy part, skip it and treat the
first full pass as the test — at ~2.5 credits per second the difference is small and a full
pass returns diagnostics on every shot at once. A hook can be 3.5 seconds, 15 seconds or the full 30. What
decides it is difficulty: number of characters, number of cuts, how much dialogue has to
lip-sync, whether the camera changes side. A 30-second single-shot monologue may need no
test; a 12-second two-hander with a hard cut usually does.

Check on the test:

- character appearance holding;
- location matching;
- camera positions and movement;
- acting;
- dialogue and pronunciation;
- lip sync;
- eyeline direction;
- overall naturalness.

Describe any errors back to the chat and let it correct the prompt or the scene structure.

### Props

Props do not go to a Soul model. Generate them with **Nano Banana Pro** — verified working:
three-quarter or overhead product shot, one prop per generation, on a plain neutral grey
surface with soft directional light, described by material and wear state.

Two things to state positively every time, because both are project constants that a prop
will otherwise break:

- **Screens are off.** "The screen is switched off and completely dark, a plain black glass
  panel reflecting only soft ambient light with nothing legible on it." A prop laptop or
  phone that renders invented interface content puts unapproved claims into the frame.
- **Nothing is branded.** "Plain unbranded casing, blank surfaces with no text and no logos."
  Naming a brand to exclude it is what puts it in the picture.

### Some constraints do not take — restage instead of repeating

A written rule the model keeps overriding is not fixed by writing it a third time. On
IT_MYS_06 "both bodies face the counter, not each other" was stated in the shot and repeated
in POSITIVE CONSTRAINTS, and both takes still turned the two adults into a conversational
two-shot. Two people side by side facing away is apparently a strong default the language
does not beat.

When that happens, change the staging so the wrong version is physically impossible — put
them at opposite ends of the room, or give one of them a task that cannot be done while
turned around — rather than spending another generation on stronger wording. Two failed
attempts is the signal to restage.

By contrast, constraints the model *does* honour reliably once stated precisely: a prop kept
off a surface ("the point hovering a clear centimetre above the paper and never touching it
at any moment"), screens left dark and unreadable, mouths closed, and action already in
progress after a cut.

## 9. Full generation, then upscale (optional)

After a passing test, restore the full dialogue and full duration and run the final
generation at **480p** — faster, and it avoids burning credits on variants that get
rejected.

### The upscale is optional — that is why it comes last

Nothing downstream depends on it. A 480p scene can go to the edit as it is; the upscale is
a finishing pass run only when the higher-resolution master is actually wanted, and only on
a generation that has already been approved. Never upscale to evaluate a take.

When it is run: **Upscale → ByteDance Upscale**, with these settings.

| Setting | Value |
|---|---|
| Model | ByteDance Upscale |
| Model version | **Pro** |
| Resolution | **1080p** |
| FPS | **30fps** |
| Preset | **Short Series** |

Preset options are Common / AIGC / Short Series / UGC / Old Film — **Short Series** is the
canonical one for this work (confirmed 2026-09-01; it supersedes the older `aigc` preset
used on MES_DRA_05). Resolution goes up to 2K/4K/8K and FPS to 60; leave both alone unless
there is a specific delivery reason, since both cost more and 30fps 1080p is what the edit
expects.

After the upscale, check faces, skin, fine detail, sharpness, and that no new artifacts
appeared.

Approved scenes go to the edit: trim to timing, join, and finish sound and picture there.

## Duration and model limits — *tunable, check before quoting*

These move as the models move. Treat them as current values, not as rules:

| | Current |
|---|---|
| Max prompt length in one scene | **30 seconds** (Higgsfield Cinema Studio 4; Seedance 2.5 / 2.0 shorter) |
| Generation resolution | **480p always**, to save credits |
| Upscale (optional) | ByteDance Upscale — Pro, 1080p, 30fps, preset **Short Series** — after approval only |
| Typical hook length | anywhere from 3.5s to 30s — no standard |

If a scene needs more than the single-prompt maximum, it is more than one generation and
gets split at a cut, not stretched.

## Rules that carry the cost

- Script stress-tested before a single generation — a weak scene generates beautifully and
  still doesn't work.
- Assets first: not one shot until every character, location and prop is named, versioned and
  locked. A new state is a new asset, never an overwrite.
- Script written in the import format, so Elements are extracted and not retyped.
- Voice-over recorded and measured before any picture, on a VO-driven piece.
- Scenes grouped into generations by location and cast, never by timeline position.
- Prompts pasted, never typed — tags only resolve on paste.
- Project constants in the brief, never restated in a prompt.
- Prompt tags copied from Elements, never from the script — the project prefix changes them.
- Location alone before characters — otherwise the room drifts every shot.
- Character sheet before any scene — front, back and close-up, or identity won't hold.
- Describe only action in prompts; identity lives in Elements.
- One camera side of the action line for the whole sequence; characters never swap sides.
- Check the first-frame still before generating video.
- Test the hard fragment before the full length whenever the scene is non-trivial.
- 480p until approved. **Upscale is optional and always last** — never to judge a take.
- Every prompt is an island. "Same as the previous shot" is an instruction to a model that has
  no "before" — positions, wardrobe, props, optics and light are spelled out from scratch, every
  time, including inside each segment of a multi-shot prompt.
- Anything the video model keeps dropping goes into the asset image instead of the prompt.
- Staging past two characters goes in a blocking map, not in words.
- Every scene opens with a one-second master shot; the spatial map is pasted into every prompt of
  that scene unchanged.
- Positions are tied to landmarks visible in the plate, never to metres.
- **Change one thing per iteration**, and log it — version, what changed, verdict. Rewriting a
  prompt in full loses the parts that worked, and without a log you cannot repeat a good shot or
  tell whether you already tried a fix.
- **After fifteen to twenty attempts, change the shot, not the sentence.** Split it in two, drop
  an action, change the angle. This is the same conclusion we reached on the counter staging in
  Block A, and the feature brief states it flatly: every failing shot they saved was saved by
  changing the shot, never by rewording it.
- **Complex action never sits in the middle of the timing** — open the prompt with it already
  underway, and make the approach a separate shot.
- **Write laws, not requests.** A rule becomes a law when it has a name, a visible proof in the
  frame, and a sentence saying what counts as a broken shot — the `= failed take` idiom. Scale is
  set by three things at once (a real measure, a fraction of the frame, a comparison to an object
  already in shot); height by a direction to fail in; object count frame by frame, because props
  duplicate in motion; emotion clamped from both sides, since a one-word tone arrives as
  caricature.
- **One clip, one speaker, one short line**, with a second of silence after it — it gives the
  edit a seam and gives the model nothing to fill with invented sound.
- `SFX only. No music.` in every prompt — continuous ambience laid in post is what glues
  generated shots into one space.
- Cut more aggressively than feels right, and trim the first and last half-second of every clip:
  generations run slow and the edges drift.

### Where a negative is allowed

Higgsfield's iron rule is "say what you want, not what you avoid — the words you write are the
words you summon, including the ones inside a 'no'". Our own results say naming a cheat is
sometimes the only thing that works. Both hold, and the line is what to write down:

| Kind of negative | Verdict |
|---|---|
| A renderable noun — *lens flare, grid, vector, flat illustration, letters, subtitles* | Never write it, not even as a ban. The token summons the thing. Ban it at the image stage only, if at all. |
| A blocking or action cheat — *do not enter from a side door, do not skip his approach, do not replace the hand raise with a glance* | Works, and often nothing else does. It names a behaviour, not an object the model can draw. |

And before strengthening any broken rule, look for the positive requirement that made breaking
it unavoidable — see the "must remain visible" trap in `references/dialogue-prompt.md`.
