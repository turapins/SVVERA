"""Modal deployment for LTX-2.3 (Lightricks) video generation.

Exposes a web endpoint that `tools/video/_shared.py::generate_ltx_modal_video`
calls via MODAL_LTX2_ENDPOINT_URL. See skills/ltx2/SKILL.md for the setup and
usage flow (`modal deploy docker/modal-ltx2/app.py`).

Request payload (JSON), matches generate_ltx_modal_video's payload builder:
    prompt: str (required)
    width, height: int
    num_frames: int          # (n - 1) % 8 == 0
    fps: int
    steps: int               # num_inference_steps
    negative_prompt: str
    seed: int (optional)
    input_image: str (optional, base64)       # image-to-video
    input_image_url: str (optional)           # image-to-video

Response: raw MP4 bytes (content-type video/mp4).

NOTE: diffusers' native LTX-2.3 pipeline support was still rolling out as of
this writing (LTX2Pipeline / LTX2ImageToVideoPipeline exist for LTX-2; the
diffusers-converted LTX-2.3 weights live at `diffusers/LTX-2.3-Diffusers`).
This app has not been run end-to-end against real Modal/GPU infrastructure —
treat it as a first deploy candidate and verify `pip install` versions
resolve before relying on it in production. If the pinned diffusers version
does not yet expose LTX-2.3 support, either bump the diffusers version below
or point MODEL_ID back at "Lightricks/LTX-2" as a fallback.
"""

from __future__ import annotations

import io
import os

import modal

MODEL_ID = os.environ.get("LTX2_MODEL_ID", "diffusers/LTX-2.3-Diffusers")
GPU_TYPE = os.environ.get("LTX2_GPU_TYPE", "A100-80GB")

app = modal.App("video-toolkit-ltx2")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("ffmpeg")
    .pip_install(
        "torch>=2.4",
        "diffusers>=0.32",
        "transformers>=4.46",
        "accelerate>=1.0",
        "sentencepiece",
        "imageio",
        "imageio-ffmpeg",
        "pillow",
        "requests",
        "fastapi[standard]",
    )
)

hf_secret = modal.Secret.from_name("huggingface-token")


@app.cls(
    image=image,
    gpu=GPU_TYPE,
    secrets=[hf_secret],
    scaledown_window=300,
    timeout=600,
)
class LTX2Model:
    @modal.enter()
    def load(self) -> None:
        import torch
        from diffusers import LTX2ImageToVideoPipeline, LTX2Pipeline

        dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16

        self.t2v_pipeline = LTX2Pipeline.from_pretrained(MODEL_ID, torch_dtype=dtype)
        self.t2v_pipeline.to("cuda")
        self.t2v_pipeline.enable_model_cpu_offload()

        self.i2v_pipeline = LTX2ImageToVideoPipeline.from_pretrained(MODEL_ID, torch_dtype=dtype)
        self.i2v_pipeline.to("cuda")
        self.i2v_pipeline.enable_model_cpu_offload()

    @modal.method()
    def generate(self, payload: dict) -> bytes:
        import base64

        import requests
        import torch
        from diffusers.utils import export_to_video
        from PIL import Image

        prompt = payload["prompt"]
        width = payload.get("width", 1024)
        height = payload.get("height", 576)
        num_frames = payload.get("num_frames", 121)
        fps = payload.get("fps", 24)
        steps = payload.get("steps", 30)
        negative_prompt = payload.get(
            "negative_prompt",
            "worst quality, low quality, blurry, distorted, watermark, text, logo",
        )
        seed = payload.get("seed")
        generator = torch.Generator(device="cpu").manual_seed(seed) if seed is not None else None

        input_image_b64 = payload.get("input_image")
        input_image_url = payload.get("input_image_url")

        generation_kwargs = {
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "width": width,
            "height": height,
            "num_frames": num_frames,
            "num_inference_steps": steps,
        }
        if generator is not None:
            generation_kwargs["generator"] = generator

        if input_image_b64 or input_image_url:
            if input_image_b64:
                image = Image.open(io.BytesIO(base64.b64decode(input_image_b64))).convert("RGB")
            else:
                resp = requests.get(input_image_url, timeout=60)
                resp.raise_for_status()
                image = Image.open(io.BytesIO(resp.content)).convert("RGB")
            image = image.resize((width, height), Image.LANCZOS)
            generation_kwargs["image"] = image
            output = self.i2v_pipeline(**generation_kwargs)
        else:
            output = self.t2v_pipeline(**generation_kwargs)

        frames = output.frames[0] if hasattr(output, "frames") else output.images

        video_path = "/tmp/ltx2_output.mp4"
        export_to_video(frames, video_path, fps=fps)
        with open(video_path, "rb") as handle:
            return handle.read()


@app.function(image=image, timeout=600)
@modal.fastapi_endpoint(method="POST")
def ltx2_generate(payload: dict):
    from fastapi import Response

    video_bytes = LTX2Model().generate.remote(payload)
    return Response(content=video_bytes, media_type="video/mp4")
