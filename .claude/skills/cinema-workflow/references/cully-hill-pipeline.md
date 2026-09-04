# Feature-scale pipeline — THE CULLY HILL BOYS

Source: the project brief for *The Cully Hill Boys*, published by Higgsfield Studio at
`higgsfield.ai/original-series/cully-hill-boys/full-film`. A 1h54m generated feature — 137
scenes, 473,214 generations, 600 approved assets on the canvas (74 lead cards, 52 supporting,
90 episodic, 159 props, 200+ location plates). Premiered New York, 5 August 2026.

Read this one *after* `oneiric-pipeline.md`. ONEIRIC is the short and the origin of the TIG
skills; this is the same studio at feature scale, and it is far more operational. Where the two
disagree, this one is later and more specific.

Everything below is what changes our practice. Their own closing line for the whole document:
every rule in it exists because a shot failed without it.

---

## Two Claude chats, not one

Image prompts and video prompts are written in **separate chats**, because the rules of one job
poison the other: the image chat wants flat light and anti-CG wording, the video chat wants
field of view in degrees and motivated light. Keeping them in one context bleeds studio-lighting
language into video prompts and camera language into sheets.

## Character sheets — the detail ONEIRIC left out

Three panels in one image: full body front, full body back, and a large close portrait, with the
prompt stating outright that it is the same person across all panels.

- **The portrait is three-quarter**, not frontal — it gives the model the face from two angles at
  once.
- **Take the head off the full-body figures.** On the wide panels the face is small and soft, and
  that is precisely the face the model copies into a wide shot. Remove it and the close portrait
  becomes the only source of the face. It holds far better.
- **Two close-ups, smiling and not.** Otherwise the model invents the teeth and the jaw the first
  time the character laughs, and the smile arrives as somebody else's mouth. Worth doing for
  every speaking character.
- Background solid neutral grey; light soft, no hard shadows, no blown highlights.
- **Never write "studio".** The model may draw an actual photo studio — stands, lights — inside
  the frame, and it can bake a studio key light that then repeats in every video generation.
  Write `no studio, no equipment, no walls` instead. `Overhead key light` draws the lamp itself.
- **Rim light is banned.** A sheet with a beautiful edge glow drags that light into every scene
  and stops reacting to the real one.
- **Hands stay empty.** Every object is its own asset, because a prop born inside a sheet can
  never be dropped, thrown or taken away.

## The stress test is a video test

A sheet that looks perfect proves nothing. Ten generations — different actions, different shot
sizes, different locations — and the character must be recognisable in ten out of ten. Run them
as real prompts: running, talking on the phone, crying, laughing, shouting. That is how you find
out a face is only stable while the hero is calm.

- **Test the character and the location together.** The two assets pull on each other, so a
  character tested against nothing tells you nothing. Never test a hero before his location
  exists, and test him in a two-shot as well — a hero who holds up alone often breaks beside
  someone.
- **When it falls apart, suspect the asset, not only the prompt.** Slop, or a hero who dissolves
  halfway through a shot, is as often a weak sheet or plate as a weak description. Fix the words
  first; if the same thing breaks again, rebuild the asset.

## Locations

- Generate as a **wide or medium in three-quarter view, never frontal.** A frontal picture of a
  room is flat wallpaper — the model cannot read volume from it and invents new surroundings
  past the frame edges every time. Three-quarter gives depth and yields almost a full circle of
  angles from one plate.
- **Leave an anchor in every location** — a column, a lamp, a sofa, a crooked chair — and tie the
  staging to it. "The hero at the lamp, facing the door" works; "the hero in the room" is a
  lottery.
- One light logic: one source, one direction of shadows, never two suns. No people and no
  weapons in the plate.
- Against the render look, use the language of real surfaces: rust, cracks, tape, fingerprints,
  oil stains, water marks.
- **Build a location kit out of one plate by generating a video of the empty room** with the
  camera slowly walking through it. The model draws the other sides of the room consistently
  with your plate; screenshot the angle you need and clean up its texture and light in an image
  model. A dialogue location needs the kit — three-quarter, front, reverse, and a background
  plate per hero in the scene. A pass-through location needs one angle.

## The era is a rule, not decoration

Their film is 2011, and nothing in frame is newer. Left alone the model drags every shot toward
today, so the year goes into every location plate *and* is repeated in every prompt. One extra
holding a phone and the shot is gone. Any period or setting constraint has to be enforced in
both places — the asset and the text.

## The shotlist card

The script is turned into a preliminary shotlist that already carries the director's script
inside it. Every shot is a card in four groups:

