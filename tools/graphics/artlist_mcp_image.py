"""Artlist AI image generation via the connected Artlist MCP server.

Same connector and same scope caveat as `tools/video/artlist_mcp.py`:
generation only (generate_image), no licensed stock-photo search. See that
module's docstring for the full explanation.
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


class ArtlistMCPImage(BaseTool):
    name = "artlist_mcp_image"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "image_generation"
    provider = "artlist_mcp"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.MCP

    dependencies = []
    install_instructions = (
        "Requires the Artlist MCP connector active in the current Claude session "
        "(already connected here). Not verifiable from Python.\n"
        "  Call generate_image on the connected Artlist MCP server directly."
    )
    agent_skills = []

    capabilities = ["text_to_image", "image_to_image"]
    supports = {"text_to_image": True, "editing": True, "stock_library_search": False}
    best_for = ["generic supporting stills / background imagery, AI-generated rather than licensed"]
    not_good_for = [
        "literal licensed stock-photo search (not exposed by this connector)",
        "headless/unattended pipeline runs with no agent present to place the MCP call",
    ]
    fallback_tools = ["pexels_image", "pixabay_image"]
    quality_score = 0.75

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "aspect_ratio": {"type": "string", "enum": ["16:9", "9:16", "1:1", "4:5"], "default": "9:16"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=0, network_required=True)
    side_effects = ["calls the connected Artlist MCP server; consumes Artlist credits"]
    user_visible_verification = ["Check generated image reads as generic support imagery"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        return ToolResult(
            success=False,
            error=(
                "artlist_mcp_image has no Python execution path. Call the "
                "connected Artlist MCP server's generate_image tool directly."
            ),
        )
