"""Higgsfield image generation via the connected Higgsfield MCP server.

Same connector as `tools/video/higgsfield_mcp.py`, registered separately
under capability="image_generation" so `image_selector` (which discovers
providers by exact capability match) picks it up. Covers Higgsfield's
reference-image-controlled stills, upscaling, outpainting, and background
removal — the still-image side of the same MCP surface used for video.

No Python execution path — see `execute()`.
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


class HiggsFieldMCPImage(BaseTool):
    name = "higgsfield_mcp_image"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "image_generation"
    provider = "higgsfield_mcp"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.MCP

    dependencies = []
    install_instructions = (
        "Requires the Higgsfield MCP connector active in the current Claude session "
        "(already connected here as of this writing). Not verifiable from Python — "
        "see tools/video/higgsfield_mcp.py for the same caveat.\n"
        "  Call mcp__higgsfield__generate_image directly (or upscale_image, "
        "outpaint_image, remove_background, reframe for adjacent still-image ops)."
    )
    agent_skills = ["ai-video-gen"]

    capabilities = ["text_to_image", "image_to_image", "upscale", "outpaint", "background_removal"]
    supports = {
        "text_to_image": True,
        "reference_image_control": True,
        "character_consistency": True,
        "upscale": True,
        "outpaint": True,
        "background_removal": True,
    }
    best_for = [
        "reference-image-controlled stills (avatar/product consistency) via the MCP connector",
        "no API key needed — routes through the connected Higgsfield MCP server",
    ]
    not_good_for = ["headless/unattended pipeline runs with no agent present to place the MCP call"]
    fallback_tools = []
    quality_score = 0.85

    input_schema = {
        "type": "object",
        "description": "Documents the shape the agent maps onto mcp__higgsfield__generate_image's own arguments.",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "reference_image": {"type": "string", "description": "Reference image path/URL for consistency"},
            "aspect_ratio": {"type": "string", "enum": ["16:9", "9:16", "1:1", "4:5"], "default": "9:16"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=0, network_required=True)
    side_effects = ["calls the connected Higgsfield MCP server; consumes Higgsfield credits"]
    user_visible_verification = ["Check reference-image likeness and composition before batch use"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        return ToolResult(
            success=False,
            error=(
                "higgsfield_mcp_image has no Python execution path. Call the "
                "connected mcp__higgsfield__generate_image tool directly."
            ),
        )
