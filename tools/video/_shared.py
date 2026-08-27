"""Shared helpers for provider-specific video generation tools."""

from __future__ import annotations

import os
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from tools.base_tool import ToolResult, ToolStatus


HEYGEN_PROVIDERS = {
    "veo_3_1": {"name": "Google VEO 3.1", "quality": "highest", "speed": "slow"},
    "veo_3_1_fast": {"name": "Google VEO 3.1 Fast", "quality": "high", "speed": "medium"},
    "veo3": {"name": "Google VEO 3", "quality": "high", "speed": "slow"},
    "veo3_fast": {"name": "Google VEO 3 Fast", "quality": "high", "speed": "medium"},
    "veo2": {"name": "Google VEO 2", "quality": "medium", "speed": "medium"},
    "kling_pro": {"name": "Kling Pro", "quality": "high", "speed": "medium"},
    "kling_v2": {"name": "Kling v2", "quality": "medium", "speed": "fast"},
    "sora_v2": {"name": "Sora v2", "quality": "high", "speed": "slow"},
    "sora_v2_pro": {"name": "Sora v2 Pro", "quality": "highest", "speed": "slow"},
    "runway_gen4": {"name": "Runway Gen-4", "quality": "high", "speed": "medium"},
    # NOTE: HeyGen's `seedance_lite` / `seedance_pro` provider strings map to
    # Seedance 1.x. Seedance 2.0 on HeyGen is exposed through Video Agent and
    # Avatar Shots endpoints, NOT via the workflow provider parameter. For 2.0
    # access today, use `seedance_video` (fal.ai) or `seedance_replicate`.
    "seedance_lite": {"name": "Seedance Lite (1.x)", "quality": "medium", "speed": "fast"},
    "seedance_pro": {"name": "Seedance Pro (1.x)", "quality": "high", "speed": "medium"},
    "ltx_distilled": {"name": "LTX Distilled", "quality": "low", "speed": "fastest"},
}

# Wan variants.  ``spatial_alignment`` is the VAE spatial compression times the
# transformer patch size — the TI2V line's 16x VAE plus 2x patching means 720p
# is 1280x704, while the 8x-VAE lines take a true 1280x720.
# Wan variants.  ``operations`` is the authoritative capability list — the engine
# refuses anything absent from it rather than loading a checkpoint that cannot
# do the job.  ``params_b`` is the transformer size used to auto-pick precision.
WAN_VARIANTS = {
    "wan2.2-ti2v-5b": {
        "name": "Wan 2.2 TI2V (5B)",
        "hf_id": "Wan-AI/Wan2.2-TI2V-5B-Diffusers",
        "pipeline_class": "WanPipeline",
        "params_b": 5.0,
        "vram_mb": 12000,
        "quality": "high",
        "speed": "medium",
        "operations": [
            "text_to_video",
            "image_to_video",
            "video_to_video",
            "first_last_frame",
            "text_to_image",
        ],
        "t2v": True,
        "i2v": True,
        "license": "Apache-2.0",
        # The TI2V line's 720p geometry is 1280x704, not 1280x720: its VAE
        # compresses 16x spatially and the transformer patches 2x on top, so
        # both dimensions must be multiples of 32 — and 720 is not.
        "default_width": 1280,
        "default_height": 704,
        "default_num_frames": 121,
        "default_steps": 50,
        "default_guidance": 5.0,
        "spatial_alignment": 32,
        "temporal_scale": 4,
        "fps": 24,
    },
    "wan2.2-t2v-a14b": {
        "name": "Wan 2.2 T2V MoE (A14B)",
        "hf_id": "Wan-AI/Wan2.2-T2V-A14B-Diffusers",
        "pipeline_class": "WanPipeline",
        "params_b": 28.0,  # two 14B experts, both resident
        "vram_mb": 40000,
        "quality": "highest",
        "speed": "slow",
        "operations": ["text_to_video", "text_to_image"],
        "t2v": True,
        "i2v": False,
        "license": "Apache-2.0",
        "default_width": 1280,
        "default_height": 720,
        "default_num_frames": 81,
        "default_steps": 40,
        "default_guidance": 4.0,
        "spatial_alignment": 16,
        "temporal_scale": 4,
        "fps": 16,
    },
    "wan2.2-i2v-a14b": {
        "name": "Wan 2.2 I2V MoE (A14B)",
        "hf_id": "Wan-AI/Wan2.2-I2V-A14B-Diffusers",
        "pipeline_class": "WanImageToVideoPipeline",
        "params_b": 28.0,
        "vram_mb": 40000,
        "quality": "highest",
        "speed": "slow",
        "operations": ["image_to_video", "first_last_frame"],
        "t2v": False,
        "i2v": True,
        "license": "Apache-2.0",
        "default_width": 1280,
        "default_height": 720,
        "default_num_frames": 81,
        "default_steps": 40,
        "default_guidance": 3.5,
        "spatial_alignment": 16,
        "temporal_scale": 4,
        "fps": 16,
    },
    "wan2.1-1.3b": {
        "name": "Wan 2.1 T2V (1.3B)",
        "hf_id": "Wan-AI/Wan2.1-T2V-1.3B-Diffusers",
        "pipeline_class": "WanPipeline",
        "params_b": 1.3,
        "vram_mb": 8000,
        "quality": "medium",
        "speed": "fast",
        # Wan 2.1 never shipped a 1.3B image-to-video checkpoint; the only I2V
        # weights in that generation are 14B.  Claiming i2v here silently pulled
        # a 14B model onto an 8GB budget.
        "operations": ["text_to_video", "video_to_video", "text_to_image"],
        "t2v": True,
        "i2v": False,
        "license": "Apache-2.0",
        "default_width": 832,
        "default_height": 480,
        "default_num_frames": 81,
        "default_steps": 50,
        "default_guidance": 5.0,
        "spatial_alignment": 16,
        "temporal_scale": 4,
        "fps": 16,
    },
    "wan2.1-14b": {
        "name": "Wan 2.1 (14B)",
        "hf_id": "Wan-AI/Wan2.1-T2V-14B-Diffusers",
        "hf_image_to_video_id": "Wan-AI/Wan2.1-I2V-14B-480P-Diffusers",
        "hf_first_last_frame_id": "Wan-AI/Wan2.1-FLF2V-14B-720P-diffusers",
        "pipeline_class": "WanPipeline",
        "params_b": 14.0,
        "vram_mb": 24000,
        "quality": "highest",
        "speed": "slow",
        "operations": [
            "text_to_video",
            "image_to_video",
            "video_to_video",
            "first_last_frame",
            "text_to_image",
        ],
        "t2v": True,
        "i2v": True,
        "license": "Apache-2.0",
        "default_width": 1280,
        "default_height": 720,
        "default_num_frames": 81,
        "default_steps": 50,
        "default_guidance": 5.0,
        "spatial_alignment": 16,
        "temporal_scale": 4,
        "fps": 16,
    },
}

