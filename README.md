# OpenClaw Bot Onboarding Skill

An OpenClaw AgentSkill for onboarding new bots/familiars with:

- safe bot identity/workspace setup
- official GitHub MCP connection guidance
- broad Google Workspace OAuth setup
- local secret storage conventions
- verification checklists
- write-action approval guardrails

This repo is intentionally public-safe. It does **not** contain secrets, user-specific token paths, or private account assumptions.

## What this is for

Use this skill when a new OpenClaw bot needs to be connected to a human/operator's GitHub and Google Workspace accounts. The skill is deliberately ambiguous about the user: before connecting anything, the bot must ask which human, GitHub account/org, and Google account(s) should be connected.

## What it includes

```text
SKILL.md
references/
  onboarding-checklist.md
  github-mcp.md
  google-workspace-oauth.md
scripts/
  google_oauth_bootstrap.py
  google_token_probe.py
```

## GitHub MCP approach

The skill references GitHub's official MCP server instead of copying install commands that may go stale:

https://github.com/github/github-mcp-server

The repo documents OpenClaw-specific setup decisions and nuances: auth identity confusion, PAT scopes, SSH vs MCP auth, tool-schema failures, stable server naming, and write-action approval boundaries.

## Google OAuth approach

The skill includes reusable local scripts adapted from the Google Workspace OAuth setup pattern:

- `scripts/google_oauth_bootstrap.py`
- `scripts/google_token_probe.py`

The default broad onboarding bundle is `workspace-ea`, covering Gmail, Calendar, Drive, Drive Activity, Docs, Sheets, Slides, Forms, Tasks, Contacts, OpenID/email/profile. Helpers should still default to read-only behavior and require approval before write actions.

## Safety boundaries

- Never commit client secrets, OAuth tokens, PATs, private keys, OTPs, or generated configs containing secrets.
- Store secrets locally under `~/.openclaw/secrets/` with `chmod 600`.
- Do not reveal or relay 2FA/OTP/login codes.
- Do not perform destructive or external write actions without exact approval.
- Do not copy another bot's private memory into a new bot.

## Installing as a skill

Clone or copy this directory into the OpenClaw skills directory for the bot, then ensure the skill metadata is visible in the runtime's available skills list.

Example:

```bash
git clone https://github.com/mikepans1013/openclaw-bot-onboarding-skill.git ~/skills/openclaw-bot-onboarding-skill
```

Then start a request such as:

> Onboard a new OpenClaw bot with GitHub MCP and Google Workspace OAuth.

The bot should load `SKILL.md`, ask the first questions, and proceed only after the target account(s) are confirmed.

## Extending

Keep this repo generic. Put customer/operator-specific paths, account names, and helper commands in that bot's local `TOOLS.md`, not in this public repo.
