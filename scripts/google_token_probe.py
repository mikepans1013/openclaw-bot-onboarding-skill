#!/usr/bin/env python3
"""Refresh and safely probe a Google OAuth token payload.

Prints only status/count summaries. Does not print tokens or raw private content.
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

CHECKS = ["userinfo", "calendar", "gmail", "drive", "docs", "sheets", "slides", "forms", "tasks", "contacts"]

def load_client_secret(path):
    data = json.load(open(os.path.expanduser(path)))
    cfg = data.get("installed") or data.get("web") or data
    return cfg.get("client_secret")

def request_json(url, access_token=None, data=None):
    headers = {"Accept": "application/json"}
    if access_token:
        headers["Authorization"] = "Bearer " + access_token
    body = None
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())

def save(path, payload):
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
        f.write("\n")
    os.chmod(path, 0o600)

def refresh(payload, client_secret):
    token = payload.get("token") or {}
    refresh_token = token.get("refresh_token")
    if not refresh_token:
        raise RuntimeError("token payload has no refresh_token")
    new = request_json("https://oauth2.googleapis.com/token", data={
        "client_id": payload["client_id"],
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
    })
    token.update(new)
    payload["token"] = token
    return token["access_token"]

def safe_call(name, fn):
    try:
        return {"check": name, "status": "ok", **fn()}
    except urllib.error.HTTPError as e:
        msg = e.read().decode(errors="replace")[:300]
        return {"check": name, "status": "error", "error": f"HTTP {e.code}: {msg}"}
    except Exception as e:
        return {"check": name, "status": "error", "error": str(e)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", required=True)
    ap.add_argument("--client-secret-json", required=True)
    ap.add_argument("--checks", default="userinfo,calendar", help="comma-separated: " + ",".join(CHECKS))
    args = ap.parse_args()

    token_path = os.path.expanduser(args.token)
    payload = json.load(open(token_path))
    client_secret = load_client_secret(args.client_secret_json)
    if not client_secret:
        raise SystemExit("client secret JSON missing client_secret")
    access = refresh(payload, client_secret)
    save(token_path, payload)

    checks = [c.strip() for c in args.checks.split(",") if c.strip()]
    results = []

    if "userinfo" in checks:
        results.append(safe_call("userinfo", lambda: {
            "email": request_json("https://openidconnect.googleapis.com/v1/userinfo", access).get("email")
        }))
    if "calendar" in checks:
        results.append(safe_call("calendar", lambda: {
            "calendar_count": len(request_json("https://www.googleapis.com/calendar/v3/users/me/calendarList?maxResults=250", access).get("items", []))
        }))
    if "gmail" in checks:
        results.append(safe_call("gmail", lambda: {
            "profile_email": request_json("https://gmail.googleapis.com/gmail/v1/users/me/profile", access).get("emailAddress")
        }))
    if "drive" in checks:
        results.append(safe_call("drive", lambda: {
            "sample_file_count": len(request_json("https://www.googleapis.com/drive/v3/files?pageSize=10&fields=files(id%2Cname)", access).get("files", []))
        }))
    if "docs" in checks:
        results.append(safe_call("docs", lambda: {
            "note": "Docs API has no list endpoint; verify via Drive doc search or fetch a known doc ID."
        }))
    if "sheets" in checks:
        results.append(safe_call("sheets", lambda: {
            "note": "Sheets API has no list endpoint; verify by opening a known spreadsheet ID."
        }))
    if "slides" in checks:
        results.append(safe_call("slides", lambda: {
            "note": "Slides API has no list endpoint; verify by opening a known presentation ID."
        }))
    if "forms" in checks:
        results.append(safe_call("forms", lambda: {
            "note": "Forms API has no list endpoint; verify by opening a known form ID."
        }))
    if "tasks" in checks:
        results.append(safe_call("tasks", lambda: {
            "tasklist_count": len(request_json("https://tasks.googleapis.com/tasks/v1/users/@me/lists?maxResults=20", access).get("items", []))
        }))
    if "contacts" in checks:
        results.append(safe_call("contacts", lambda: {
            "connection_sample_count": len(request_json("https://people.googleapis.com/v1/people/me/connections?pageSize=10&personFields=names,emailAddresses", access).get("connections", []))
        }))

    print(json.dumps({
        "status": "ok",
        "account_label": payload.get("account_label"),
        "email": payload.get("email"),
        "scope_count": len(payload.get("scopes") or []),
        "checks": results,
    }, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}), file=sys.stderr)
        sys.exit(1)
