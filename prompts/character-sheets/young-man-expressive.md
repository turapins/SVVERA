# Character Sheet — Young Man, Expressive Face

Reference-sheet build for a new production character. Output feeds Higgsfield Soul ID training,
Seedance 2.5 multi-view references, and/or a human editor.

> **Revised 2026-08-17.** The first version of this file was a single one-shot prompt that
> generated both panels in one image. Higgsfield's own guidance says that method fails — see
> [`character-sheet-production`](../../.agents/skills/character-sheet-production/SKILL.md).
> The one-shot prompt is preserved at the bottom as a **quick-look draft only**.

- **Method:** manual — every panel generated as its own full-resolution image, assembled last.
- **Model:** GPT Image 2 (strongest at detail + identity lock for this workflow).
- **Panel aspect:** 3:4. **Resolution:** 2K close-ups, 4K full-body.
- **Backdrop:** clean seamless light grey, held identical across every panel.

---

## Panel plan

Generate in this order — each panel references the ones before it.

| # | Save name | Panel | Res |
|---|---|---|---|
| 1 | `M01_base_identity` | Base face, front, neutral | 2K |
| 2 | `M02_face_three_quarter` | ¾ face | 2K |
| 3 | `M03_face_profile` | Profile | 2K |
| 4 | `M04_expr_smile` | Half-smile | 2K |
| 5 | `M05_expr_laugh` | Open laugh — **locks teeth + facial dynamics** | 2K |
| 6 | `M06_expr_surprise` | Raised-brow surprise | 2K |
| 7 | `M07_expr_listening` | Focused, narrow-eyed listening | 2K |
| 8 | `M08_body_front` | Full body, front | 4K |
| 9 | `M09_body_three_quarter` | Full body, ¾ | 4K |
| 10 | `M10_body_side` | Full body, side | 4K |
| 11 | `M11_body_back` | Full body, back | 4K |
| 12 | `M12_detail_eye` | Eye detail | 2K |
| 13 | `M13_detail_hair` | Hair detail | 2K |
| 14 | `M14_detail_skin` | Skin texture | 2K |
| 15 | `M15_color_palette` | Palette strip | 2K |

Panel 5 is not optional if this feeds Seedance 2.5 — that model wants one strong-expression frame
to learn facial dynamics and teeth structure, not only the resting face.

---

## Panel 1 — base identity

```
Photorealistic editorial front-facing portrait of a young man in his mid-twenties, short dark
brown hair with a natural side-swept fringe and loose texture at the crown, high mobile eyebrows
sitting slightly asymmetric, large clear hazel eyes, a wide mouth at rest, a light scatter of
freckles across the nose and upper cheeks, clean-shaven with faint stubble shadow along the jaw,
neutral expression, looking straight into the lens.
Framed collarbone up.
Clean seamless light grey studio background, full-frame camera 100mm f/2.8.
Brightly lit, soft even studio lighting with a subtle directional key from camera left.
Single sharp catchlight and anatomically correct round circular pupils, hyperrealistic skin
texture with visible pores, fine peach fuzz, and natural unretouched imperfections.
Real unfiltered mirrorless camera capture, zero waxy plastic quality, zero AI smoothing,
photorealism.

Save as: M01_base_identity
```

Run this a few times until you have a base you want to keep. **Everything downstream locks to it.**

## Panels 2–7 — angles and expressions

Attach `M01` as `@Image 1`. Change exactly one thing per panel and never re-describe the face.

```
Photorealistic editorial portrait of the same man from @Image 1, keeping his exact face, hair,
eyes, skin, and identity from @Image 1 unchanged, [THE ONE CHANGE].
Framed collarbone up.
Clean seamless light grey studio background, full-frame camera 100mm f/2.8.
Brightly lit, soft even studio lighting with a subtle directional key from camera left.
Single sharp catchlight and anatomically correct round circular pupils, hyperrealistic skin
texture with visible pores, fine peach fuzz, and natural unretouched imperfections.
Real unfiltered mirrorless camera capture, zero waxy plastic quality, zero AI smoothing,
photorealism.

Save as: [SAVE NAME]
```

| Panel | `[THE ONE CHANGE]` |
|---|---|
| `M02` | `head turned to a three-quarter angle toward camera left` |
| `M03` | `head turned to a full profile facing camera left` |
| `M04` | `a faint half-smile pulling one corner of the mouth up` |
| `M05` | `an open genuine laugh with eyes creased and upper teeth visible` |
| `M06` | `eyebrows raised in surprise with the mouth slightly open` |
| `M07` | `a focused narrow-eyed listening expression` |

Keep the pose wording that simple — over-specifying makes the model overshoot.

## Panels 8–11 — full body

Attach `M01` as `@Image 1`. Once `M08` exists, attach it as `@Image 2` for the remaining angles.