- **Material** — location and INT/EXT with the asset covering it; time of day (an asset variant
  choice); everyone in frame with tags and state variants; props and vehicles with tags; the
  action in one to three sentences; the lines verbatim; running time in seconds; complexity
  simple / medium / complex.
- **Direction** — the goal of the shot in one line; the task as a verb (interrogate, expose,
  shame); the dramaturgy, i.e. what changed between start and end; the blocking relative to
  camera; the acting, and what the character hides.
- **Camera** — shot size, movement, lens, angle.
- **Edit** — cut type, pace, how this shot hooks into the next.

The card carries the scene number plus a letter for the shot — 50B, 50C — and that identifier
stays on the card, in the version log and on the prompt file. From the card the prompt is
written almost mechanically, and the holes show up *before* a generation is spent: a shot with
no goal, a character with no task, a scene with no asset.

## The fifteen-block prompt skeleton

```
SCENE CONTEXT · ACTIVE REFERENCES · LOCATION MAP · FIRST FRAME AND SPATIAL BLOCKING ·
FORMAT MODE · OPTICS · CAMERA · ACTION TIMING · PHYSICS · LIGHTING · AUDIO ·
CHARACTER ACTING · STYLE · QUALITY · POSITIVE CONSTRAINTS
```

Three hard operational rules attached to it:

1. **No negative block.** A prohibition is written as the desired outcome inside the relevant
   section, because "does NOT fall on his back" reads as an invitation to think about falling on
   his back. Write "falls on his stomach".
2. **Every tag appears exactly once, inside ACTIVE REFERENCES.** A duplicated tag at the end of a
   prompt is named as *the most common reason a generation refuses to launch*.
3. **The location reference carries an explicit ban on inheritance** — it controls geometry,
   materials, light and atmosphere but never framing. Without that line the model hands back a
   near-copy of the plate. (Our own kitchen block hit exactly this.)

**Reference budget per generation: 9 images, 3 videos, 3 audio.** That budget is what decides
how many named heroes can share a shot — plan the shot list around it, not the other way round.

## Optics — ten anchors and a native zone

Degrees, never millimetres, off a ladder: **180 · 135 · 107 · 84 · 63 · 47 · 29 · 18 · 12 · 8**.
The native zone is **29–84°** and comes out reliably; outside it the risk starts. (Our
`cinedance/references/optics.md` carries six of these — 180, 135, 63 and 12 are additions.)

- **Content decides the lens.** The model does not obey the number; it infers the lens from what
  is in the frame. That is why fine detail on 135° collapses and a crowd on 8° collapses.
- **One lens per shot, declared**, or it slides to a comfortable middle — written as e.g.
  `84°/47°/47°/29°/47°, FOV changes only on the hard cuts`.
- **A long lens needs its whole observation pattern** or it snaps back to normal: the degrees,
  the camera distance in metres, the background compressed to a colour wash, and mandatory
  foreground occlusion — blurred foreground shapes occupying the lower third to nearly half of
  frame.

## Geography: the master shot and the spatial map

This is their answer to the failure we recorded three times over — positions and screen sides
not holding.

**Every scene opens with a master shot**: a wide with fixed blocking, about a second long, no
lines and no action. The model photographs the arrangement — who is where, what lies where,
where the light comes from — and holds it through the following shots of the scene. Remove that
second and the heroes start swapping places.

Two hacks on it: let someone say one short word ("hm") in it and the model treats the wide as a
proper shot more readily; and if the scene answers the previous one, feed the tail of the
previous clip's line into that first second, so the actor answers the right thing in the right
tone and the two clips glue at the seam.

**Under the master sits the spatial map** — a compass written once per scene and pasted into
every shot of that scene unchanged. Its shape:

- which wall the camera side is, and the explicit statement that the 180° line is never crossed;
- where the major landmarks sit in frame terms (deep frame-right, beside the stage, filling the
  middle);
- each character tied to a visible landmark, not to a distance;
- the exact head count, and that nobody else is present.

The rules that make it work:

- **Positions come from what is visible in the plate, not from measurements.** Metres mean
  nothing to the model, and "to the left of the hero" means less than nothing, because it does
  not know where the hero is. Tie every body to a landmark it can see — the lamp, the second
  chair row, the stage edge, the door — and use **frame-left / frame-right** for sides.
- Name the camera side and the line it never crosses. That one sentence keeps every cut on one
  axis.
- **After every cut, name again who is where and where they look.**
- **Give a static dialogue a corner of the room rather than the whole room** — less space, less
  choice.
