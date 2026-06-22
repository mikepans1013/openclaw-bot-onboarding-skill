---
name: openclaw-bot-onboarding
description: Onboard a new OpenClaw bot/familiar with safe identity setup, official GitHub MCP connection, broad Google Workspace OAuth access, local secret storage, verification, and write-action guardrails.
---

# OpenClaw Bot Onboarding

Use this skill when an already-created OpenClaw bot/familiar needs GitHub MCP access and Google Workspace OAuth access. Assume OpenClaw's normal bot onboarding has already handled bot identity, name, workspace, and basic persona files. This skill is deliberately account-ambiguous: never assume which GitHub account, org, or Google account should be connected.

## First Questions

Before installing or authorizing anything, ask only the connection-specific questions:

1. Which GitHub user/org should this bot connect to?
2. Which Google account(s) should this bot connect to?
3. Is broad Workspace access approved for those Google account(s)?
4. Should the bot stay read-only by default, or are write helpers expected after explicit approval?

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

1. Clarify GitHub target, Google account(s), broad-scope approval, and write boundaries.
2. Connect GitHub via the official GitHub MCP server reference, then verify tools load in OpenClaw.
3. Connect Google Workspace via OAuth using the broad `workspace-ea` scope bundle in `references/google-workspace-oauth.md`.
4. Verify scopes and APIs with `scripts/google_token_probe.py`.
5. Document only safe operational facts in `TOOLS.md`: account labels, helper commands, token file paths without values, verified APIs, and guardrails.
6. Run smoke tests and leave the bot with a short connection report listing what is connected, what is blocked, and what still needs human approval.

## Output Standard

When onboarding is complete, report:

- Connected GitHub account/org and MCP status
- Connected Google account(s) and verified APIs
- Secret file paths, without secret values
- Safety boundaries and pending approvals
- Smoke tests run and results
