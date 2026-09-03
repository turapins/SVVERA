# Dialogue scenes — what a working two-hander prompt does differently

Analysed from a Kirill prompt and its result: 28 seconds, nine shots, two women of similar
age in one room, shot-reverse-shot with spoken dialogue. Identity held for the full take —
no swapped face, wardrobe, seat, voice or line. That outcome is not luck; it is bought with
techniques a silent b-roll prompt never needs.

## 1. Bind identity to visual anchors, not just to tags

A tag is invisible to a viewer and weakly held by the model. Give each character an anchor
the model can *see* and repeat it everywhere: a garment, a piece of furniture, a side of
frame.

```
The woman in the blue shirt is always @char_friend_1.
The woman on the olive-green sofa is always @char_mom_1_home.
@char_friend_1 always wears the same clearly visible blue shirt.
@char_friend_1 always sits in the caramel-brown leather armchair on screen-right.
```

Three redundant handles per person — clothing, seat, screen side — so a drift in one is
caught by the other two. Wardrobe colours are chosen to be maximally unlike each other.

## 2. Say it in a CAST MAP before the references, and again at the end

The prompt opens with an `IMMUTABLE CAST MAP` and closes with a `FINAL IDENTITY LOCK` that
restates the same bindings, plus the explicit negative:

```
Faces, hairstyles, wardrobes, seats, voices, screen positions and dialogue roles
never exchange between the women.
The blue shirt always belongs to @char_friend_1 and never appears on @char_mom_1_home.
@char_mom_1_home never speaks @char_friend_1's lines.
```

This is deliberate over-specification. For a two-hander the identity swap is *the* dominant
failure, so the binding is stated four or five times in different sections rather than once.

## 3. A SPEAKER LOCK inside every shot, not once globally

Each of the nine shots carries its own lock, in the same words:

```
SPEAKER LOCK: only @char_friend_1 in the blue shirt speaks. Only @char_friend_1's lips move.
@char_mom_1_home's lips remain fully closed.
```

Plus a standing rule earlier that the listener "reacts naturally with eyes and posture but
never mouths, repeats or lip-syncs the speaker's words" — which is the specific failure being
blocked: models like to animate both mouths.

## 4. Lock the voices as well as the faces

```
@char_mom_1_home's voice: warm, grounded female mezzo, neutral American accent, calm
conversational delivery.
@char_friend_1's voice: brighter and slightly more energetic, playful at first and more
concerned later.
The voices never exchange between characters.
```

Two same-gender characters can swap voices across a cut even when the faces hold.

## 5. PHYSICAL CONTINUITY as its own section

Not general "keep continuity" but specific checkable body facts that survive every cut:

```
@char_mom_1_home's folded leg remains beneath her on the sofa. Her other foot remains on
the rug. Neither woman changes seats, switches leg positions or exchanges wardrobe.
Preserve realistic cushion compression and grounded body weight.
```

A named posture is far more enforceable than "same position".

## 6. Compose the last shot as the handoff to the next generation

```
Keep the composition stable. This exact final frame will be attached as @LAST_FRAME for
the next generation.
```

This is how a piece longer than the single-prompt maximum gets built with continuity: the
closing frame is designed to be the opening reference of the following block. It is an
alternative to grouping scenes by location — use chaining when the story must run
continuously through one conversation, and grouping when scattered scenes share a room.

## Other things worth copying

- **Shot timings to a tenth of a second**, including very short shots — a 0.8-second cut for
  a two-word question. Nine shots in 28 seconds is far denser than a b-roll block and the
  model handled it.
- **Lighting assigned per character**: daylight from the left window shapes one woman, the
  floor lamp shapes the other. It reinforces the identity separation optically.
- **Reactions start before the other person finishes** — written into the shots, not just the
  performance section.
- **47° stated inline** in the two-shots.

## What the model changed anyway

Shot B specified the friend "fully offscreen"; the result put her shoulder in frame as an
over-the-shoulder. Harmless here — arguably better coverage — but a reminder that "outside
the frame" is a weaker instruction than a positive description of what the frame contains.

---

# Variant B — one speaker on camera, the rest offscreen

Second Kirill pair: 28 seconds, four shots, a woman answering audience questions on an
auditorium stage. Two questioners are heard but never seen.

**The structural trick: keep every other speaker out of frame.** Multi-character lip sync is
the hardest thing to hold across cuts, and this prompt sidesteps it entirely — only one pair
of lips exists in the world of the shot. Reach for it whenever the scene can plausibly hide
the other voices: a phone call, a doorway, an audience, a car passenger, an off-camera
interviewer. It buys the density of a dialogue scene at the reliability of a monologue.

What the offscreen voices need in return:

```
VOICE A comes from screen-left, roughly four rows back.
VOICE B comes from screen-right, closer to the stage.
Her eyes reach each offscreen speaker before her head turns.
```

A screen direction per voice, and the eye-leads-the-head beat from the acting system so the
turn reads as listening rather than blocking. Without the direction the model points her at
the lens.

## Pacing stated as a number

```
Approximately 160-165 words per minute.
Questions follow answers immediately. No dead air.
Use the entire 28-second duration.
The complete scripted dialogue must be spoken without omissions or paraphrasing.
```

