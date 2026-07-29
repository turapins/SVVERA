"""Real stock music/SFX via a live, logged-in browser session.

Same rationale as tools/video/browser_stock_fetch.py: Artlist's only real
developer API covers music search/download but requires enterprise
account-manager credentials Ivan may not have (see
tools/audio/artlist_mcp_audio.py), and has no SFX coverage at all. Until/
unless that API is wired up, a live browser session against Ivan's own
logged-in Artlist account is the only way to get a real licensed track or
SFX rather than an AI-generated stand-in.

No Python execution path — see `execute()`. Same one-at-a-time, human-
supervised caveat as the video variant: not for scripted bulk downloading.
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


class BrowserStockFetchAudio(BaseTool):
    name = "browser_stock_fetch_audio"
    version = "0.1.0"
    tier = ToolTier.SOURCE
    capability = "music_search"
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
        "  Load the claude-in-chrome tools, navigate to the site's music/SFX "
        "search page, confirm login state, search, review the result, and "
        "download to projects/<id>/assets/music/ or assets/sfx/. One "
        "deliberate lookup per asset, not a scripted loop."
    )
    agent_skills = []

    capabilities = ["stock_music", "stock_sfx", "search_music", "download_music"]
    supports = {"music": True, "sound_effects": True, "requires_login_session": True}
    best_for = [
        "one-off real/licensed tracks or SFX when no API covers the provider",
        "using an account the user already pays for, exactly as they would manually",
    ]
    not_good_for = [
        "bulk or scripted downloading",
        "headless/unattended runs with no agent present to drive the browser",
    ]
    fallback_tools = ["pixabay_music", "freesound_music", "music_gen"]
    quality_score = 0.6

    input_schema = {
        "type": "object",
        "required": ["query"],
        "properties": {
            "site": {"type": "string", "default": "artlist"},
            "query": {"type": "string", "description": "Mood/genre for music, or the specific SFX needed"},
            "asset_type": {"type": "string", "enum": ["music", "sfx"], "default": "music"},
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=128, vram_mb=0, disk_mb=100, network_required=True)
    side_effects = [
        "drives a real, logged-in browser session on the target site",
        "downloads a file under the account's own license terms",
    ]
    user_visible_verification = ["Confirm the downloaded track/SFX fits the brief and the license covers this use"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        return ToolResult(
            success=False,
            error=(
                "browser_stock_fetch_audio has no Python execution path. "
                "Drive a live browser session with the claude-in-chrome "
                "tools instead — navigate to the target site, search, and "
                "download manually."
            ),
        )
