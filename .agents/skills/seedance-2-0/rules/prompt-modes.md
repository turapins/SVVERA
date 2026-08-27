---
name: prompt-modes
description: The 8 Seedance prompt modes with copyable skeletons — Single-Shot, Multi-Shot 15s, Reference-Based, Continuation, Action/Movement, Emotion/Performance, Style/Director-Language, Atmosphere/Environment. Pick a mode before writing a word.
---

# Seedance Prompt Modes — the 8 skeletons

Source: *Seedance 2.0 Prompt Skeletons Handbook* + *Serious Examples Supplement* (Higgsfield).

Pick the mode **before** writing a word. Each mode fixes a different thing; using the wrong
skeleton is the most common cause of a prompt that "looks fine" and generates badly.

## The core mental model

A Seedance prompt behaves like a **production brief, not a poetic paragraph**. A strong prompt
answers four questions:

1. What is in the frame?
2. What changes?
3. How does the camera read it?
4. What must remain stable?

Prompts usually fail from **overload**, not brevity: too many actions, too many camera ideas,
too many style words, references with no assigned roles, no hierarchy.

> **The practical rule: one shot carries one dominant readable action. Everything else supports it.**

## Universal prompt logic

Two baseline orderings — use whichever fits, but know the role each block plays:

```
STANDARD:          Subject → Environment → Action → Camera → Lighting → Style → Audio → Continuity
DIRECTOR-ORIENTED: Subject → Action → Environment → Dramatic beat → Camera → Lens/shot size → Lighting → Rhythm → Mood → Texture
```

## Mode selection

| # | Mode | Reach for it when |
|---|---|---|
| 1 | Single-Shot | One continuous action, one camera intention, one dramatic beat |
| 2 | Multi-Shot 15s | The scene needs progression over 10–15s |
| 3 | Reference-Based | Text is combined with image/video/audio assets |
| 4 | Continuation | You need the *next moment in time*, not a similar-looking scene |
| 5 | Action / Movement | Movement itself is the point of the shot |
| 6 | Emotion / Performance | Behaviour under pressure matters more than plot |
| 7 | Style / Director-Language | Strong cinematic identity without vague labels |
| 8 | Atmosphere / Environment | Weather/air/light is doing real dramatic work |

Learning order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8.

---

## 1. Single-Shot

```
[Subject / identity]
[Environment]
[Main action]
[Camera]
[Lighting]
[Style]
[Audio]
[Continuity / stability]
```

Fails when: too many actions in one shot; decorative camera movement with no function;
vague action like "looks emotional" instead of observable behaviour.

## 2. Multi-Shot 15s

```
[Continuity block]      ← what stays fixed across the WHOLE clip

[0–3s]
[3–6s]
[6–10s]
[10–15s]

[Ending / final state]
[Audio]
```

The continuity block is what holds the sequence together. Without it each segment reads as a
different scene. The ending must land on a **clear new condition**, not dissolve into vagueness.

## 3. Reference-Based

```
[Reference roles]       ← one line per asset, each with an explicit job
[Action]                ← must come from the TEXT, not the reference
[Camera]
[Continuity lock]
```

```
Use @image1 as character identity reference.
Use @image2 as environment reference.
Use @video1 as camera rhythm reference.
```

Fails when: references are uploaded without assigned roles; the prompt assumes the reference will
invent the new action; several references compete for the same function.

## 4. Continuation

```
[Continuation start]                    ← where the previous clip ended
[What stays the same]
[New action starting immediately after]
[What must not repeat]                  ← non-negotiable
[Camera]
[Continuity lock]
```

Continuation is a **temporal** instruction, not a resemblance one. Without an explicit
"do not repeat X", the model restages the previous beat instead of continuing from it.

## 5. Action / Movement

```
[Subject / movement mode]
[Approach]
[Weight transfer]
[Contact with surface or object]
[Trajectory]
[Rotation / stabilization]
[Landing / recovery]
[Camera]
[Physical realism / stylization]
```

Describe **mechanics, not verbs**. "Jumps" produces a frictionless animation rig; preload,
inertia, contact and recovery produce a body. Keep the camera wide enough to read the motion.

## 6. Emotion / Performance

```
[Character]
[Trigger]
[Visible facial behavior]
[Body behavior]
[Breathing / rhythm]
[Control / suppression / mask]
[Camera]
[Lighting / intimacy level]
```

Never label the emotion and stop. Name the trigger, the dominant line, the visible signs, and
**what the character is trying to suppress**. The strongest performances are built from
regulation → leakage → decision, not from adjectives.

## 7. Style / Director-Language

```
[Scene premise]
[Camera behavior]
[Spatial logic]
[Lighting / color]
[Performance mode]
[Rhythm / editing feel]
[Texture / material world]
```

Do not name a director and stop — unpack the style into observable operating choices.
Avoid mixing contradictory style systems, and avoid adjective-only style ("cinematic", "epic").

## 8. Atmosphere / Environment

```
[Location]
[Atmospheric conditions]
[Visible environmental behavior]
[Light behavior]
[Character interaction with the environment]
[Camera]
[Texture / sensory detail]
```

The weather has to **behave**, not be named. It should change visibility, light, body behaviour
and sound. Atmosphere that doesn't affect bodies, surfaces or light is decoration.

---

## Density: the high-end modes

Two further patterns appear in the supplement for dense work:

- **Extended Multi-Layer Sequence** — several layers at once (character behaviour, environmental
  pressure, camera progression, physical stakes, tonal arc) held together because every layer
  intensifies *the same objective*. Density is fine; density without hierarchy is not.
- **Transformation** — describe the change as a sequence of **visible causes and effects** with
  material logic and phased escalation, never as a pile of horror adjectives and never jumping
  straight to the finished form.

## Final rule

> Do not try to impress the model. Try to make the scene legible.

A strong prompt is the one where the scene is readable, the action is physical, the camera has a
job, the references have roles, the continuity is explicit, and the whole thing can be tested
systematically — see [testing-protocol.md](testing-protocol.md).
