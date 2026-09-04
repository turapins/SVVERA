---
name: seedance-2-5-multireference
description: Seedance 2.5 capabilities beyond 2.0 — up to 50 reference materials with per-type caps, the five-step reference-mapping workflow (roles, subjects, groups, subject profiles, per-scene selection), one-character-multiple-views identity fusion, 30-second stage structure, and timestamp/pacing control.
---

# Seedance 2.5 — Multi-Reference, 30-Second Stages, Timestamps

Source: *Seedance 2.5 — New Capabilities (Part 2)*, Higgsfield / JellyFortuna.

Seedance 2.5 raises three ceilings over 2.0: **50 reference materials**, **30-second videos built
from stages**, and **timestamp/pacing control**. None of them help unless the references are
mapped and the events are staged.

> Map the references. Stage the events. Know the locks.

---

## 1. Reference budget

Up to **50 materials**, but the split is fixed per type — it is not a free pool of 50:

| Type | Input limit | Recommended range |
|---|---|---|
| Images | up to 30, each ≤ 4K | 1–8 distinct subjects across subject-reference images |
| Videos | up to 10, combined ≤ 30s | 1–5 distinct subjects, 5–10s per subject video |
| Audio | up to 10, combined ≤ 30s | dialogue, voice characteristics, ambience or music only — nothing incidental |
| Video editing | a source video may be combined with reference images | source video < 20s, 1–5 reference images |

✅ 30 images + 10 videos + 10 audio = 50
❌ 40 images + 5 videos + 5 audio = 50 — the per-type caps still apply

**More references do not equal more control.** Each material needs a clear purpose and a stated
relationship to the others.

---

## 2. The five-step workflow

`Define Roles → Map Subjects → Group by Type → Subject Profiles → Select by Scene`

### Step 1 — Define each material's role

A reference contains many usable details at once, but you usually want it for exactly one.
Assigning a role tells the model what to extract **and what not to treat as primary**.

```
Image 1 → Character A       Video 1 → Action reference
Image 2 → Character B       Video 2 → Camera reference
Image 3 → Outfit reference  Audio 1 → Voice reference
Image 4 → Prop reference    Audio 2 → Music reference
Image 5 → Scene reference
```

### Step 2 — Name and map each subject individually

One line per subject, one reference per line, stating exactly which attributes to take:
appearance/hairstyle/clothing for characters, structure/material/color for props,
layout/architecture/lighting for scenes.

```
✅ <Character A> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
   <Prop A> corresponds to @Image 3. Use only the structure, material, and color.

❌ "@Images 1 through 4 define four characters respectively."
```

#### One character, multiple views — unique to 2.5

2.5 is the only version that **fuses several views into one locked identity straight from the
prompt**. Declare each view explicitly, then close with a line asserting they are one character:

```
@Image 1 defines the front view of the same <Character A>.
@Image 2 defines the back view of the same <Character A>.
@Image 3 defines the facial details of the same <Character A>, neutral expression.
@Image 4 defines the facial dynamics and teeth of the same <Character A>, strong emotion.
All four images define one <Character A>. The output must contain only one such person throughout.
```

**Slot budget.** Every angle spends one of the 30 image slots. Past 5 characters, switch to a
character sheet plus a Subject Profile (Step 4) to hold identity.

> ⚠️ **Never combine angles into one grid image.** Feed each view as its own reference.
> See the `character-sheet-production` skill for how to build those views so they stay
> identity-locked.

Generate each view on a **neutral light grey background**, and include one frame with a strong
expression (anger, wide smile) so the model learns facial dynamics and teeth structure — not
only the resting face.

### Step 3 — Group materials by type

Flat lists blur together. Sort every reference into four labelled groups, each with its own rule:

- **[Characters]** — appearance, hairstyle, clothing per image, plus an explicit rule against
  interchanging them ("Do not interchange the four characters' appearances, clothing, actions,
  positions, or dialogue.")
- **[Props]** — each prop belongs to exactly one owner, stated in the group.
- **[Scenes]** — use only the space, materials and lighting; **never the people** in the reference.
- **[Motion and Audio]** — videos define motion only; audio defines voice and dialogue. Never
  people or scenes. ("@Video 1 defines the motion of <Conservator> opening <Sample Case>. Do not
  use the person or scene from the video.")

### Step 4 — Centralized Subject Profile

When one character uses several references across multiple scenes, collect everything about them
into one block:

```
[Subject Profile: Conservator] Appearance and clothing: @Image 1. Fixed prop: <Sample Case>
from @Image 5. Locations: <Conservation Lab> and <Gallery>. Motion references: the case-opening
motion from @Video 1 and the sample-placement motion from @Video 2. Do not use: other characters'
clothing. Do not give this character <Record Board> or guide equipment.
```

### Step 5 — Select by scene

Each scene declares three things: which materials it uses, the one event that happens, and the
end state visible when it closes.

```
Scene N | <scene name>
Use: the characters, props, scenes, and motions this scene needs.
Event: one primary action.
End state: positions, ownership, and what stays visible in frame.
```

> The goal of multi-reference creation is to help the model **select the correct materials for the
> current scene** — not to make every material appear at once.

---

## 3. 30-second videos — stages

Divide the story into consecutive stages. Per stage: **one primary state change** and **one
visible end state**. Across stages: a **consistency block**.

```
[Generation Goal] Generate a <video type>. The central subject is <subject>, and the primary
event is <story summary>.

[Stage 1] Initial state: <initial state of characters, props, and scene>.
Primary event: <one primary action or event>. End state: <character positions, prop ownership,
or visible scene state>.

[Stage 2] Continue from the previous stage: <state that must remain unchanged>.
Primary event → End state.

[Stage 3] Primary event: <closing event>. End state: <final visible state>.

[Maintain Consistency] Keep <character identity, number of characters, clothing, prop ownership,
spatial direction, and audio relationships> consistent.
```

## 4. Timestamps and pacing

**Use stages by default.** Timestamps are point reinforcement — reach for one-second precision
only for a critical handoff, entrance/exit, transition, or explicit beat.

| Form | Use | Example |
|---|---|---|
| **Time range** | Default. Allocates pacing across events; each range closes with its own End state | `0–3 seconds: … End state: … 3–7 seconds: …` |
| **Exact time point** | The exception, for one critical beat | `At 5 seconds, the camera whip-pans rapidly to the left` |
| **Relative timing** | Anchors a delay to an event, not the clock | `3 seconds after the character presses the button, the room lights gradually turn off` |

Four rules:

- **Budgets, not cuts.** Ranges are consecutive and non-overlapping — a time budget, never a
  precise edit point.
- **Soft edges.** Actions may land slightly before or after a boundary; never frame-accurate.
- **Fill the budget.** Too little content gives the model freedom; too much causes cuts or
  omitted events.
- **No frequencies.** Never demand rates like "complete three actions in one second."
