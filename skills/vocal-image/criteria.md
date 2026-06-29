# Vocal Image — Evaluation Criteria

Used by the Analysis Agent (A) to score finished ads.
Also used by Script Agent (S) to self-check before submitting.

---

## Pre-Flight: Creative Bible Check

Before scoring, verify the ad was built against the Creative Bible formula:
- [ ] One specific avatar targeted (not "everyone")
- [ ] Awareness stage known and matched to script formula
- [ ] Mechanism present (resonance/release/practice — not generic "confidence")
- [ ] No fabricated statistics (all numbers must be real or tagged {VERIFY})
- [ ] No Mehrabian myth ("93% of communication is nonverbal" — never use this)

---

## Scoring (1–10 per dimension)

### Hook Rate (0–3s)
- 9–10: Names a specific relatable situation. Viewer cannot scroll past.
- 7–8: Clear problem or situation. Good but not magnetic.
- 5–6: Understandable but slow or generic. No urgency.
- 1–4: Opens with brand name, "Hi I'm...", or a generic statement. Scroll risk.

**Test:** Does the hook name a situation the avatar would immediately recognize? (e.g. "Why does your voice shake in meetings?" vs. "Communication is important.")

### Message Clarity
- 9–10: One clear avatar. One clear mechanism. Zero ambiguity about what the product does.
- 7–8: Clear but slightly overloaded with avatars or benefits.
- 5–6: The mechanism is buried or missing. "Speak better" is not a mechanism.
- 1–4: Multiple competing messages. Viewer doesn't know what action to take.

### Visual–Audio Sync
- 9–10: Visuals directly illustrate the narration. App screen shown where relevant.
- 7–8: Good alignment but some scenes feel generic (random stock footage).
- 5–6: Narration and visuals run in parallel but aren't connected.
- 1–4: Visuals don't match what's being said.

### Presenter Authenticity
- 9–10: Feels like a real person. No uncanny valley. Aria/Nick/James consistent with reference.
- 7–8: Mostly real-feeling. Minor AI artifacts.
- 5–6: Obviously AI but acceptable for the format.
- 1–4: Distracting AI artifacts. Character inconsistency between scenes.

### CTA Strength
- 9–10: One clear action. Matches campaign type (install vs. visit). Urgency present.
- 7–8: Clear but slightly generic ("Download now" with no context).
- 5–6: Exists but weak or vague ("Check it out").
- 1–4: Missing, multiple CTAs, or contradicts the campaign type.

### Production Quality
- 9–10: Clean audio, sharp 1080×1920, subtitles present, no glitches.
- 7–8: Minor quality issues that don't hurt performance.
- 5–6: Noticeable issues (compression artifacts, audio levels off, no subtitles).
- 1–4: Blocking quality issues. Not publishable.

---

## Minimum Threshold for Publishing

All six dimensions must score **≥ 7** to approve for publishing.
If any dimension scores < 6, the ad goes back to the relevant agent.

| Score < 6 in... | Send back to... |
|----------------|-----------------|
| Hook Rate | Script Agent (S) |
| Message Clarity | Script Agent (S) — check avatar/awareness match |
| Visual–Audio Sync | Edit Agent (E) |
| Presenter Authenticity | Video Agent (V) — regenerate with reference |
| CTA Strength | Script Agent (S) |
| Production Quality | Edit Agent (E) |

---

## Gemini Vision Analysis Prompt

When analyzing a finished Vocal Image ad, use this prompt:

```
Watch this video ad for Vocal Image — an AI speaking coach app that teaches
voice training through daily practice and real-time AI feedback.

Score it on these 6 dimensions (1–10 each):
1. Hook Rate (0–3s): Does it name a specific situation the viewer recognizes? Does it stop the scroll?
2. Message Clarity: Is ONE specific benefit obvious? Is the mechanism (practice, not content) present?
3. Visual–Audio Sync: Do visuals match narration? Is the app screen shown?
4. Presenter Authenticity: Does Aria/Nick/James feel real? Consistent across scenes?
5. CTA Strength: Is there one clear action that matches the campaign goal?
6. Production Quality: 1080×1920, clean audio, subtitles present, no glitches?

For each score < 8, explain what specifically is weak and how to fix it.

Also note: Does the ad target a specific customer avatar (professional, non-native speaker,
founder, anxious speaker, etc.) or does it feel generic? Specificity = performance.

End with: PUBLISH / REVISE / REJECT and one sentence why.
```

---

## Common Failure Patterns (from real Vocal Image production)

- **Generic hook** → "Communication is key" or "Speak with confidence" — no avatar recognition
- **Missing mechanism** → Ad says "get better at speaking" but not HOW or WHY the product works
- **Stock-footage mismatch** → Narration about Zoom calls, visuals show someone hiking
- **No app screen** → Viewer has no proof the product exists
- **Double CTA** → "Download now AND visit our website" — kills conversion
- **Mehrabian myth** → "93% of communication is nonverbal" — never use, easily Googled as false
- **Invented stats** → Any metric you don't have confirmed data for must be tagged {VERIFY}
