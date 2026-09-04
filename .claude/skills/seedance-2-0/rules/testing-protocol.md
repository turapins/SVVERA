---
name: testing-protocol
description: How to build and iterate a Seedance prompt in a controlled way — the 10-step fast building method, six-pass single-variable iteration, the six anti-patterns, and training drills.
---

# Seedance Testing Protocol & Anti-Patterns

Source: *Seedance 2.0 Prompt Skeletons Handbook*, Part II (Higgsfield).

## The fast building method

Build every new prompt in this order:

1. Choose the prompt mode.
2. Lock the subject.
3. Lock the environment.
4. Define **one** dominant readable action.
5. Define the camera's job.
6. Add light and material behavior.
7. Add sound only if it helps execution.
8. Add continuity / stability notes.
9. Remove decorative clutter.
10. Test one variable at a time.

## Controlled iteration — six passes

Do **not** rewrite everything at once. Change one layer per pass:

| Pass | Change only |
|---|---|
| 1 — Base clarity | Subject, environment, main action |
| 2 — Camera clarity | Camera logic |
| 3 — Light and mood | Lighting and atmosphere (action stays fixed) |
| 4 — Style pressure | Style language, added carefully |
| 5 — Reference pressure | References, with explicit roles |
| 6 — Continuity pressure | Stability across versions / follow-up shots |

After each version, record: what stayed stable, what drifted, what got weaker, what improved,
and which instruction seems overloaded.

## Anti-patterns

| Anti-pattern | What it looks like |
|---|---|
| **Overload** | Too many actions, camera instructions, style tags |
| **No hierarchy** | Everything reads as equally important, so the model averages it |
| **Abstract action** | "dramatic", "intense", "emotional" with no physical behaviour |
| **Decorative camera** | Movement that doesn't help the viewer read the action |
| **Reference confusion** | Many references, no assigned roles |
| **False continuation** | Says "continue" but never defines what starts next and what must not repeat |

## Training drills

| Drill | Hold constant | Vary |
|---|---|---|
| 1 — One subject, three cameras | The shot | Camera logic |
| 2 — One subject, three temperatures | The action | Behaviour, rhythm, lighting |
| 3 — One location, three atmospheres | The blocking | Environment behaviour |
| 4 — Single-shot → multi-shot | The moment | Expand into a 15s sequence |
| 5 — Reference role assignment | — | 2–3 references, each role named |
| 6 — Continuation correction | — | Write a bad continuation prompt, then fix it |

## Verification questions

Before shipping a prompt, confirm:

- Is the scene readable?
- Is the action physical (observable behaviour, not a label)?
- Does the camera have a job?
- Do the references have roles?
- Is the continuity explicit?
- Can this be tested and improved systematically?
