# Script format for Higgsfield Import elements

Cinema Studio can read a script and pull characters, locations and props out of it into
Elements — **Import elements** accepts `.pdf`, `.xlsx`, `.csv`, `.docx`, `.txt`, `.md`, and
extracts a list for review before anything is added.

Nothing is added until it is reviewed, so a bad extraction costs time, not credits. But a
vague script makes the extractor guess, and guesses arrive as duplicate characters, a prop
promoted to a location, or three names for one person.

**All scripts are written in the format below, exported as `.md`.**

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

## Element IDs after import

**"Include project name in element ID" stays checked.** Imported elements come back
prefixed with the project name — `@C1` in the script becomes something like
`@vi_raise_01_C1` in Elements. That is what stops two projects both owning `@C1` in a
shared library.

**The consequence is a trap:** the tag written in the script is *not* the tag typed into a
generation prompt. After import, open Elements, copy the real IDs, and use those in the
scene prompt. A prompt referencing `@C1` when the element is `@vi_raise_01_C1` silently
loses the reference — the generation runs, the character is simply invented.

## After importing

The dialog extracts and shows the list for review before adding. Check, in this order:

- **Count** — is every character, location and prop there, and nothing extra?
- **Duplicates** — the same person extracted twice under two names is the common failure.
- **Categories** — props filed as locations, or a location filed as a prop.
- **Descriptions** — did the visual description survive, or did it get replaced by plot?

Fix in the script and re-import rather than patching by hand in Elements — the script stays
the source of truth, and the next revision re-imports cleanly.

Imported elements arrive as entries with names, tags and descriptions. They still need
their visuals: character sheets (step 3) and the empty location (step 4) are generated
afterwards and attached.
