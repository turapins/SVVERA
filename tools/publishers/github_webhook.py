"""GitHub webhook registration and event parsing tool.

Registers a webhook on the SVVERA GitHub repo so that:
  - push to feat/* → logs preflight signal
  - PR merged to main → triggers skills refresh

Auth:
    GITHUB_TOKEN      — personal access token with repo + admin:repo_hook scopes
    GITHUB_WEBHOOK_SECRET — HMAC secret for X-Hub-Signature-256 verification
    WEBHOOK_PORT      — port where webhook_server.py is running (default 8080)
"""
from __future__ import annotations

import hashlib
import hmac
import json
import os
from typing import Any

import requests

from tools.base_tool import (
    BaseTool,
    DependencyError,
    ResourceProfile,
    ResumeSupport,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)

_GITHUB_API = "https://api.github.com"
_SVVERA_REPO = "turapins/SVVERA"
_WEBHOOK_EVENTS = ["push", "pull_request"]


class GithubWebhook(BaseTool):
    name = "github_webhook"
    version = "0.1.0"
    tier = ToolTier.PUBLISH
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "publish"
    provider = "github"

    dependencies = ["env:GITHUB_TOKEN"]
    install_instructions = (
        "Set GITHUB_TOKEN (repo + admin:repo_hook scopes) and "
        "GITHUB_WEBHOOK_SECRET in .env"
    )
    resource_profile = ResourceProfile.MINIMAL
    resume_support = ResumeSupport.NONE

    input_schema = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["register", "list", "delete"],
                "description": "register = create webhook; list = show existing; delete = remove by id",
            },
            "webhook_url": {
                "type": "string",
                "description": "Public HTTPS URL where webhook_server.py is reachable (required for register)",
            },
            "hook_id": {
                "type": "integer",
                "description": "Webhook ID (required for delete)",
            },
        },
        "required": ["action"],
    }

    def get_status(self) -> ToolStatus:
        token = os.environ.get("GITHUB_TOKEN", "")
        if not token:
            return ToolStatus(
                available=False,
                message="GITHUB_TOKEN not set",
                missing_deps=["env:GITHUB_TOKEN"],
            )
        return ToolStatus(available=True, message="GitHub token configured")

    def _headers(self) -> dict:
        token = os.environ.get("GITHUB_TOKEN", "")
        if not token:
            raise DependencyError("GITHUB_TOKEN not set")
        return {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def execute(self, inputs: dict) -> ToolResult:
        action = inputs["action"]

        if action == "register":
            return self._register(inputs.get("webhook_url", ""))
        elif action == "list":
            return self._list()
        elif action == "delete":
            return self._delete(inputs.get("hook_id"))
        else:
            return ToolResult(success=False, error=f"Unknown action: {action}")

    def _register(self, webhook_url: str) -> ToolResult:
        if not webhook_url:
            return ToolResult(success=False, error="webhook_url is required for register")

        secret = os.environ.get("GITHUB_WEBHOOK_SECRET", "")
        payload = {
            "name": "web",
            "active": True,
            "events": _WEBHOOK_EVENTS,
            "config": {
                "url": f"{webhook_url.rstrip('/')}/webhook/github",
                "content_type": "json",
                "insecure_ssl": "0",
                **({"secret": secret} if secret else {}),
            },
        }

        resp = requests.post(
            f"{_GITHUB_API}/repos/{_SVVERA_REPO}/hooks",
            headers=self._headers(),
            json=payload,
            timeout=15,
        )

        if resp.status_code == 201:
            hook = resp.json()
            return ToolResult(
                success=True,
                output={
                    "hook_id": hook["id"],
                    "url": hook["config"]["url"],
                    "events": hook["events"],
                    "active": hook["active"],
                },
                message=f"Webhook #{hook['id']} registered on {_SVVERA_REPO}",
            )

        return ToolResult(
            success=False,
            error=f"GitHub API error {resp.status_code}: {resp.text[:300]}",
        )

    def _list(self) -> ToolResult:
        resp = requests.get(
            f"{_GITHUB_API}/repos/{_SVVERA_REPO}/hooks",
            headers=self._headers(),
            timeout=15,
        )
        resp.raise_for_status()
        hooks = resp.json()
        summary = [
            {"id": h["id"], "url": h["config"].get("url", ""), "events": h["events"], "active": h["active"]}
            for h in hooks
        ]
        return ToolResult(success=True, output={"hooks": summary}, message=f"{len(summary)} webhook(s) on {_SVVERA_REPO}")

    def _delete(self, hook_id: Any) -> ToolResult:
        if hook_id is None:
            return ToolResult(success=False, error="hook_id is required for delete")
        resp = requests.delete(
            f"{_GITHUB_API}/repos/{_SVVERA_REPO}/hooks/{hook_id}",
            headers=self._headers(),
            timeout=15,
        )
        if resp.status_code == 204:
            return ToolResult(success=True, message=f"Webhook #{hook_id} deleted")
        return ToolResult(success=False, error=f"GitHub API error {resp.status_code}: {resp.text[:200]}")


def verify_github_signature(secret: str, payload: bytes, sig_header: str) -> bool:
    """Standalone helper — used by webhook_server.py to verify incoming requests."""
    if not secret:
        return True
    expected = "sha256=" + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, sig_header or "")
