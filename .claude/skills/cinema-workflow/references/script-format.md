# Script format for Higgsfield Import elements

Cinema Studio can read a script and pull characters, locations and props out of it into
Elements — **Import elements** accepts `.pdf`, `.xlsx`, `.csv`, `.docx`, `.txt`, `.md`, and
extracts a list for review before anything is added.

Nothing is added until it is reviewed, so a bad extraction costs time, not credits. But a
vague script makes the extractor guess, and guesses arrive as duplicate characters, a prop
promoted to a location, or three names for one person.

**All scripts are written in the format below, exported as `.md`.** The format is verified:
a 16-element script imported with all 16 extracted, correctly typed and correctly
scene-stamped, on 2026-09-01.

## Why Markdown

- One file — the elements table and the scenes cannot drift apart, which is what happens
  with a separate spreadsheet the moment the script is revised.
- The `## ELEMENTS` table is deterministic to parse; the scene bodies stay readable for the
  writer, the director and the editor.
- Google Docs exports to it, so the team keeps writing where it writes today.

## The format

````markdown
# PROJECT: VI_RAISE_01

## ELEMENTS

| Type | Tag | Name | Description |
|---|---|---|---|
| Character | @C1 | Anna, 32 | Marketing manager. Reserved, self-critical. Casual office wear, no jacket. |
| Character | @C2 | Mark, 40 | Her lead. Warm, direct. Charcoal suit, no tie. |
| Location | @OFFICE | Open-plan office, day | Glass partitions, daylight from the left, muted greys and wood. |
| Prop | @CUP | Paper coffee cup | Plain white, no logo. Held by @C1. |

## SCENE 1 — @OFFICE, day

**Elements:** @C1, @C2, @CUP
**Duration:** 24s
**Action:** @C1 asks for a raise and loses her thread halfway through. @C2 hears her out,
names the problem plainly, then recommends the app.
**Dialogue:**
@C1: "I wanted to talk about my role — I've been, um, taking on a lot more since…"
@C2: "You just lost the sentence. That's the whole problem."
````

### Rules

1. **One `## ELEMENTS` table, at the top, before any scene.** Four columns, exactly these
   headers: `Type | Tag | Name | Description`.
2. **`Type` is one of `Character`, `Location`, `Prop`.** Nothing else — an "Element" or
   "Extra" column value is what makes the extractor invent categories.
3. **Every element gets a tag** — `@C1`, `@OFFICE`, `@CUP`. Short, uppercase,
   no spaces, no punctuation beyond `_`.
4. **One tag per real thing, used everywhere.** Never "Anna" in one scene and "@C1" in
   another; never two tags for the same person across scenes.
5. **`Description` is what the element looks like**, not what it does in the plot. This is
   the text that seeds the character sheet or location generation.
6. **Every scene lists its elements** on an `**Elements:**` line, tags only. That is what
   ties a scene to what has to exist before it can be shot.
7. **Scene headings carry the location tag** — `## SCENE 1 — @OFFICE, day`.
8. **Dialogue lines are prefixed with the speaker's tag.** `@C1: "…"`.
9. **A character introduced mid-script still goes in the table at the top.** The table is
   the complete cast list, not a running one.

## Element IDs after import — verified 2026-09-01

**"Include project name in element ID" stays checked.** Higgsfield's own description:
*"Adds a short project tag to every element ID, abbreviated from the document title."*

Verified on a real import (IT_MYS_06, 16 elements, all 16 extracted with correct types). The
ID scheme is:

```
@<type>_<PROJECTTAG>_<name-slug>_s<N>_v<M>
```

| Part | Source | Example |
|---|---|---|
| `type` | the `Type` column | `char` · `loc` · `prop` |
| `PROJECTTAG` | abbreviated from the document title | `IT_MYS_06` → `ITM` |
| `name-slug` | the `Name` column, slugified | `Mother, 38` → `mother-38` |
| `s<N>` | **the first scene the element appears in** | `_s1`, `_s7`, `_s12` |
| `v<M>` | version, increments on re-import | `_v1` |

Real examples from that import:

```
@char_ITM_mother-38_s1_v1      @loc_ITM_family-kitchen_s1_v1
@char_ITM_boy-11_s1_v1         @loc_ITM_childs-bedroom-desk_s2_v1
@char_ITM_girl-13_s2_v1        @prop_ITM_returned-math-test_s1_v1
@char_ITM_mother-35_s7_v1      @prop_ITM_parents-phone_s12_v1
```

**The scene number is the load-bearing discovery.** It comes from the per-scene
`**Elements:**` lines — the extractor reads them and stamps each element with the first scene
it is used in. So rule 6 is not housekeeping: get those lines wrong and every ID is wrong.
It also means the ID doubles as a running order — sort the Elements panel and you get the
sequence in which things first have to exist.

**And the trap:** the tag written in the script is *not* the tag typed into a generation
prompt, and the full ID is only knowable after the import. `@P1` in the script is
`@char_ITM_mother-38_s1_v1` in the project. A prompt referencing `@P1` does not error — it
silently loses the reference and the model invents the character. Open Elements, copy the
real IDs, use those.

## After importing

The dialog extracts and shows the list for review before adding. Check, in this order:

- **Count** — is every character, location and prop there, and nothing extra?
- **Duplicates** — the same person extracted twice under two names is the common failure.
- **Categories** — props filed as locations, or a location filed as a prop.
- **Descriptions** — did the visual description survive, or did it get replaced by plot?

Fix in the script and re-import rather than patching by hand in Elements — the script stays
the source of truth, and the next revision re-imports cleanly.

Imported elements arrive as entries with names, tags and descriptions, each showing an
**Add element image** placeholder. They carry no visuals — character sheets (step 3) and the
empty locations (step 4) are generated afterwards and attached to these entries.
