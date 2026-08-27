"""Modal deployment for MOVA (OpenMOSS) synchronized video+audio generation.

Exposes a web endpoint that `tools/video/_shared.py::generate_mova_modal_video`
calls via MODAL_MOVA_ENDPOINT_URL. See skills/mova/SKILL.md for setup/usage
(`modal deploy docker/modal-mova/app.py`).

Unlike the LTX-2.3 Modal app (docker/modal-ltx2/app.py), MOVA has no
pip-installable pipeline class — it ships as a standalone repo invoked via
`torchrun scripts/inference_single.py`. This app clones that repo at image
build time and shells out to the same CLI inside the container, mirroring
tools/video/_shared.py::generate_mova_local_video.

Request payload (JSON), matches generate_mova_modal_video's payload builder:
    prompt: str (required)
    model_variant: "mova-360p" | "mova-720p"
    width, height: int
    num_frames: int
    fps: float
    num_inference_steps: int
    seed: int
    negative_prompt: str (optional)
    ref_image: str (base64, image-to-video reference — required, MOVA has no
                    text-only mode)
    ref_image_url: str (alternative to ref_image)

Response: raw MP4 bytes (content-type video/mp4), audio muxed in by MOVA itself.

NOTE: this app has not been run end-to-end against real Modal/GPU infra.
Checkpoint downloads (~tens of GB) are cached on a persistent Modal Volume so
repeated cold starts don't re-download; the first deploy will be slow.
"""

from __future__ import annotations

import os

import modal

MODEL_VARIANT_TO_HF_ID = {
    "mova-360p": "OpenMOSS-Team/MOVA-360p",
    "mova-720p": "OpenMOSS-Team/MOVA-720p",
}
GPU_TYPE = os.environ.get("MOVA_GPU_TYPE", "A100-80GB")

app = modal.App("video-toolkit-mova")

checkpoint_volume = modal.Volume.from_name("mova-checkpoints", create_if_missing=True)
CKPT_ROOT = "/checkpoints"

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("git", "ffmpeg")
    .run_commands(
        "git clone --depth 1 https://github.com/OpenMOSS/MOVA.git /opt/mova",
        "pip install -e /opt/mova",
    )
    .pip_install("huggingface_hub", "fastapi[standard]")
)

hf_secret = modal.Secret.from_name("huggingface-token")


@app.function(
    image=image,
    gpu=GPU_TYPE,
    secrets=[hf_secret],
    volumes={CKPT_ROOT: checkpoint_volume},
    scaledown_window=300,
    timeout=1800,
)
def ensure_checkpoint(model_variant: str) -> str:
    from huggingface_hub import snapshot_download

    hf_id = MODEL_VARIANT_TO_HF_ID[model_variant]
    local_dir = f"{CKPT_ROOT}/{model_variant}"
    if not os.path.isdir(local_dir) or not os.listdir(local_dir):
        snapshot_download(repo_id=hf_id, local_dir=local_dir)
        checkpoint_volume.commit()
    return local_dir


@app.function(
    image=image,
    gpu=GPU_TYPE,
    secrets=[hf_secret],
    volumes={CKPT_ROOT: checkpoint_volume},
    scaledown_window=300,
    timeout=1800,
)
def generate(payload: dict) -> bytes:
    import base64
    import subprocess
    import tempfile
    from pathlib import Path

    import requests

    model_variant = payload.get("model_variant", "mova-360p")
    ckpt_path = ensure_checkpoint.local(model_variant)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp = Path(tmp_dir)

        ref_b64 = payload.get("ref_image")
        ref_url = payload.get("ref_image_url")
        ref_path = tmp / "ref.png"
        if ref_b64:
            ref_path.write_bytes(base64.b64decode(ref_b64))
        elif ref_url:
            resp = requests.get(ref_url, timeout=60)
            resp.raise_for_status()
            ref_path.write_bytes(resp.content)
        else:
            raise ValueError("ref_image or ref_image_url is required — MOVA has no text-only mode.")

        output_path = tmp / "output.mp4"
        cmd = [
            "torchrun",
            "--nproc_per_node=1",
            "scripts/inference_single.py",
            "--ckpt_path", ckpt_path,
            "--prompt", payload["prompt"],
            "--ref_path", str(ref_path),
            "--output_path", str(output_path),
            "--height", str(payload.get("height", 352)),
            "--width", str(payload.get("width", 640)),
            "--num_frames", str(payload.get("num_frames", 193)),
            "--fps", str(payload.get("fps", 24.0)),
            "--seed", str(payload.get("seed", 42)),
            "--num_inference_steps", str(payload.get("num_inference_steps", 50)),
            "--offload", "group",
        ]
        if payload.get("negative_prompt"):
            cmd += ["--negative_prompt", payload["negative_prompt"]]

        proc = subprocess.run(cmd, cwd="/opt/mova", capture_output=True, text=True, timeout=1700, check=False)
        if proc.returncode != 0:
            raise RuntimeError(f"MOVA inference failed (exit {proc.returncode}): {proc.stderr[-4000:]}")
        if not output_path.exists():
            raise RuntimeError("MOVA reported success but produced no output file")

        return output_path.read_bytes()


@app.function(image=image, timeout=1800)
@modal.fastapi_endpoint(method="POST")
def mova_generate(payload: dict):
    from fastapi import Response

    video_bytes = generate.remote(payload)
    return Response(content=video_bytes, media_type="video/mp4")