Four separate locks on the same failure: the model finishing the lines early and holding on a
static face, or trimming a sentence to fit. "Use the entire duration" and the no-paraphrase
line are the two that carry the most weight — say both.

## Deliberate mixed lenses, unlike the b-roll rule

The kitchen block locks one 47° across all four shots. This one does the opposite on purpose:
47° for the establishing wide from the aisle, 29° short telephoto for the portraits, hard cuts
between. The rule is not "always lock the lens" — it is *decide* the lens per shot and state
it, so the model never picks. Lock it when the shots are meant to feel like one continuous
observation; vary it when the cut is meant to feel like coverage.

## Directing a crowd without animating a crowd

```
The audience never reacts in unison.
The audience sits one stop darker than the stage.
Blurred foreground shoulders and heads frame the lower edge.
```

Underexposed, defocused, staggered — three ways of saying *do not try to act*. Extras are
treated as a lighting and depth layer, not as performers. Same logic as the offscreen voices:
remove the thing the model is bad at rather than instructing it harder.

## FINAL FRAME as a written section

The stage prompt closes with a `FINAL FRAME` block specifying exactly where her eyes are,
that her lips are closed and that the mic is back at chest height — composed so the next
generation can attach it. Same technique as §6 above, but note it is a *section with content*,
not a one-line note: describe the frame you want to inherit.

---

# Variant C — three characters, four camera positions, one escalating argument

Third pair: 18 seconds, a girl's bedroom, both parents arguing over her homework until she
shouts and leaves. Three speaking characters, seven lines, four camera setups. It came back
almost exactly as written, including the closing frame — the empty chair, the dropped pencil,
the daughter visible mid-exit through the doorway between the two parents.

## Separate world position from screen position

The single most useful idea in the prompt:

```
Their physical world positions never change: Mom always remains on the bed side of the
chair and Dad always remains on the opposite side. Their apparent screen positions may
reverse only because the camera deliberately moves to the opposite side of the room
after a HARD CUT.
```

CINEDANCE's action-line rule says keep every camera on one side. That is right for continuous
observation and wrong for shot-reverse-shot, where crossing is the whole point. This clause
replaces the line rule with something stronger: the *people* are pinned in the room, the
camera is free, and any left/right change is declared in advance as a consequence of the move.
Use this wording whenever a scene needs true reverse angles.

## Name the angle and then deny the thing it usually collapses into

```
This is a genuine over-the-shoulder angle, not a frontal three-person composition.
Camera is now physically positioned on Mom's side of the desk, just behind her right
shoulder... Mom's shoulder and hair form a soft foreground edge.
```

"Over-the-shoulder" alone reliably degrades into a slightly-offset frontal. Saying where the
camera physically stands, what forms the foreground edge, and what it is *not* held both
reverse angles cleanly. The prompt also opens with a global version — "four clearly different
camera positions from different sides of the room. No repeated frontal coverage with only
changes in shot size" — which is the failure mode named exactly.

## Escalation written as a physical ladder, not as emotion

```
Shot 1: both parents still address the notebook.
Shot 2: Dad begins addressing Mom rather than the problem.
Shot 3: both parents are fully turned toward each other, voices raised.
Shot 4: Daughter's shout breaks the argument and instantly removes its energy.
```

Four lines, each a body orientation. The emotional arc is never described directly — it is
entirely encoded in where people are pointed. This is the acting system's "objective, not
state" rule applied at sequence level, and it is what makes a rising argument readable in
18 seconds.

## The silent character needs more writing than the loud ones

The daughter has one line and most of the direction: writes, erases, restarts, traces a line,
stops, checks both faces, knee moves, knuckles tense, breathing shortens, then the shout. Plus
`Her frustration accumulates without resetting across cuts.` A character who is being talked
over is the one the model will freeze; give them continuous business and an explicit
no-reset clause.

## Overlap given a number

```
The parents' replies follow one another with gaps shorter than 0.2 seconds. Reactions begin
before the previous speaker finishes. Key words remain clean and intelligible.
Only Daughter's final line is a full shout.
```

The last line matters as much as the first three — without a stated ceiling every raised voice
converges on the same volume and the climax lands flat.

## Plant the exit before it is needed

`The open bedroom doorway remains clearly visible for Daughter's final exit` sits in the
LOCATION MAP at the top, not in shot 4. Anything a late shot depends on — a door, a window, a
second chair, a prop to pick up — goes into the location map, or the model builds a room
without it and improvises when it is called for.

## What drifted

The bedroom did not survive four camera positions. Shot 1 reads as a child's desk in a
bedroom; by shots 3 and 4 the desk has become a dining table with dining chairs, a wall shelf
and a different window, despite a location reference and an explicit "preserve the exact
bedroom geography". The performance, blocking, dialogue and continuity of props all held —
the *room* is what the model spent to buy four genuinely different angles.

Practical reading: the more distinct camera positions a single generation asks for, the less
the location reference binds. If the room itself has to be recognisable — a product shot, a
returning set across blocks — use fewer setups, or cut the scene into separate generations per
angle and hold the room with `@LAST_FRAME`.
