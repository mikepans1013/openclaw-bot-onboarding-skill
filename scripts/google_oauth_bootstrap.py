#!/usr/bin/env python3
"""Bootstrap a local Google OAuth token payload for account-agnostic helpers.

Uses a loopback redirect, exchanges the auth code, verifies account identity when
possible, and writes a refresh-capable token payload with chmod 600.
"""
import argparse
import http.server
import json
import os
import secrets
import socketserver
import sys
import threading
import urllib.parse
import urllib.request
import webbrowser

SCOPE_BUNDLES = {
    "calendar-read": ["openid", "email", "profile", "https://www.googleapis.com/auth/calendar.readonly"],
    "calendar-write": ["openid", "email", "profile", "https://www.googleapis.com/auth/calendar"],
    "workspace-ea-readmostly": [
        "openid", "email", "profile",
        "https://www.googleapis.com/auth/calendar.readonly",
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
        "https://www.googleapis.com/auth/drive.activity.readonly",
        "https://www.googleapis.com/auth/documents.readonly",
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/presentations.readonly",
        "https://www.googleapis.com/auth/forms.body.readonly",
        "https://www.googleapis.com/auth/forms.responses.readonly",
        "https://www.googleapis.com/auth/tasks.readonly",
        "https://www.googleapis.com/auth/contacts.readonly",
    ],
    "workspace-ea": [
        "openid", "email", "profile",
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.activity.readonly",
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/presentations",
        "https://www.googleapis.com/auth/forms.body",
        "https://www.googleapis.com/auth/forms.responses.readonly",
        "https://www.googleapis.com/auth/tasks",
        "https://www.googleapis.com/auth/contacts",
    ],
}

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    result = {}
    expected_state = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        state = (params.get("state") or [None])[0]
        code = (params.get("code") or [None])[0]
        error = (params.get("error") or [None])[0]
        if state != self.expected_state:
            self.result = {"error": "state_mismatch"}
        elif error:
            self.result = {"error": error}
        elif code:
            self.result = {"code": code}
        else:
            self.result = {"error": "missing_code"}
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body><h2>Google OAuth complete.</h2><p>You can close this tab and return to OpenClaw.</p></body></html>")

    def log_message(self, fmt, *args):
        return

def load_client(path):
    data = json.load(open(os.path.expanduser(path)))
    cfg = data.get("installed") or data.get("web") or data
    client_id = cfg.get("client_id")
    client_secret = cfg.get("client_secret")
    if not client_id or not client_secret:
        raise SystemExit("client secret JSON must include client_id and client_secret")
    return client_id, client_secret

def post_json(url, data):
    req = urllib.request.Request(
        url,
        data=urllib.parse.urlencode(data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def get_json(url, access_token):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + access_token, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--account-label", required=True, help="short local label, e.g. mhppros")
    ap.add_argument("--email", help="expected authenticated email")
    ap.add_argument("--client-secret-json", required=True)
    ap.add_argument("--token-out", required=True)
    ap.add_argument("--scope-bundle", choices=sorted(SCOPE_BUNDLES), default="calendar-read")
    ap.add_argument("--scope", action="append", default=[], help="extra or explicit scope; repeatable")
    ap.add_argument("--port", type=int, default=0, help="loopback port; 0 chooses a free port")
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    client_id, client_secret = load_client(args.client_secret_json)
    scopes = list(dict.fromkeys(SCOPE_BUNDLES[args.scope_bundle] + args.scope))
    state = secrets.token_urlsafe(24)

    Handler = CallbackHandler
    Handler.expected_state = state
    Handler.result = {}
    with socketserver.TCPServer(("127.0.0.1", args.port), Handler) as httpd:
        port = httpd.server_address[1]
        redirect_uri = f"http://127.0.0.1:{port}/callback"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(scopes),
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }
        url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
        print("Open this Google OAuth URL:")
        print(url)
        if not args.no_browser:
            webbrowser.open(url)
        thread = threading.Thread(target=httpd.handle_request, daemon=True)
        thread.start()
        thread.join(timeout=300)
        if not Handler.result:
            raise SystemExit("timed out waiting for OAuth callback")
        if Handler.result.get("error"):
            raise SystemExit("OAuth failed: " + Handler.result["error"])
        code = Handler.result["code"]

    token = post_json("https://oauth2.googleapis.com/token", {
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    })
    access_token = token.get("access_token")
    if not token.get("refresh_token"):
        print("WARNING: Google did not return a refresh_token. Revoke prior app consent and rerun if this must be long-lived.", file=sys.stderr)
    actual_email = None
    if access_token:
        try:
            actual_email = get_json("https://openidconnect.googleapis.com/v1/userinfo", access_token).get("email")
        except Exception as e:
            print(f"WARNING: userinfo verification failed: {e}", file=sys.stderr)
    if args.email and actual_email and args.email.lower() != actual_email.lower():
        raise SystemExit(f"authenticated email mismatch: expected {args.email}, got {actual_email}")

    payload = {
        "account_label": args.account_label,
        "email": actual_email or args.email,
        "client_id": client_id,
        "scopes": scopes,
        "token": token,
    }
    out = os.path.expanduser(args.token_out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    os.chmod(out, 0o600)
    print(json.dumps({"status": "ok", "email": payload["email"], "scope_count": len(scopes), "token_path": out}, indent=2))

if __name__ == "__main__":
    main()
