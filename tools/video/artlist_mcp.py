"""Artlist AI video generation via the connected Artlist MCP server.

Important scope note: the connected Artlist MCP server
(`mcp__<artlist-connector-id>__*` — identify it in the current session's tool
list by its "Artlist's AI generation service" description if the id differs)
exposes AI *generation* (generate_video, generate_image, generate_audio,
generate_voiceover, upload/confirm helpers, balance/model/voice listing).
It does **not** expose a search/browse endpoint over Artlist's licensed stock
library — there is no "search_stock_footage" tool. So "primary stock source"
here means: prefer Artlist-generated b-roll/support footage over Pexels/
Pixabay stock-site search, not licensed pre-shot clips. If a literal
licensed-library search integration is ever wanted, that is a different,
not-yet-connected Artlist API and would need its own tool.

No Python execution path — the agent must call the MCP tool directly; see
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


class ArtlistMCPVideo(BaseTool):
    name = "artlist_mcp_video"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "artlist_mcp"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.MCP

    dependencies = []
    install_instructions = (
        "Requires the Artlist MCP connector active in the current Claude session "
        "(already connected here as of this writing). Not verifiable from Python — "
        "this entry reports AVAILABLE unconditionally.\n"
        "  Call generate_video on the connected Artlist MCP server directly. Use "
        "get_model_config / list_models first to pick a model, then poll "
        "get_generation_status until done. This is AI-generated footage, not a "
        "licensed stock-library search — see module docstring."
    )
    agent_skills = []

    capabilities = ["text_to_video", "image_to_video"]
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "stock_library_search": False,
    }
    best_for = [
        "primary source for generic supporting/b-roll footage (replaces Pexels/Pixabay as first choice)",
        "AI-generated stock-style clips with no licensing lookup needed",
    ]
    not_good_for = [
        "literal licensed stock-footage search (not exposed by this connector)",
        "character-consistent avatar shots (use Higgsfield for Andy/Peter/Arya continuity)",
        "headless/unattended pipeline runs with no agent present to place the MCP call",
    ]
    fallback_tools = ["pexels_video", "pixabay_video"]
    quality_score = 0.75

    input_schema = {
        "type": "object",
        "description": "Documents the shape the agent maps onto the connected server's generate_video arguments.",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "aspect_ratio": {"type": "string", "enum": ["16:9", "9:16", "1:1"], "default": "9:16"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=0, network_required=True)
    side_effects = ["calls the connected Artlist MCP server; consumes Artlist credits (check get_balance)"]
    user_visible_verification = ["Check generated b-roll reads as generic support footage, not a hero shot"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        return ToolResult(
            success=False,
            error=(
                "artlist_mcp_video has no Python execution path. Call the "
                "connected Artlist MCP server's generate_video tool directly, "
                "or fall back to pexels_video/pixabay_video for licensed stock."
            ),
        )
