"""Frame.io webhook tool — register webhooks and parse/verify incoming events.

Supports Frame.io Webhooks Beta.
Events subscribed: asset.ready, comment.created, asset.approved
"""

from __future__ import annotations

import hashlib
import hmac
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


class FrameioWebhook(BaseTool):
    name = "frameio_webhook"
    version = "0.1.0"
    tier = ToolTier.PUBLISH
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "publish"
    provider = "frameio"

    dependencies = [
        "env:FRAMEIO_TOKEN",
        "env:FRAMEIO_WEBHOOK_SECRET",
    ]
    install_instructions = (
        "Set FRAMEIO_TOKEN and FRAMEIO_WEBHOOK_SECRET. "
        "Register webhook URL at app.frame.io → Team Settings → Webhooks (Beta)."
    )

    resource_profile = ResourceProfile(network_required=True)
    side_effects = ["registers webhook with Frame.io API"]
    best_for = [
        "register Frame.io webhook for asset approval events",
        "parse incoming Frame.io webhook payload",
        "verify Frame.io webhook HMAC signature",
    ]
    agent_skills = []

    _API_BASE = "https://api.frame.io/v2"
    _SUBSCRIBED_EVENTS = ["asset.ready", "comment.created", "asset.approved"]

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {os.environ['FRAMEIO_TOKEN']}",
            "Content-Type": "application/json",
        }

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        action = inputs.get("action")

        if action == "register":
            return self._register(inputs, start)
        elif action == "parse":
            return self._parse(inputs, start)
        elif action == "verify_signature":
            return self._verify_signature(inputs, start)
        else:
            return ToolResult(
                success=False,
                error="'action' must be one of: register, parse, verify_signature",
            )

    def _register(self, inputs: dict[str, Any], start: float) -> ToolResult:
        url = inputs.get("webhook_url")
        team_id = inputs.get("team_id") or os.environ.get("FRAMEIO_WORKSPACE_ID", "")

        if not url:
            return ToolResult(success=False, error="'webhook_url' required for action=register")
        if not team_id:
            return ToolResult(
                success=False,
                error="'team_id' or FRAMEIO_WORKSPACE_ID env var required",
            )

        try:
            resp = requests.post(
                f"{self._API_BASE}/teams/{team_id}/webhooks",
                headers=self._headers(),
                json={
                    "url": url,
                    "name": "OpenMontage webhook",
                    "events": self._SUBSCRIBED_EVENTS,
                    "secret": os.environ.get("FRAMEIO_WEBHOOK_SECRET", ""),
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            return ToolResult(
                success=True,
                data={"webhook_id": data.get("id"), "events": self._SUBSCRIBED_EVENTS},
                duration_seconds=time.time() - start,
            )
        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"Frame.io API {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )

    def _parse(self, inputs: dict[str, Any], start: float) -> ToolResult:
        payload = inputs.get("payload", {})
        event_type = payload.get("type", "")
        resource = payload.get("resource", {})

        parsed = {
            "event_type": event_type,
            "asset_id": resource.get("id", ""),
            "asset_name": resource.get("name", ""),
            "status": resource.get("status", ""),
            "comment_text": "",
        }

        if event_type == "comment.created":
            parsed["comment_text"] = resource.get("text", "") or resource.get("body", "")

        return ToolResult(
            success=True,
            data=parsed,
            duration_seconds=time.time() - start,
        )

    def _verify_signature(self, inputs: dict[str, Any], start: float) -> ToolResult:
        signature_header = inputs.get("signature_header", "")
        raw_body = inputs.get("raw_body", "")
        secret = os.environ.get("FRAMEIO_WEBHOOK_SECRET", "")

        if not secret:
            return ToolResult(success=False, error="FRAMEIO_WEBHOOK_SECRET not set")

        expected = hmac.new(
            secret.encode(),
            raw_body.encode() if isinstance(raw_body, str) else raw_body,
            hashlib.sha256,
        ).hexdigest()

        # Frame.io sends "sha256=<hex>"
        incoming = signature_header.removeprefix("sha256=")
        valid = hmac.compare_digest(expected, incoming)

        return ToolResult(
            success=True,
            data={"valid": valid},
            duration_seconds=time.time() - start,
        )
