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
5. Simple edits → Remotion + FFmpeg. Complex projects → DaVinci Resolve (davinci-resolve-mcp — see "DaVinci Resolve MCP" below for location/update instructions)
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
- **Character/visual reference database**: Pinterest — split across two tools because the API and the website support different things:
  - `pinterest_boards` (real API, works unrestricted) — create boards/pins to build a persistent character database. Only for Vocal Image's **own original images** (Higgsfield generations, produced frames) — that's what Pinterest's `pins_create` endpoint is documented for.
  - `pinterest_browser_search` (live browser session) — the only way to actually *discover* new public Pinterest content or *curate* (Save) someone else's pin, since Pinterest's API has no public search endpoint at all. Use this, not `pinterest_boards.create_pin`, to save a found reference.
  - `pinterest_reference` (real API) — searches/reads only Ivan's **own already-saved** pins/boards, not the public platform. Useful for re-finding something already pinned, not for discovery.
  - One-time setup: create an app at developers.pinterest.com, set `PINTEREST_APP_ID`/`PINTEREST_APP_SECRET` in `.env`, run `python3 scripts/pinterest_auth.py` once.

### DaVinci Resolve MCP

Lives at `.mcp-servers/davinci-resolve-mcp/` — a real git clone of
[samuelgursky/davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp), not a
zip drop, so it can be updated with `git pull`. Gitignored (machine-specific
venv/node_modules and absolute paths) — not part of OpenMontage's own repo
history.

Two servers are registered in the project-root `.mcp.json` (also gitignored,
same reason):
- `davinci-resolve` — the original compound Python server
- `davinci-resolve-advanced` — newer Node server with the deeper render/AAF/
  delivery-target tooling from recent releases

**To update to the latest release** (on-demand — do not automate this into a
cron/background job; same "check when asked" policy as the SVVERA↔calesthio
upstream sync):
```bash
cd .mcp-servers/davinci-resolve-mcp
python3 install.py --update-now         # safe git fast-forward if a newer release exists
npm install                              # only if package.json changed
```
Update policy is set to `notify` (surfaces that a new version exists, doesn't
apply it silently). Change with `python3 install.py --update-policy auto|prompt|never`
if a different behavior is ever wanted.
