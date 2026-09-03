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

---

# Variant D — the difficulty is movement in depth, not the dialogue

Fourth pair: 12 seconds, office corridor, four shots. A woman walks, nods to a passing
colleague, is called from behind by her manager, stops, turns; he walks the distance to her
and only then delivers the line. Two spoken sentences in the whole piece — everything hard
about it is *staging*.

## Block the three ways a model cheats an approach

Models compress travel. Asked for "he walks up to her", they cut to him already there, or
slide him in from the frame edge, or produce him out of a side door. This prompt names all
three and refuses them, then repeats the refusal in a second section:

```
The MANAGER must first appear in the deep background directly behind her. He approaches
her from behind by walking straight forward along the corridor.
The MANAGER never enters through a side door, side corridor or edge of the frame. He never
appears suddenly beside C1 and never teleports closer between shots.
...
Do not make the MANAGER appear suddenly beside C1. Do not bring him through a side doorway.
Do not skip or conceal his approach.
```

It worked: at 0.3 seconds he is already a small figure in the centre of the corridor, and he
covers the whole distance on camera across two shots. Positive description alone would not
have done it — this is one of the places a named negative earns its space.

## A cut condition, not only a cut time

```
Do not cut before the MANAGER has visibly crossed the distance and fully stopped.
```

The timecode says *when* the cut falls; this says *what must be finished* by then. Use the
pair whenever a shot's length is doing narrative work rather than just filling time.

## Split a line across shots and gate the second half on a physical event

`"Sarah."` is called from several metres back while walking. `"You handled that well. Let's
talk about that promotion."` comes only after he has stopped — stated three separate times
(movement lock, shot 3, audio section). That is how a line lands *on* a blocking beat instead
of floating anywhere in the shot.

## An extra without a reference, defined by role and by exit

```
The PASSING EMPLOYEE is one unnamed adult office worker without a character reference. This
person is a visually secondary background performer wearing ordinary neutral professional
clothing. The employee has no dialogue, passes C1 only once and leaves before the
conversation begins.
...
The PASSING EMPLOYEE is no longer visible and does not return.
```

A background human costs no element and adds no identity risk — provided the prompt says
plainly that they are secondary, silent, and gone. The "does not return" line, placed in the
next shot, is what stops them reappearing as a duplicate.

## Spell a micro-interaction out as a checklist

The nod between them is under a second and gets five constraints:

```
- one small nod from C1;
- one restrained nod in response;
- both continue walking;
- no dialogue or handshake;
- C1 keeps her right hand in her pocket.
```

"They nod at each other" becomes a conversation, a wave, or a stop. Any social beat that must
stay small needs its ceiling written down.

## One body detail doing three jobs

The right hand in the pocket is introduced in shot 1, held explicitly through the nod, and
then *removed* in shot 2 as the physical beat that carries the turn. Continuity anchor,
characterisation, and beat change from a single detail — cheaper and more reliable than three
separate instructions.

## Restate the whole scene as an ordered list at the end

Eight bullets replaying the beats in order, after they have already been written shot by
shot. Same deliberate redundancy as the CAST MAP in the two-hander: the spatial progression is
the thing most likely to collapse, so it is stated twice in two different shapes.

## What drifted

**The over-the-shoulder sides came back mirrored.** The prompt asked for C1's shoulder on the
*right* edge in shot 3 and the manager's on the *left* in shot 4. The result put hers left and
his right — the *relationship* is a correct corresponding reverse, only the absolute sides are
flipped. Reading: `the physically corresponding reverse over-the-shoulder` is the instruction
that carries weight; the named edge is not reliable. When a specific edge matters — matching a
neighbouring block in the edit — verify it on the first frame and regenerate, rather than
restating the sentence.

**The prompt shipped with unfilled placeholders.** ROLE ASSIGNMENT still read
`@[INSERT_FEMALE_C1_WORK_CHARACTER_TAG_HERE]` while ACTIVE REFERENCES carried the real tags.
It survived because the real tags did the binding, but a bracketed placeholder is a live
hazard: at best noise, at worst an invented character. Grep every prompt for `[` before
generating.

---

# Variant E — master, over, reverse: the standard coverage of a decision

Fifth pair: 12 seconds, three shots, a manager telling an employee she did not get the
promotion. Both characters speak. It is the plainest structure of the five — wide master,
over-the-shoulder onto the speaker, reverse onto the listener — and it produced the cleanest
result. Three setups instead of four also kept the room intact, unlike Variant C.

## Give the silences a duration and a content

Silence at the head:

```
For the first approximately 1.0 second, both characters remain silent with relaxed closed
lips. The MANAGER maintains steady eye contact, preparing to deliver the difficult
decision. C1 waits tensely and studies his face, already sensing that the news will be bad.
```

And at the tail, after the last word, a hold of 1.1-1.2 seconds with six things written into
it:

```
- C1's lips close and remain still;
- her gaze stays lowered toward the presentation folder;
- she gives one almost imperceptible nod;
- her shoulders remain slightly lowered;
- one slow natural blink follows;
- she does not recover, smile or restore her original professional posture.
```

This is the acting rule "a pause is legal only if something happens inside it" made
executable. A hold without content comes back as a frozen face; a hold with six small events
is the best two seconds in the scene. The `does not recover` line is what stops the model
resetting the expression before the last frame.

## Make a sentence atomic against the cut

```
Keep the camera in this wide master composition throughout the entire sentence.
Do not cut during the sentence.
Do not cut away before the word "anyone" has been spoken completely.
```

The cut is anchored to a **word**, not only to a timecode. Then on the far side of it:

```
The MANAGER continues the same conversation without restarting the previous sentence.
Maintain the same male voice, volume, emotional state and speaking rhythm across the cut.
The cut feels like continuous coverage of one uninterrupted conversation.
```

Restarting or re-saying a line after a hard cut is a standard failure — dialogue split across
shots needs both halves of this: what must finish before the cut, and what must not restart
after it.

## Write emotion as vocal mechanics, not as an adjective

```
She says the first word directly on this disappointed exhale:
C1: "Right."
"Right" is soft, breath-led and slightly unsteady. It is not a neutral acknowledgment or
calm agreement. The word sounds as though C1 is using the remaining breath to keep her
disappointment under control.
...
"I understand" is controlled but noticeably subdued. Her voice has less support and volume
than "Right".
```

Three mechanics — the word rides an exhale, breath is audible in it, and the second line is
quantifiably weaker than the first. A stated *relative* dynamic between two lines is far more
enforceable than "sad", which produces a performed sad face.

## Define sympathy by the clichés it excludes

```
His sympathy appears through a slightly quieter delivery, restrained facial movement and
steady eye contact. He does not perform an exaggerated sad expression, smile reassuringly
or look away from C1.
```

Naming the three things a model reaches for when told "sympathetic" is what leaves room for
the real thing.

## Let the set carry the backstory

```
A closed laptop, a thin presentation folder, several printed pages and two water glasses
remain in fixed positions on the desk, suggesting that an important meeting has just ended.
The laptop is closed and the presentation pages lie untouched. The meeting has already
ended. The room has become noticeably quiet.
```

Nobody has to say the meeting is over. Dressing is also continuity: the folder is what her
gaze drops to in the final shot, so it had to exist in the location map.

## Characters pinned as Elements survive across generations

The manager arrives identical to his appearance in the corridor scene — same face, grey
suit, burgundy tie, pocket square — in a completely separate generation. That is the return
on pinning characters as Elements rather than describing them per prompt.

## What drifted

**The backgrounds swapped across the cuts.** The master establishes windows and skyline behind
him, the office wall and entrance behind her. The over-the-shoulder then gives *him* a wall
and a framed picture, and the reverse gives *her* the window blinds — precisely what
`preserve matching eyelines and physically corresponding backgrounds across every cut` was
written to prevent.

Read this together with Variant D. There, the shoulder edges came back mirrored and nothing
was said about backgrounds; here the shoulder edges were exactly as written and the
backgrounds flipped instead. The model reliably produces *a* corresponding reverse; which
axis of it matches the master — shoulder side, or what is behind each face — is not something
the prompt has been able to control in either direction. Treat it as a check, not an
instruction: look at the first frames of an OTS pair before paying for the full generation,
and regenerate rather than rewording.

---

# Variant F — a seven-shot podcast, run twice on the same prompt

Sixth and seventh videos: the *same prompt text*, generated twice. 29 seconds, two people at a
podcast table, seven fixed shots, both characters speaking, a supplied starting-frame image and
a very heavy prop map. Running one prompt twice is the only way to separate "the instruction
works" from "it worked once", so this pair is worth more than any single result.

## New techniques in the prompt itself

**A supplied image as the starting frame.**

```
Use the @Image 1 as the exact starting frame.
Preserve the same host and guest, identities, wardrobe, accessories, seated positions,
posture, eyelines, podcast table, studio architecture, lighting, camera perspective and
color. Do not reconstruct, mirror or reinterpret the starting frame.
```

