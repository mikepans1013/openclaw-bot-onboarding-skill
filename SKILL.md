---
name: openclaw-bot-onboarding
description: Connect an existing OpenClaw bot/familiar to the official GitHub MCP server and route Google Workspace OAuth setup to the dedicated private Google OAuth skill repo, with local secret storage, verification, and write-action guardrails.
---

# OpenClaw Bot Onboarding

Use this skill when an already-created OpenClaw bot/familiar needs GitHub MCP access and/or a handoff to the dedicated Google Workspace OAuth setup skill. Assume OpenClaw's normal bot onboarding has already handled bot identity, name, workspace, channels, and persona. Do not ask about or change those here. This skill is deliberately account-ambiguous: never assume which GitHub account, org, or Google account should be connected.

## Operating Modes

Before doing live setup, determine which mode the user wants:

- **Prep only** — review docs, collect requirements, propose file paths/labels, but do not save secrets or change live config.
- **Live GitHub only** — install/configure GitHub MCP only.
- **Live Google only** — set up Google OAuth only.
- **Full live onboarding** — do both GitHub MCP and Google OAuth.

If the user's request is ambiguous (for example, "begin this process"), default to **Prep only** and ask before persisting credentials or editing live config.

## First Response Contract

The first substantive reply should explicitly confirm or ask:

1. Is this **prep only** or **live setup**?
2. For GitHub, should access start **read-only** or **write-capable with explicit per-action approval**?
3. For Google, is broad Workspace access already approved, or is approval still pending?
4. Should secrets be stored locally under `~/.openclaw/secrets/` on this host?

Do not persist tokens, client secrets, or live MCP config until the user has clearly authorized the relevant live setup mode.

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

Read `references/onboarding-checklist.md` first. Read `references/github-mcp.md` for GitHub MCP setup. For Google OAuth, use the dedicated private repo `mikepans1013/google-workspace-oauth-skill`; this repo intentionally does not duplicate Google OAuth setup instructions or scripts.

## Standard Workflow

1. Clarify GitHub target, Google account(s), broad-scope approval, and write boundaries.
2. Connect GitHub via the official GitHub MCP server reference, then verify tools load in OpenClaw.
3. If Google Workspace access is requested, switch to / clone the dedicated private `mikepans1013/google-workspace-oauth-skill` repo and follow that skill; do not use copied instructions from this repo.
4. Verify Google scopes/APIs using the probe script from the dedicated Google OAuth repo, not a local copy in this repo.
5. Document only safe operational facts in `TOOLS.md`: account labels, helper commands, token file paths without values, verified APIs, and guardrails.
6. Run smoke tests and leave the bot with a short connection report listing what is connected, what is blocked, and what still needs human approval.

## Output Standard

When onboarding is complete, report:

- Connected GitHub account/org and MCP status
- Connected Google account(s) and verified APIs
- Secret file paths, without secret values
- Safety boundaries and pending approvals
- Smoke tests run and results
