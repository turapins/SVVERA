"""Pinterest reference search — find visual inspiration and character ideas.

Used when writing scripts and building visual briefs:
  1. No character in /Characters database → search Pinterest for visual types
  2. Need reference image for a specific scene/vibe/color palette

Pinterest API v5: https://developers.pinterest.com/docs/api/v5/
Auth: Bearer token (env: PINTEREST_ACCESS_TOKEN)

Endpoints used:
  GET /v5/search/pins/       — keyword search for pins
  GET /v5/pins/{pin_id}      — pin detail (full image URL, description)
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


class PinterestReference(BaseTool):
    name = "pinterest_reference"
    version = "0.1.0"
    tier = ToolTier.SOURCE
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "research"
    provider = "pinterest"

    dependencies = ["env:PINTEREST_ACCESS_TOKEN"]
    install_instructions = (
        "Set PINTEREST_ACCESS_TOKEN. "
        "Create an app at developers.pinterest.com → My Apps → Create App. "
        "Generate an access token with scopes: boards:read, pins:read."
    )

    resource_profile = ResourceProfile(network_required=True)
    side_effects = []
    best_for = [
        "find character visual reference when Characters database is empty",
        "search visual inspiration for a specific scene or vibe",
        "find color palette and composition references for script visual brief",
        "discover background/location aesthetics",
    ]
    agent_skills = []

    _API_BASE = "https://api.pinterest.com/v5"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {os.environ['PINTEREST_ACCESS_TOKEN']}",
            "Content-Type": "application/json",
        }

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        action = inputs.get("action", "search")

        if action == "search":
            return self._search(inputs, start)
        elif action == "get_pin":
            return self._get_pin(inputs, start)
        else:
            return ToolResult(
                success=False,
                error="'action' must be one of: search, get_pin",
            )

    def _search(self, inputs: dict[str, Any], start: float) -> ToolResult:
        query = inputs.get("query")
        if not query:
            return ToolResult(success=False, error="'query' required")

        page_size = min(int(inputs.get("page_size", 10)), 25)
        save_to = inputs.get("save_to")

        try:
            resp = requests.get(
                f"{self._API_BASE}/search/pins/",
                headers=self._headers(),
                params={"query": query, "page_size": page_size},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items", [])
            pins = []
            for pin in items:
                media = pin.get("media", {})
                images = media.get("images", {})
                # Prefer highest resolution available
                image_url = (
                    (images.get("1200x") or images.get("750x") or images.get("600x") or {})
                    .get("url", "")
                )
                pins.append({
                    "pin_id": pin.get("id", ""),
                    "title": pin.get("title", ""),
                    "description": (pin.get("description", "") or "")[:200],
                    "image_url": image_url,
                    "pin_url": f"https://pinterest.com/pin/{pin.get('id', '')}",
                    "board_id": pin.get("board_id", ""),
                })

            if save_to:
                output_path = Path(save_to)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "w", encoding="utf-8") as fh:
                    json.dump({"query": query, "pins": pins}, fh, indent=2, ensure_ascii=False)

            return ToolResult(
                success=True,
                data={
                    "pins": pins,
                    "total": len(pins),
                    "query": query,
                    "next_bookmark": data.get("bookmark"),
                },
                artifacts=[save_to] if save_to else [],
                duration_seconds=time.time() - start,
            )

        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"Pinterest API {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
                duration_seconds=time.time() - start,
            )

    def _get_pin(self, inputs: dict[str, Any], start: float) -> ToolResult:
        pin_id = inputs.get("pin_id")
        if not pin_id:
            return ToolResult(success=False, error="'pin_id' required")

        try:
            resp = requests.get(
                f"{self._API_BASE}/pins/{pin_id}",
                headers=self._headers(),
                timeout=15,
            )
            resp.raise_for_status()
            pin = resp.json()

            media = pin.get("media", {})
            images = media.get("images", {})
            image_url = (
                (images.get("1200x") or images.get("750x") or images.get("600x") or {})
                .get("url", "")
            )

            return ToolResult(
                success=True,
                data={
                    "pin_id": pin.get("id"),
                    "title": pin.get("title", ""),
                    "description": pin.get("description", ""),
                    "image_url": image_url,
                    "pin_url": f"https://pinterest.com/pin/{pin.get('id')}",
                    "link": pin.get("link", ""),
                },
                duration_seconds=time.time() - start,
            )

        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"Pinterest API {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
                duration_seconds=time.time() - start,
            )
