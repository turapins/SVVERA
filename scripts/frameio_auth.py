#!/usr/bin/env python3
"""
One-time Frame.io V4 OAuth2 authorization.
Run once to get access_token + refresh_token saved to .env

Usage:
    uv run --with requests --with python-dotenv scripts/frameio_auth.py

Set in .env before running:
    FRAMEIO_CLIENT_ID=...
    FRAMEIO_CLIENT_SECRET=...
"""
import os
import sys
import urllib.parse
import webbrowser

import requests
from dotenv import dotenv_values, set_key

ADOBE_AUTH_URL = "https://ims-na1.adobelogin.com/ims/authorize/v2"
ADOBE_TOKEN_URL = "https://ims-na1.adobelogin.com/ims/token/v3"
REDIRECT_URI = "https://localhost:8080/oauth/callback"
SCOPES = "openid,profile,email,offline_access,AdobeID,frameio.all"

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))


def main():
    env = dotenv_values(ENV_PATH)
    client_id = env.get("FRAMEIO_CLIENT_ID", "").strip()
    client_secret = env.get("FRAMEIO_CLIENT_SECRET", "").strip()

    if not client_id or not client_secret:
        print("ERROR: Set FRAMEIO_CLIENT_ID and FRAMEIO_CLIENT_SECRET in .env first.")
        sys.exit(1)

    auth_params = urllib.parse.urlencode({
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "response_type": "code",
    })
    auth_url = f"{ADOBE_AUTH_URL}?{auth_params}"

    print("\nOpening Adobe login in your browser...")
    webbrowser.open(auth_url)

    print("""
After you authorize, Adobe will redirect your browser to:
    https://localhost:8080/oauth/callback?code=XXXXXXXX...

The page will show "connection refused" — that's fine.
Copy the FULL URL from the browser address bar and paste it here.
""")
    raw = input("Paste the full redirect URL: ").strip()

    # Extract code from URL or accept raw code
    if raw.startswith("http"):
        parsed = urllib.parse.urlparse(raw)
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get("code", [""])[0]
    else:
        code = raw  # user pasted just the code value

    if not code:
        print("ERROR: Could not extract authorization code from the URL.")
        sys.exit(1)

    print("Exchanging code for tokens...")
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

    if not resp.ok:
        print(f"ERROR: Token exchange failed ({resp.status_code}): {resp.text}")
        sys.exit(1)

    tokens = resp.json()
    access_token = tokens.get("access_token", "")
    refresh_token = tokens.get("refresh_token", "")

    if not access_token:
        print(f"ERROR: No access_token in response: {tokens}")
        sys.exit(1)

    set_key(ENV_PATH, "FRAMEIO_ACCESS_TOKEN", access_token)
    if refresh_token:
        set_key(ENV_PATH, "FRAMEIO_REFRESH_TOKEN", refresh_token)
        print("Saved FRAMEIO_ACCESS_TOKEN + FRAMEIO_REFRESH_TOKEN to .env")
    else:
        print("Saved FRAMEIO_ACCESS_TOKEN to .env (no refresh_token returned)")

    print("\nDone! Frame.io V4 auth complete.")


if __name__ == "__main__":
    main()
