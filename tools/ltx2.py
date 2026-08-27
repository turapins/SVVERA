#!/usr/bin/env python3
"""LTX-2.3 video generation CLI.

Thin wrapper around the registered `ltx_video_modal` / `ltx_video_local`
tools (see .agents/skills/ltx2/SKILL.md for the full prompting guide).
Tries Modal first (requires MODAL_LTX2_ENDPOINT_URL), then falls back to
local diffusers-based generation (requires VIDEO_GEN_LOCAL_ENABLED=true
and a GPU) if Modal is not configured.

Usage:
    python3 tools/ltx2.py --prompt "A sunset over the ocean" --output sunset.mp4
    python3 tools/ltx2.py --prompt "Gentle camera drift" --input photo.jpg --output animated.mp4
"""

from __future__ import annotations

import argparse
import sys

from tools.video.ltx_video_local import LTXVideoLocal
from tools.video.ltx_video_modal import LTXVideoModal


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate video clips with LTX-2.3")
    parser.add_argument("--prompt", required=True, help="Text description of the video")
    parser.add_argument("--input", help="Input image path for image-to-video")
    parser.add_argument("--width", type=int, help="Video width (divisible by 64)")
    parser.add_argument("--height", type=int, help="Video height (divisible by 64)")
    parser.add_argument("--num-frames", type=int, dest="num_frames", help="Frame count, (n-1) %% 8 == 0")
    parser.add_argument("--fps", type=int, default=24, help="Frames per second")
    parser.add_argument(
        "--quality",
        choices=["standard", "fast"],
        default="standard",
        help="standard (30 steps) or fast (15 steps)",
    )
    parser.add_argument("--steps", type=int, help="Override inference steps directly")
    parser.add_argument("--seed", type=int, help="Seed for reproducibility")
    parser.add_argument("--output", help="Output file path (default: auto-generated)")
    parser.add_argument("--negative-prompt", dest="negative_prompt", help="What to avoid")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    steps = args.steps if args.steps is not None else (15 if args.quality == "fast" else 30)

    inputs: dict[str, object] = {
        "prompt": args.prompt,
        "operation": "image_to_video" if args.input else "text_to_video",
        "num_inference_steps": steps,
    }
    if args.input:
        inputs["reference_image_path"] = args.input
    if args.width:
        inputs["width"] = args.width
    if args.height:
        inputs["height"] = args.height
    if args.num_frames:
        inputs["num_frames"] = args.num_frames
    if args.seed is not None:
        inputs["seed"] = args.seed
    if args.output:
        inputs["output_path"] = args.output
    if args.negative_prompt:
        inputs["negative_prompt"] = args.negative_prompt

    modal_tool = LTXVideoModal()
    if modal_tool.get_status().value == "available":
        result = modal_tool.execute(inputs)
    else:
        local_tool = LTXVideoLocal()
        if local_tool.get_status().value != "available":
            print(
                "Neither ltx_video_modal nor ltx_video_local is available.\n\n"
                f"Modal setup:\n{modal_tool.install_instructions}\n\n"
                f"Local setup:\n{local_tool.install_instructions}",
                file=sys.stderr,
            )
            return 1
        result = local_tool.execute(inputs)

    if not result.success:
        print(f"Generation failed: {result.error}", file=sys.stderr)
        return 1

    print(f"Wrote video to {result.data.get('output')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
