---
name: character-sheet-production
description: |
  Build a production-grade character sheet by generating each panel as its own full-resolution
  image and assembling them in an editor — the manual method. Use when: (1) creating a character
  reference sheet for a Soul ID photo set, for Seedance 2.5 multi-view references, or for a
  freelance illustrator/editor brief, (2) a one-shot "generate the whole sheet in one prompt"
  attempt has drifted, (3) you need identity, wardrobe, marks and accessories to stay locked
  across every panel. Includes the GPT Image 2 prompting formula, hard rules, panel plan, and
  drift-control techniques.
allowed-tools: Bash, Read, Write
---

# Character Sheet Production — the manual method

> **A single prompt cannot lock every detail. That is exactly why the manual method exists.**

## Why not one prompt

Generating the whole sheet from a single prompt — even with one reference image for the face and
one for the wardrobe — **fails most of the time**: the face changes on every generation, detail
panels come out wrong, makeup gets altered, accessories drift, and close-ups don't match what was
asked for.

Strict wording does not save it. Even "…keeping the exact same face…" still drifts: the face stays
*recognizable* some of the time, but specific details move. In the documented example the makeup
tear shifted position between panels.

There is also a hard resolution argument. **With a one-shot, the whole sheet is a single image**,
so every face is shrunk down and loses detail. Generate each panel on its own and it stays
full-resolution: the model has far more to lock onto, and it drifts less. GPT Image 2 is genuinely
strong at detail and consistency, but it still misses sometimes — full-resolution panels give it
the best shot.

Manual costs more — more generations, more hands-on work — but you walk away with a far
higher-quality sheet.

> ⚠️ This also means: **never feed a combined grid image as a reference.** Seedance 2.5 requires
> each view as its own reference image (see `seedance-2-0/rules/seedance-2-5-multireference.md`),
> and Soul ID wants individual photos (see `higgsfield-soul-id`).

## Step 1 — Plan the sheet first

It starts with visualizing the sheet. Decide which expressions and angles will appear, what
clothes and accessories the character has, and which details you'll focus on.

**Ask: "What would I need for my use case?"** A sheet destined for a Soul ID photo set wants
simple clothes, visible skin, a few helper expressions, the key details, and a color palette —
different priorities from a sheet for a costume designer.

Documented generation order:

```
base → ¾ → profile side → smile → laugh → surprised → looking up → kissing
→ front full body → ¾ full body → side full body → back full body
→ eye detail → hair detail → skin texture → color palette
```

## Step 2 — Build the base identity

You need a base face to build from. Generate it with GPT Image 2 using the formula below; a few
tries in, you'll have your base. Every subsequent panel references it.

## Step 3 — The prompting formula

> **GPT Image 2 weights the earliest words the most, so order matters.**

| # | Block | Content |
|---|---|---|
| 1 | **Opener / medium** | `photorealistic editorial [shot type]` — anchors realism. **Never** "professional headshot" → gives a stock look. |
| 2 | **Subject + identity + the ONE change** | First ~50 words = top priority. Base: full appearance. Reference-based: `of the same [woman/man] from @Image 1, keeping her exact face, hair, eyes, skin, and identity from @Image 1 unchanged` + the single thing that changes (pose / angle / expression). |
| 3 | **Framing** | `framed [collarbone up / mid-chest up / waist up / full body head to feet]` |
| 4 | **Setting + camera** | `clean seamless white studio background, full-frame camera [100mm f/2.8 close-ups · 85mm f/4 half-body · 50mm f/5.6 full-body]` |
| 5 | **Lighting** | `brightly lit, soft even studio lighting with a subtle directional key from [direction]` — **always specify; the model trends dark.** |
| 6 | **Texture / eyes (constants)** | `single sharp catchlight and anatomically correct round circular pupils, hyperrealistic skin texture with visible pores, fine peach fuzz, and natural unretouched imperfections` |
| 7 | **Realism close** | `real unfiltered mirrorless camera capture, zero waxy plastic quality, zero AI smoothing, photorealism` — affirmative, **not** a negative block |
| 8 | **Text** | Last, and only if the shot has a title / labels |

### Hard rules

- **No trailing "NO X, NO Y" block** — bake every constraint affirmatively into the body.
- **"Photorealism" is always the last word.**
- Reference attached images as `@Image 1 / 2 / 3` **in attach order**. Keep identity from the
  reference and describe only what changes — **never re-describe the face/hair on
  reference-based shots.**
- **Resolution:** 2K for close-ups; 4K for full-body shots (the subject is small in frame, so the
  face needs the resolution). Character aspect = **3:4**.
- **Keep pose wording simple** — over-specifying makes the model overshoot.
- **Give the save name with every prompt** (e.g. `F02_face_three_quarter`) so the set stays tidy
  and ordered.

## Step 4 — Drift control

**Generate in order, and attach helpful reference images as you go.** Later panels can reference
several earlier ones (e.g. face close-up + full body) for better consistency.

**Watch your marks.** If the character has a mole, a beauty mark or a freckle pattern, check it
across every generation — it should land in nearly the same spot each time.

**Force the marks with a reference.** If moles, freckles or similar keep drifting, stop fighting
it and *show* the model instead: crop a tight, zoomed-in shot of the area with the marks — not
*too* close, the model needs to recognise the area too — and point the prompt right at it.

The same technique builds the **color palette panel**: attach the hair / skin / eye / lip crops
and ask for a clean flat palette strip of four equal solid rectangular color blocks side by side
on a plain white background, each block filled with the exact color sampled from its reference.

## Step 5 — Assemble

Once all images are generated you need an editor. Start with a blank 16:9 canvas — a custom
**7680×4320** works well (GPT Image 2 rescales internally, so 3840×2160 is fine too). Look at the
images you have, plan the layout, then crop and arrange them. Export.

Typical layout: full-body angles (front / ¾ / side / back) down the left, a grid of face close-ups
and expressions upper-right, detail panels (eye / hair / skin texture / color palette) along the
bottom, with height and body type labelled in the top-left corner.

## Downstream

A finished sheet feeds three consumers, each with different needs:

| Consumer | What it wants | Skill |
|---|---|---|
| **Higgsfield Soul ID** | The individual panels as a 20+ photo training set — *not* the assembled sheet | `higgsfield-soul-id` |
| **Seedance 2.5** | Individual view images as separately-declared references; one image slot per angle | `seedance-2-0/rules/seedance-2-5-multireference.md` |
| **Human editor / illustrator** | The assembled 16:9 sheet | — |

## Sources

Higgsfield "Character Sheet", material provided by power user @madmax6xx.