HUNYUAN_VARIANTS = {
    "hunyuan-1.5": {
        "name": "HunyuanVideo 1.5",
        "hf_id": "tencent/HunyuanVideo-1.5",
        "pipeline_class": "HunyuanVideoPipeline",
        "vram_mb": 14000,
        "quality": "high",
        "speed": "medium",
        "t2v": True,
        "i2v": True,
        "license": "Apache-2.0",
        "default_width": 848,
        "default_height": 480,
        "default_num_frames": 121,
        "fps": 24,
    },
}

LTX_LOCAL_VARIANTS = {
    "ltx2-local": {
        "name": "LTX-2.3 (Local)",
        # Diffusers-converted weights repo; the raw Lightricks/LTX-2.3 checkpoint
        # uses the separate `ltx_pipelines` package, not diffusers, directly.
        "hf_id": "diffusers/LTX-2.3-Diffusers",
        "pipeline_class": "LTX2Pipeline",
        "pipeline_class_i2v": "LTX2ImageToVideoPipeline",
        "vram_mb": 12000,
        "quality": "high",
        "speed": "medium",
        "t2v": True,
        "i2v": True,
        "license": "LTX-2.3 Open Weights (Community — free under $10M ARR, else contact Lightricks)",
        "default_width": 768,
        "default_height": 512,
        "default_num_frames": 121,
        # Was 30 previously, which contradicted LTX2_FRAME_COUNTS below (that
        # table assumes 24fps, e.g. 121 frames -> ~5s, 193 frames -> ~8s).
        "fps": 24,
    },
}

COGVIDEO_VARIANTS = {
    "cogvideo-5b": {
        "name": "CogVideoX 1.5 (5B)",
        "hf_id": "THUDM/CogVideoX-5b",
        "pipeline_class": "CogVideoXPipeline",
        "vram_mb": 12000,
        "quality": "medium",
        "speed": "medium",
        "t2v": True,
        "i2v": True,
        "license": "Apache-2.0",
        "default_width": 720,
        "default_height": 480,
        "default_num_frames": 49,
        "fps": 8,
    },
    "cogvideo-2b": {
        "name": "CogVideoX (2B)",
        "hf_id": "THUDM/CogVideoX-2b",
        "pipeline_class": "CogVideoXPipeline",
        "vram_mb": 6000,
        "quality": "medium",
        "speed": "fast",
        "t2v": True,
        "i2v": False,
        "license": "Apache-2.0",
        "default_width": 720,
        "default_height": 480,
        "default_num_frames": 49,
        "fps": 8,
    },
}

