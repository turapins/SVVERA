"""Higgsfield video generation via the connected Higgsfield MCP server.

Preferred path for Higgsfield video on this machine: the agent calls the
connected MCP tools directly (`mcp__higgsfield__generate_video`,
`models_explore`, `get_workflow_instructions`, `reframe`, `upscale_video`,
`motion_control`, etc.) instead of going through Higgsfield's Cloud API.
The MCP surface is a superset of `higgsfield_video` (this repo's API-key
tool) — it also covers image, audio, 3D, upscaling, outpainting, background
removal, and full templated workflows (explainer, ad, avatar, podcast).

This class exists so the registry/preflight can see Higgsfield as a
configured video_generation provider even when only the MCP connector (no
API key) is set up. It cannot execute anything itself — there is no Python
client for an MCP connector's tools; only the agent's own tool-calling can
reach them. `execute()` fails loud with the exact tool name to call instead
of silently no-op'ing.
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


class HiggsFieldMCP(BaseTool):
    name = "higgsfield_mcp"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "higgsfield_mcp"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.MCP

    dependencies = []
    install_instructions = (
        "Requires the Higgsfield MCP connector to be active in the current Claude "
        "session (already connected here as of this writing). The registry cannot "
        "verify a live MCP connector from Python, so this entry reports AVAILABLE "
        "unconditionally — if the connector isn't actually connected, calling the "
        "mcp__higgsfield__* tools will fail at call time instead.\n"
        "  Call mcp__higgsfield__generate_video directly (or motion_control, "
        "reframe, upscale_video, outpaint_image, remove_background, generate_image, "
        "generate_audio, generate_3d for adjacent capabilities). For templated "
        "briefs (explainer, ad, avatar, podcast, shorts) call "
        "get_workflow_instructions first to see the catalog. Call models_explore "
        "with the brief when unsure which model fits."
    )
    agent_skills = ["seedance-2-0", "ai-video-gen"]

    capabilities = [
        "text_to_video", "image_to_video", "reframe", "upscale",
        "motion_control", "outpaint", "background_removal", "templated_workflows",
    ]
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "reference_image_control": True,
        "character_consistency": True,
        "multi_model_routing": True,
        "reframe": True,
        "upscale": True,
        "motion_control": True,
        "outpaint": True,
        "background_removal": True,
        "3d_generation": True,
        "audio_generation": True,
        "templated_workflows": True,
        "virality_prediction": True,
    }
    best_for = [
        "primary Higgsfield path on this machine — MCP connector, no API key needed",
        "reference-image-controlled video/photo generation (Vocal Image avatar consistency)",
        "broadest Higgsfield surface: image, video, audio, 3D, upscale, reframe, outpaint, bg removal",
        "templated end-to-end workflows (explainer, ad, avatar, podcast, shorts) via get_workflow_instructions",
    ]
    not_good_for = ["headless/unattended pipeline runs with no agent present to place the MCP call"]
    fallback_tools = ["higgsfield_video"]
    quality_score = 0.9

    input_schema = {
        "type": "object",
        "description": (
            "Not used for direct execution — this schema documents the shape the "
            "agent should map onto mcp__higgsfield__generate_video's own arguments."
        ),
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video"],
                "default": "text_to_video",
            },
            "reference_image": {"type": "string", "description": "Reference image path/URL for character/product consistency"},
            "aspect_ratio": {"type": "string", "enum": ["16:9", "9:16", "1:1", "21:9"], "default": "9:16"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=256, vram_mb=0, disk_mb=0, network_required=True)
    side_effects = ["calls the connected Higgsfield MCP server; consumes Higgsfield credits"]
    user_visible_verification = ["Watch generated clip for motion coherence, character consistency, and visual quality"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        return ToolResult(
            success=False,
            error=(
                "higgsfield_mcp has no Python execution path. Call the connected "
                "mcp__higgsfield__generate_video tool directly with this prompt "
                "(see get_workflow_instructions / models_explore for guidance), "
                "or fall back to the higgsfield_video tool if the MCP connector "
                "is unavailable."
            ),
        )
