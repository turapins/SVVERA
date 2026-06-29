#!/usr/bin/env python3
"""
upload_to_archive.py

Uploads a final video to the Vocal Image Google Drive Archive.
Automatically picks the correct YYYY.MM folder, creates it if missing.

First run: opens browser for Google OAuth — approves once, saves token.
All future runs: fully automatic, no interaction needed.

Usage:
    python3 scripts/upload_to_archive.py <file_path> [--title "Custom Name"]

Examples:
    python3 scripts/upload_to_archive.py output/S268_V1.mov
    python3 scripts/upload_to_archive.py ~/Desktop/final.mp4 --title "S269_V2_final"
"""

import os
import sys
import argparse
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# --- Config ---
SCOPES = ["https://www.googleapis.com/auth/drive"]
ARCHIVE_FOLDER_ID = "1zeTJs-UpzHp_a6myXAFHs8G2CP5zPpos"

# Saved token lives next to this script
SCRIPT_DIR = Path(__file__).parent
TOKEN_PATH = SCRIPT_DIR / "drive_token.json"
CREDENTIALS_PATH = SCRIPT_DIR / "drive_credentials.json"

# Known monthly folder IDs (add new ones as months are created)
MONTHLY_FOLDERS = {
    "2026.07": "14hXRT693Lj9J_OMrT3eLOD3NRQooElcL",
    "2026.06": "1R41eCe9wdFwve3NfGU4kPnCSKM_57yBl",
    "2026.05": "19xFpK9ZnYTjwq7mOxdyEiNC6FeGQWQwP",
    "2026.04": "1xBrR8mIjylwZFtNBcC_nC5TO3KzfWU0I",
    "2026.03": "186VPAfn3J0aMu9JN1eNCkqPKdf3Vp3gi",
    "2026.02": "1ZsfEZ5-Cj03Tu3wKjyNlwoITPlpmKkXp",
    "2026.01": "1VhJKFsEmwLQqxbj_0SpvQcnCx_feDktL",
}

MIME_TYPES = {
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".webm": "video/webm",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
}


def get_credentials():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print(f"\nERROR: OAuth credentials file not found at:\n  {CREDENTIALS_PATH}")
                print("\nTo set up:")
                print("  1. Go to console.cloud.google.com → APIs & Services → Credentials")
                print("  2. Create OAuth 2.0 Client ID (Desktop app)")
                print(f"  3. Download JSON → save as {CREDENTIALS_PATH}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0, prompt="select_account")
        with open(TOKEN_PATH, "w") as f:
            f.write(creds.to_json())
    return creds


def get_month_key():
    now = datetime.now()
    return f"{now.year}.{now.month:02d}"


def get_or_create_month_folder(service, month_key):
    if month_key in MONTHLY_FOLDERS:
        print(f"  Folder: Archive/{month_key} ({MONTHLY_FOLDERS[month_key]})")
        return MONTHLY_FOLDERS[month_key]

    # Search Drive (supportsAllDrives for Shared Drive support)
    results = service.files().list(
        q=f"name='{month_key}' and '{ARCHIVE_FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false",
        fields="files(id, name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()

    files = results.get("files", [])
    if files:
        folder_id = files[0]["id"]
        print(f"  Folder: Archive/{month_key} (found: {folder_id})")
        return folder_id

    # Create new month folder
    metadata = {
        "name": month_key,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [ARCHIVE_FOLDER_ID],
    }
    folder = service.files().create(body=metadata, fields="id", supportsAllDrives=True).execute()
    folder_id = folder["id"]
    print(f"  Created new folder: Archive/{month_key} ({folder_id})")
    print(f"  Add to MONTHLY_FOLDERS in this script: \"{month_key}\": \"{folder_id}\"")
    return folder_id


def upload(file_path, title=None):
    file_path = Path(file_path).expanduser().resolve()

    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)

    file_name = title or file_path.name
    mime_type = MIME_TYPES.get(file_path.suffix.lower(), "application/octet-stream")
    file_size = file_path.stat().st_size
    month_key = get_month_key()

    print(f"\nUploading: {file_name}")
    print(f"  Size: {file_size / 1024 / 1024:.1f} MB")
    print(f"  Type: {mime_type}")

    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    folder_id = get_or_create_month_folder(service, month_key)

    media = MediaFileUpload(str(file_path), mimetype=mime_type, resumable=True)
    metadata = {"name": file_name, "parents": [folder_id]}

    request = service.files().create(body=metadata, media_body=media, fields="id,name,webViewLink", supportsAllDrives=True)

    print("  Uploading", end="", flush=True)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"\r  Progress: {int(status.progress() * 100)}%", end="", flush=True)

    print(f"\r  Progress: 100%")
    print(f"\nDone.")
    print(f"  Name: {response['name']}")
    print(f"  ID:   {response['id']}")
    print(f"  URL:  {response['webViewLink']}")
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a video to Vocal Image Drive Archive")
    parser.add_argument("file", help="Path to the video file")
    parser.add_argument("--title", help="Custom filename in Drive (default: original filename)")
    args = parser.parse_args()

    upload(args.file, args.title)