LTX2_FRAME_COUNTS = {
    "1s": 25,
    "2s": 49,
    "3s": 73,
    "4s": 97,
    "5s": 121,
    "6.7s": 161,
    "8s": 193,
}

# MOVA (OpenMOSS) — synchronized video+audio generation. Unlike the diffusers-
# based variants above, MOVA ships no pip-installable pipeline class; it's run
# via `torchrun scripts/inference_single.py` against a locally cloned
# https://github.com/OpenMOSS/MOVA checkout. A reference image is *required*
# (there is no pure text-to-video mode) — that maps directly onto this
# project's "always use reference image control" rule.
MOVA_LOCAL_VARIANTS = {
    "mova-360p": {
        "name": "MOVA 360p",
        "hf_id": "OpenMOSS-Team/MOVA-360p",
        "vram_mb": 12000,  # layerwise offload, per upstream README
        "quality": "medium",
        "speed": "medium",
        "default_width": 640,
        "default_height": 352,
        "default_num_frames": 193,
        "fps": 24.0,
        "license": "Apache-2.0",
    },
    "mova-720p": {
        "name": "MOVA 720p",
        "hf_id": "OpenMOSS-Team/MOVA-720p",
        "vram_mb": 48000,  # component-wise offload, per upstream README
        "quality": "high",
        "speed": "slow",
        "default_width": 1280,
        "default_height": 720,
        "default_num_frames": 193,
        "fps": 24.0,
        "license": "Apache-2.0",
    },
}


def get_torch_device() -> str:
    """Return best available torch device: cuda > mps (Apple Silicon Metal) > cpu.

    Priority order:
      1. cuda  — NVIDIA GPU (fastest for most diffusion models)
      2. mps   — Apple Silicon Metal (M1/M2/M3/M4/M5, macOS >= 12.3)
      3. cpu   — fallback, always available but slow

    MPS detection is guarded for torch builds that lack ``torch.backends.mps``
    (e.g. older pip wheels or Linux builds).  We check both build-time support
    (``is_built()``) and runtime availability (``is_available()``).
    """
    try:
        import torch as _torch  # noqa: PLC0415
    except ImportError:
        return "cpu"
    if _torch.cuda.is_available():
        return "cuda"
    # Guard: torch.backends.mps may not exist on older/non-macOS builds
    try:
        mps_backend = getattr(_torch, "backends", None)
        mps_backend = getattr(mps_backend, "mps", None) if mps_backend else None
        if mps_backend is not None:
            # Check build-time support first, then runtime availability
            is_built = getattr(mps_backend, "is_built", lambda: True)()
            is_available = getattr(mps_backend, "is_available", lambda: False)()
            if is_built and is_available:
                return "mps"
    except Exception:
        pass
    return "cpu"


def local_generation_enabled() -> bool:
    return os.environ.get("VIDEO_GEN_LOCAL_ENABLED", "").lower() in {"true", "1", "yes"}


def local_generation_status() -> ToolStatus:
    if not local_generation_enabled():
        return ToolStatus.UNAVAILABLE
    try:
        import diffusers  # noqa: F401
        import torch  # noqa: F401
    except ImportError:
        return ToolStatus.UNAVAILABLE
    return ToolStatus.AVAILABLE


def local_install_instructions() -> str:
    return (
        "Enable local video generation and install the diffusers stack:\n"
        "  export VIDEO_GEN_LOCAL_ENABLED=true\n"
        "  uv pip install diffusers transformers accelerate torch pillow requests\n"
        "\n"
        "GPU support — pick what matches your hardware:\n"
        "  NVIDIA CUDA    — works out of the box with the above\n"
        "  Apple Silicon (MPS, macOS >= 12.3) — works out of the box; no extra build\n"
        "  CPU fallback   — slow but functional on any machine\n"
        "\n"
        "VRAM profile: see the selected tool's resource_profile for minimum VRAM."
    )


def mova_repo_path() -> Path | None:
    raw = os.environ.get("MOVA_REPO_PATH")
    if not raw:
        return None
    path = Path(raw)
    return path if (path / "scripts" / "inference_single.py").is_file() else None


