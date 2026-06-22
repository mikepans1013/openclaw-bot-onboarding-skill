# Google Workspace OAuth for OpenClaw Bot Onboarding

This is adapted from the `google-workspace-oauth` skill pattern. Use it when onboarding a new bot that needs direct Google Workspace API access.

## First questions

Ask which Google user(s) to connect. Do not assume the current user's account.

For each account, confirm:

- email address
- account label for local files, e.g. `client-a` or `ops-admin`
- whether broad Workspace access is approved
- whether writes are expected, or read-only behavior should remain the default

## Safety rules

- Google tokens and client secrets are sensitive.
- Store secrets under `~/.openclaw/secrets/` with `chmod 600`.
- Do not reveal OTP/2FA/login codes. The human completes Google login and 2FA directly.
- Even with broad scopes, helpers default to read-only behavior.
- Ask for exact approval before sending email, changing calendar events, editing/deleting/sharing Drive files, changing Docs/Sheets/Slides/Forms, or updating contacts/tasks.

## Required APIs

Enable the APIs needed for the broad Workspace bundle:

- Gmail API
- Google Calendar API
- Google Drive API
- Google Drive Activity API
- Google Docs API
- Google Sheets API
- Google Slides API
- Google Forms API
- Google Tasks API
- People API / Contacts
- OAuth userinfo / OpenID Connect

## Broad onboarding scope bundle: `workspace-ea`

Use the same broad scope bundle from the existing Google OAuth skill when the user approves full bot onboarding access:

```text
openid
email
profile
https://www.googleapis.com/auth/gmail.modify
https://www.googleapis.com/auth/gmail.send
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/drive
https://www.googleapis.com/auth/drive.activity.readonly
https://www.googleapis.com/auth/documents
https://www.googleapis.com/auth/spreadsheets
https://www.googleapis.com/auth/presentations
https://www.googleapis.com/auth/forms.body
https://www.googleapis.com/auth/forms.responses.readonly
https://www.googleapis.com/auth/tasks
https://www.googleapis.com/auth/contacts
```

## OAuth client

Use a Google Cloud project controlled by the human/org. A Desktop app OAuth client is usually simplest for local OpenClaw helpers.

Store the downloaded client secret JSON as:

```text
~/.openclaw/secrets/google-<label>-client-secret.json
```

Set permissions:

```bash
chmod 600 ~/.openclaw/secrets/google-<label>-client-secret.json
```

## Bootstrap token

Run from this skill directory:

```bash
python3 scripts/google_oauth_bootstrap.py \
  --account-label <label> \
  --email user@example.com \
  --client-secret-json ~/.openclaw/secrets/google-<label>-client-secret.json \
  --token-out ~/.openclaw/secrets/google-<label>-oauth.json \
  --scope-bundle workspace-ea
```

The human must complete browser login/consent directly. Do not ask them to paste OTP/2FA codes into chat.

## Verify token and APIs

```bash
python3 scripts/google_token_probe.py \
  --token ~/.openclaw/secrets/google-<label>-oauth.json \
  --client-secret-json ~/.openclaw/secrets/google-<label>-client-secret.json \
  --checks userinfo,calendar,gmail,drive
```

Verify the returned account email matches the intended user.

## Helper design

Build only helpers that make onboarding easy or support a known workflow. Do not build broad exporters by default.

Recommended pattern:

```text
read token payload -> refresh access token -> save refreshed token -> call Google API -> print minimal operational summary
```

Good first helpers:

- calendar brief
- Gmail action/metadata summary with OTP suppression
- Drive metadata search
- token/API healthcheck

## Documentation in local TOOLS.md

Document safe details in `TOOLS.md`:

- account label
- connected email address
- token path and client-secret path, without values
- helper commands
- verified APIs/date
- write-action guardrails
