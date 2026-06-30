# OpenClaw Bot Onboarding Checklist

## 1. Confirm connection targets

Assume OpenClaw's standard bot onboarding has already handled the bot name, owner, workspace, channel setup, and persona files. Do not ask about, inspect, or change those general onboarding settings here.

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

- Whether the install was intended as prep-only or live
- GitHub MCP tools appear in OpenClaw tool list/status.
- The authenticated account is the intended GitHub user or installation.
- Repository visibility matches intended access.
- Destructive actions require explicit approval.

## 3. Google Workspace OAuth

Google OAuth is intentionally not documented in this onboarding repo. Use the dedicated private repo instead:

- `https://github.com/mikepans1013/google-workspace-oauth-skill`
- Local canonical path when available: `/Users/henrykent/skills/google-workspace-oauth`

Follow that skill for scope selection, OAuth bootstrap, token probing, Drive structure/routing, and safety rules. Do not copy or fork those instructions back into this repo. Verification commands should come from that repo's `SKILL.md` / scripts.

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
- Google OAuth, if requested, was completed and verified using `mikepans1013/google-workspace-oauth-skill`.
- A read-only calendar/Gmail/Drive metadata query works, as appropriate for the approved scopes.
- Secrets are not printed in logs or committed to git.
- `git status` is clean for any skill/repo created.

## 6. Final report

Include:

- What was connected
- Which account(s) were connected
- What was verified
- What remains blocked or needs approval
- Where safe docs/helper commands live
