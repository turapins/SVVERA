---
name: mova
description: Synchronized video+audio generation with MOVA (OpenMOSS) — image-to-video with native speech and lip-sync in a single pass. Use when generating UGC-style talking clips, avatar/spokesperson video, or any content where speech and video must be generated together rather than stitched. Triggers include lip-sync, talking video, speech video, video with voice, avatar video, MOVA.
---

# MOVA Video+Audio Generation

Generate ~8 second video clips **with synchronized speech and lip-sync** from a
reference image + text prompt, using the OpenMOSS/MOVA model.
Runs locally (`torchrun`, self-hosted GPU) or on Modal (A100-80GB).

**Requires a reference image.** MOVA has no text-only mode — this maps
directly onto this project's "always use reference image control" rule
(Rule 2 in `CLAUDE.md`).

## Quick Reference

```bash
# Local (requires MOVA_REPO_PATH + MOVA_CKPT_PATH, see Setup below)
python3 -c "
from tools.video.mova_video_local import MOVAVideoLocal
result = MOVAVideoLocal().execute({
    'prompt': 'A person speaks warmly: \'Welcome to Vocal Image.\'',
    'reference_image_path': 'headshot.png',
    'output_path': 'talking_clip.mp4',
})
print(result.data)
"

# Modal (requires MODAL_MOVA_ENDPOINT_URL)
python3 -c "
from tools.video.mova_video_modal import MOVAVideoModal
result = MOVAVideoModal().execute({
    'prompt': 'A person speaks warmly: \'Welcome to Vocal Image.\'',
    'reference_image_path': 'headshot.png',
    'output_path': 'talking_clip.mp4',
})
print(result.data)
"
```

There is no `tools/mova.py` CLI yet (unlike `tools/ltx2.py`) — call the tool
classes directly, or add one following the same pattern if a CLI is needed.

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `prompt` | (required) | Text description **including the speech/dialogue** to generate |
| `reference_image_path` / `reference_image_url` | (required) | Reference image — single person or multi-person |
| `model_variant` | `mova-360p` | `mova-360p` (faster, less VRAM) or `mova-720p` (higher quality, ~48GB+ VRAM) |
| `width` / `height` | 640×352 (360p) / 1280×720 (720p) | Output resolution |
| `num_frames` | 193 | Frame count (~8s at 24fps) |
| `fps` | 24.0 | Frames per second |
| `num_inference_steps` | 50 | Diffusion sampling iterations |
| `seed` | 42 | Reproducibility |
| `offload` | `group` (local only) | `none` / `cpu` / `group` — trades VRAM for speed |
| `negative_prompt` | sensible default | What to avoid |

## Prompting Guide

Unlike silent b-roll models (LTX-2.3, Wan), the **prompt is also the script**
— MOVA generates its own speech audio from what you write. Put the actual
dialogue in the prompt, in quotes, plus enough visual/scene description to
anchor the video:

```
A confident presenter in a modern studio looks at the camera and says:
"Welcome to Vocal Image — let's fix your voice today." Warm studio lighting,
subtle natural head movement, shallow depth of field.
```

For multi-person scenes, use a multi-person reference image and describe
each speaker's turn in the prompt in order.

## Technical Details

- **Model:** MOVA-360p or MOVA-720p (OpenMOSS-Team, HuggingFace)
- **GPU:** local — 12-48GB VRAM depending on `--offload` mode (layerwise vs
  component-wise); Modal — A100-80GB
- **Inference:** ~35-45s per 8s clip on an RTX 4090 (360p, per upstream README);
  expect similar or better on A100
- **Output:** MP4 with audio muxed in (speech + ambient), no separate TTS step needed
- **License:** Apache-2.0 — free, unrestricted commercial use, no revenue
  threshold (contrast with LTX-2.3's $10M ARR community-license cutoff, see
  `.agents/skills/ltx2/SKILL.md`)

### Known Limitations

- **No text-only mode.** A reference image is always required.
- **Not vetted for silent b-roll.** If you need atmospheric motion without
  speech, use LTX-2.3, Wan, or HunyuanVideo instead — don't force MOVA into
  that role just because it's installed.
- **Falling back to another video tool loses lip-sync/audio.** If MOVA is
  unavailable, `fallback_tools` route to a silent-video generator or HeyGen —
  the agent must say so explicitly, not silently swap and hope no one notices
  the missing voice (see AGENT_GUIDE.md "Do not hide degraded paths").
- **Local generation is a subprocess (torchrun), not an in-process pipeline.**
  Slower to iterate on than diffusers-based tools since each call launches a
  fresh process; there's no persistent-pipeline "warm" mode in this
  integration yet.

## Setup

> **Status:** this integration (tool wrappers, Modal app, this skill doc) was
> authored to match the upstream MOVA README but has not been run end-to-end
> against real GPU infra. Validate `torchrun`/`modal deploy` actually complete
> a generation before relying on it in production.

### Local

```bash
# 1. Clone and install MOVA
git clone https://github.com/OpenMOSS/MOVA.git
cd MOVA
conda create -n mova python=3.13 -y && conda activate mova
pip install -e .

# 2. Download a checkpoint
hf download OpenMOSS-Team/MOVA-360p --local-dir ../MOVA-360p

# 3. Point the tool at both paths
export VIDEO_GEN_LOCAL_ENABLED=true
export MOVA_REPO_PATH=/path/to/MOVA
export MOVA_CKPT_PATH=/path/to/MOVA-360p

# 4. Test
python3 -c "
from tools.video.mova_video_local import MOVAVideoLocal
print(MOVAVideoLocal().get_status())
"
```

### Modal

```bash
# 1. Create Modal secret for HuggingFace (one-time; shared with the LTX-2.3 app)
modal secret create huggingface-token HF_TOKEN=hf_your_token

# 2. Deploy (clones MOVA + downloads checkpoint on first real call, cached in a Modal Volume)
modal deploy docker/modal-mova/app.py

# 3. Save endpoint URL to .env
echo "MODAL_MOVA_ENDPOINT_URL=https://yourname--video-toolkit-mova-mova-generate.modal.run" >> .env
```
