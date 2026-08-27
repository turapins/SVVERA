---
name: kling-motion-control
description: |
  Transfer a specific body motion, facial performance and timing from a reference video onto a
  still character image using Kling Motion Control 3.0 on Higgsfield. Use when: (1) you need a
  precise, repeatable gesture, dance, sport move, acting beat or reaction rather than a loosely
  interpreted "magic" result, (2) transferring the same motion pattern across different
  characters, (3) ad/social/creator workflows that need repeatability, (4) prototyping a scene
  before a more complex Kling VIDEO 3.0 assembly. Not for text-only motion invention — Motion
  Control always requires a motion reference video.
allowed-tools: Bash, Read, Write
---

# Kling Motion Control 3.0 (via Higgsfield)

> **Motion Control = character image + motion reference video.**
> The video drives the motion; the prompt shapes the world around it.

Transfers body motion, facial performance and timing from a motion reference onto a still
character image. The motion can come from an uploaded clip or from Higgsfield's motion library.

## When to choose it

Reach for Motion Control when you need **directed, repeatable motion** instead of a loosely
interpreted result:

- dance, sports, acting beats, reactions, precise gestures
- transferring the same motion pattern across different characters
- ad, social and creator workflows that need repeatability
- scene prototyping before a more complex Kling VIDEO 3.0 assembly

For more complex scenes: Motion Control **plus** the broader Kling VIDEO 3.0 toolkit.

## The five preconditions

Before generating, confirm all five — most bad outputs trace back to one of these:

1. Clean motion reference with no cuts
2. Face and body clearly readable
3. Correct Scene source selected
4. Correct orientation mode selected
5. The prompt describes **the world around the motion**, not the base motion itself

## Best practices and practical limits

> Rule of thumb: **clean motion reference first, prompt second.** Input quality determines
> output quality.

### A. Motion reference

| Requirement | Detail |
|---|---|
| Subject count | One clear subject |
| Framing | Head and body visible |
| Motion type | Real human motion |
| Editing | Avoid cuts and strong camera motion |
| Speed | Avoid very fast actions |
| Duration | Recommended 3–30 seconds |

**Diagnostic:** if the output is suddenly *shorter than the source clip*, the motion is usually
too fast or too complex for a clean continuous transfer. Slow it down or simplify it.

### B. Face binding and orientation

- Close-up face input
- Emotional transitions carry across
- Two orientation modes: **Matches Video** vs **Matches Image**
- Element binding is available **only in Matches Video mode**

## Workflow on Higgsfield

Higgsfield keeps the whole flow on one screen — model, motion library, quality, scene source,
generate:

1. Open the **Video** tab
2. Choose **Kling Motion Control 3.0**
3. Upload the motion reference video
4. Upload the character image, with a readable face and body
5. Pick **720p or 1080p**
6. Set **Scene source** — pull the environment from the video or from the image
7. In **Advanced Settings**, describe lighting, atmosphere and background, then choose the
   orientation mode
8. Generate

## Prompting note

Because the reference video owns the motion, the prompt's job is the surrounding world:
lighting, atmosphere, background, and scene character. Do **not** spend prompt tokens
re-describing the base motion — that competes with the reference rather than reinforcing it.

This is the same division of labour as Soul ID (identity vs frame) — see
`higgsfield-soul-id`. If the character also needs a locked identity across many
generations, train a Soul ID and use it as the character image source.

## Sources

Kling AI guides and the Higgsfield "Kling Motion Control 3.0" article.
