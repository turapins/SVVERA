#!/usr/bin/env python3
"""
One-time Frame.io V4 OAuth2 authorization.
Run once to get access_token + refresh_token saved to .env

Usage:
    python3 scripts/frameio_auth.py

Requirements:
    pip install requests python-dotenv

Set in .env before running:
    FRAMEIO_CLIENT_ID=...
    FRAMEIO_CLIENT_SECRET=...
"""
import http.server
import os
import ssl
import subprocess
import sys
import tempfile
import threading
import urllib.parse
import webbrowser

import requests
from dotenv import dotenv_values, set_key

ADOBE_AUTH_URL = "https://ims-na1.adobelogin.com/ims/authorize/v2"
ADOBE_TOKEN_URL = "https://ims-na1.adobelogin.com/ims/token/v3"
REDIRECT_URI = "https://localhost:8080/oauth/callback"
SCOPES = "openid,profile,email,offline_access,AdobeID,frameio.all"

ENV_PATH = os.path.join(os.path.dirname(__file__), "..", ".env")
ENV_PATH = os.path.abspath(ENV_PATH)

_received_code: list[str] = []
_server_done = threading.Event()


class _CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        if "code" in params:
            _received_code.append(params["code"][0])
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h2>Authorization successful. You can close this tab.</h2>")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"<h2>No code received. Try again.</h2>")
        _server_done.set()

    def log_message(self, *args):
        pass  # suppress access logs


def _make_self_signed_cert():
    """Generate a throwaway self-signed cert for localhost."""
    import subprocess, tempfile
    cert_file = tempfile.NamedTemporaryFile(suffix=".pem", delete=False)
    key_file = tempfile.NamedTemporaryFile(suffix=".key", delete=False)
    cert_file.close()
    key_file.close()
    subprocess.run([
        "openssl", "req", "-x509", "-newkey", "rsa:2048",
        "-keyout", key_file.name,
        "-out", cert_file.name,
        "-days", "1", "-nodes",
        "-subj", "/CN=localhost",
    ], check=True, capture_output=True)
    return cert_file.name, key_file.name


def _run_server(cert, key):
    server = http.server.HTTPServer(("localhost", 8080), _CallbackHandler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)
    server.timeout = 120
    server.handle_request()


def main():
    env = dotenv_values(ENV_PATH)
    client_id = env.get("FRAMEIO_CLIENT_ID", "").strip()
    client_secret = env.get("FRAMEIO_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        print("ERROR: Set FRAMEIO_CLIENT_ID and FRAMEIO_CLIENT_SECRET in .env first.")
        sys.exit(1)

    print("Generating self-signed cert for localhost:8080 ...")
    cert, key = _make_self_signed_cert()

    t = threading.Thread(target=_run_server, args=(cert, key), daemon=True)
    t.start()

    auth_params = urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "response_type": "code",
    })
    auth_url = f"{ADOBE_AUTH_URL}?{auth_params}"
    print(f"\nOpening browser for Adobe login...\n{auth_url}\n")
    print("NOTE: Your browser will warn about a self-signed certificate on the callback.")
    print("      Click 'Advanced' → 'Proceed to localhost' to complete the flow.\n")
    webbrowser.open(auth_url)

    print("Waiting for callback (120s timeout)...")
    _server_done.wait(timeout=120)

    if not _received_code:
        print("ERROR: No authorization code received within 120 seconds.")
        sys.exit(1)

    code = _received_code[0]
    print(f"Got authorization code. Exchanging for tokens...")

    resp = requests.post(
        ADOBE_TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        timeout=15,
    )
    resp.raise_for_status()
    tokens = resp.json()

    access_token = tokens.get("access_token", "")
    refresh_token = tokens.get("refresh_token", "")

    if not access_token:
        print(f"ERROR: No access_token in response: {tokens}")
        sys.exit(1)

    set_key(ENV_PATH, "FRAMEIO_ACCESS_TOKEN", access_token)
    if refresh_token:
        set_key(ENV_PATH, "FRAMEIO_REFRESH_TOKEN", refresh_token)
        print(f"Saved FRAMEIO_ACCESS_TOKEN + FRAMEIO_REFRESH_TOKEN to .env")
    else:
        print(f"Saved FRAMEIO_ACCESS_TOKEN to .env (no refresh_token returned)")

    os.unlink(cert)
    os.unlink(key)
    print("\nDone! Run your pipeline — frameio_upload.py will use these tokens automatically.")


if __name__ == "__main__":
    main()
