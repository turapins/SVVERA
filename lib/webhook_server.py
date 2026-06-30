"""Shared webhook server — receives events from Frame.io, ClickUp, and GitHub.

Run:
    python lib/webhook_server.py
    # or
    uvicorn lib.webhook_server:app --host 0.0.0.0 --port 8080

Routes:
    POST /webhook/frameio   — asset.ready / comment.created / asset.approved
    POST /webhook/clickup   — taskStatusUpdated / taskCommentPosted / taskCreated
    POST /webhook/github    — push / pull_request events
    GET  /health            — {"status": "ok"}

Each event is appended to lib/webhook_events.jsonl as one JSON line.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from fastapi import FastAPI, Header, HTTPException, Request, Response
    import uvicorn
except ImportError:
    sys.exit(
        "fastapi and uvicorn are required. "
        "pip install fastapi uvicorn[standard]"
    )

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("webhook_server")

app = FastAPI(title="OpenMontage Webhook Server", version="0.1.0")

_EVENTS_LOG = Path(__file__).parent / "webhook_events.jsonl"


def _append_event(source: str, event: str, payload: dict[str, Any]) -> None:
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "event": event,
        "payload": payload,
    }
    with open(_EVENTS_LOG, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    log.info("[%s] %s", source, event)


def _verify_hmac(secret: str, raw_body: bytes, signature_header: str, prefix: str = "sha256=") -> bool:
    expected = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    incoming = signature_header.removeprefix(prefix)
    return hmac.compare_digest(expected, incoming)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/webhook/frameio")
async def webhook_frameio(request: Request) -> Response:
    raw = await request.body()
    secret = os.environ.get("FRAMEIO_WEBHOOK_SECRET", "")

    if secret:
        sig = request.headers.get("x-frameio-signature", "")
        if not _verify_hmac(secret, raw, sig):
            raise HTTPException(status_code=401, detail="Invalid Frame.io signature")

    payload: dict[str, Any] = {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event_type = payload.get("type", "unknown")
    resource = payload.get("resource", {})
    asset_name = resource.get("name", "")

    if event_type == "asset.approved":
        log.info("APPROVED: %s", asset_name)
    elif event_type == "comment.created":
        log.info("COMMENT on %s: %s", asset_name, resource.get("text", "")[:100])
    elif event_type == "asset.ready":
        log.info("ASSET READY: %s", asset_name)

    _append_event("frameio", event_type, payload)
    return Response(status_code=200)


@app.post("/webhook/clickup")
async def webhook_clickup(request: Request) -> Response:
    raw = await request.body()
    secret = os.environ.get("CLICKUP_WEBHOOK_SECRET", "")

    if secret:
        sig = request.headers.get("x-signature", "")
        if sig and not _verify_hmac(secret, raw, sig, prefix=""):
            raise HTTPException(status_code=401, detail="Invalid ClickUp signature")

    payload: dict[str, Any] = {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    event_type = payload.get("event", "unknown")
    task_id = payload.get("task_id", "")
    log.info("ClickUp event=%s task_id=%s", event_type, task_id)

    _append_event("clickup", event_type, payload)
    return Response(status_code=200)


@app.post("/webhook/github")
async def webhook_github(request: Request) -> Response:
    raw = await request.body()
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET", "")

    if secret:
        sig = request.headers.get("x-hub-signature-256", "")
        if not _verify_hmac(secret, raw, sig, prefix="sha256="):
            raise HTTPException(status_code=401, detail="Invalid GitHub signature")

    payload: dict[str, Any] = {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    github_event = request.headers.get("x-github-event", "unknown")
    ref = payload.get("ref", "")
    repo = payload.get("repository", {}).get("full_name", "")
    log.info("GitHub event=%s ref=%s repo=%s", github_event, ref, repo)

    _append_event("github", github_event, {"ref": ref, "repo": repo, "action": payload.get("action", "")})
    return Response(status_code=200)


if __name__ == "__main__":
    port = int(os.environ.get("WEBHOOK_PORT", "8080"))
    log.info("Starting webhook server on port %d", port)
    uvicorn.run(app, host="0.0.0.0", port=port)
