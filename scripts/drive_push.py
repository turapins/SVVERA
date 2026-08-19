#!/usr/bin/env python3
"""Put local video(s) on Google Drive and link-share them so HeyGen can fetch.

Usage:
    python3 drive_push.py FILE [FILE ...]              # upload to My Drive root
    python3 drive_push.py --folder <FOLDER_ID> FILE    # try a specific folder first

Prints one "NAME<TAB>URL" line per file. HeyGen's Video Translate URL field needs
`anyone with the link` access — a named-user grant is invisible to it, because it
fetches anonymously.

Note: write access to a Shared Drive folder is NOT implied by being able to read it.
If the target folder 403s, the file falls back to My Drive root (still link-shared,
so HeyGen works either way) and the script says so.
"""
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]
def _token_path() -> Path:
    """OAuth token is deliberately kept OUT of the repo. Check the usual spots."""
    for c in (Path.home() / "OpenMontage/scripts/drive_token.json",
              Path(__file__).resolve().parent / "drive_token.json"):
        if c.is_file():
            return c
    sys.exit("drive_token.json not found — expected at ~/OpenMontage/scripts/drive_token.json")


TOKEN = None  # resolved lazily in service()
MIME = {".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm"}


def service():
    global TOKEN
    TOKEN = _token_path()
    c = Credentials.from_authorized_user_file(str(TOKEN), SCOPES)
    if not c.valid:
        if c.expired and c.refresh_token:
            c.refresh(Request())
            TOKEN.write_text(c.to_json())
        else:
            sys.exit("Drive token invalid and cannot refresh — needs interactive re-auth.")
    return build("drive", "v3", credentials=c)


def push(s, path: Path, folder: str | None):
    mime = MIME.get(path.suffix.lower(), "video/mp4")

    def upload(parents):
        media = MediaFileUpload(str(path), mimetype=mime, resumable=True,
                                chunksize=16 * 1024 * 1024)
        body = {"name": path.name}
        if parents:
            body["parents"] = parents
        req = s.files().create(body=body, media_body=media, fields="id,name",
                               supportsAllDrives=True)
        resp = None
        while resp is None:
            status, resp = req.next_chunk()
            if status:
                print(f"  {path.name}: {int(status.progress()*100)}%",
                      file=sys.stderr, flush=True)
        return resp

    where = "My Drive root"
    try:
        f = upload([folder] if folder else None)
        if folder:
            where = f"folder {folder}"
    except Exception as e:
        print(f"  ! folder upload failed ({str(e)[:80]}), falling back to My Drive root",
              file=sys.stderr)
        f = upload(None)

    fid = f["id"]
    try:
        s.permissions().create(fileId=fid, body={"type": "anyone", "role": "reader"},
                               fields="id", supportsAllDrives=True).execute()
    except Exception as e:
        print(f"  ! link-share failed for {path.name}: {str(e)[:100]}", file=sys.stderr)

    print(f"  -> {where}", file=sys.stderr)
    return fid


def main():
    args = sys.argv[1:]
    folder = None
    if args and args[0] == "--folder":
        folder = args[1]
        args = args[2:]
    if not args:
        sys.exit(__doc__)
    s = service()
    for a in args:
        p = Path(a)
        if not p.is_file():
            print(f"  ! not a file: {a}", file=sys.stderr)
            continue
        fid = push(s, p, folder)
        print(f"{p.name}\thttps://drive.google.com/file/d/{fid}/view?usp=sharing")


if __name__ == "__main__":
    main()
