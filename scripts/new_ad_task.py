#!/usr/bin/env python3
"""
new_ad_task.py

Standard Vocal Image Performance Ads cycle:
  1. Creates a Google Doc brief with task name + template
  2. Creates a ClickUp task in Performance Ads list (ready for gen)
  3. Posts the Google Doc link as first comment
  4. Assigns to specified team member or leaves for agent

Usage:
    python3 scripts/new_ad_task.py "IT_TST_AM_S100" --assign kirill
    python3 scripts/new_ad_task.py "[Video] KR_DATING_CEO_002" --assign diana
    python3 scripts/new_ad_task.py "IT_RW1_AM_V90" --assign daniil
    python3 scripts/new_ad_task.py "IT_TST_AM_S101" --assign ivan
    python3 scripts/new_ad_task.py "IT_TST_AM_S102" --assign agent   # unassigned / AI-produced

Assignees:
    kirill  → Kirill Repin      (ID: 36377650)
    ivan    → Ivan Turapin      (ID: 93620567)
    diana   → Diana Oflyan      (ID: 93750369)
    daniil  → Daniil Volotskoi  (ID: 93782061)
    agent   → unassigned (AI handles production)

Requires:
    CLICKUP_API_TOKEN in .env  (Settings → Apps → API in ClickUp)
    drive_token.json + drive_credentials.json in this scripts/ folder
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime

# --- Google OAuth ---
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# ── Config ────────────────────────────────────────────────────────────────────

CLICKUP_LIST_ID = "901214874069"     # Performance Ads → List
CLICKUP_API = "https://api.clickup.com/api/v2"

# Briefs live in their own Drive folder (shared with the team)
# Set BRIEFS_FOLDER_ID in .env to pin a folder; falls back to My Drive root.
BRIEFS_FOLDER_ID = os.environ.get("BRIEFS_FOLDER_ID", "1kJI9bVlFK1laApRRZceWOMFe_Fu8m-dS")

# Google OAuth — needs Drive + Docs scopes
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents",
]

SCRIPT_DIR = Path(__file__).parent
TOKEN_PATH = SCRIPT_DIR / "drive_token.json"
CREDENTIALS_PATH = SCRIPT_DIR / "drive_credentials.json"

ASSIGNEE_MAP = {
    "kirill": 36377650,
    "ivan":   93620567,
    "diana":  93750369,
    "daniil": 93782061,
    "agent":  None,   # unassigned — agent produces autonomously
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_env():
    env_path = SCRIPT_DIR.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip("'\"")
        if key and key not in os.environ:
            os.environ[key] = val


def get_drive_creds():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print("ERROR: drive_credentials.json not found in scripts/")
                print("Download OAuth 2.0 Client ID (Desktop) from Google Cloud Console.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0, prompt="select_account")
        TOKEN_PATH.write_text(creds.to_json())
    return creds


def get_clickup_token():
    token = os.environ.get("CLICKUP_API_TOKEN", "")
    if not token:
        print("ERROR: CLICKUP_API_TOKEN not set in .env")
        print("  1. Open ClickUp → your avatar → Settings → Apps")
        print("  2. Generate Personal API Token")
        print("  3. Add to .env:  CLICKUP_API_TOKEN=pk_...")
        sys.exit(1)
    return token


# ── Step 1: Google Doc ────────────────────────────────────────────────────────

def create_brief_doc(task_name: str, creds) -> tuple[str, str]:
    """Creates a Google Doc brief. Returns (doc_id, doc_url)."""
    drive = build("drive", "v3", credentials=creds)
    docs  = build("docs",  "v1", credentials=creds)

    # Create blank Google Doc
    file_meta = {
        "name": task_name,
        "mimeType": "application/vnd.google-apps.document",
    }
    if BRIEFS_FOLDER_ID:
        file_meta["parents"] = [BRIEFS_FOLDER_ID]

    doc_file = drive.files().create(body=file_meta, fields="id, webViewLink").execute()
    doc_id  = doc_file["id"]
    doc_url = doc_file["webViewLink"]

    # Fill brief template via Docs API
    today = datetime.today().strftime("%Y-%m-%d")
    template_text = f"""{task_name}
Brief · {today}

━━━━━━━━━━━━━━━━━━━━━━━━━━━

HOOK (first 3 sec)


SCRIPT / NARRATION


VISUAL REFERENCE


AVATAR / PERFORMER


KEY MESSAGE


CTA


NOTES / INSTRUCTIONS FOR EDITOR


━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: ready for gen
"""

    docs.documents().batchUpdate(
        documentId=doc_id,
        body={
            "requests": [
                {
                    "insertText": {
                        "location": {"index": 1},
                        "text": template_text,
                    }
                }
            ]
        },
    ).execute()

    # Doc is inside the Performance Ads folder — inherits all folder permissions.
    # No individual sharing needed.

    return doc_id, doc_url


# ── Step 2: ClickUp Task ──────────────────────────────────────────────────────

def create_clickup_task(task_name: str, assignee_id: int | None, token: str) -> tuple[str, str]:
    """Creates task in Performance Ads. Returns (task_id, task_url)."""
    headers = {"Authorization": token, "Content-Type": "application/json"}

    payload = {
        "name": task_name,
        "status": "ready for gen",
    }
    if assignee_id is not None:
        payload["assignees"] = [assignee_id]

    resp = requests.post(
        f"{CLICKUP_API}/list/{CLICKUP_LIST_ID}/task",
        headers=headers,
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["id"], data["url"]


# ── Step 3: Comment with Doc link ─────────────────────────────────────────────

def post_doc_comment(task_id: str, doc_url: str, token: str):
    """Posts the Google Doc link as the first comment on the task."""
    headers = {"Authorization": token, "Content-Type": "application/json"}
    payload = {"comment_text": f"Brief (Google Doc):\n{doc_url}"}
    resp = requests.post(
        f"{CLICKUP_API}/task/{task_id}/comment",
        headers=headers,
        json=payload,
        timeout=15,
    )
    resp.raise_for_status()


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Create Performance Ads task cycle")
    parser.add_argument("task_name", help='Task name, e.g. "IT_TST_AM_S100" or "[Video] KR_CEO_001"')
    parser.add_argument(
        "--assign",
        choices=list(ASSIGNEE_MAP.keys()),
        default="agent",
        help="Who to assign: kirill | ivan | diana | daniil | agent (default: agent)",
    )
    args = parser.parse_args()

    task_name   = args.task_name
    assignee_id = ASSIGNEE_MAP[args.assign]

    load_env()

    clickup_token = get_clickup_token()
    drive_creds   = get_drive_creds()

    print(f"\n→ Creating Google Doc brief: {task_name!r}")
    doc_id, doc_url = create_brief_doc(task_name, drive_creds)
    print(f"  ✓ Doc: {doc_url}")

    assignee_label = args.assign if assignee_id else "agent (unassigned)"
    print(f"\n→ Creating ClickUp task in Performance Ads → assignee: {assignee_label}")
    task_id, task_url = create_clickup_task(task_name, assignee_id, clickup_token)
    print(f"  ✓ Task: {task_url}")

    print(f"\n→ Posting Google Doc link as comment")
    post_doc_comment(task_id, doc_url, clickup_token)
    print(f"  ✓ Comment added")

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DONE

  Task:  {task_url}
  Brief: {doc_url}
  Assignee: {assignee_label}
  Status: ready for gen
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


if __name__ == "__main__":
    main()
