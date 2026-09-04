"""Competitor ad intelligence via Atria's Ad Library API (https://www.tryatria.com/api)."""

from __future__ import annotations

import os
import time
from typing import Any

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


class AtriaAdIntel(BaseTool):
    name = "atria_ad_intel"
    version = "0.1.0"
    tier = ToolTier.ANALYZE
    capability = "ad_intelligence"
    provider = "atria"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set ATRIA_API_KEY to your Atria API key (prefix atria-sk_).\n"
        "  Get one at https://www.tryatria.com/api"
    )
    agent_skills = []

    capabilities = ["search_competitor_ads", "ad_library_search"]
    supports = {
        "order_by_longevity": True,
        "order_by_impressions": True,
        "platform_filter": True,
        "language_filter": True,
    }
    best_for = [
        "finding longest-running competitor ads (proxy for winning creative)",
        "finding highest-impression competitor ads",
        "pulling reference creative before scripting a new Vocal Image ad",
    ]
    not_good_for = [
        "exact spend/ROAS figures (Atria's open API does not expose these)",
        "non-Meta platforms",
    ]
    fallback_tools = []

    input_schema = {
        "type": "object",
        "required": ["query"],
        "properties": {
            "query": {
                "type": "string",
                "description": "Search term, e.g. brand name or category keyword",
            },
            "platform": {
                "type": "string",
                "default": "facebook",
                "description": "Ad platform to search (e.g. facebook, instagram)",
            },
            "status": {
                "type": "string",
                "enum": ["active", "inactive", "all"],
                "default": "active",
            },
            "order": {
                "type": "string",
                "enum": ["newest", "oldest", "most_active", "best_match", "longevity"],
                "default": "most_active",
                "description": (
                    "Atria native sort (newest/oldest/most_active/best_match). "
                    "'longevity' is a client-side post-sort by (end_date - start_date), "
                    "since Atria's open API exposes no direct impressions field."
                ),
            },
            "language": {
                "type": "string",
                "default": "en",
                "description": "ISO language code filter, e.g. 'en'",
            },
            "page_size": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100},
            "page": {"type": "integer", "default": 1},
            "download_media": {
                "type": "boolean",
                "default": False,
                "description": (
                    "If true, download each ad's first image and/or first video "
                    "to output_dir and attach local_image_path/local_video_path."
                ),
            },
            "output_dir": {
                "type": "string",
                "description": "Directory to save downloaded creative files under (required if download_media=true)",
            },
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=128, vram_mb=0, disk_mb=0, network_required=True
    )
    retry_policy = RetryPolicy(max_retries=2, retryable_errors=["rate_limit", "timeout"])
    idempotency_key_fields = ["query", "platform", "status", "order", "language", "page"]
    side_effects = ["calls Atria ad-library API", "optionally writes creative files to output_dir"]
    user_visible_verification = [
        "Cross-check returned ad IDs/links against the platform's own ad library UI"
    ]

    BASE_URL = "https://api.tryatria.com"

    def get_status(self) -> ToolStatus:
        if os.environ.get("ATRIA_API_KEY"):
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        return 0.0

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = os.environ.get("ATRIA_API_KEY")
        if not api_key:
            return ToolResult(
                success=False,
                error="ATRIA_API_KEY not set. " + self.install_instructions,
            )

        import re
        import requests
        from datetime import datetime, timezone
        from pathlib import Path
        from urllib.parse import urlparse

        start = time.time()
        requested_order = inputs.get("order", "most_active")
        # Atria's open API has no "longevity" sort — fetch its most-active
        # ranking, then re-sort client-side by observed running duration.
        api_order = "most_active" if requested_order == "longevity" else requested_order

        params: dict[str, Any] = {
            "query": inputs["query"],
            "platform": inputs.get("platform", "facebook"),
            "status": inputs.get("status", "active"),
            "order": api_order,
            "language": inputs.get("language", "en"),
            "page_size": inputs.get("page_size", 20),
            "page": inputs.get("page", 1),
        }

        try:
            response = requests.get(
                f"{self.BASE_URL}/open/v1/ad-library/search",
                headers={"X-API-Key": api_key},
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
        except Exception as e:
            return ToolResult(success=False, error=f"Atria ad-library search failed: {e}")

        if payload.get("code"):
            return ToolResult(
                success=False,
                error=f"Atria API error {payload['code']}: {payload.get('message')}",
            )

        ads = (payload.get("data") or {}).get("items", [])

        def _running_days(ad: dict[str, Any]) -> float:
            start_raw = ad.get("start_date")
            if not start_raw:
                return 0.0
            end_raw = ad.get("end_date")
            try:
                start_dt = datetime.fromisoformat(start_raw).replace(tzinfo=None)
                end_dt = (
                    datetime.fromisoformat(end_raw).replace(tzinfo=None)
                    if end_raw
                    else datetime.now(timezone.utc).replace(tzinfo=None)
                )
            except ValueError:
                return 0.0
            return (end_dt - start_dt).total_seconds() / 86400

        for ad in ads:
            ad["running_days"] = round(_running_days(ad), 1)

        if requested_order == "longevity":
            ads.sort(key=lambda a: a["running_days"], reverse=True)

        artifacts: list[str] = []

        if inputs.get("download_media"):
            if not inputs.get("output_dir"):
                return ToolResult(
                    success=False,
                    error="output_dir is required when download_media=true",
                )
            output_root = Path(inputs["output_dir"])

            def _slug(text: str) -> str:
                text = re.sub(r"[^a-zA-Z0-9]+", "_", text or "unknown_brand").strip("_")
                return text.lower() or "unknown_brand"

            def _ext_from_url(url: str, default: str) -> str:
                suffix = Path(urlparse(url).path).suffix
                return suffix if suffix else default

            def _download(url: str, dest: Path) -> bool:
                try:
                    resp = requests.get(url, timeout=120)
                    resp.raise_for_status()
                except Exception:
                    return False
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(resp.content)
                return True

            for ad in ads:
                brand_dir = output_root / _slug(ad.get("brand_name"))
                ad_id = ad.get("id", "unknown")

                images = ad.get("images") or []
                if images and images[0].get("url"):
                    ext = _ext_from_url(images[0]["url"], ".jpg")
                    dest = brand_dir / f"{ad_id}{ext}"
                    if _download(images[0]["url"], dest):
                        ad["local_image_path"] = str(dest)
                        artifacts.append(str(dest))

                videos = ad.get("videos") or []
                if videos and videos[0].get("url"):
                    ext = _ext_from_url(videos[0]["url"], ".mp4")
                    dest = brand_dir / f"{ad_id}{ext}"
                    if _download(videos[0]["url"], dest):
                        ad["local_video_path"] = str(dest)
                        artifacts.append(str(dest))

        return ToolResult(
            success=True,
            data={
                "provider": "atria",
                "query": inputs["query"],
                "requested_order": requested_order,
                "api_order_used": api_order,
                "results_returned": len(ads),
                "ads": ads,
            },
            artifacts=artifacts,
            cost_usd=0.0,
            duration_seconds=round(time.time() - start, 2),
        )
