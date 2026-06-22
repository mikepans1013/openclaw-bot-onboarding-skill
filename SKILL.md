---
name: openclaw-bot-onboarding
description: Onboard a new OpenClaw bot/familiar with safe identity setup, official GitHub MCP connection, broad Google Workspace OAuth access, local secret storage, verification, and write-action guardrails.
---

# OpenClaw Bot Onboarding

Use this skill when creating or configuring a new OpenClaw bot/familiar that needs GitHub MCP access and Google Workspace OAuth access. This is deliberately user-ambiguous: never assume which human, GitHub account, org, or Google account should be connected.

## First Questions

Before installing or authorizing anything, ask:

1. Which human/operator owns this bot?
2. What should the bot be called, and where is its workspace?
3. Which GitHub user/org should it connect to?
4. Which Google account(s) should it connect to?
5. Is broad Workspace access approved for those Google accounts?
6. Should the bot be read-only by default, or are write helpers expected after explicit approval?

Stop if the user cannot identify the target account(s). Never reuse another bot's tokens or credentials.

## Safety Rules

- Treat GitHub tokens, Google OAuth credentials, refresh tokens, email/calendar/Drive data, and repo contents as sensitive.
- Never paste, print, commit, or summarize token/client-secret values.
- Store secrets under `~/.openclaw/secrets/` with `chmod 600`.
- Never reveal, relay, summarize, copy, or use OTP/2FA/login/verification codes. The human must read and enter codes directly.
- Do not send email, mutate calendars, edit/delete/share Drive files, update contacts/tasks, merge PRs, delete repos, change repo visibility, or perform destructive GitHub actions without explicit approval for the exact action.
- Prefer official integrations and first-party OAuth. Do not connect random outside MCPs/APIs without checking official docs, reputation, and approval.

## Files in This Skill

- `references/onboarding-checklist.md` — end-to-end OpenClaw bot onboarding checklist.
- `references/github-mcp.md` — official GitHub MCP reference, OpenClaw setup guidance, and install nuances.
- `references/google-workspace-oauth.md` — broad Google Workspace OAuth workflow and exact scope bundle.
- `scripts/google_oauth_bootstrap.py` — local OAuth bootstrap helper.
- `scripts/google_token_probe.py` — safe token/API verification helper.

Read `references/onboarding-checklist.md` first. Read the GitHub and Google references only when doing those setup phases.

## Standard Workflow

1. Clarify owner, bot identity, GitHub target, and Google account(s).
2. Set up bot workspace files (`AGENTS.md`, `SOUL.md`, `USER.md`, `TOOLS.md`) without copying another user's private memory.
3. Connect GitHub via the official GitHub MCP server reference, then verify tools load in OpenClaw.
4. Connect Google Workspace via OAuth using the broad `workspace-ea` scope bundle in `references/google-workspace-oauth.md`.
5. Verify scopes and APIs with `scripts/google_token_probe.py`.
6. Document only safe operational facts in `TOOLS.md`: account labels, helper commands, token file paths without values, verified APIs, and guardrails.
7. Run smoke tests and leave the bot with a short onboarding report listing what is connected, what is blocked, and what still needs human approval.

## Output Standard

When onboarding is complete, report:

- Bot name/workspace
- Connected GitHub account/org and MCP status
- Connected Google account(s) and verified APIs
- Secret file paths, without secret values
- Safety boundaries and pending approvals
- Smoke tests run and results
