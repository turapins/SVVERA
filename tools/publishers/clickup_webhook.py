"""ClickUp webhook tool — parse and verify incoming ClickUp webhook payloads.

ClickUp sends signed POST requests for:
  - taskStatusUpdated
  - taskCommentPosted
  - taskCreated

If CLICKUP_WEBHOOK_SECRET is set, HMAC-SHA256 signature is verified.
"""

from __future__ import annotations

import hashlib
import hmac
import os
import time
from typing import Any

from tools.base_tool import (
    BaseTool,
    ResourceProfile,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolTier,
)

_APPROVAL_KEYWORDS = {"approved", "approve", "lgtm", "looks good", "ship it", "go"}


class ClickupWebhook(BaseTool):
    name = "clickup_webhook"
    version = "0.1.0"
    tier = ToolTier.PUBLISH
    stability = ToolStability.BETA
    runtime = ToolRuntime.LOCAL
    capability = "publish"
    provider = "clickup"

    dependencies = ["env:CLICKUP_API_TOKEN"]
    install_instructions = "Set CLICKUP_API_TOKEN."

    resource_profile = ResourceProfile()
    side_effects = []
    best_for = [
        "parse ClickUp webhook event payload",
        "verify ClickUp webhook HMAC signature",
        "detect task approval from comment",
    ]
    agent_skills = []

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        action = inputs.get("action")

        if action == "parse":
            return self._parse(inputs, start)
        elif action == "verify":
            return self._verify(inputs, start)
        else:
            return ToolResult(
                success=False,
                error="'action' must be one of: parse, verify",
            )

    def _parse(self, inputs: dict[str, Any], start: float) -> ToolResult:
        payload = inputs.get("payload", {})
        event_type = payload.get("event", "")
        history_items = payload.get("history_items", [])

        task_id = payload.get("task_id", "")
        task_name = ""
        status = ""
        comment_text = ""
        user_name = ""
        is_approved = False

        if history_items:
            item = history_items[0]
            user_name = item.get("user", {}).get("username", "")
            if event_type == "taskStatusUpdated":
                status = item.get("after", {}).get("status", "")
                is_approved = status.lower() in {"approved", "done", "complete"}
            elif event_type == "taskCommentPosted":
                comment_text = item.get("comment", {}).get("comment_text", "")
                is_approved = any(
                    kw in comment_text.lower() for kw in _APPROVAL_KEYWORDS
                )

        return ToolResult(
            success=True,
            data={
                "event_type": event_type,
                "task_id": task_id,
                "task_name": task_name,
                "status": status,
                "comment_text": comment_text,
                "user_name": user_name,
                "is_approved": is_approved,
            },
            duration_seconds=time.time() - start,
        )

    def _verify(self, inputs: dict[str, Any], start: float) -> ToolResult:
        secret = os.environ.get("CLICKUP_WEBHOOK_SECRET", "")
        if not secret:
            return ToolResult(
                success=True,
                data={"valid": True, "skipped": True, "reason": "CLICKUP_WEBHOOK_SECRET not set"},
                duration_seconds=time.time() - start,
            )

        raw_body = inputs.get("raw_body", "")
        signature_header = inputs.get("signature_header", "")

        expected = hmac.new(
            secret.encode(),
            raw_body.encode() if isinstance(raw_body, str) else raw_body,
            hashlib.sha256,
        ).hexdigest()

        valid = hmac.compare_digest(expected, signature_header)
        return ToolResult(
            success=True,
            data={"valid": valid},
            duration_seconds=time.time() - start,
        )
