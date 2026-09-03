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
