# OpenClaw Bot Onboarding Checklist

## 1. Confirm target identity

Ask and record:

- Human/operator name
- Bot/familiar name
- Bot workspace path
- Primary chat surfaces/channels
- GitHub user/org to connect
- Google account(s) to connect
- Whether broad Google Workspace access is approved

Do not assume the current machine's user, current GitHub login, or existing Google tokens are the right target.

## 2. Prepare bot workspace

Create or review:

- `AGENTS.md` — operating rules and red lines
- `SOUL.md` — personality/tone
- `USER.md` — public-safe facts about the human/operator
- `TOOLS.md` — local tool notes, helper commands, token file paths without values
- `memory/` — daily notes directory
- `MEMORY.md` — only if this is a private main-session bot for a single human

Do not copy another user's private `MEMORY.md` into a new bot.

## 3. GitHub MCP

Read `references/github-mcp.md`.

Connect through the official GitHub MCP server only:

- https://github.com/github/github-mcp-server

After setup, verify:

- GitHub MCP tools appear in OpenClaw tool list/status.
- The authenticated account is the intended GitHub user or installation.
- Repository visibility matches intended access.
- Destructive actions require explicit approval.

## 4. Google Workspace OAuth

Read `references/google-workspace-oauth.md`.

Use the `workspace-ea` scope bundle when the user explicitly approves broad Google Workspace access. Store client secrets and token payloads in `~/.openclaw/secrets/` with `chmod 600`.

Verify using:

```bash
python3 scripts/google_token_probe.py \
  --token ~/.openclaw/secrets/google-<label>-oauth.json \
  --client-secret-json ~/.openclaw/secrets/google-<label>-client-secret.json \
  --checks userinfo,calendar,gmail,drive
```

## 5. Build only useful helpers

Do not build helpers just because APIs are available. Build only what makes onboarding easier or supports a known workflow.

Good default helpers:

- Calendar brief / upcoming events
- Gmail metadata/action summary, with OTP suppression
- Drive metadata search
- Token/API probe

Avoid broad data exports and write helpers unless specifically requested.

## 6. Final smoke test

Minimum checks:

- OpenClaw sees the GitHub MCP tools.
- Google token probe verifies the intended account.
- A read-only calendar or Gmail metadata query works.
- Secrets are not printed in logs or committed to git.
- `git status` is clean for any skill/repo created.

## 7. Final report

Include:

- What was connected
- Which account(s) were connected
- What was verified
- What remains blocked or needs approval
- Where safe docs/helper commands live
