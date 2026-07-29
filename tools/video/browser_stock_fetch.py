"""Real stock footage via a live, logged-in browser session.

Neither Artlist nor several other subscription stock sites expose a public
search/download API for footage (Artlist's only documented developer API
covers music, not video or SFX — see tools/audio/artlist_mcp_audio.py). When
a real licensed clip is needed and no API/MCP path covers it, the agent can
drive a live Chrome session (claude-in-chrome tools) against the site's own
web UI — the same way a human editor would — using whatever account/session
is already logged in.

No Python execution path: this is the agent navigating, searching, and
clicking download in a real browser, not a subprocess or HTTP call. See
`execute()`.

Use sparingly and manually — one asset at a time, only for a genuine
licensed-account entitlement. Do not use this to script bulk/automated
scraping of a site's catalog; that is almost certainly against its terms of
service even though this class does not enforce that mechanically.
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


class BrowserStockFetch(BaseTool):
    name = "browser_stock_fetch"
    version = "0.1.0"
    tier = ToolTier.SOURCE
    capability = "video_generation"
    provider = "browser"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.BROWSER

    dependencies = []
    install_instructions = (
        "Requires an active, logged-in browser session for the target site "
        "(e.g. Ivan's Artlist subscription) and the claude-in-chrome tools "
        "connected in this session. Not verifiable from Python.\n"
        "  Load the claude-in-chrome tools (ToolSearch "
        "'select:mcp__claude-in-chrome__tabs_context_mcp,navigate,computer,"
        "read_page,tabs_create_mcp'), navigate to the site's stock-footage "
        "search page, confirm login state, search, review the result, and "
        "download the file to projects/<id>/assets/video/. Do this as one "
        "deliberate, human-supervised lookup per asset — not a scripted loop."
    )
    agent_skills = []

    capabilities = ["stock_video", "search_video", "download_video"]
    supports = {"stock_video": True, "search_video": True, "download_video": True, "requires_login_session": True}
    best_for = [
        "one-off real/licensed clips when no API or MCP covers the provider (e.g. Artlist footage)",
        "using an account the user already pays for, exactly as they would manually",
    ]
    not_good_for = [
        "bulk or scripted downloading — do this one asset at a time, by hand, per request",
        "headless/unattended runs with no agent present to drive the browser",
        "sites without an already-authenticated session",
    ]
    fallback_tools = ["pexels_video", "pixabay_video"]
    quality_score = 0.6

    input_schema = {
        "type": "object",
        "description": "Documents intent — the agent performs this as live browser navigation, not a function call.",
        "required": ["query"],
        "properties": {
            "site": {"type": "string", "description": "Target site, e.g. 'artlist', 'pexels'", "default": "artlist"},
            "query": {"type": "string", "description": "Search terms for the footage needed"},
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=500, network_required=True)
    side_effects = [
        "drives a real, logged-in browser session on the target site",
        "downloads a file under the account's own license terms",
    ]
    user_visible_verification = ["Confirm the downloaded clip matches the brief and the license covers this use"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        return ToolResult(
            success=False,
            error=(
                "browser_stock_fetch has no Python execution path. Drive a live "
                "browser session with the claude-in-chrome tools instead — "
                "navigate to the target site, search, and download manually."
            ),
        )
