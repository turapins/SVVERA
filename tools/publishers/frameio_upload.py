"""Frame.io upload tool — uploads rendered video and returns a review link.

Frame.io is now owned by Adobe. API V4 uses Adobe IMS OAuth2.

Auth options (in priority order):
  1. FRAMEIO_TOKEN — legacy V2 Bearer token (still works until Dec 2026)
  2. FRAMEIO_ACCESS_TOKEN — pre-obtained V4 OAuth token (from scripts/frameio_auth.py)
     + FRAMEIO_REFRESH_TOKEN — auto-refreshed when access_token expires
  3. FRAMEIO_CLIENT_ID + FRAMEIO_CLIENT_SECRET — Adobe OAuth2 Server-to-Server
     (requires enterprise Adobe org with Frame.io entitlement)

To get option 2 credentials (recommended for most users):
  1. Create project at developer.adobe.com/console → Add Frame.io API → OAuth Web App
  2. Run: python3 scripts/frameio_auth.py
  3. Tokens are saved automatically to .env

V4 upload flow:
  GET  /projects/{project_id} → get root_asset_id
  POST /assets/{parent_id}/children → create asset record
  PUT  upload_urls → upload file bytes to S3
"""

from __future__ import annotations

import os
import time
from pathlib import Path
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

_V2_API = "https://api.frame.io/v2"
_V4_API = "https://api.frame.io/v4"
_ADOBE_TOKEN_URL = "https://ims-na1.adobelogin.com/ims/token/v3"


class FrameioUpload(BaseTool):
    name = "frameio_upload"
    version = "0.2.0"
    tier = ToolTier.PUBLISH
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "publish"
    provider = "frameio"

    # At least one auth method must be configured (see module docstring)
    dependencies = ["env:FRAMEIO_PROJECT_ID"]
    install_instructions = (
        "Set FRAMEIO_PROJECT_ID plus one of:\n"
        "  A) FRAMEIO_TOKEN — legacy V2 token (works until Dec 2026)\n"
        "  B) FRAMEIO_ACCESS_TOKEN + FRAMEIO_REFRESH_TOKEN — run scripts/frameio_auth.py\n"
        "  C) FRAMEIO_CLIENT_ID + FRAMEIO_CLIENT_SECRET — Server-to-Server (enterprise only)"
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

    def get_status(self) -> ToolStatus:
        has_project = bool(os.environ.get("FRAMEIO_PROJECT_ID"))
        has_auth = bool(
            os.environ.get("FRAMEIO_TOKEN")
            or os.environ.get("FRAMEIO_ACCESS_TOKEN")
            or (os.environ.get("FRAMEIO_CLIENT_ID") and os.environ.get("FRAMEIO_CLIENT_SECRET"))
        )
        return ToolStatus.AVAILABLE if (has_project and has_auth) else ToolStatus.UNAVAILABLE

    def _refresh_access_token(self) -> str:
        """Exchange refresh_token for a new access_token, persist to .env."""
        client_id = os.environ.get("FRAMEIO_CLIENT_ID", "")
        client_secret = os.environ.get("FRAMEIO_CLIENT_SECRET", "")
        refresh_token = os.environ.get("FRAMEIO_REFRESH_TOKEN", "")
        if not (client_id and client_secret and refresh_token):
            raise DependencyError("Cannot refresh: need FRAMEIO_CLIENT_ID, FRAMEIO_CLIENT_SECRET, FRAMEIO_REFRESH_TOKEN")
        resp = requests.post(
            _ADOBE_TOKEN_URL,
            data={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "client_secret": client_secret,
                "refresh_token": refresh_token,
            },
            timeout=15,
        )
        resp.raise_for_status()
        tokens = resp.json()
        new_token = tokens["access_token"]
        # Persist refreshed token to .env
        env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        if os.path.exists(env_path):
            try:
                from dotenv import set_key
                set_key(os.path.abspath(env_path), "FRAMEIO_ACCESS_TOKEN", new_token)
                if "refresh_token" in tokens:
                    set_key(os.path.abspath(env_path), "FRAMEIO_REFRESH_TOKEN", tokens["refresh_token"])
            except ImportError:
                pass
        os.environ["FRAMEIO_ACCESS_TOKEN"] = new_token
        return new_token

    def _get_bearer_token(self) -> str:
        """Return a valid Bearer token — tries all configured auth methods in order."""
        # Priority 1: legacy V2 token
        legacy = os.environ.get("FRAMEIO_TOKEN", "")
        if legacy:
            return legacy

        # Priority 2: pre-obtained access token (from scripts/frameio_auth.py)
        access_token = os.environ.get("FRAMEIO_ACCESS_TOKEN", "")
        if access_token:
            return access_token

        # Priority 3: Adobe Server-to-Server (enterprise orgs only)
        client_id = os.environ.get("FRAMEIO_CLIENT_ID", "")
        client_secret = os.environ.get("FRAMEIO_CLIENT_SECRET", "")
        if client_id and client_secret:
            resp = requests.post(
                _ADOBE_TOKEN_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "scope": "openid,AdobeID,frame_io_api",
                },
                timeout=15,
            )
            resp.raise_for_status()
            return resp.json()["access_token"]

        raise DependencyError(
            "No Frame.io auth configured. Run scripts/frameio_auth.py to set up V4 OAuth, "
            "or set FRAMEIO_TOKEN for legacy V2 access."
        )

    def _headers(self, token: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def _api_base(self) -> str:
        # V4 when any modern auth is configured; V2 only for bare legacy token
        if os.environ.get("FRAMEIO_ACCESS_TOKEN") or os.environ.get("FRAMEIO_CLIENT_ID"):
            return _V4_API
        return _V2_API

    def _get_root_asset_id(self, token: str, project_id: str) -> str:
        resp = requests.get(
            f"{self._api_base()}/projects/{project_id}",
            headers=self._headers(token),
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        # V4 wraps response in {"data": {...}}, V2 is flat
        project = data.get("data", data)
        return project["root_asset_id"]

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()

        file_path = inputs.get("file_path")
        asset_name = inputs.get("asset_name")
        folder_id = inputs.get("folder_id")

        if not file_path:
            return ToolResult(success=False, error="'file_path' required")
        if not asset_name:
            return ToolResult(success=False, error="'asset_name' required")

        local = Path(file_path)
        if not local.exists():
            return ToolResult(success=False, error=f"File not found: {file_path}")

        try:
            token = self._get_bearer_token()
            project_id = os.environ["FRAMEIO_PROJECT_ID"]
            try:
                parent_id = folder_id or self._get_root_asset_id(token, project_id)
            except requests.HTTPError as exc:
                # Token expired — try refresh once
                if exc.response.status_code == 401 and os.environ.get("FRAMEIO_REFRESH_TOKEN"):
                    token = self._refresh_access_token()
                    parent_id = folder_id or self._get_root_asset_id(token, project_id)
                else:
                    raise

            file_size = local.stat().st_size
            create_payload = {
                "name": asset_name,
                "type": "file",
                "filetype": local.suffix.lstrip(".").upper() or "MP4",
                "filesize": file_size,
            }

            resp = requests.post(
                f"{self._api_base()}/assets/{parent_id}/children",
                headers=self._headers(token),
                json=create_payload,
                timeout=30,
            )
            resp.raise_for_status()

            raw = resp.json()
            asset = raw.get("data", raw)  # V4 wraps in data, V2 is flat

            upload_urls: list[str] = asset.get("upload_urls", [])
            if upload_urls:
                chunk_size = max(1, (file_size + len(upload_urls) - 1) // len(upload_urls))
                with open(local, "rb") as fh:
                    for url in upload_urls:
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
                    "asset_url": f"https://next.frame.io/projects/{project_id}/assets/{asset_id}",
                    "file_size_bytes": file_size,
                    "api_version": "v4" if self._api_base() == _V4_API else "v2",
                },
                artifacts=[file_path],
                duration_seconds=time.time() - start,
            )

        except DependencyError as exc:
            return ToolResult(success=False, error=str(exc), duration_seconds=time.time() - start)
        except requests.HTTPError as exc:
            return ToolResult(
                success=False,
                error=f"Frame.io API {exc.response.status_code}: {exc.response.text[:300]}",
                duration_seconds=time.time() - start,
            )
        except Exception as exc:
            return ToolResult(success=False, error=str(exc), duration_seconds=time.time() - start)
