# OpenMontage — SVVERA

**MANDATORY: Read [`AGENT_GUIDE.md`](AGENT_GUIDE.md) before responding to ANY user message.**

Do not act on the user's request until you have read AGENT_GUIDE.md.
It contains routing rules that determine your first action based on what the user asked.
Skipping it WILL cause you to take the wrong action.

---

## SVVERA Context — Vocal Image

This installation is configured for **Vocal Image** — an AI communication coaching app.
Owner: Ivan (ivan@vocalimage.com).

Read [`SVVERA.md`](SVVERA.md) for the full system architecture.
Read [`skills/vocal-image/playbook.md`](skills/vocal-image/playbook.md) for Vocal Image creative rules (when it exists).
Read [`skills/vocal-image/avatars.md`](skills/vocal-image/avatars.md) for character profiles — Andy, Peter, Arya.
Read [`context/scripts/`](context/scripts/) for winning and losing ad scripts with performance data.

### Key rules for this project:
1. Default format is **9:16 vertical** (Instagram Reels / TikTok)
2. **No random generation** — always use reference image control via Higgsfield
3. **Ivan approves** every stage before moving forward
4. Narration voices: ElevenLabs (primary) or Higgsfield Voice (alternative)
5. Simple edits → Remotion + FFmpeg. Complex projects → DaVinci Resolve (davinci-resolve-mcp)
6. Content types: UGC ads, podcasts (2 characters), showmensets, stickers, statics
7. Campaigns: **Web funnel** (longer, educational) vs **App installs** (short, action-oriented)

### Providers in use:
- **Video/Photo generation**: Higgsfield (reference image control)
- **Voice**: ElevenLabs (Andy/Peter/Arya) or Higgsfield Voice
- **Analysis**: Gemini Vision
- **Avatars**: HeyGen
- **Stock media**: Pexels + Pixabay
- **Competitor research**: Tryatria (pending access)
