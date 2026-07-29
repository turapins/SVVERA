"""Artlist AI music/SFX generation via the connected Artlist MCP server.

Same connector as `tools/video/artlist_mcp.py`. `generate_audio` is the one
tool covering both music beds and sound effects — there's no separate SFX
endpoint, so route both use cases through it with a prompt that specifies
which one is wanted (e.g. "upbeat corporate music bed, 30s, no vocals" vs.
"single whoosh transition sound effect"). Voiceover is a distinct tool
(`generate_voiceover`, not covered here) — see CLAUDE.md if that's ever
wired in too. No licensed stock-music/SFX library search is exposed.
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


class ArtlistMCPAudio(BaseTool):
    name = "artlist_mcp_audio"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "music_generation"
    provider = "artlist_mcp"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.MCP

    dependencies = []
    install_instructions = (
        "Requires the Artlist MCP connector active in the current Claude session "
        "(already connected here). Not verifiable from Python.\n"
        "  Call generate_audio on the connected Artlist MCP server directly for "
        "both music beds and sound effects — describe which one is wanted in the "
        "prompt. Poll get_generation_status until done."
    )
    agent_skills = []

    capabilities = ["music_generation", "sound_effect_generation"]
    supports = {"music": True, "sound_effects": True, "stock_library_search": False}
    best_for = [
        "primary source for background music beds and sound effects (replaces pixabay_music/freesound as first choice)",
        "AI-generated, no licensing lookup needed",
    ]
    not_good_for = [
        "literal licensed stock-music/SFX library search (not exposed by this connector)",
        "headless/unattended pipeline runs with no agent present to place the MCP call",
    ]
    fallback_tools = ["pixabay_music", "freesound_music", "music_gen"]
    quality_score = 0.75

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string", "description": "Describe music mood/genre or the specific SFX wanted"},
            "duration_seconds": {"type": "number"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=128, vram_mb=0, disk_mb=0, network_required=True)
    side_effects = ["calls the connected Artlist MCP server; consumes Artlist credits"]
    user_visible_verification = ["Listen for correct mood/length and clean loop points before use"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        return ToolResult(
            success=False,
            error=(
                "artlist_mcp_audio has no Python execution path. Call the "
                "connected Artlist MCP server's generate_audio tool directly."
            ),
        )
