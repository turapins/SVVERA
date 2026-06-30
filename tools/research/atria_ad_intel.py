"""Atria AI — competitor ad intelligence.

Actions:
  search_ads      — ad library search by platform / brand / status / order
  followed_brands — list brands you follow in Atria (your competitor watchlist)
  boards          — list your saved ad boards

API base: https://api.tryatria.com
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
    version = "0.2.0"
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
        "find longest-running (highest-spend) competitor ads on Facebook/TikTok",
        "list followed competitor brands from your Atria watchlist",
        "browse saved ad boards for inspiration",
        "competitive intelligence for paid ads in edtech/coaching",
    ]
    agent_skills = ["ads", "ad-creative"]

    _API_BASE = "https://api.tryatria.com"

    # Valid order values accepted by the ad-library search endpoint
    _VALID_ORDERS = {"newest", "oldest", "longest_running", "most_ads", "ad_volume"}

    def _headers(self) -> dict[str, str]:
        return {"X-API-Key": os.environ["ATRIA_API_KEY"]}

    def _get(self, path: str, params: dict | None = None) -> Any:
        resp = requests.get(
            f"{self._API_BASE}{path}",
            headers=self._headers(),
            params=params or {},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------ #
    # action: search_ads                                                   #
    # ------------------------------------------------------------------ #
    def _search_ads(self, inputs: dict[str, Any]) -> dict[str, Any]:
        platform = inputs.get("platform", "facebook")
        status = inputs.get("status", "active")
        order = inputs.get("order", "longest_running")
        if order not in self._VALID_ORDERS:
            order = "longest_running"
        page_size = min(int(inputs.get("page_size", 10)), 50)
        brand_name = inputs.get("brand_name")

        params: dict[str, Any] = {
            "platform": platform,
            "status": status,
            "order": order,
            "page_size": page_size,
        }
        if brand_name:
            params["brand_name"] = brand_name

        raw = self._get("/open/v1/ad-library/search", params)
        items_raw = raw.get("items", raw.get("data", raw.get("results", [])))
        items = [
            {
                "id": item.get("id", ""),
                "brand_name": item.get("brand_name", item.get("advertiser", "")),
                "display_format": item.get("display_format", item.get("format", "")),
                "title": (item.get("ad_text") or item.get("body") or item.get("title") or "")[:120],
                "start_date": item.get("start_date", item.get("started_running", "")),
                "platform": item.get("platform", platform),
            }
            for item in items_raw
        ]
        return {"action": "search_ads", "items": items, "total": len(items), "platform": platform, "order": order}

    # ------------------------------------------------------------------ #
    # action: followed_brands                                              #
    # ------------------------------------------------------------------ #
    def _followed_brands(self, inputs: dict[str, Any]) -> dict[str, Any]:
        page_size = min(int(inputs.get("page_size", 50)), 100)
        raw = self._get("/open/v1/brand-library/followed", {"page_size": page_size})
        brands_raw = raw.get("items", raw.get("data", raw.get("brands", raw if isinstance(raw, list) else [])))
        brands = [
            {
                "id": b.get("id", ""),
                "name": b.get("name", b.get("brand_name", "")),
                "platform": b.get("platform", ""),
                "total_ads": b.get("total_ads", b.get("ad_count", "")),
                "website": b.get("website", b.get("url", "")),
            }
            for b in (brands_raw if isinstance(brands_raw, list) else [])
        ]
        return {"action": "followed_brands", "brands": brands, "total": len(brands)}

    # ------------------------------------------------------------------ #
    # action: boards                                                       #
    # ------------------------------------------------------------------ #
    def _boards(self, inputs: dict[str, Any]) -> dict[str, Any]:
        raw = self._get("/open/v1/boards")
        boards_raw = raw.get("items", raw.get("data", raw.get("boards", raw if isinstance(raw, list) else [])))
        boards = [
            {
                "id": b.get("id", ""),
                "name": b.get("name", b.get("title", "")),
                "ad_count": b.get("ad_count", b.get("total_ads", "")),
                "created_at": b.get("created_at", ""),
            }
            for b in (boards_raw if isinstance(boards_raw, list) else [])
        ]
        return {"action": "boards", "boards": boards, "total": len(boards)}

    # ------------------------------------------------------------------ #
    # main entrypoint                                                      #
    # ------------------------------------------------------------------ #
    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        action = inputs.get("action", "search_ads")
        save_to = inputs.get("save_to")

        try:
            if action == "followed_brands":
                data = self._followed_brands(inputs)
            elif action == "boards":
                data = self._boards(inputs)
            else:
                data = self._search_ads(inputs)

            if save_to:
                output_path = Path(save_to)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as fh:
                    json.dump(data, fh, indent=2, ensure_ascii=False)

            return ToolResult(
                success=True,
                data=data,
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