- **When a generation contradicts the real location, re-read the reference, not the prompt.**
  They lost several versions of a football scene attacking the wrong end of the pitch because it
  was written from memory.

## Acting: physics, inner line, and micro-events

- **Physics, not adjectives.** On "sad", "angry", "shocked" the model improvises and goes
  shallow. Describe the muscle work: a tremble, a jaw clenched and flexing, cheekbones drawn
  tight, a light exhale through the nose.
- **An INNER LINE** — one line of inner monologue, explicitly marked as unspoken and never
  subtitled. The model builds micro-expressions from the goal, and the face starts living between
  the lines. In their two-hander example the words *nostalgic*, *jealous* and *sad* appear
  nowhere in the prompt.
- **Phased blinking**, written out: one lazy blink → a quick double-blink → one hard reset-blink.
- Always write the gaze direction.
- **Against frozen faces in a static shot: one visible micro-event every one or two seconds.**
  Stillness is written as held tension — "nobody moves" freezes the frame itself.
- **Never mirrored.** Two characters reacting to the same thing get different rhythms and
  different intonations, stated as such.
- Three signs of a living shot: the reaction starts before the other line ends; emotion does not
  switch off instantly, and that tail carries into the next clip and stitches the cuts; the hands
  stay busy, and the strongest accent in a scene is the moment that work stops because of what
  he just heard.

## Voice and accent

Voice is not an asset — it is a written block decided before the dialogues: register, timbre,
tempo, accent, manner. Pasted verbatim every time, never a synonym changed, because changing the
wording widens what the model samples from and the voice drifts.

The **accent is part of the block, named as a category plus one or two phonetic markers** —
dropped h, glottal t, -ing to -in' — rather than as a label. Where it matters the markers are
spelled out inside the line itself.

**One clip holds one speaker and one short line.** Longer exchanges are written as separate
clips, with the answer in the next one.

Each character also carries a **written manner** — one paragraph, about the character rather than
the actor: how he stands, how he talks, what his face does when he loses. Fixed before the first
shot, pasted into every prompt. Written once, it stops the character becoming a different person
in the next shot.

## Colour, as a bible written before the first shot

The film is split into worlds, each with one register, and every plate was built to it. Inside a
world: **80–85% base field, 10–15% one or two accents, about 5% counter-note.**

- **The accent is not graded in — it is found as an object with a real source in frame**: a green
  door, a sodium lamp, an orange tent, the glow of a monitor.
- **One hue is separated by finish and age rather than shade.** Two rich interiors both in red
  and gold stop looking like one set when one is patina (dried oxblood, tarnished gold, a single
  aged lamp) and the other is polish (saturated crimson, mirror-bright brass, many identical
  lamps in symmetry).

## Laws instead of requests

> A rule becomes a law when it has a name, a visible proof in the frame and a sentence stating
> what counts as a broken shot.

Their prompt library carries about **150 named locks**, and roughly **eighty sentences end in
"= failed take"**. That idiom is the portable part. Four they used constantly:

- **Scale is set by three things at once** — a real-world measure, a fraction of the frame, and a
  comparison to an object already in the shot.
- **Height is set by a direction to fail in**: "NOT taller by a single centimetre; if in doubt,
  render him a touch shorter."
- **Object count is written frame by frame**, because the model duplicates props in motion — a
  sandwich knocked out of a hand becomes two.
- **Emotion is clamped from both sides**, because a tone written as one word arrives as
  caricature: between joy and aggression, with a rage-twisted face, a soft beaming smile *and*
  deadpan each named as a failed take.

## Fixes that saved generations

- **After fifteen to twenty attempts, look for another solution — not a better sentence.** Split
  the shot in two, drop an action, change the angle, get the physics another way. Their line:
  every failing shot they saved was saved by changing the shot, never by rewording it. This
  independently confirms what we found on the counter staging in Block A.
- **Complex action never sits in the middle of the timing.** A door would not break — the hero
  shuffled beside it and froze. The fix is to open the prompt with the action already underway
  ("he is ALREADY mid-swing, the door ALREADY cracking") and make the approach a separate shot.
- **Crowds**: one asset with a range of heights and clothes, plus one or two lead extras with
  their own assets for close-ups. Over fifteen people a crowd collapses into three to five
  figures, so a packed room is written as bodies pressed against the stage edge with arms in the
  foreground — never as a number.
- **A car interior is its own asset**, separate from the car and from the location, and one of
  the most reusable things they built.
