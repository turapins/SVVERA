"""Modal-hosted MOVA (OpenMOSS) video+audio generation."""

from __future__ import annotations

import os
import time

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)
from tools.video._shared import generate_mova_modal_video


class MOVAVideoModal(BaseTool):
    name = "mova_video_modal"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "mova-modal"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.SEEDED
    runtime = ToolRuntime.API

    install_instructions = (
        "Set the MODAL_MOVA_ENDPOINT_URL environment variable to your deployed MOVA endpoint:\n"
        "  set MODAL_MOVA_ENDPOINT_URL=https://<your-modal-endpoint>\n"
        "Deploy it with: modal deploy docker/modal-mova/app.py"
    )
    fallback = "mova_video_local"
    fallback_tools = ["mova_video_local", "heygen_video", "ltx_video_modal", "ltx_video_local"]
    agent_skills = ["mova"]

    capabilities = ["image_to_video"]
    supports = {
        "reference_image": True,
        "reference_image_required": True,
        "offline": False,
        "native_audio": True,
        "lip_sync": True,
        "self_hosted_cloud": True,
    }
    best_for = ["self-hosted cloud GPU rendering for MOVA without local workstation dependence"]
    not_good_for = ["zero-setup local workflows", "silent b-roll / pure text-to-video"]
    provider_matrix = {
        "mova-modal": {
            "tool": "mova_video_modal",
            "name": "MOVA (Modal)",
            "mode": "api",
            "quality": "high",
            "speed": "slow",
        }
    }

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "model_variant": {"type": "string", "enum": ["mova-360p", "mova-720p"], "default": "mova-360p"},
            "reference_image_url": {"type": "string"},
            "reference_image_path": {"type": "string"},
            "width": {"type": "integer"},
            "height": {"type": "integer"},
            "num_frames": {"type": "integer"},
            "fps": {"type": "number"},
            "num_inference_steps": {"type": "integer"},
            "seed": {"type": "integer"},
            "negative_prompt": {"type": "string"},
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True)
    retry_policy = RetryPolicy(max_retries=1, backoff_seconds=15.0, retryable_errors=["timeout", "server_error"])
    idempotency_key_fields = ["prompt", "model_variant", "reference_image_path", "reference_image_url", "seed"]
    side_effects = ["writes video file to output_path", "calls modal endpoint"]
    user_visible_verification = ["Watch generated clip for lip-sync accuracy and speech content correctness"]

    def get_status(self) -> ToolStatus:
        return ToolStatus.AVAILABLE if os.environ.get("MODAL_MOVA_ENDPOINT_URL") else ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, object]) -> float:
        return 0.30

    def estimate_runtime(self, inputs: dict[str, object]) -> float:
        return 240.0

    def execute(self, inputs: dict[str, object]) -> ToolResult:
        if self.get_status() != ToolStatus.AVAILABLE:
            return ToolResult(success=False, error="Modal MOVA generation is unavailable. " + self.install_instructions)
        start = time.time()
        try:
            result = generate_mova_modal_video(inputs)
        except Exception as exc:
            return ToolResult(success=False, error=f"Modal MOVA generation failed: {exc}")
        result.duration_seconds = round(time.time() - start, 2)
        result.cost_usd = self.estimate_cost(inputs)
        return result
