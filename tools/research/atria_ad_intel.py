"""Atria AI — competitor ad library search.

Run this before producing a paid ad to research what competitors are currently running.

API: GET https://api.tryatria.com/open/v1/ad-library/search
Auth: X-API-Key header
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any

import requests

from tools.base_tool import (
    BaseTool,
    ResourceProfile,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolTier,
)


class AtriaAdIntel(BaseTool):
    name = "atria_ad_intel"
    version = "0.1.0"
    tier = ToolTier.ANALYZE
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "research"
    provider = "atria"

    dependencies = ["env:ATRIA_API_KEY"]
    install_instructions = (
        "Set ATRIA_API_KEY. Get your key at app.tryatria.com → Settings → API Keys."
    )

    resource_profile = ResourceProfile(network_required=True)
    side_effects = []
    best_for = [
        "research competitor ads before production",
        "find top performing hooks on Facebook/TikTok/Instagram",
        "competitive intelligence for paid ads",
        "discover what ad formats work in the edtech/coaching space",
    ]
    agent_skills = ["ads", "ad-creative"]

    _API_BASE = "https://api.tryatria.com"

    def _headers(self) -> dict[str, str]:
        return {"X-API-Key": os.environ["ATRIA_API_KEY"]}

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()

        platform = inputs.get("platform", "facebook")
        status = inputs.get("status", "active")
        order = inputs.get("order", "newest")
        page_size = min(int(inputs.get("page_size", 10)), 50)
        brand_name = inputs.get("brand_name")
        save_to = inputs.get("save_to")

        params: dict[str, Any] = {
            "platform": platform,
            "status": status,
            "order": order,
            "page_size": page_size,
        }
        if brand_name:
            params["brand_name"] = brand_name

        try:
            resp = requests.get(
                f"{self._API_BASE}/open/v1/ad-library/search",
                headers=self._headers(),
                params=params,
                timeout=30,
            )
            resp.raise_for_status()
            raw = resp.json()

            items_raw = raw.get("items", raw.get("data", raw.get("results", [])))
            items = [
                {
                    "id": item.get("id", ""),
                    "brand_name": item.get("brand_name", item.get("advertiser", "")),
                    "display_format": item.get("display_format", item.get("format", "")),
                    "title": item.get("title", item.get("ad_text", item.get("body", ""))[:120] if item.get("ad_text") or item.get("body") else ""),
                    "start_date": item.get("start_date", item.get("started_running", "")),
                    "platform": item.get("platform", platform),
                }
                for item in items_raw
            ]

            if save_to:
                output_path = Path(save_to)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as fh:
                    json.dump({"platform": platform, "items": items}, fh, indent=2, ensure_ascii=False)

            return ToolResult(
                success=True,
                data={
                    "items": items,
                    "total": len(items),
                    "platform": platform,
                    "status_filter": status,
                    "order": order,
                },
                artifacts=[save_to] if save_to else [],
                duration_seconds=time.time() - start,
            )

        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"Atria API {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
                duration_seconds=time.time() - start,
            )