- **If the model keeps drawing what you never asked for, ban it by name.** Their railway plate
  insisted on arriving as a station — platforms, canopies, floodlights, a standing train — and a
  lock listing all of it as absent, plus an exact track count, cured it. Note this is a real
  exception to "never write a negative": it applies to a persistent hallucinated *object*, after
  positive description has already failed.

## Production discipline

- Work in scene blocks, in film order, each block its own shotlist file.
- Descriptors and the fixed look-and-camera block of each world live as **constants**, so one
  edit updates every shot at once.
- **Change one thing per iteration**, everything into a version log — version, what changed,
  verdict. Without it you cannot repeat a good shot and cannot tell whether you already tried a
  fix. Rewriting a prompt in full loses the parts that worked.
- **The edit runs in parallel with generation.** The editor assembles scenes as they arrive and
  orders what is missing — "need a cutaway to the hands", "need a wider one". A re-shoot costs
  minutes, so the edit shapes production instead of waiting for it.
- **Generations almost always feel slow.** Cut more aggressively than feels right, and plan to
  trim the first and last half-second of every clip, because the edges drift.
- **A second of silence after every line**, inside the clip: it gives the editor a seam and gives
  the model nothing to fill with invented sound.

## Post

- After picture lock, a separate **polish pass** — text on a sign, a number plate, a small
  artifact that only shows on a big screen — retouched frame by frame. A properly broken shot is
  regenerated instead, from the saved final prompt with one line changed, which only works
  because the prompt library is complete and versioned. First priority: close-ups of faces and
  hands. All of it before colour.
- **Generation supervising is its own job**, not a hope: someone watches the assembled cut for
  shots that technically exist but do not work — a look that lands a beat late, a hand that reads
  wrong, a face that drifts on the third second — and sends them back with a named fix. Slop
  found in the assembly costs one prompt; slop that reaches the screen costs reputation.
- Colour starts with **unification** — every generation arrives with its own built-in grade — and
  the look itself was baked into the location assets in pre-production, so the colourist refines
  rather than invents.
- Voices were **cleaned straight from the generations**, not re-recorded: noise removal, evening
  the timbre between clips, placing the voice in the space.
- **Continuous ambience is what glues generated shots into one space** even where the picture
  drifts — which is why `SFX only. No music.` is mandatory in every prompt.

## Music and lip-sync — an entirely separate pipeline

A video model will not perform your song; asked to rap it moves a mouth to nothing. So the music
never comes from the model — the track is made first, and the model is made to perform it.

1. The track is **finished** — full verse, real vocal, final mix. The mouth locks to a specific
   waveform, so a demo you plan to replace will not do.
2. Cut into blocks of about **twelve seconds**, with the cuts falling on the vocal's breaths and
   never mid-word.
3. Each block becomes a **video file with a black picture** — the video track is a placeholder,
   the audio track is the block of the song. That file is attached to the generation.
4. **The generation's own audio is switched off in the settings.** The vocal still drives the
   lip-sync, because the mouth is built from the waveform, but the clip comes back silent — so
   the copyright check has nothing to catch and cannot block the take. The track is laid back
   under the silent picture in the edit, where it belongs anyway.
5. Blocks are generated one at a time and butted together in the edit; the seams fall on the
   breaths.

Two prompt add-ons carry it:

- **The file is the song and he is singing it** — stated plainly, with no explanation of the
  workflow. Meta wording about placeholders and pipelines confuses the model. The attached file's
  audio *is* the live performance; its picture is black filler and the image never comes from it.
- **The lyrics of the block, plus the truth rule**: written-out words help the mouth shapes,
  because the model reads the phonetics and pre-shapes the vowels — but text and audio will not
  match at the edges, so the prompt says explicitly that if the block starts or ends mid-line the
  mouth follows the *file*, not the text.

Plus two locks: a hard **lip-sync lock** (every syllable shaped exactly as it sounds, no lag, no
drift, no idle mouth — missing the timing of a bar is a failed take) and a **mouth ownership
lock** (every audible word belongs to the performer; the other mouths stay alive with laughter
and shouts but never mouth the lyric).

## The five rules they close on

1. **Assets first.** Not one shot until every character, location and prop is locked, named,
   versioned and stress-tested. This rule saves more money than everything else combined.
2. **Describe everything, every time.** The model has no memory; the descriptor goes into every
   prompt word for word and is never shortened.
3. **Change one thing at a time.** One line per iteration, everything into the log.
4. **Give the model less freedom.** A corner instead of a room, a landmark instead of open space,
   a map instead of guesswork, one lens per shot, one action per beat. Laws with visible proof
   instead of requests.
5. **If it will not come together, simplify the shot, not the wording.**
