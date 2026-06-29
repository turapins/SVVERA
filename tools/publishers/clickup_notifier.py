"""ClickUp notifier — find task by name, post export comment, @mention Artemiy.

After a video is exported to Drive, this tool:
  1. Finds the ClickUp task by name (task name = video name = first line of script)
  2. Posts a comment with Drive share link + Frame.io review link
  3. Tags @Artemiy Proskuryakov for review

Performance Ads list ID: 901214874069
"""

from __future__ import annotations

import os
import time
from typing import Any

import requests

from tools.base_tool import (
    BaseTool,
    ResourceProfile,
    ResumeSupport,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolTier,
)

# Performance Ads ClickUp list — do not hardcode elsewhere
_PERFORMANCE_ADS_LIST_ID = "901214874069"


class ClickupNotifier(BaseTool):
    name = "clickup_notifier"
    version = "0.1.0"
    tier = ToolTier.PUBLISH
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "publish"
    provider = "clickup"

    dependencies = [
        "env:CLICKUP_API_TOKEN",
        "env:CLICKUP_TEAM_ID",
    ]
    install_instructions = (
        "Set CLICKUP_API_TOKEN (ClickUp → avatar → Settings → Apps → API Token) "
        "and CLICKUP_TEAM_ID (Workspace ID visible in your ClickUp URL)."
    )

    resource_profile = ResourceProfile(network_required=True)
    resume_support = ResumeSupport.FROM_START
    side_effects = [
        "posts comment to ClickUp task",
        "may update task status to 'in review'",
    ]
    best_for = [
        "notify team after video export",
        "tag Artemiy on ClickUp task with Drive link",
        "update task status to in review after export",
    ]
    agent_skills = []

    _API_BASE = "https://api.clickup.com/api/v2"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": os.environ["CLICKUP_API_TOKEN"],
            "Content-Type": "application/json",
        }

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        action = inputs.get("action")

        if action == "find_task":
            return self._find_task(inputs, start)
        elif action == "post_export_comment":
            return self._post_export_comment(inputs, start)
        elif action == "update_status":
            return self._update_status(inputs, start)
        else:
            return ToolResult(
                success=False,
                error="'action' must be one of: find_task, post_export_comment, update_status",
            )

    def _find_task(self, inputs: dict[str, Any], start: float) -> ToolResult:
        task_name = inputs.get("task_name")
        list_id = inputs.get("list_id", _PERFORMANCE_ADS_LIST_ID)

        if not task_name:
            return ToolResult(success=False, error="'task_name' required")

        try:
            resp = requests.get(
                f"{self._API_BASE}/list/{list_id}/task",
                headers=self._headers(),
                params={"query": task_name, "include_closed": "true"},
                timeout=15,
            )
            resp.raise_for_status()
            tasks = resp.json().get("tasks", [])

            # Exact name match (case-insensitive)
            matched = [t for t in tasks if t["name"].strip().lower() == task_name.strip().lower()]
            if not matched:
                matched = tasks  # fall back to first result if no exact match

            if not matched:
                return ToolResult(
                    success=False,
                    error=f"No task found with name '{task_name}' in list {list_id}",
                    duration_seconds=time.time() - start,
                )

            task = matched[0]
            return ToolResult(
                success=True,
                data={
                    "task_id": task["id"],
                    "task_name": task["name"],
                    "task_url": task.get("url", f"https://app.clickup.com/t/{task['id']}"),
                    "status": task.get("status", {}).get("status", ""),
                },
                duration_seconds=time.time() - start,
            )

        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"ClickUp API {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )

    def _post_export_comment(self, inputs: dict[str, Any], start: float) -> ToolResult:
        task_id = inputs.get("task_id")
        drive_link = inputs.get("drive_link", "")
        frameio_link = inputs.get("frameio_link", "")
        version = inputs.get("version", "V1")
        task_name = inputs.get("task_name", "")

        if not task_id:
            return ToolResult(success=False, error="'task_id' required")
        if not drive_link:
            return ToolResult(success=False, error="'drive_link' required")

        lines = [
            f"✅ Export ready: {task_name} {version}",
            f"Drive: {drive_link}",
        ]
        if frameio_link:
            lines.append(f"Frame.io: {frameio_link}")
        lines.append("")
        lines.append("@Artemiy please review")

        comment_text = "\n".join(lines)

        try:
            resp = requests.post(
                f"{self._API_BASE}/task/{task_id}/comment",
                headers=self._headers(),
                json={"comment_text": comment_text, "notify_all": True},
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()
            return ToolResult(
                success=True,
                data={
                    "comment_id": data.get("id"),
                    "task_id": task_id,
                    "comment_text": comment_text,
                },
                duration_seconds=time.time() - start,
            )
        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"ClickUp API {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )

    def _update_status(self, inputs: dict[str, Any], start: float) -> ToolResult:
        task_id = inputs.get("task_id")
        status = inputs.get("status", "in review")

        if not task_id:
            return ToolResult(success=False, error="'task_id' required")

        try:
            resp = requests.put(
                f"{self._API_BASE}/task/{task_id}",
                headers=self._headers(),
                json={"status": status},
                timeout=15,
            )
            resp.raise_for_status()
            return ToolResult(
                success=True,
                data={"task_id": task_id, "new_status": status},
                duration_seconds=time.time() - start,
            )
        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"ClickUp API {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )
