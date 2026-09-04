"""Google Drive manager — create script docs, upload assets, generate share links.

Manages the Vocal Image production Shared Drive (driveId env: GDRIVE_MAIN_DRIVE_ID).
All API calls use supportsAllDrives=True (required for Shared Drives).
"""

from __future__ import annotations

import io
import os
import time
from pathlib import Path
from typing import Any

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


class GDriveManager(BaseTool):
    name = "gdrive_manager"
    version = "0.1.0"
    tier = ToolTier.PUBLISH
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    capability = "storage"
    provider = "google"

    dependencies = [
        "env:GOOGLE_APPLICATION_CREDENTIALS",
        "env:GDRIVE_MAIN_DRIVE_ID",
        "python:googleapiclient",
    ]
    install_instructions = (
        "Set GOOGLE_APPLICATION_CREDENTIALS to a service-account JSON path "
        "and GDRIVE_MAIN_DRIVE_ID. "
        "pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    )

    resource_profile = ResourceProfile(network_required=True)
    resume_support = ResumeSupport.FROM_START
    side_effects = ["creates/uploads files to Google Drive"]

    best_for = [
        "create script Google Doc from template",
        "upload final video to Drive /Export",
        "organize production assets in Drive",
        "get shareable Drive link after export",
    ]
    agent_skills = []

    _FOLDER_NAMES = {
        "scripts": "scripts",
        "references": "references",
        "ai_generations": "AI generations",
        "prompts": "prompts",
        "characters": "Characters",
        "assets": "Assets",
        "export": "Export",
    }

    _SHARED_DRIVE_PARAMS = {
        "supportsAllDrives": True,
        "includeItemsFromAllDrives": True,
    }

    def _build_service(self):
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
        scopes = ["https://www.googleapis.com/auth/drive"]
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=scopes
        )
        return build("drive", "v3", credentials=creds, cache_discovery=False)

    def _drive_id(self) -> str:
        return os.environ["GDRIVE_MAIN_DRIVE_ID"]

    def _find_folder(self, service, name: str, parent_id: str | None = None) -> str | None:
        """Return folder ID by name inside the Shared Drive (or under parent_id)."""
        drive_id = self._drive_id()
        parent_clause = (
            f"'{parent_id}' in parents"
            if parent_id
            else f"'{drive_id}' in parents"
        )
        q = (
            f"mimeType='application/vnd.google-apps.folder' "
            f"and name='{name}' "
            f"and {parent_clause} "
            f"and trashed=false"
        )
        resp = (
            service.files()
            .list(
                q=q,
                driveId=drive_id,
                corpora="drive",
                **self._SHARED_DRIVE_PARAMS,
                fields="files(id,name)",
            )
            .execute()
        )
        files = resp.get("files", [])
        return files[0]["id"] if files else None

    def _get_or_create_folder(self, service, name: str, parent_id: str | None = None) -> str:
        folder_id = self._find_folder(service, name, parent_id)
        if folder_id:
            return folder_id
        drive_id = self._drive_id()
        meta = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id or drive_id],
            "driveId": drive_id,
        }
        f = service.files().create(body=meta, **self._SHARED_DRIVE_PARAMS, fields="id").execute()
        return f["id"]

    def _share_link(self, service, file_id: str) -> str:
        """Create anyone-with-link permission and return the share URL."""
        service.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"},
            **self._SHARED_DRIVE_PARAMS,
        ).execute()
        return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        start = time.time()
        action = inputs.get("action")
        if not action:
            return ToolResult(success=False, error="'action' is required")

        try:
            service = self._build_service()
        except Exception as exc:
            return ToolResult(success=False, error=f"Drive auth failed: {exc}")

        try:
            if action == "find_folder":
                return self._action_find_folder(service, inputs, start)
            elif action == "create_script_doc":
                return self._action_create_script_doc(service, inputs, start)
            elif action == "upload_reference":
                return self._action_upload(service, inputs, "references", start)
            elif action == "upload_generation":
                return self._action_upload_generation(service, inputs, start)
            elif action == "upload_export":
                return self._action_upload_export(service, inputs, start)
            else:
                return ToolResult(
                    success=False,
                    error=f"Unknown action '{action}'. Valid: find_folder, create_script_doc, upload_reference, upload_generation, upload_export",
                )
        except Exception as exc:
            return ToolResult(
                success=False,
                error=str(exc),
                duration_seconds=time.time() - start,
            )

    def _action_find_folder(self, service, inputs, start) -> ToolResult:
        name = inputs.get("folder_name")
        parent_id = inputs.get("parent_id")
        if not name:
            return ToolResult(success=False, error="'folder_name' required")
        folder_id = self._find_folder(service, name, parent_id)
        return ToolResult(
            success=bool(folder_id),
            data={"folder_id": folder_id, "found": bool(folder_id)},
            error=None if folder_id else f"Folder '{name}' not found",
            duration_seconds=time.time() - start,
        )

    def _action_create_script_doc(self, service, inputs, start) -> ToolResult:
        """Copy the script template and place it in /scripts folder."""
        script_name = inputs.get("script_name")
        if not script_name:
            return ToolResult(success=False, error="'script_name' required")

        template_id = os.environ.get(
            "GDRIVE_SCRIPT_TEMPLATE_ID",
            "1Ls08r5DeJRFK3bZOEa_uGi0faqshJRw6LVt6wMjo7Rc",
        )

        scripts_folder_id = self._get_or_create_folder(
            service, self._FOLDER_NAMES["scripts"]
        )

        copy_body = {"name": script_name, "parents": [scripts_folder_id]}
        copied = (
            service.files()
            .copy(
                fileId=template_id,
                body=copy_body,
                **self._SHARED_DRIVE_PARAMS,
                fields="id,webViewLink",
            )
            .execute()
        )

        return ToolResult(
            success=True,
            data={
                "doc_id": copied["id"],
                "doc_url": copied.get("webViewLink", f"https://docs.google.com/document/d/{copied['id']}/edit"),
                "script_name": script_name,
                "folder_id": scripts_folder_id,
            },
            duration_seconds=time.time() - start,
        )

    def _action_upload(self, service, inputs, folder_key: str, start) -> ToolResult:
        file_path = inputs.get("file_path")
        script_name = inputs.get("script_name", "")
        if not file_path:
            return ToolResult(success=False, error="'file_path' required")

        local = Path(file_path)
        if not local.exists():
            return ToolResult(success=False, error=f"File not found: {file_path}")

        folder_id = self._get_or_create_folder(
            service, self._FOLDER_NAMES[folder_key]
        )

        from googleapiclient.http import MediaFileUpload

        media = MediaFileUpload(str(local), resumable=True)
        file_meta = {
            "name": inputs.get("asset_name", local.name),
            "parents": [folder_id],
        }
        uploaded = (
            service.files()
            .create(
                body=file_meta,
                media_body=media,
                **self._SHARED_DRIVE_PARAMS,
                fields="id,webViewLink",
            )
            .execute()
        )

        return ToolResult(
            success=True,
            data={
                "file_id": uploaded["id"],
                "file_url": uploaded.get("webViewLink", ""),
                "folder_id": folder_id,
            },
            artifacts=[file_path],
            duration_seconds=time.time() - start,
        )

    def _action_upload_generation(self, service, inputs, start) -> ToolResult:
        """Upload AI-generated asset to /AI generations/<script_name>/."""
        script_name = inputs.get("script_name")
        file_path = inputs.get("file_path")
        if not script_name:
            return ToolResult(success=False, error="'script_name' required")
        if not file_path:
            return ToolResult(success=False, error="'file_path' required")

        parent_folder_id = self._get_or_create_folder(
            service, self._FOLDER_NAMES["ai_generations"]
        )
        script_folder_id = self._get_or_create_folder(
            service, script_name, parent_id=parent_folder_id
        )

        local = Path(file_path)
        if not local.exists():
            return ToolResult(success=False, error=f"File not found: {file_path}")

        from googleapiclient.http import MediaFileUpload

        media = MediaFileUpload(str(local), resumable=True)
        file_meta = {
            "name": inputs.get("asset_name", local.name),
            "parents": [script_folder_id],
        }
        uploaded = (
            service.files()
            .create(
                body=file_meta,
                media_body=media,
                **self._SHARED_DRIVE_PARAMS,
                fields="id,webViewLink",
            )
            .execute()
        )

        return ToolResult(
            success=True,
            data={
                "file_id": uploaded["id"],
                "file_url": uploaded.get("webViewLink", ""),
                "folder_id": script_folder_id,
                "script_folder": script_name,
            },
            artifacts=[file_path],
            duration_seconds=time.time() - start,
        )

    def _action_upload_export(self, service, inputs, start) -> ToolResult:
        """Upload final video to /Export and create a share link."""
        file_path = inputs.get("file_path")
        video_name = inputs.get("video_name")
        if not file_path:
            return ToolResult(success=False, error="'file_path' required")
        if not video_name:
            return ToolResult(success=False, error="'video_name' required (S[n]_V[n] format)")

        local = Path(file_path)
        if not local.exists():
            return ToolResult(success=False, error=f"File not found: {file_path}")

        export_folder_id = self._get_or_create_folder(
            service, self._FOLDER_NAMES["export"]
        )

        from googleapiclient.http import MediaFileUpload

        export_filename = f"{video_name}{local.suffix}"
        media = MediaFileUpload(str(local), resumable=True)
        file_meta = {
            "name": export_filename,
            "parents": [export_folder_id],
        }
        uploaded = (
            service.files()
            .create(
                body=file_meta,
                media_body=media,
                **self._SHARED_DRIVE_PARAMS,
                fields="id,webViewLink",
            )
            .execute()
        )

        share_link = self._share_link(service, uploaded["id"])

        return ToolResult(
            success=True,
            data={
                "file_id": uploaded["id"],
                "file_name": export_filename,
                "share_link": share_link,
                "folder_id": export_folder_id,
            },
            artifacts=[file_path],
            duration_seconds=time.time() - start,
        )
