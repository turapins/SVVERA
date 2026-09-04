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
- **Video/Photo generation**: Higgsfield (reference image control) — use the **`higgsfield` CLI** (`~/.npm-global/bin/higgsfield`, authenticated; `higgsfield account status` to confirm). There is **no Higgsfield MCP server** — it does not exist, the CLI exposes no `mcp` command, and the only npm package named `higgsfield-mcp` is an unaffiliated third-party wrapper that has not been vetted or installed. Do not look for `mcp__higgsfield__*` tools; earlier revisions of this file told you to prefer them, which cost every session a failed search. Cinema Studio is likewise **UI-only** (projects, briefs, Elements) — see the `higgsfield-generate` skill and `feedback_higgsfield_cli_bypasses_cinema_studio` for the CLI route that binds cast/location via `seedance_2_5` + `omni_reference` PNGs instead. `tools/video/higgsfield_video.py` / `tools/graphics/higgsfield_mcp_image.py` remain the API-key path for headless runs; they keep their historical `higgsfield_mcp` / `higgsfield_mcp_image` registry names so preflight still sees them as configured — the names are legacy, not evidence of an MCP server.
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

### Where skills live — and which copy to edit

Four locations, four owners. Editing the wrong one loses the edit.

| Location | Count | Owner | Edit it? |
|---|---|---|---|
| `.agents/skills/` | ~107 | mirror of upstream **calesthio/OpenMontage** | **No — read-only** |
| `.claude/skills/` | ~75 | this project; **the copy Claude Code loads natively** | Yes |
| `skills/` | 7 areas | SVVERA's own (`vocal-image`, `brand`, `creative`, `meta`, …) | Yes |
| `~/.claude/skills/` | ~25 | vendor CLIs install here themselves | No — they overwrite it |

`.agents/skills/` arrives through the upstream sync. An edit there is either
reverted by the next sync or becomes a merge conflict, and pruning it guarantees
conflicts. Treat it as a mirror: read it, copy from it, do not write to it.

62 skills exist in **both** `.agents/skills/` and `.claude/skills/`. Since the
agent loads the `.claude/` copy, a stale copy there is an instruction it follows
rather than questions. On 2026-09-04 two had drifted with nothing surfacing it:
`.claude/skills/elevenlabs` was four months behind and missing the whole
provider-routing section (no `fal_elevenlabs_tts`, and it still implied asking
the user for a `.env` key), and `.claude/skills/ai-video-gen` was missing the
Kling Official path.

`tests/contracts/test_skill_dir_parity.py` fails on any such drift and names the
files. To resolve one, copy from the mirror:

```bash
rm -rf .claude/skills/<name> && cp -r .agents/skills/<name> .claude/skills/<name>
```

Leave `~/.claude/skills/` alone. The installers recreate what they ship on every
update — the higgsfield CLI 1.1.24 added `higgsfield-brandkit` and
`higgsfield-youtube-thumbnail` that way — so deleting those is a fight you lose
repeatedly.

### Verifying Python changes

Run the suite through make, not bare pytest:

```bash
make test              # whole suite; provisions .venv and dev deps if needed
make test-contracts    # contracts only, faster
make lint
```

`make test` is what CI runs (after `make install-dev`), so a green `make test`
means the same thing locally as it does on GitHub. A bare
`python3 -m pytest tests/...` uses whatever interpreter happens to be on PATH —
on this machine that is Homebrew's Python 3.14 with a coincidentally sufficient
set of packages, while the project targets 3.10. It can pass locally and fail in
CI, or the reverse; treat its result as unverified.

Two traps worth knowing about the suite itself:

- **One broken module under `tools/` takes down the entire run.**
  `tool_registry.discover()` imports every tool module and the contract tests
  call it at collection time, so an import-time error aborts pytest with
  `Interrupted: 1 error during collection` and *zero* tests execute. A reported
  "1 failure" is often N failures stacked behind an import error — fix the
  import and re-run before believing the count. Sweep imports directly with:
  ```bash
  .venv/bin/python -c "import sys,pkgutil,importlib;sys.path.insert(0,'.');[importlib.import_module(m.name) for m in pkgutil.walk_packages(['tools'],'tools.')]"
  ```
- `ResourceProfile` is a dataclass and `ToolStatus` is an Enum, despite looking
  interchangeable. Copy the spelling from a sibling tool
  (`tools/research/pinterest_reference.py` for a network tool) rather than
  inferring the API.

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
git fetch origin
git status -sb                            # which branch are we on?
git rev-list --count HEAD..origin/main    # how far behind?
```

**`python3 install.py --update-now` cannot be trusted as the check.** It only
fast-forwards, and this clone sits on the local branch `svvera/local-fixes`,
which carries fixes not yet upstream. A diverged branch cannot fast-forward, so
the script does nothing and still prints "Environment ready!" — on 2026-09-04 it
reported success while the clone was **150 commits and 100 minor versions**
behind (v2.103.2 vs v2.205.0). Always confirm with `git rev-list --count`, never
with the script's exit message.

The real update is a rebase of the local fixes onto upstream:
```bash
git branch svvera/local-fixes-backup-$(date +%Y%m%d)   # cheap escape hatch
git rebase origin/main
./venv/bin/pip install -r requirements.txt   # deps drift across 100 versions
npm install                                   # only if package.json changed
./venv/bin/python -c "import importlib.util as u; s=u.spec_from_file_location('s','src/server.py'); m=u.module_from_spec(s); s.loader.exec_module(m)"
```
That last line is the smoke test — it catches an import-level break before the
MCP client tries to start the server. Restart the session afterwards so the
client reconnects.

Local fixes should be sent upstream rather than carried forever; each one is a
rebase conflict waiting to happen. Open PRs against
[samuelgursky/davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp)
from the fork `turapins/davinci-resolve-mcp` (remote `fork` in this clone;
`origin` stays upstream). Currently outstanding: PR #184 (`plan["output_root"]`
is a mapping, not a path).

Update policy is set to `notify` (surfaces that a new version exists, doesn't
apply it silently). Change with `python3 install.py --update-policy auto|prompt|never`
if a different behavior is ever wanted.