```
Photorealistic editorial full-body portrait of the same man from @Image 1, keeping his exact
face, hair, eyes, skin, and identity from @Image 1 unchanged, slim athletic build, around 180 cm,
standing straight in a neutral A-pose with arms relaxed slightly away from the body and feet
shoulder-width apart, wearing a plain heather-grey crew-neck t-shirt, dark navy slim-fit jeans,
and white low-top sneakers, [ANGLE].
Framed full body head to feet.
Clean seamless light grey studio background, full-frame camera 50mm f/5.6.
Brightly lit, soft even studio lighting with a subtle directional key from camera left.
Hyperrealistic skin texture with visible pores and natural unretouched imperfections, garment
seams and fabric weave clearly readable.
Real unfiltered mirrorless camera capture, zero waxy plastic quality, zero AI smoothing,
photorealism.

Save as: [SAVE NAME]
```

| Panel | `[ANGLE]` |
|---|---|
| `M08` | `seen from the front` |
| `M09` | `seen from a three-quarter angle toward camera left` |
| `M10` | `seen from a full side profile facing camera left` |
| `M11` | `seen from directly behind, showing the same shoulder seams, rear jean pockets, and hair from behind` |

4K here is not optional — the face is small in frame and needs the resolution.

## Panels 12–15 — details

Attach the relevant earlier panel and crop tight. For the palette, attach the hair / skin / eye
crops:

```
A clean flat color palette strip of four equal solid rectangular color blocks side by side on a
plain white background, each block filled with the exact color sampled from its reference:
hair from @Image 1, skin from @Image 2, eyes from @Image 3, and the shirt grey from @Image 4.
Labelled HAIR, SKIN, EYES, SHIRT beneath the blocks.

Save as: M15_color_palette
```

## Assembly

Blank 16:9 canvas at 7680×4320. Full-body angles (front / ¾ / side / back) down the left, the
face close-ups and expressions as a grid upper-right, detail panels along the bottom. Height and
body type labelled top-left. Export.

---

## Drift control

- **Watch the freckles.** They are this character's identity mark — they should land in nearly the
  same spot on every panel. If they drift, crop a tight (but not too tight) shot of the nose and
  cheeks and point the next prompt straight at it.
- Check `M05` hard. Teeth are where generated faces most often become a different person.
- Any panel where the face reads as "similar, but a different person" gets regenerated, not
  accepted. That drift compounds downstream.

## Downstream routing

| Consumer | Feed it |
|---|---|
| **Soul ID** | The individual panels as training photos — **not** the assembled sheet. 15 panels is short of the 20+ target; generate extra angle and expression variants to reach it. |
| **Seedance 2.5** | Individual views declared separately (`@Image 1` front, `@Image 2` back, `@Image 3` face neutral, `@Image 4` strong emotion), closed with "all four images define one <Character>". **Never the assembled grid.** |
| **Human editor** | The assembled 16:9 sheet. |

## Casting knobs

| Knob | Current | Alternatives |
|---|---|---|
| Age read | mid-twenties | early twenties / late twenties |
| Hair | short dark brown, side-swept fringe | loose curls / cropped fade / shoulder-length |
| Build | slim athletic, ~180 cm | lean and tall / broader and shorter |
| Wardrobe | grey tee, navy jeans, white sneakers | oxford shirt + chinos (business) / hoodie (creator) |

Change a knob in `M01` only, then regenerate the chain — never mid-sheet.

---

## Appendix — the superseded one-shot prompt

Fast, cheap, and fine for showing Ivan a casting direction before committing to the 15-panel run.
Do not use its output as a Soul ID or Seedance reference.

```
Character reference sheet of a young man in his mid-twenties, laid out as two panels side by side
against a single seamless neutral grey backdrop (#9E9E9E) that stays perfectly flat and even edge
to edge, with no gradient, no vignette and no shadow falloff behind him.

LEFT PANEL — close-up. Head-and-shoulders portrait, front-facing, shot at eye level on a 50mm
lens, direct gaze into camera. High mobile eyebrows sitting slightly asymmetric, large clear hazel
eyes with a bright catchlight, a wide mouth caught in a faint half-smile that pulls one corner up,
soft crease lines at the outer eyes, a light scatter of freckles across the nose and upper cheeks.
Short dark brown hair with a natural side-swept fringe and loose texture at the crown. Clean-shaven
with faint stubble shadow along the jaw.

RIGHT PANEL — full-body turnaround. The same man at full length twice: front view on the left,
back view on the right. Both stand straight in a neutral A-pose, arms relaxed slightly away from
the body, feet shoulder-width apart. Both are the same height, share one ground line, and are
framed head to toe with equal margin. Slim athletic build, around 180 cm. Plain heather-grey
crew-neck t-shirt, dark navy slim-fit jeans, white low-top sneakers — identical wardrobe in both
views.

Lighting: soft, even three-point studio lighting, low contrast, neutral white balance.
Style: photorealistic studio photography, sharp focus edge to edge, one consistent identity and
wardrobe across all three figures, straight-on orthographic framing. The sheet is clean and
unlabelled.

16:9 landscape.
```
