#!/usr/bin/env python3
"""
upload_folder_to_drive.py

Uploads every file from a local folder into a given Google Drive folder.
Resumable uploads, skips files already present in the destination by name,
prints one line per file. Built for delivering creative batches (statics, cuts)
without touching the GUI.

First run needs OAuth: put a Desktop-app OAuth client JSON at
scripts/drive_credentials.json, then run this once — a browser opens, you approve,
and the token is saved to scripts/drive_token.json. Every later run is unattended.

Usage:
    python3 scripts/upload_folder_to_drive.py <local_folder> <drive_folder_id> [--ext png,jpg] [--dry-run]

Example:
    python3 scripts/upload_folder_to_drive.py \
        ~/Downloads/MYEDSPACE_ES_upload 1U4YvQffVGUP0acYlSlzbP0xkqIvRv-16 --ext png
"""

import argparse
import mimetypes
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]
SCRIPT_DIR = Path(__file__).parent
TOKEN_PATH = SCRIPT_DIR / "drive_token.json"
CREDENTIALS_PATH = SCRIPT_DIR / "drive_credentials.json"


def get_credentials():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json())
        return creds
    if not CREDENTIALS_PATH.exists():
        sys.exit(
            f"ERROR: no OAuth client at {CREDENTIALS_PATH}\n"
            "Google Cloud Console -> APIs & Services -> Credentials -> Create OAuth client ID\n"
            "-> Desktop app -> download JSON -> save it to that path. Enable the Drive API too."
        )
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_PATH.write_text(creds.to_json())
    return creds


def existing_names(service, folder_id):
    """Names already in the destination, so re-runs are idempotent."""
    names, token = set(), None
    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(name)",
            pageSize=1000,
            pageToken=token,
            supportsAllDrives=True,
        ).execute()
        names.update(f["name"] for f in resp.get("files", []))
        token = resp.get("nextPageToken")
        if not token:
            return names


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("local_folder")
    ap.add_argument("drive_folder_id")
    ap.add_argument("--ext", default="", help="comma-separated extensions to include, e.g. png,jpg")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    src = Path(args.local_folder).expanduser()
    if not src.is_dir():
        sys.exit(f"ERROR: not a folder: {src}")

    exts = {e.strip().lower().lstrip(".") for e in args.ext.split(",") if e.strip()}
    files = sorted(p for p in src.iterdir()
                   if p.is_file() and not p.name.startswith(".")
                   and (not exts or p.suffix.lower().lstrip(".") in exts))
    if not files:
        sys.exit("ERROR: nothing to upload")

    service = build("drive", "v3", credentials=get_credentials())
    folder = service.files().get(fileId=args.drive_folder_id,
                                 fields="id,name", supportsAllDrives=True).execute()
    present = existing_names(service, args.drive_folder_id)

    todo = [f for f in files if f.name not in present]
    total_mb = sum(f.stat().st_size for f in todo) / 1e6
    print(f"Destination: {folder['name']} ({folder['id']})")
    print(f"{len(files)} local files, {len(files) - len(todo)} already there, "
          f"{len(todo)} to upload ({total_mb:.0f} MB)")
    if args.dry_run:
        for f in todo:
            print(f"  would upload  {f.name}")
        return

    ok = fail = 0
    for i, f in enumerate(todo, 1):
        mime = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
        media = MediaFileUpload(str(f), mimetype=mime, resumable=True, chunksize=8 * 1024 * 1024)
        try:
            req = service.files().create(
                body={"name": f.name, "parents": [args.drive_folder_id]},
                media_body=media, fields="id", supportsAllDrives=True)
            resp = None
            while resp is None:
                _, resp = req.next_chunk()
            print(f"  [{i}/{len(todo)}] ok    {f.name}  ({f.stat().st_size/1e6:.1f} MB)")
            ok += 1
        except HttpError as e:
            print(f"  [{i}/{len(todo)}] FAIL  {f.name}  {e}")
            fail += 1

    print(f"\nuploaded {ok}, failed {fail}")
    print(f"https://drive.google.com/drive/folders/{args.drive_folder_id}")


if __name__ == "__main__":
    main()