def mova_local_generation_status() -> ToolStatus:
    if not local_generation_enabled():
        return ToolStatus.UNAVAILABLE
    if mova_repo_path() is None:
        return ToolStatus.UNAVAILABLE
    if not shutil.which("torchrun"):
        return ToolStatus.UNAVAILABLE
    try:
        import torch  # noqa: F401
    except ImportError:
        return ToolStatus.UNAVAILABLE
    return ToolStatus.AVAILABLE


def mova_local_install_instructions() -> str:
    return (
        "Clone and install OpenMOSS/MOVA, then point at it via env vars:\n"
        "  git clone https://github.com/OpenMOSS/MOVA.git\n"
        "  cd MOVA && conda create -n mova python=3.13 -y && conda activate mova\n"
        "  pip install -e .\n"
        "  hf download OpenMOSS-Team/MOVA-360p --local-dir ../MOVA-360p\n"
        "\n"
        "  export VIDEO_GEN_LOCAL_ENABLED=true\n"
        "  export MOVA_REPO_PATH=/path/to/MOVA\n"
        "  export MOVA_CKPT_PATH=/path/to/MOVA-360p\n"
        "\n"
        "GPU: 360p needs ~12-48GB VRAM depending on --offload mode (layerwise vs "
        "component-wise); 720p needs ~48GB+. See upstream README for exact profiles."
    )


def estimate_quality_cost(quality: str) -> float:
    if quality == "highest":
        return 0.50
    if quality == "high":
        return 0.35
    if quality == "low":
        return 0.15
    return 0.20


def estimate_speed_runtime(speed: str) -> float:
    return {"fastest": 30.0, "fast": 60.0, "medium": 120.0, "slow": 300.0}.get(speed, 120.0)


def estimate_local_runtime(speed: str) -> float:
    return {"fast": 120.0, "medium": 240.0, "slow": 600.0}.get(speed, 240.0)


def load_diffusers_pipeline(pipeline_class: str, model_id: str, enable_offload: bool):
    import diffusers
    import torch

    pipeline_map = {
        "WanPipeline": "WanPipeline",
        "HunyuanVideoPipeline": "HunyuanVideoPipeline",
        "LTXPipeline": "LTXPipeline",  # legacy LTX-Video (v1) pipeline class
        "LTX2Pipeline": "LTX2Pipeline",  # LTX-2 / LTX-2.3 text-to-video
        "LTX2ImageToVideoPipeline": "LTX2ImageToVideoPipeline",  # LTX-2 / LTX-2.3 image-to-video
        "CogVideoXPipeline": "CogVideoXPipeline",
    }
    pipeline_name = pipeline_map.get(pipeline_class, pipeline_class)
    pipeline_class_obj = getattr(diffusers, pipeline_name)

    device = get_torch_device()
    # bfloat16 is only reliable on CUDA; MPS uses float16 for inference,
    # CPU must use float32 (float16 is emulated and unreliable on CPU)
    if device == "cuda" and torch.cuda.is_bf16_supported():
        dtype = torch.bfloat16
    elif device == "cpu":
        dtype = torch.float32
    else:
        dtype = torch.float16

    pipeline = pipeline_class_obj.from_pretrained(model_id, torch_dtype=dtype)

    if enable_offload:
        if device == "cuda":
            pipeline.enable_model_cpu_offload()
        else:
            # enable_model_cpu_offload() is CUDA-only; fall back to direct device placement
            pipeline = pipeline.to(device)
    else:
        pipeline = pipeline.to(device)

    if hasattr(pipeline, "enable_attention_slicing"):
        pipeline.enable_attention_slicing()

    if hasattr(pipeline, "vae") and pipeline.vae is not None:
        if hasattr(pipeline.vae, "enable_tiling"):
            pipeline.vae.enable_tiling()
        if hasattr(pipeline.vae, "enable_slicing"):
            pipeline.vae.enable_slicing()
    return pipeline


def load_reference_image(inputs: dict[str, Any], width: int, height: int):
    from io import BytesIO

    import requests
    from PIL import Image

    ref_path = inputs.get("reference_image_path")
    ref_url = inputs.get("reference_image_url")

    if ref_path:
        image = Image.open(ref_path).convert("RGB")
    elif ref_url:
        response = requests.get(ref_url, timeout=60)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content)).convert("RGB")
    else:
        return ToolResult(
            success=False,
            error="image_to_video requires reference_image_url or reference_image_path",
        )

    return image.resize((width, height), Image.LANCZOS)


