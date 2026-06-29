# Vocal Image — Evaluation Criteria

Used by the Analysis Agent (A) to score finished ads.
Also used by Script Agent (S) to self-check before submitting.

---

## Scoring (1–10 per dimension)

### Hook Rate (0–3s)
- 9–10: Immediately creates tension or curiosity. Viewer cannot scroll past.
- 7–8: Clear and relevant. Good but not magnetic.
- 5–6: Understandable but slow. No urgency.
- 1–4: Starts with intro, filler, or brand name. Scroll risk.

### Message Clarity
- 9–10: One clear message. Zero ambiguity about what the product does.
- 7–8: Clear but slightly overloaded.
- 5–6: Requires effort to understand the core point.
- 1–4: Multiple competing messages. Viewer doesn't know what action to take.

### Visual–Audio Sync
- 9–10: Visuals directly illustrate the narration. Every scene has a reason.
- 7–8: Good alignment but some scenes feel generic.
- 5–6: Narration and visuals are parallel but not connected.
- 1–4: Visuals don't match what's being said.

### Presenter Authenticity
- 9–10: Feels like a real person. No uncanny valley. Eye contact natural.
- 7–8: Mostly real-feeling. Minor AI artifacts.
- 5–6: Obviously AI but acceptable for the format.
- 1–4: Distracting AI artifacts. Viewer notices.

### CTA Strength
- 9–10: One clear, direct action. Matches campaign type perfectly.
- 7–8: Clear but slightly generic.
- 5–6: Exists but weak or vague.
- 1–4: Missing, multiple, or confusing.

### Production Quality
- 9–10: Clean audio, sharp video, correct format, no glitches.
- 7–8: Minor quality issues that don't hurt performance.
- 5–6: Noticeable issues (compression, audio quality, timing).
- 1–4: Blocking quality issues.

---

## Minimum Threshold for Publishing

All six dimensions must score **≥ 7** to approve for publishing.
If any dimension scores < 6, the ad goes back to the relevant agent.

| Score < 6 in... | Send back to... |
|----------------|-----------------|
| Hook Rate | Script Agent (S) |
| Message Clarity | Script Agent (S) |
| Visual–Audio Sync | Edit Agent (E) |
| Presenter Authenticity | Video Agent (V) |
| CTA Strength | Script Agent (S) |
| Production Quality | Edit Agent (E) |

---

## Gemini Vision Prompt Template

When analyzing a finished ad, use this prompt:

```
Watch this video ad for Vocal Image, an AI communication coaching app.
Score it on these 6 dimensions (1–10 each):
1. Hook Rate (0–3s): Does it stop the scroll?
2. Message Clarity: Is the core benefit obvious?
3. Visual–Audio Sync: Do visuals match narration?
4. Presenter Authenticity: Does it feel real?
5. CTA Strength: Is the call to action clear and direct?
6. Production Quality: Audio, video, format, timing.

For each score < 8, explain what specifically is weak and how to fix it.
End with: PUBLISH / REVISE / REJECT and one sentence why.
```
