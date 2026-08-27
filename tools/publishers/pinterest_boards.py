"""Pinterest boards + pins — build a visual character/reference database.

This is the part of Pinterest's v5 API that genuinely works as a database:
creating boards and pins under Vocal Image's own authenticated account.
`boards_create` / `pins_create` are real, unrestricted endpoints — no beta
gate, no partner approval needed.

IMPORTANT — Pinterest's own policy on pins_create: it is documented as
"intended solely for publishing new content created by the user," not for
re-hosting pins/images found elsewhere ("curated content" — Pinterest asks
that you use the in-app Save button for that instead). So:
  - Use create_pin here for Vocal Image's OWN original images — e.g. a
    Higgsfield-generated character portrait, a frame from a produced ad,
    an asset already hosted on Drive/CDN.
  - Use tools/research/pinterest_browser_search.py (Save button, in-browser)
    to curate someone else's pin onto a board instead of re-uploading it
    via this tool.

Pinterest API v5: https://developers.pinterest.com/docs/api/v5/
Auth: Bearer token (env: PINTEREST_ACCESS_TOKEN)

Endpoints used:
  POST /v5/boards           — create a board
  GET  /v5/boards           — list the account's boards
  POST /v5/pins             — create a pin (image_url media source)
  GET  /v5/boards/{id}/pins — list pins on a board
"""

from __future__ import annotations

import os
import time
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


class PinterestBoards(BaseTool):
    name = "pinterest_boards"
    version = "0.1.0"
    tier = ToolTier.PUBLISH
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "board_publish"
    provider = "pinterest"

    dependencies = ["env:PINTEREST_ACCESS_TOKEN"]
    install_instructions = (
        "Set PINTEREST_ACCESS_TOKEN (and PINTEREST_REFRESH_TOKEN). "
        "Create an app at developers.pinterest.com -> My Apps -> Create App, "
        "set PINTEREST_APP_ID/PINTEREST_APP_SECRET in .env, then run "
        "`python3 scripts/pinterest_auth.py` once to complete OAuth with "
        "boards:write and pins:write scopes."
    )

    resource_profile = ResourceProfile(network_required=True)
    side_effects = ["creates real boards/pins on Ivan's live Pinterest account"]
    best_for = [
        "building a persistent visual database of characters (one board, one pin per character/variant)",
        "publishing Vocal Image's own original images (Higgsfield generations, produced frames) to Pinterest",
    ]
    not_good_for = [
        "re-hosting someone else's pin found via search — use pinterest_browser_search's Save flow instead, "
        "per Pinterest's own content policy for this endpoint",
    ]
    fallback_tools = []
    agent_skills = []
    quality_score = 0.8

    _API_BASE = "https://api.pinterest.com/v5"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {os.environ['PINTEREST_ACCESS_TOKEN']}",
            "Content-Type": "application/json",
        }

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        action = inputs.get("action")
        actions = {
            "create_board": self._create_board,
            "list_boards": self._list_boards,
            "create_pin": self._create_pin,
            "list_board_pins": self._list_board_pins,
        }
        handler = actions.get(action)
        if handler is None:
            return ToolResult(
                success=False,
                error=f"'action' must be one of: {', '.join(actions)}",
            )
        return handler(inputs, start)

    def _create_board(self, inputs: dict[str, Any], start: float) -> ToolResult:
        name = inputs.get("name")
        if not name:
            return ToolResult(success=False, error="'name' required")

        body = {
            "name": name,
            "description": inputs.get("description", ""),
            "privacy": inputs.get("privacy", "SECRET"),
        }
        try:
            resp = requests.post(
                f"{self._API_BASE}/boards", headers=self._headers(), json=body, timeout=15
            )
            resp.raise_for_status()
            board = resp.json()
            return ToolResult(
                success=True,
                data={
                    "board_id": board.get("id"),
                    "name": board.get("name"),
                    "privacy": board.get("privacy"),
                    "board_url": f"https://pinterest.com/board/{board.get('id')}",
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

    def _list_boards(self, inputs: dict[str, Any], start: float) -> ToolResult:
        try:
            resp = requests.get(
                f"{self._API_BASE}/boards",
                headers=self._headers(),
                params={"page_size": min(int(inputs.get("page_size", 25)), 100)},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            boards = [
                {"board_id": b.get("id"), "name": b.get("name"), "pin_count": b.get("pin_count", 0)}
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

    def _create_pin(self, inputs: dict[str, Any], start: float) -> ToolResult:
        board_id = inputs.get("board_id")
        image_url = inputs.get("image_url")
        if not board_id or not image_url:
            return ToolResult(success=False, error="'board_id' and 'image_url' required")

        body: dict[str, Any] = {
            "board_id": board_id,
            "media_source": {"source_type": "image_url", "url": image_url},
        }
        if inputs.get("title"):
            body["title"] = inputs["title"]
        if inputs.get("description"):
            body["description"] = inputs["description"]
        if inputs.get("alt_text"):
            body["alt_text"] = inputs["alt_text"]

        try:
            resp = requests.post(
                f"{self._API_BASE}/pins", headers=self._headers(), json=body, timeout=30
            )
            resp.raise_for_status()
            pin = resp.json()
            return ToolResult(
                success=True,
                data={
                    "pin_id": pin.get("id"),
                    "board_id": pin.get("board_id"),
                    "pin_url": f"https://pinterest.com/pin/{pin.get('id')}",
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

    def _list_board_pins(self, inputs: dict[str, Any], start: float) -> ToolResult:
        board_id = inputs.get("board_id")
        if not board_id:
            return ToolResult(success=False, error="'board_id' required")

        try:
            resp = requests.get(
                f"{self._API_BASE}/boards/{board_id}/pins",
                headers=self._headers(),
                params={"page_size": min(int(inputs.get("page_size", 25)), 100)},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            pins = []
            for pin in data.get("items", []):
                media = pin.get("media", {})
                images = media.get("images", {})
                image_url = (
                    (images.get("1200x") or images.get("750x") or images.get("600x") or {})
                    .get("url", "")
                )
                pins.append({
                    "pin_id": pin.get("id"),
                    "title": pin.get("title", ""),
                    "image_url": image_url,
                })
            return ToolResult(
                success=True,
                data={"pins": pins, "total": len(pins)},
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