def generate_local_video(
    *,
    tool_name: str,
    variants: dict[str, dict[str, Any]],
    default_variant: str,
    inputs: dict[str, Any],
) -> ToolResult:
    import torch
    from diffusers.utils import export_to_video

    variant = inputs.get("model_variant", default_variant)
    if variant not in variants:
        return ToolResult(
            success=False,
            error=f"Unknown model_variant: {variant}. Available: {', '.join(sorted(variants))}",
        )

    meta = variants[variant]
    prompt = inputs["prompt"]
    operation = inputs.get("operation", "text_to_video")
    seed = inputs.get("seed")
    enable_offload = inputs.get("enable_model_offload", True)

    if operation == "image_to_video" and not meta.get("i2v"):
        return ToolResult(
            success=False,
            error=f"{meta['name']} does not support image_to_video.",
        )

    width = inputs.get("width", meta["default_width"])
    height = inputs.get("height", meta["default_height"])
    num_frames = inputs.get("num_frames", meta["default_num_frames"])
    fps = meta["fps"]
    model_id = meta.get("hf_i2v_id") if operation == "image_to_video" and meta.get("hf_i2v_id") else meta["hf_id"]
    pipeline_class = meta.get("pipeline_class_i2v") if operation == "image_to_video" and meta.get("pipeline_class_i2v") else meta["pipeline_class"]
    pipeline = load_diffusers_pipeline(pipeline_class, model_id, enable_offload)

    generation_args: dict[str, Any] = {
        "prompt": prompt,
        "num_frames": num_frames,
        "width": width,
        "height": height,
        "num_inference_steps": inputs.get("num_inference_steps", 30),
    }
    if seed is not None:
        generation_args["generator"] = torch.Generator(device="cpu").manual_seed(seed)
    if operation == "image_to_video":
        image = load_reference_image(inputs, width, height)
        if isinstance(image, ToolResult):
            return image
        generation_args["image"] = image
    if meta["pipeline_class"] == "CogVideoXPipeline":
        generation_args["negative_prompt"] = "worst quality, low quality, blurry, distorted, watermark"

    output = pipeline(**generation_args)
    frames = output.frames[0] if hasattr(output, "frames") else output.images

    output_path = Path(inputs.get("output_path", f"{tool_name}_{variant}.mp4"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    export_to_video(frames, str(output_path), fps=fps)

    return ToolResult(
        success=True,
        data={
            "provider": tool_name,
            "model_variant": variant,
            "provider_name": meta["name"],
            "mode": "local",
            "prompt": prompt,
            "model_id": model_id,
            "width": width,
            "height": height,
            "num_frames": num_frames,
            "fps": fps,
            "duration_seconds": round(num_frames / fps, 2),
            "operation": operation,
            "output": str(output_path),
            "format": "mp4",
            "license": meta["license"],
            **probe_output(output_path),
        },
        artifacts=[str(output_path)],
        seed=seed,
        model=model_id,
    )


def generate_mova_local_video(
    *,
    variants: dict[str, dict[str, Any]],
    default_variant: str,
    inputs: dict[str, Any],
) -> ToolResult:
    """Run OpenMOSS/MOVA via `torchrun scripts/inference_single.py` as a subprocess.

    Unlike generate_local_video (diffusers pipeline call in-process), MOVA has
    no pip-installable pipeline class — it ships as a standalone repo you run
    with torchrun. This shells out against a locally cloned checkout.
    """
    repo_path = mova_repo_path()
    if repo_path is None:
        return ToolResult(
            success=False,
            error="MOVA_REPO_PATH is not set or does not point at a valid OpenMOSS/MOVA checkout.",
        )

    variant = inputs.get("model_variant", default_variant)
    if variant not in variants:
        return ToolResult(
            success=False,
            error=f"Unknown model_variant: {variant}. Available: {', '.join(sorted(variants))}",
        )
    meta = variants[variant]

    prompt = inputs["prompt"]
    ref_path = inputs.get("reference_image_path")
    ref_url = inputs.get("reference_image_url")
    if not ref_path and not ref_url:
        return ToolResult(
            success=False,
            error="MOVA requires a reference image — pass reference_image_path or reference_image_url "
            "(there is no text-only generation mode).",
        )
    if ref_url and not ref_path:
        import tempfile

        import requests

        resp = requests.get(ref_url, timeout=60)
        resp.raise_for_status()
        suffix = Path(ref_url).suffix or ".png"
        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        tmp.write(resp.content)
        tmp.close()
        ref_path = tmp.name

    ckpt_path = os.environ.get("MOVA_CKPT_PATH")
    if not ckpt_path:
        return ToolResult(success=False, error="MOVA_CKPT_PATH is not set (path to the downloaded checkpoint dir).")

    width = inputs.get("width", meta["default_width"])
    height = inputs.get("height", meta["default_height"])
    num_frames = inputs.get("num_frames", meta["default_num_frames"])
    fps = inputs.get("fps", meta["fps"])
    seed = inputs.get("seed", 42)
    num_inference_steps = inputs.get("num_inference_steps", 50)
    output_path = Path(inputs.get("output_path", "mova_video_local.mp4"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        "torchrun",
        "--nproc_per_node=1",
        "scripts/inference_single.py",
        "--ckpt_path", ckpt_path,
        "--prompt", prompt,
        "--ref_path", ref_path,
        "--output_path", str(output_path.resolve()),
        "--height", str(height),
        "--width", str(width),
        "--num_frames", str(num_frames),
        "--fps", str(fps),
        "--seed", str(seed),
        "--num_inference_steps", str(num_inference_steps),
        "--offload", inputs.get("offload", "group"),
    ]
    if inputs.get("negative_prompt"):
        cmd += ["--negative_prompt", inputs["negative_prompt"]]

    proc = subprocess.run(cmd, cwd=str(repo_path), capture_output=True, text=True, timeout=1800, check=False)
    if proc.returncode != 0:
        return ToolResult(
            success=False,
            error=f"MOVA inference failed (exit {proc.returncode}): {proc.stderr[-2000:]}",
        )
    if not output_path.exists():
        return ToolResult(success=False, error=f"MOVA reported success but no output file at {output_path}")

    return ToolResult(
        success=True,
        data={
            "provider": "mova",
            "model_variant": variant,
            "provider_name": meta["name"],
            "mode": "local",
            "prompt": prompt,
            "model_id": meta["hf_id"],
            "width": width,
            "height": height,
            "num_frames": num_frames,
            "fps": fps,
            "duration_seconds": round(num_frames / fps, 2),
            "operation": "image_to_video",
            "output": str(output_path),
            "format": "mp4",
            "license": meta["license"],
            "native_audio": True,
            "lip_sync": True,
            **probe_output(output_path),
        },
        artifacts=[str(output_path)],
        seed=seed,
        model=meta["hf_id"],
    )


def generate_mova_modal_video(inputs: dict[str, Any]) -> ToolResult:
    import base64

    import requests

    endpoint_url = os.environ.get("MODAL_MOVA_ENDPOINT_URL")
    if not endpoint_url:
        return ToolResult(success=False, error="MODAL_MOVA_ENDPOINT_URL not set.")

    prompt = inputs["prompt"]
    ref_path = inputs.get("reference_image_path")
    ref_url = inputs.get("reference_image_url")
    if not ref_path and not ref_url:
        return ToolResult(
            success=False,
            error="MOVA requires a reference image — pass reference_image_path or reference_image_url "
            "(there is no text-only generation mode).",
        )

    variant = inputs.get("model_variant", "mova-360p")
    width = inputs.get("width", 640 if variant == "mova-360p" else 1280)
    height = inputs.get("height", 352 if variant == "mova-360p" else 720)
    num_frames = inputs.get("num_frames", 193)
    fps = inputs.get("fps", 24.0)

    payload: dict[str, Any] = {
        "prompt": prompt,
        "model_variant": variant,
        "width": width,
        "height": height,
        "num_frames": num_frames,
        "fps": fps,
        "seed": inputs.get("seed", 42),
        "num_inference_steps": inputs.get("num_inference_steps", 50),
    }
    if inputs.get("negative_prompt"):
        payload["negative_prompt"] = inputs["negative_prompt"]
    if ref_path:
        payload["ref_image"] = base64.b64encode(Path(ref_path).read_bytes()).decode()
    else:
        payload["ref_image_url"] = ref_url

    response = requests.post(endpoint_url, json=payload, timeout=600)
    response.raise_for_status()
    output_path = Path(inputs.get("output_path", "mova_video_modal.mp4"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content_type = response.headers.get("content-type", "")
    if "video" in content_type or "octet-stream" in content_type:
        output_path.write_bytes(response.content)
    else:
        response_payload = response.json()
        video_url = response_payload.get("video_url") or response_payload.get("url")
        if not video_url:
            return ToolResult(success=False, error=f"No video data in response: {response_payload}")
        download = requests.get(video_url, timeout=120)
        download.raise_for_status()
        output_path.write_bytes(download.content)

    return ToolResult(
        success=True,
        data={
            "provider": "mova-modal",
            "provider_name": "MOVA (Modal)",
            "mode": "modal",
            "prompt": prompt,
            "model_variant": variant,
            "width": width,
            "height": height,
            "num_frames": num_frames,
            "fps": fps,
            "duration_seconds": round(num_frames / fps, 2),
            "operation": "image_to_video",
            "output": str(output_path),
            "format": "mp4",
            "native_audio": True,
            "lip_sync": True,
        },
        artifacts=[str(output_path)],
        seed=inputs.get("seed", 42),
        model="mova",
    )


def poll_heygen(execution_id: str, api_key: str, timeout: int = 600) -> str:
    import requests

    headers = {"X-Api-Key": api_key}
    url = f"https://api.heygen.com/v1/workflows/executions/{execution_id}"
    deadline = time.time() + timeout
    interval = 5.0

    while time.time() < deadline:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json().get("data", {})
        status = data.get("status", "")

        if status == "completed":
            video_url = (
                data.get("output", {}).get("video", {}).get("video_url")
                or data.get("output", {}).get("video_url")
            )
            if video_url:
                return video_url
            raise RuntimeError(f"Completed but no video_url in output: {data}")

        if status in {"failed", "error"}:
            raise RuntimeError(f"HeyGen generation failed: {data.get('error', 'Unknown')}")

        time.sleep(min(interval, max(0.0, deadline - time.time())))
        interval = min(interval * 1.2, 30.0)

    raise TimeoutError(f"HeyGen execution {execution_id} timed out after {timeout}s")


def upload_image_fal(image_path: str) -> str:
    """Upload a local image to fal.ai storage and return a public URL."""
    import requests

    api_key = os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_API_KEY")
    if not api_key:
        raise RuntimeError("FAL_KEY or FAL_AI_API_KEY required for image upload")

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    suffix = path.suffix.lower()
    content_type = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(
        suffix.lstrip("."), "image/png"
    )

    # Initiate upload
    init_resp = requests.post(
        "https://rest.alpha.fal.ai/storage/upload/initiate",
        headers={"Authorization": f"Key {api_key}", "Content-Type": "application/json"},
        json={"content_type": content_type, "file_name": path.name},
        timeout=30,
    )
    init_resp.raise_for_status()
    data = init_resp.json()

    # Upload file content
    put_resp = requests.put(
        data["upload_url"],
        headers={"Content-Type": content_type},
        data=path.read_bytes(),
        timeout=60,
    )
    put_resp.raise_for_status()

    return data["file_url"]


def upload_image_heygen(image_path: str, api_key: str) -> str:
    """Upload a local image to HeyGen and return a public URL.

    Tries the v2 presigned-upload endpoint first, falls back to fal.ai storage.
    """
    import requests

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Try HeyGen v2 presigned upload
    try:
        resp = requests.post(
            "https://api.heygen.com/v2/assets/upload",
            headers={"X-Api-Key": api_key, "Content-Type": "application/json"},
            json={"content_type": "image/png", "file_name": path.name},
            timeout=30,
        )
        if resp.status_code == 200:
            data = resp.json().get("data", {})
            upload_url = data.get("upload_url")
            file_url = data.get("url") or data.get("file_url")
            if upload_url and file_url:
                put_resp = requests.put(
                    upload_url,
                    headers={"Content-Type": "image/png"},
                    data=path.read_bytes(),
                    timeout=60,
                )
                put_resp.raise_for_status()
                return file_url
    except Exception:
        pass

    # Fallback to fal.ai storage upload
    return upload_image_fal(image_path)


def generate_heygen_video(inputs: dict[str, Any]) -> ToolResult:
    import requests

    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        return ToolResult(success=False, error="HEYGEN_API_KEY not set.")

    provider = inputs.get("provider_variant", "veo_3_1")
    if provider not in HEYGEN_PROVIDERS:
        return ToolResult(
            success=False,
            error=f"Unknown provider_variant: {provider}. Available: {', '.join(sorted(HEYGEN_PROVIDERS))}",
        )

    prompt = inputs["prompt"]
    aspect_ratio = inputs.get("aspect_ratio", "16:9")
    operation = inputs.get("operation", "text_to_video")
    workflow_input: dict[str, Any] = {
        "prompt": prompt,
        "provider": provider,
        "aspect_ratio": aspect_ratio,
    }
    if operation == "image_to_video":
        ref_url = inputs.get("reference_image_url")
        ref_path = inputs.get("reference_image_path")
        if ref_path and not ref_url:
            ref_url = upload_image_heygen(ref_path, api_key)
        if not ref_url:
            return ToolResult(
                success=False,
                error="image_to_video requires reference_image_url or reference_image_path",
            )
        workflow_input["reference_image_url"] = ref_url

    response = requests.post(
        "https://api.heygen.com/v1/workflows/executions",
        headers={"X-Api-Key": api_key, "Content-Type": "application/json"},
        json={"workflow_type": "GenerateVideoNode", "input": workflow_input},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    execution_id = payload.get("data", {}).get("execution_id")
    if not execution_id:
        return ToolResult(success=False, error=f"No execution_id in response: {payload}")

    video_url = poll_heygen(execution_id, api_key, timeout=600)
    output_path = Path(inputs.get("output_path", f"heygen_video_{execution_id}.mp4"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    download = requests.get(video_url, timeout=120)
    download.raise_for_status()
    output_path.write_bytes(download.content)

    meta = HEYGEN_PROVIDERS[provider]
    return ToolResult(
        success=True,
        data={
            "provider": "heygen",
            "provider_variant": provider,
            "provider_name": meta["name"],
            "mode": "api",
            "prompt": prompt,
            "aspect_ratio": aspect_ratio,
            "operation": operation,
            "execution_id": execution_id,
            "output": str(output_path),
            "format": "mp4",
        },
        artifacts=[str(output_path)],
        model=provider,
    )


def generate_ltx_modal_video(inputs: dict[str, Any]) -> ToolResult:
    import base64

    import requests

    endpoint_url = os.environ.get("MODAL_LTX2_ENDPOINT_URL")
    if not endpoint_url:
        return ToolResult(success=False, error="MODAL_LTX2_ENDPOINT_URL not set.")

    prompt = inputs["prompt"]
    operation = inputs.get("operation", "text_to_video")
    aspect = inputs.get("aspect_ratio", "16:9")
    width = inputs.get("width")
    height = inputs.get("height")
    if width is None or height is None:
        if aspect == "16:9":
            width, height = 1024, 576
        elif aspect == "9:16":
            width, height = 576, 1024
        else:
            width, height = 512, 512

    num_frames = inputs.get("num_frames", LTX2_FRAME_COUNTS.get(inputs.get("duration_hint", "5s"), 121))
    if (num_frames - 1) % 8 != 0:
        num_frames = ((num_frames - 1) // 8) * 8 + 1

    payload: dict[str, Any] = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "num_frames": num_frames,
        "fps": 24,
        "steps": inputs.get("num_inference_steps", 30),
        "negative_prompt": "worst quality, low quality, blurry, distorted, watermark, text, logo",
    }
    if inputs.get("seed") is not None:
        payload["seed"] = inputs["seed"]

    if operation == "image_to_video":
        ref_path = inputs.get("reference_image_path")
        ref_url = inputs.get("reference_image_url")
        if ref_path:
            payload["input_image"] = base64.b64encode(Path(ref_path).read_bytes()).decode()
        elif ref_url:
            payload["input_image_url"] = ref_url
        else:
            return ToolResult(
                success=False,
                error="image_to_video requires reference_image_url or reference_image_path",
            )

    response = requests.post(endpoint_url, json=payload, timeout=300)
    response.raise_for_status()
    output_path = Path(inputs.get("output_path", "ltx_video_modal.mp4"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    content_type = response.headers.get("content-type", "")
    if "video" in content_type or "octet-stream" in content_type:
        output_path.write_bytes(response.content)
    else:
        response_payload = response.json()
        video_url = response_payload.get("video_url") or response_payload.get("url")
        if not video_url:
            return ToolResult(success=False, error=f"No video data in response: {response_payload}")
        download = requests.get(video_url, timeout=120)
        download.raise_for_status()
        output_path.write_bytes(download.content)

    return ToolResult(
        success=True,
        data={
            "provider": "ltx-modal",
            "provider_name": "LTX-2.3 (Modal)",
            "mode": "modal",
            "prompt": prompt,
            "width": width,
            "height": height,
            "num_frames": num_frames,
            "fps": 24,
            "duration_seconds": round(num_frames / 24, 2),
            "operation": operation,
            "output": str(output_path),
            "format": "mp4",
        },
        artifacts=[str(output_path)],
        seed=inputs.get("seed"),
        model="ltx-2.3",
    )


def probe_output(path: Path) -> dict[str, Any]:
    info: dict[str, Any] = {"file_size_bytes": path.stat().st_size}
    if not shutil.which("ffprobe"):
        return info

    import json

    try:
        proc = subprocess.run(
            [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-show_format",
                "-show_streams",
                str(path),
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        if proc.returncode == 0:
            probe = json.loads(proc.stdout)
            fmt = probe.get("format", {})
            info["duration_seconds"] = float(fmt.get("duration", 0))
            info["file_size_mb"] = round(path.stat().st_size / (1024 * 1024), 2)
            for stream in probe.get("streams", []):
                if stream.get("codec_type") == "video":
                    info["video_width"] = int(stream.get("width", 0))
                    info["video_height"] = int(stream.get("height", 0))
                    info["video_codec"] = stream.get("codec_name", "")
                    break
    except Exception:
        pass
    return info
