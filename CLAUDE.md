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
- **Video/Photo generation**: Higgsfield (reference image control) — **prefer the connected Higgsfield MCP tools** (`mcp__higgsfield__generate_video`, `generate_image`, `reframe`, `upscale_video`, `motion_control`, etc. — call `get_workflow_instructions` for templated briefs) over the API-key-based `tools/video/higgsfield_video.py` / `tools/graphics/higgsfield_mcp_image.py` pair. The API tool is the fallback for headless runs where no agent is present to place the MCP call; registered in the tool registry as `higgsfield_mcp` / `higgsfield_mcp_image` so preflight sees it as configured.
- **Stock/support footage, music, SFX**: several options are registered — **no forced default; present them and let Ivan pick per project** (per AGENT_GUIDE's planning protocol, same as render-runtime choice):
  - **Artlist MCP** (`artlist_mcp_video` / `artlist_mcp_image` / `artlist_mcp_audio`) — AI-*generated* b-roll/music/SFX via the connected Artlist MCP server's `generate_video` / `generate_image` / `generate_audio`. Not a licensed-catalog search — there's no "browse Artlist's library" tool in this connector.
  - **Browser fetch** (`browser_stock_fetch` / `browser_stock_fetch_audio`) — when a real licensed asset is needed (e.g. an actual Artlist track/clip, not a generated stand-in), the agent drives a live, logged-in Chrome session (`claude-in-chrome` tools) against the site's own web UI and downloads it manually, one asset at a time. Not scripted/bulk — a deliberate per-request lookup.
  - **Pexels / Pixabay / Freesound** — traditional API-key stock search, still fully available (`fallback_tools` on the entries above).
  - Note for later: Artlist does have a real developer API (`developer.artlist.io`), but it's music-only and needs Enterprise API credentials from an Artlist account manager — not self-serve, not currently wired up. Worth revisiting if that relationship exists.
- **Voice**: ElevenLabs (Andy/Peter/Arya) or Higgsfield Voice
- **Analysis**: Gemini Vision
- **Avatars**: HeyGen
- **Competitor research**: Tryatria (pending access)
