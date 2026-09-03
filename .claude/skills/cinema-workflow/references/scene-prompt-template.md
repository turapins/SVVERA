# Scene prompt template — worked example

A real 24-second, two-character, two-shot dialogue prompt (Vocal Image, outdoor bench).
Copy the section order and the level of specificity; replace the content.
`@` is always a tag of an Element — a character, a location or a prop.

**Use the real element ID from Elements, not the short tag from the script.** With the
project prefix on, `@C1` in the script is `@vi_raise_01_C1` in the project. A prompt
pointing at a tag that does not exist does not error — the character is silently invented.
See `script-format.md`.

The scene ships with a **first-frame still** generated before the video — the opening
blocking, exactly as `FIRST FRAME AND SPATIAL BLOCKING` describes it. Check that still
first: if screen-left/screen-right or the eyelines are wrong there, they are wrong in every
shot that follows.

Note on this example: the still that shipped with it shows two men on the bench while the
prompt text below says "her". Pronouns follow the actual cast — match them to the Elements
attached, not to the template.

## Section order (fixed)

1. `SCENE CONTEXT` — one paragraph: who, where, emotional state, what the scene does.
2. `ACTIVE REFERENCES` — one line per tag, plus what to take from it. State "100% matches
   the reference" for characters; for a location, name exactly which parts to use.
3. `LOCATION MAP` — where bodies are in the space relative to each other and the set.
4. `FIRST FRAME AND SPATIAL BLOCKING` — the first visible frame, screen-left/screen-right
   assignment, and the action line. No empty establishing frame.
5. `FORMAT MODE` — total duration, aspect ratio, camera character, cut points with timecodes.
6. `SHOT n — 0:00–13:00 (SHOT SIZE)` — one block per shot: camera, then blocking, action,
   acting beats and dialogue inline in delivery order.
7. `PHYSICS` — weight, handheld quality, fabric and hair, held objects.
8. `LIGHTING` — must match the location Element.
9. `AUDIO` — who speaks when, listener behaviour, ambience, no music, no subtitles.
10. `POSITIVE CONSTRAINTS` — everything stated as what IS true, never as "do not".

---

SCENE CONTEXT
Two colleagues sit together on a bench in an outdoor square within an office district, mid-conversation. C1 is visibly frustrated, venting about her struggles speaking up in meetings. C2 listens, gives an honest diagnosis, then a warm, confident recommendation.

ACTIVE REFERENCES
@C1: 100% matches the reference. Frustrated, self-critical energy.
@C2: 100% matches the reference. Calm, warm, supportive energy.
@LOCATION: the outdoor bench in the office-district courtyard. Use for the wooden bench, hedges, building facade and daylight only.

LOCATION MAP
Both sit together on the wooden slatted bench within @LOCATION, close to each other, bodies angled slightly inward to face one another. Green hedges and the glass-and-concrete building facade remain behind them.

FIRST FRAME AND SPATIAL BLOCKING
The first visible frame already contains both characters in position: @C1 on screen-left, @C2 on screen-right, both seated on the bench, angled inward toward each other. No empty establishing frame. The action line runs between them; every camera stays on the same side of it for the whole sequence.

FORMAT MODE
Controlled multi-shot sequence, calm and steady natural handheld camera throughout — no push-in, no zoom, no dramatic tightening between shots. 24 seconds total. Vertical 9:16. One hard cut at 13.0 seconds, during the pause before C1's last question.

SHOT 1 — 0:00–13:00 (WIDE TWO-SHOT)
Camera sits at roughly seated eye height, holding both faces clearly in frame for the whole shot — steady, calm handheld presence only, no push, no drift closer. @C1 on screen-left, @C2 on screen-right, both seated on the bench, angled toward each other, feet on the ground. Green hedges and the building facade fill the background.