This is the mechanism behind `@LAST_FRAME` chaining, used here to continue a conversation from
a previous generation. Identity and set carried across perfectly — but see below for what the
0.4-second "hold the frame" shot actually produced.

**An IMMUTABLE PROP MAP for anything two characters could share.** Nine sentences for two
microphones:

```
MICROPHONE 1 belongs exclusively to @host and remains mounted to the host's side with its
own boom arm. MICROPHONE 2 belongs exclusively to @guest ... on a separate boom arm.
The microphones never switch sides, exchange owners, move, merge, duplicate, disappear or
transform. There is never one shared microphone or one central microphone for both
characters. The two boom arms remain attached to opposite sides and never cross.
Neither character touches, moves or adjusts either microphone.
In every two-shot, both microphones are clearly visible in their correct positions.
In close shots, the featured character's own microphone remains visible. The other
microphone may appear only as a geographically correct foreground object.
```

The load-bearing sentence is `There is never one shared microphone` — it names the exact thing
the model wants to do (collapse two props into one central one). The general form: ownership,
then the specific list of banned transformations, then what must be visible in each shot size.

**SPEAKER LOCK as a line inventory.** Beyond the per-shot locks, a closing section lists every
line each character is permitted to say, followed by `The host never speaks the guest's lines.`
Both takes obeyed the inventory.

**A menu of listener behaviour, a ban list, and an anti-checklist clause.** Seven allowed
behaviours (brief genuine smiles, small amused reactions, subtle eyebrow movement, responsive
eye contact, occasional nods, small posture adjustments, relaxed hand gestures), then eight
banned ones (constant smiling, repeated nodding, emotionless listening, fixed serious faces,
mechanical gestures, abrupt pose changes, twitching, theatrical overacting) — and crucially:

```
Movements emerge organically rather than appearing as separate assigned actions.
One reaction develops naturally at a time.
```

Without that last pair the menu gets *performed*, in order, as a sequence of tics. Any time a
prompt gives a list of behaviours, it needs this clause underneath it.

**Emphasis written at word level.** `Use natural vocal emphasis on: "stop freezing," "stay
calm," "answer clearly," "handle yourself."` — and the host's arc compressed to four words:
`engaged curiosity → growing enthusiasm → practical motivation → readiness to begin.`

## What the duplicate proves

**Stable across both takes** — treat these as genuinely controlled:

- both identities, wardrobe, glasses, jewellery, hair — indistinguishable between takes;
- microphone ownership and sides — held in all seven shots, in both takes;
- the seven-shot structure and the cut points;
- the dialogue and who speaks it;
- the studio's overall look and lighting.

**Different between the two takes** — luck, not control:

- one boom arm is simply missing from the final two-shot in take A and present in take B,
  despite `the two boom arms remain attached to opposite sides`. Prop *ownership* is
  controllable; prop *mechanical attachment* is not;
- the set dressing behind the over-the-shoulder shots differs between takes, and also drifts
  *within* each take — warm shelving in one shot, a dark studio wall in another;
- **take A lost a shot assignment**: at 23.5 seconds, where shot 6 should have cut to the host
  asking "What's the first step?", it is still on the guest mid-sentence. Take B cut correctly.
  A seven-shot structure with cuts specified to a tenth of a second still comes back with one
  shot wrong roughly half the time.

**Wrong in both takes, identically** — which means the prompt, not variance:

Every named foreground-shoulder edge came back mirrored. The prompt asks for the guest's
shoulder at the *right* edge in shots 2, 4 and 6 and the host's at the *left* in shots 3 and 5;
both takes produced the opposite in every one of them.

That is now the third scene in a row (see Variants D and E). **Stop writing the edge.** The
model builds an internally consistent reverse-angle geometry and chooses the side itself; the
sentence naming a left or right edge has never once carried. Write which character is in the
foreground and which is sharp, and check the side on the first frame if it has to match a
neighbouring block.

## And what the starting frame actually did

Neither take reproduced shot 1 as written — a 0.4-second hold on the supplied two-shot. Both
opened directly on a close-up of the host instead. Identity, wardrobe and set all carried, so
the image was read as an identity and style seed rather than as a literal opening frame.

Practical: a starting frame is worth attaching, but do not spend a shot on holding it. Let
shot 1 be real content and let the image do its work underneath.

## A prop required to stay visible in a vertical close-up lands on the face

In take B the host's boom arm runs diagonally across his cheek and chin, with the microphone
ending in front of his chest — despite `the two boom arms ... never cross`.

The cause is elsewhere in the prompt:

