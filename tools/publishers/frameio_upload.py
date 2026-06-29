"""Frame.io upload tool — uploads rendered video and returns a review link.

Uses Frame.io API v2. Upload flow:
  1. Fetch project root asset via GET /projects/{project_id}
  2. Create child asset record (POST /assets/{parent_id}/children)
  3. Upload file bytes to the S3 upload_urls returned in step 2
"""

from __future__ import annotations

import os
import time
from pathlib import Path
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


class FrameioUpload(BaseTool):
    name = "frameio_upload"
    version = "0.1.0"
    tier = ToolTier.PUBLISH
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "publish"
    provider = "frameio"

    dependencies = [
        "env:FRAMEIO_TOKEN",
        "env:FRAMEIO_PROJECT_ID",
    ]
    install_instructions = (
        "Set FRAMEIO_TOKEN (Frame.io → Account → Developer → Tokens) "
        "and FRAMEIO_PROJECT_ID (from the URL on app.frame.io)."
    )

    resource_profile = ResourceProfile(network_required=True, disk_mb=2000)
    resume_support = ResumeSupport.FROM_START
    side_effects = ["uploads file to Frame.io project"]

    best_for = [
        "upload final video for contractor/client review",
        "get review link after render completes",
        "notify Frame.io reviewer of new version",
    ]
    agent_skills = []

    _API_BASE = "https://api.frame.io/v2"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {os.environ['FRAMEIO_TOKEN']}",
            "Content-Type": "application/json",
        }

    def _get_root_asset_id(self, project_id: str) -> str:
        """Return the root asset (folder) ID for a project."""
        resp = requests.get(
            f"{self._API_BASE}/projects/{project_id}",
            headers=self._headers(),
            timeout=15,
        )
        resp.raise_for_status()
        return resp.json()["root_asset_id"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()

        file_path = inputs.get("file_path")
        asset_name = inputs.get("asset_name")
        folder_id = inputs.get("folder_id")

        if not file_path:
            return ToolResult(success=False, error="'file_path' required")
        if not asset_name:
            return ToolResult(success=False, error="'asset_name' required (use script first-line name)")

        local = Path(file_path)
        if not local.exists():
            return ToolResult(success=False, error=f"File not found: {file_path}")

        try:
            project_id = os.environ["FRAMEIO_PROJECT_ID"]
            parent_id = folder_id or self._get_root_asset_id(project_id)

            file_size = local.stat().st_size
            create_payload = {
                "name": asset_name,
                "type": "file",
                "filetype": local.suffix.lstrip(".").upper() or "MP4",
                "filesize": file_size,
            }

            resp = requests.post(
                f"{self._API_BASE}/assets/{parent_id}/children",
                headers=self._headers(),
                json=create_payload,
                timeout=30,
            )
            resp.raise_for_status()
            asset = resp.json()

            upload_urls: list[str] = asset.get("upload_urls", [])
            if upload_urls:
                chunk_size = (file_size + len(upload_urls) - 1) // len(upload_urls)
                with open(local, "rb") as fh:
                    for i, url in enumerate(upload_urls):
                        chunk = fh.read(chunk_size)
                        put_resp = requests.put(
                            url,
                            data=chunk,
                            headers={"Content-Type": "application/octet-stream"},
                            timeout=300,
                        )
                        put_resp.raise_for_status()

            asset_id = asset["id"]
            review_link = asset.get("share_url") or f"https://app.frame.io/reviews/{asset_id}"

            return ToolResult(
                success=True,
                data={
                    "asset_id": asset_id,
                    "asset_name": asset_name,
                    "review_link": review_link,
                    "asset_url": f"https://app.frame.io/projects/{project_id}/assets/{asset_id}",
                    "file_size_bytes": file_size,
                },
                artifacts=[file_path],
                duration_seconds=time.time() - start,
            )

        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"Frame.io API error {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
                duration_seconds=time.time() - start,
            )
