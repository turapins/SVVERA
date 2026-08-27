"""Real Pinterest discovery via a live, logged-in browser session.

Pinterest's public API has no general search endpoint (see
tools/research/pinterest_reference.py's docstring) — it can only read/manage
the authenticated account's OWN pins and boards, never discover new public
content. The only way to actually search Pinterest's public platform is the
website itself, so this tool drives a live Chrome session (claude-in-chrome
tools) against pinterest.com, the way a human would.

This also matters for Pinterest's own policy: `POST /v5/pins` (pinterest_boards.
create_pin) is documented as being "intended solely for publishing new
content created by the user" — NOT for re-hosting pins/images found via
someone else's board. If the goal is to save/curate someone else's pin,
Pinterest's own guidance is to use the in-app "Save" button — which is
exactly what a live browser session does, and an API call does not. Use
this tool (search + Save in-browser) for curated/found references; use
pinterest_boards.create_pin only for Vocal Image's own original images
(e.g. a Higgsfield-generated character portrait).

No Python execution path: this is the agent navigating, searching, and
clicking Save in a real browser, not a subprocess or HTTP call. See
`execute()`.
"""

from __future__ import annotations

from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolTier,
)


class PinterestBrowserSearch(BaseTool):
    name = "pinterest_browser_search"
    version = "0.1.0"
    tier = ToolTier.SOURCE
    capability = "visual_reference"
    provider = "pinterest_browser"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.BROWSER

    dependencies = []
    install_instructions = (
        "Requires an active, logged-in Pinterest session in Chrome and the "
        "claude-in-chrome tools connected in this session. Not verifiable "
        "from Python.\n"
        "  Load the claude-in-chrome tools (ToolSearch "
        "'select:mcp__claude-in-chrome__tabs_context_mcp,navigate,computer,"
        "read_page,tabs_create_mcp'), navigate to pinterest.com/search/pins/"
        "?q=<query>, review results visually, and either note the image URLs "
        "for use as a script's visual brief, or click Save on a specific pin "
        "to add it to one of Ivan's boards (the ToS-correct way to curate "
        "someone else's content — do not re-upload it via pinterest_boards."
        "create_pin, which is meant for original content only)."
    )
    agent_skills = []

    capabilities = ["search_pins", "save_pin", "discover_visual_references"]
    supports = {"public_search": True, "curated_save": True, "requires_login_session": True}
    best_for = [
        "finding NEW character/visual reference images from the public Pinterest platform",
        "discovering color palette, composition, or aesthetic references for a script's visual brief",
        "curating (Save button) someone else's pin onto a Vocal Image board, per Pinterest's own content policy",
    ]
    not_good_for = [
        "bulk/scripted scraping — do this one deliberate lookup at a time",
        "headless/unattended runs with no agent present to drive the browser",
        "publishing Vocal Image's own original images (use pinterest_boards.create_pin instead)",
    ]
    fallback_tools = ["pinterest_reference"]
    quality_score = 0.6

    input_schema = {
        "type": "object",
        "description": "Documents intent — performed as live browser navigation, not a function call.",
        "required": ["query"],
        "properties": {
            "query": {"type": "string", "description": "Search terms, e.g. a character archetype or visual style"},
            "save_to_board": {"type": "string", "description": "Board name to Save matching pins into, if curating"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=0, network_required=True)
    side_effects = ["drives a real, logged-in Pinterest session in the browser", "may Save pins to a real board"]
    user_visible_verification = ["Confirm found references actually match the character/visual brief before using them"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        return ToolResult(
            success=False,
            error=(
                "pinterest_browser_search has no Python execution path. "
                "Drive a live browser session with the claude-in-chrome "
                "tools instead — navigate to pinterest.com/search, review "
                "results, and Save manually."
            ),
        )
