"""Pinterest reference lookup — search/read from YOUR OWN Pinterest account.

IMPORTANT SCOPE NOTE: Pinterest's public API has no general "search all of
Pinterest" endpoint for third-party apps. `GET /v5/search/pins` (used below)
only searches pins already saved/owned by the authenticated account — not
the public platform. So this tool only surfaces what Ivan has already
pinned/curated on his own Pinterest account; it cannot discover new
character/visual references from the wider platform.

For actual discovery of new public Pinterest content, use
tools/research/pinterest_browser_search.py instead, which drives a live
logged-in browser session (the only way Pinterest's API model supports
finding content you don't already own).

`search/partner/pins` also exists but is beta/partner-gated — not available
without a separate Pinterest partnership approval; not used here.

Pinterest API v5: https://developers.pinterest.com/docs/api/v5/
Auth: Bearer token (env: PINTEREST_ACCESS_TOKEN)

Endpoints used:
  GET /v5/search/pins    — search the account's OWN saved pins (not public search)
  GET /v5/search/boards  — search the account's OWN boards
  GET /v5/pins/{pin_id}  — pin detail (full image URL, description)
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
    version = "0.2.0"
    tier = ToolTier.SOURCE
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "visual_reference"
    provider = "pinterest"

    dependencies = ["env:PINTEREST_ACCESS_TOKEN"]
    install_instructions = (
        "Set PINTEREST_ACCESS_TOKEN (and PINTEREST_REFRESH_TOKEN). "
        "Create an app at developers.pinterest.com -> My Apps -> Create App, "
        "set PINTEREST_APP_ID/PINTEREST_APP_SECRET in .env, then run "
        "`python3 scripts/pinterest_auth.py` once to complete OAuth."
    )

    resource_profile = ResourceProfile(network_required=True)
    side_effects = []
    best_for = [
        "re-find a character reference already saved to Ivan's own Pinterest boards",
        "pull full image URL / description for a specific pin_id",
    ]
    not_good_for = [
        "discovering NEW visual references from the public platform — the API cannot do this, "
        "use pinterest_browser_search for that",
    ]
    fallback_tools = ["pinterest_browser_search"]
    agent_skills = []

    _API_BASE = "https://api.pinterest.com/v5"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {os.environ['PINTEREST_ACCESS_TOKEN']}",
            "Content-Type": "application/json",
        }

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        action = inputs.get("action", "search_own_pins")

        if action == "search_own_pins":
            return self._search_own_pins(inputs, start)
        elif action == "search_own_boards":
            return self._search_own_boards(inputs, start)
        elif action == "get_pin":
            return self._get_pin(inputs, start)
        else:
            return ToolResult(
                success=False,
                error="'action' must be one of: search_own_pins, search_own_boards, get_pin",
            )

    def _search_own_pins(self, inputs: dict[str, Any], start: float) -> ToolResult:
        query = inputs.get("query")
        if not query:
            return ToolResult(success=False, error="'query' required")

        save_to = inputs.get("save_to")

        try:
            resp = requests.get(
                f"{self._API_BASE}/search/pins",
                headers=self._headers(),
                params={"query": query},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items", [])
            pins = []
            for pin in items:
                media = pin.get("media", {})
                images = media.get("images", {})
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
                    "scope": "account's own saved pins only, not public Pinterest",
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
            return ToolResult(success=False, error=str(exc), duration_seconds=time.time() - start)

    def _search_own_boards(self, inputs: dict[str, Any], start: float) -> ToolResult:
        query = inputs.get("query")

        try:
            params: dict[str, Any] = {}
            if query:
                params["query"] = query
            resp = requests.get(
                f"{self._API_BASE}/search/boards",
                headers=self._headers(),
                params=params,
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            boards = [
                {
                    "board_id": b.get("id", ""),
                    "name": b.get("name", ""),
                    "description": b.get("description", ""),
                    "privacy": b.get("privacy", ""),
                    "pin_count": b.get("pin_count", 0),
                }
                for b in data.get("items", [])
            ]

            return ToolResult(
                success=True,
                data={"boards": boards, "total": len(boards)},
                duration_seconds=time.time() - start,
            )

        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"Pinterest API {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc), duration_seconds=time.time() - start)

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
                    "board_id": pin.get("board_id", ""),
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
            return ToolResult(success=False, error=str(exc), duration_seconds=time.time() - start)
