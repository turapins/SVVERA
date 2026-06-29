#!/usr/bin/env python3
"""
One-time Pinterest OAuth2 authorization.
Run once to get an access_token + refresh_token saved to .env

Usage:
    uv run --with requests --with python-dotenv scripts/pinterest_auth.py

Set in .env before running:
    PINTEREST_APP_ID=...
    PINTEREST_APP_SECRET=...
"""
import os
import sys
import urllib.parse
import webbrowser
import base64

import requests
from dotenv import dotenv_values, set_key

PINTEREST_AUTH_URL = "https://www.pinterest.com/oauth/"
PINTEREST_TOKEN_URL = "https://api.pinterest.com/v5/oauth/token"
REDIRECT_URI = "https://vocalimage.com"
SCOPES = "boards:read,pins:read,user_accounts:read"

ENV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))


def main():
    env = dotenv_values(ENV_PATH)
    app_id = env.get("PINTEREST_APP_ID", "").strip()
    app_secret = env.get("PINTEREST_APP_SECRET", "").strip()

    if not app_id or not app_secret:
        print("ERROR: Set PINTEREST_APP_ID and PINTEREST_APP_SECRET in .env first.")
        print("  Get them at: https://developers.pinterest.com/apps/")
        sys.exit(1)

    auth_params = urllib.parse.urlencode({
        "client_id": app_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
    })
    auth_url = f"{PINTEREST_AUTH_URL}?{auth_params}"

    print("\nOpening Pinterest login in your browser...")
    webbrowser.open(auth_url)

    print(f"""
After you authorize, Pinterest will redirect to:
    {REDIRECT_URI}?code=XXXXXXXX...

Copy the FULL URL from the browser address bar and paste it here.
(The page itself doesn't matter — we just need the URL)
""")
    raw = input("Paste the full redirect URL: ").strip()

    if raw.startswith("http"):
        parsed = urllib.parse.urlparse(raw)
        params = urllib.parse.parse_qs(parsed.query)
        code = params.get("code", [""])[0]
    else:
        code = raw

    if not code:
        print("ERROR: Could not extract authorization code from the URL.")
        sys.exit(1)

    print("Exchanging code for tokens...")

    credentials = base64.b64encode(f"{app_id}:{app_secret}".encode()).decode()
    resp = requests.post(
        PINTEREST_TOKEN_URL,
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
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

    set_key(ENV_PATH, "PINTEREST_ACCESS_TOKEN", access_token)
    if refresh_token:
        set_key(ENV_PATH, "PINTEREST_REFRESH_TOKEN", refresh_token)
        print("Saved PINTEREST_ACCESS_TOKEN + PINTEREST_REFRESH_TOKEN to .env")
    else:
        print("Saved PINTEREST_ACCESS_TOKEN to .env")

    # Show token expiry if present
    expires_in = tokens.get("expires_in")
    if expires_in:
        days = expires_in // 86400
        print(f"Token expires in ~{days} days")

    print("\nDone! Pinterest auth complete.")


if __name__ == "__main__":
    main()
