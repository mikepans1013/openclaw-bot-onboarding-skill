# OpenClaw Bot Onboarding Checklist

## 1. Confirm connection targets

Assume OpenClaw's standard bot onboarding has already handled the bot name, owner, workspace, channel setup, and persona files. Do not ask those general onboarding questions here.

Ask and record only connection-specific targets:

- GitHub user/org to connect
- GitHub repo access scope: public-only, selected private repos, or broad private repo access
- Google account(s) to connect
- Whether broad Google Workspace access is approved
- Whether the bot should remain read-only by default, or whether write helpers are expected after exact approval

Do not assume the current machine's user, current GitHub login, or existing Google tokens are the right target.

## 2. GitHub MCP

Read `references/github-mcp.md`.

Connect through the official GitHub MCP server only:

- https://github.com/github/github-mcp-server

After setup, verify:

- GitHub MCP tools appear in OpenClaw tool list/status.
- The authenticated account is the intended GitHub user or installation.
- Repository visibility matches intended access.
- Destructive actions require explicit approval.

## 3. Google Workspace OAuth

Read `references/google-workspace-oauth.md`.

Use the `workspace-ea` scope bundle when the user explicitly approves broad Google Workspace access. Store client secrets and token payloads in `~/.openclaw/secrets/` with `chmod 600`.

Verify using:

```bash
python3 scripts/google_token_probe.py \
  --token ~/.openclaw/secrets/google-<label>-oauth.json \
  --client-secret-json ~/.openclaw/secrets/google-<label>-client-secret.json \
  --checks userinfo,calendar,gmail,drive
```

## 4. Build only useful helpers

Do not build helpers just because APIs are available. Build only what makes onboarding easier or supports a known workflow.

Good default helpers:

- Calendar brief / upcoming events
- Gmail metadata/action summary, with OTP suppression
- Drive metadata search
- Token/API probe

Avoid broad data exports and write helpers unless specifically requested.

## 5. Final smoke test

Minimum checks:

- OpenClaw sees the GitHub MCP tools.
- Google token probe verifies the intended account.
- A read-only calendar or Gmail metadata query works.
- Secrets are not printed in logs or committed to git.
- `git status` is clean for any skill/repo created.

## 6. Final report

Include:

- What was connected
- Which account(s) were connected
- What was verified
- What remains blocked or needs approval
- Where safe docs/helper commands live