```
In close shots, the featured character's own microphone remains visible.
```

A 9:16 medium close-up has no lateral room. Asked to keep both a face and that face's own prop
in frame, the model has one option left: overlap them. The visibility requirement produced the
occlusion. Take A sat the microphone just under the chin instead — same bind, different roll.

So in vertical, a prop that must stay in a close shot needs a **position relative to the face**,
not just permission to be there:

```
In close shots the microphone stays in the lower third of the frame, below the chin line,
and never crosses the face, mouth or eyes. The boom arm enters from the lower frame edge.
```

Or drop the requirement: demand both props only in the two-shots, and let close-ups carry
whatever falls naturally into frame. `Never crosses the face` on its own is not enough — it is
a negative competing against a positive the model has no other way to satisfy.

---

# Variant G — one specific physical action, and two instructive failures

Eighth video: 16 seconds, six shots, a classroom. A boy half-raises his hand to ask a question,
sees nobody else has, and lowers it. The action is the whole creative — if the hand raise does
not read, there is no scene.

## MANDATORY ACTION LOCKS — the best-executed physical beat of any pair analysed

```
Ethan must visibly attempt to raise his LEFT HAND during Shot 3.
His left palm must fully leave the desk.
His left elbow and forearm must visibly rise.
His left fingers must reach approximately shoulder height.
The partially raised left hand must remain visible in the air for approximately half a
second before lowering.
The complete action must be visible in one uninterrupted shot: hand resting on desk →
hand rising → brief hold → hand lowering back to desk.
Do not replace the hand raise with a sideways glance, pencil movement, shoulder movement,
hair adjustment or any other gesture.
```

Three things make this work, and they generalise to any action a scene depends on:

1. **Decompose it into checkable sub-events.** Not "raises his hand" but palm leaves surface →
   elbow lifts → forearm rises → fingers reach a named height → held for a named duration.
   Each is separately verifiable in a frame.
2. **Guarantee the framing.** `The entire rise, brief hold and lowering movement must remain
   visible inside the frame. Do not crop Ethan's left elbow, forearm or hand.` An action the
   frame crops did not happen.
3. **Name the substitutions.** Models downgrade a specific gesture into a vaguer one — a glance,
   a shrug, touching hair. Listing the likely substitutes blocks the downgrade.

The result is unmistakable: palm off the desk, elbow up, forearm vertical, fingers above the
shoulder. Copy this section shape whenever one physical beat carries the scene.

## Failure 1 — positions were specified, orientation was not

The boy sits *sideways to the whiteboard*. His desk, and several others, face across the room.

The location map gives whiteboard on the front wall, windows along the left, door and podium
front-right, `Ethan sits at an individual desk in the third row, slightly left of the central
aisle`. Every one of those is a **position**. None is a **facing**. "Third row" and "central
aisle" imply an orientation to a reader and imply nothing to the model.

Always state facing separately from position:

```
Every desk faces the whiteboard on the front wall. Every seated student's shoulders are
square to the front wall. Ethan's torso faces the whiteboard throughout; only his head and
eyes turn toward the other students.
```

**And a positive requirement elsewhere made it worse.** Shot 3 asks for a *side* three-quarter
angle in which `his face, shoulders, both arms, both hands, notebook and desktop remain clearly
visible`. Showing a face and both hands from the side is far easier if the subject is turned
sideways — so the visibility lock quietly rewrote the seating for the whole scene.

This is the second confirmed instance of the same mechanism (see the microphone across the face
in Variant F), so it is worth stating as a rule:

> **A positive visibility requirement will rewrite staging to satisfy itself.** When a result
> breaks a rule, look first for a "must remain visible / must stay in frame" line that cannot
> be satisfied any other way. Strengthening the broken rule does nothing; the fix is to remove
> the conflict — give the required element a position, or require it only in the shots where
> the framing has room for it.

## Failure 2 — the last shot on a long list is the one that gets dropped

Shot 6 was a return to a wide showing the whole classroom, the teacher's neutral nod and the
class resuming. What came back is a tight close-up of the boy, still talking. The entire closing
beat is missing.

Take A of the podcast lost shot 6 as well. Two of two long shot lists lost their final setup.
Read across both: **a shot list longer than about five setups reliably loses its tail.** If the
last shot carries meaning — a reveal, a closing wide, the beat that makes the scene land —
generate it separately rather than as item six of six.

Shot 3 also lost the background students the story needs (`several other students remain visible
behind Ethan in soft focus, with all their hands down`) — the window filled the background
instead, so the comparison that motivates him lowering his hand is never actually shown.
