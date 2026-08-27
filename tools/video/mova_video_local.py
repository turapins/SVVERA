"""MOVA (OpenMOSS) local video+audio generation."""

from __future__ import annotations

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
from tools.video._shared import (
    MOVA_LOCAL_VARIANTS,
    estimate_local_runtime,
    generate_mova_local_video,
    mova_local_generation_status,
    mova_local_install_instructions,
)


class MOVAVideoLocal(BaseTool):
    name = "mova_video_local"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "mova"
    stability = ToolStability.EXPERIMENTAL
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.SEEDED
    runtime = ToolRuntime.LOCAL_GPU

    install_instructions = mova_local_install_instructions()
    fallback = "mova_video_modal"
    # Falling back to these loses native audio + lip-sync — MOVA is the only
    # local/self-hosted tool in this registry that generates synced speech.
    fallback_tools = ["mova_video_modal", "heygen_video", "ltx_video_modal", "ltx_video_local"]
    agent_skills = ["mova"]

    capabilities = ["image_to_video"]
    supports = {
        "reference_image": True,
        "reference_image_required": True,
        "offline": True,
        "native_audio": True,
        "lip_sync": True,
        "local_gpu": True,
    }
    best_for = [
        "UGC-style talking clips where video + speech + lip-sync must be generated together",
        "avatar/spokesperson content where a single-pass audio-visual model beats stitching TTS onto a silent clip",
    ]
    not_good_for = [
        "silent b-roll or pure text-to-video (MOVA always requires a reference image)",
        "CPU-only machines",
    ]
    provider_matrix = {key: {"tool": "mova_video_local", **value, "mode": "local_gpu"} for key, value in MOVA_LOCAL_VARIANTS.items()}

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
            "offload": {"type": "string", "enum": ["none", "cpu", "group"], "default": "group"},
            "seed": {"type": "integer"},
            "negative_prompt": {"type": "string"},
            "output_path": {"type": "string"},
        },
    }

    resource_profile = ResourceProfile(cpu_cores=4, ram_mb=80000, vram_mb=12000, disk_mb=20000, network_required=False)
    retry_policy = RetryPolicy(max_retries=0)  # long-running GPU job; don't silently retry
    idempotency_key_fields = ["prompt", "model_variant", "reference_image_path", "reference_image_url", "seed"]
    side_effects = ["writes video file to output_path", "spawns a torchrun subprocess against MOVA_REPO_PATH"]
    user_visible_verification = [
        "Watch generated clip for lip-sync accuracy and audio/video sync drift",
        "Confirm speech content matches the intended script — MOVA generates its own audio from the prompt",
    ]

    def get_status(self) -> ToolStatus:
        return mova_local_generation_status()

    def estimate_cost(self, inputs: dict[str, object]) -> float:
        return 0.0

    def estimate_runtime(self, inputs: dict[str, object]) -> float:
        variant = inputs.get("model_variant", "mova-360p")
        return estimate_local_runtime(MOVA_LOCAL_VARIANTS.get(variant, MOVA_LOCAL_VARIANTS["mova-360p"])["speed"])

    def execute(self, inputs: dict[str, object]) -> ToolResult:
        if self.get_status() != ToolStatus.AVAILABLE:
            return ToolResult(success=False, error="Local MOVA generation is unavailable. " + self.install_instructions)
        start = time.time()
        try:
            result = generate_mova_local_video(variants=MOVA_LOCAL_VARIANTS, default_variant="mova-360p", inputs=inputs)
        except Exception as exc:
            return ToolResult(success=False, error=f"Local MOVA generation failed: {exc}")
        result.duration_seconds = round(time.time() - start, 2)
        return result
