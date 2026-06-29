"""Shared webhook server for SVVERA integrations.

Listens on :8080 (WEBHOOK_PORT env var to override).
Routes:
    POST /webhook/github   — push + pull_request events from GitHub
    POST /webhook/frameio  — asset.approved, comment.created from Frame.io
    POST /webhook/clickup  — taskStatusUpdated, taskCommentPosted from ClickUp

Run:
    uv run --with fastapi --with uvicorn lib/webhook_server.py

Each route verifies the provider's HMAC-SHA256 signature before dispatching.
"""
from __future__ import annotations

import hashlib
import hmac
import os
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.responses import JSONResponse

app = FastAPI(title="SVVERA Webhook Server", version="1.0.0")


def _verify_hmac(secret: str, payload: bytes, sig_header: Optional[str], prefix: str = "sha256=") -> None:
    """Raise 401 if signature doesn't match. No-op when secret is empty (dev mode)."""
    if not secret:
        return
    if not sig_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing signature header")
    expected = prefix + hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig_header):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signature mismatch")


# ── GitHub ────────────────────────────────────────────────────────────────────

@app.post("/webhook/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: Optional[str] = Header(None),
    x_github_event: Optional[str] = Header(None),
):
    body = await request.body()
    secret = os.environ.get("GITHUB_WEBHOOK_SECRET", "")
    _verify_hmac(secret, body, x_hub_signature_256, prefix="sha256=")

    payload = await request.json()
    event = x_github_event or "unknown"

    if event == "push":
        ref = payload.get("ref", "")
        repo = payload.get("repository", {}).get("full_name", "")
        pusher = payload.get("pusher", {}).get("name", "")
        commits = len(payload.get("commits", []))
        print(f"[github] push → {ref} ({commits} commit(s)) by {pusher} in {repo}")

        if ref.startswith("refs/heads/feat/"):
            branch = ref.removeprefix("refs/heads/")
            print(f"[github] feat branch push detected: {branch} — preflight recommended")

    elif event == "pull_request":
        pr = payload.get("pull_request", {})
        action = payload.get("action", "")
        merged = pr.get("merged", False)
        base = pr.get("base", {}).get("ref", "")
        title = pr.get("title", "")
        number = pr.get("number", "?")

        print(f"[github] pull_request #{number} '{title}' action={action} merged={merged} base={base}")

        if action == "closed" and merged and base == "main":
            print(f"[github] PR #{number} merged to main — triggering skills refresh")
            _on_pr_merged_to_main(pr)

    else:
        print(f"[github] unhandled event: {event}")

    return JSONResponse({"ok": True})


def _on_pr_merged_to_main(pr: dict) -> None:
    """Called when a PR merges into main. Logs the event; extend to trigger CI."""
    title = pr.get("title", "")
    number = pr.get("number", "?")
    author = pr.get("user", {}).get("login", "unknown")
    print(f"[github] skills refresh triggered by PR #{number} '{title}' from @{author}")


# ── Frame.io ──────────────────────────────────────────────────────────────────

@app.post("/webhook/frameio")
async def frameio_webhook(
    request: Request,
    x_frameio_signature: Optional[str] = Header(None),
):
    body = await request.body()
    secret = os.environ.get("FRAMEIO_WEBHOOK_SECRET", "")
    _verify_hmac(secret, body, x_frameio_signature, prefix="sha256=")

    payload = await request.json()
    event_type = payload.get("type", "unknown")
    resource = payload.get("resource", {})
    asset_name = resource.get("name", "?")

    print(f"[frameio] event={event_type} asset='{asset_name}'")

    if event_type == "asset.approved":
        print(f"[frameio] APPROVED: '{asset_name}' — ready for export to Drive")
    elif event_type == "comment.created":
        text = resource.get("text", "")
        author = payload.get("user", {}).get("name", "?")
        print(f"[frameio] comment by {author}: {text[:120]}")

    return JSONResponse({"ok": True})


# ── ClickUp ───────────────────────────────────────────────────────────────────

@app.post("/webhook/clickup")
async def clickup_webhook(
    request: Request,
    x_signature: Optional[str] = Header(None),
):
    body = await request.body()
    secret = os.environ.get("CLICKUP_WEBHOOK_SECRET", "")
    _verify_hmac(secret, body, x_signature, prefix="")

    payload = await request.json()
    event = payload.get("event", "unknown")
    task_id = payload.get("task_id", "?")

    print(f"[clickup] event={event} task_id={task_id}")

    if event == "taskStatusUpdated":
        history = payload.get("history_items", [{}])
        new_status = history[0].get("after", {}).get("status", "?") if history else "?"
        print(f"[clickup] task {task_id} → status: {new_status}")
    elif event == "taskCommentPosted":
        print(f"[clickup] comment on task {task_id}")

    return JSONResponse({"ok": True})


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "routes": ["/webhook/github", "/webhook/frameio", "/webhook/clickup"]}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("WEBHOOK_PORT", 8080))
    uvicorn.run("lib.webhook_server:app", host="0.0.0.0", port=port, reload=False)