@C1 leans forward slightly, fingers tightening around a paper coffee cup held in her lap, eyes dropping before she looks up at @C2. She says: "Why am I so awkward in meetings? Why can't I just say what I mean?" Her voice is tight, self-critical. @C2 listens with steady, warm eye contact, then replies, gently but plainly: "You literally lose your words mid-sentence." No hedging in her delivery — honest, not harsh. @C1's hand stills on the coffee cup mid-sentence — the fidget stops the moment the truth lands — and she asks, brow furrowing, leaning in slightly: "What do you mean?" Genuinely searching, not defensive. @C2 explains further, delivered evenly, without judgment: "You start your sentence and then just go blank. It kills your authority." @C1 listens, her gaze drifting down and away partway through the line — the words land somewhere private.

SHOT 2 — 13:00–24:00 (WIDE TWO-SHOT, SAME DISTANCE, CALM ANGLE CHANGE)
Hard cut to a different camera position at roughly the same distance and framing as Shot 1 — a calm angle change, not a push closer. Both faces remain clearly visible throughout. Camera stays steady, natural handheld presence only, no zoom, no dolly-in.

@C1's shoulders lower, a small deflated exhale before she asks, quieter than her earlier lines: "So what do I do?" She's stopped defending herself and started actually asking. @C2 sits up a fraction straighter, energy warming into genuine enthusiasm, and says: "Vocal Image. Just nine minutes of communication training a day. I've been promoted twice since I started using it." The line about her promotions carries quiet pride, not a sales pitch tone. @C1 listens, something shifting in her face from defeat toward curiosity — her posture opens slightly, a small hopeful expression breaking through. @C2 gives a small, confident nod. Neither speaks for the final beat. Natural handheld stillness holds on both of them as the scene closes.

PHYSICS
Natural handheld quality throughout: operator breath, subtle micro-settling, no digital jitter, no gimbal-smooth glide. @C1's coffee cup and hand carry real weight — grip tightens and releases naturally, never floating. Natural fabric and hair movement as both characters shift weight on the bench, and in any light outdoor breeze.

LIGHTING
Soft, even natural daylight matching @LOCATION, slightly overcast, gentle diffused fill on both faces, no harsh shadows.

AUDIO
Only the identified speaker talks at each moment, exactly as scripted, natural conversational pacing. The listener's lips stay closed but their face and eyes stay alive and reactive — not frozen. Natural outdoor courtyard ambience — faint distant traffic, occasional birdsong, no music, no subtitles.

POSITIVE CONSTRAINTS
Only two people in frame throughout. Both shots stay at the same camera distance — no push-in, no zoom, no dramatic tightening between them. Every camera stays on the same side of the action line. @C1 stays screen-left, @C2 stays screen-right in every shot. No character crosses the line or swaps sides. Lips move only for whichever character is speaking at that moment. Both characters sit naturally on the bench, feet on the ground, bodies fully separate from each other and from the hedge behind them.

> `@` is replaced by the tag of a location, character or prop.

---

## The load-bearing habits in this example

- **Dialogue lives inside the shot block**, interleaved with the acting beat that goes with
  it ("her hand stills on the coffee cup mid-sentence — the fidget stops the moment the
  truth lands"), not listed separately. The model needs the beat attached to the line.
- **Screen-left / screen-right is stated and then restated** in POSITIVE CONSTRAINTS. This
  is the single most common continuity failure.
- **Camera distance is pinned across the cut** — "a calm angle change, not a push closer" —
  otherwise the model tightens automatically on every cut.
- **Constraints are positive**: "Lips move only for whichever character is speaking" rather
  than "no talking over each other".
- **Timecodes are explicit** and the cut is placed on a pause, not mid-line.
- **Duration and cut count are the tunable parts.** 24 seconds and one cut here; the current
  single-prompt maximum is 30 seconds (Higgsfield Cinema Studio 4; Seedance 2.5/2.0 shorter).
  Longer than that is more than one generation, split at a cut.
