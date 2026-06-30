# OpenClaw Bot Onboarding Skill

An OpenClaw AgentSkill for onboarding new bots/familiars with:

- official GitHub MCP connection guidance
- Google Workspace OAuth handoff to the dedicated private OAuth skill repo
- local secret storage conventions
- verification checklists
- write-action approval guardrails

This repo is intentionally public-safe. It does **not** contain secrets, user-specific token paths, or private account assumptions.

## What this is for

Use this skill when an already-created OpenClaw bot needs to be connected to GitHub and Google Workspace accounts. It assumes standard OpenClaw onboarding has already handled bot identity, name, workspace, channels, and persona; this skill should not ask about or change those. Before connecting anything, the bot asks only which GitHub account/org and Google account(s) should be connected.

It should also clarify whether the user wants **prep only** or **live setup** before saving secrets or changing live MCP/OAuth configuration.

## What it includes

```text
SKILL.md
references/
  onboarding-checklist.md
  github-mcp.md
scripts/
```

## GitHub MCP approach

The skill references GitHub's official MCP server instead of copying install commands that may go stale:

https://github.com/github/github-mcp-server

The repo documents OpenClaw-specific setup decisions and nuances: auth identity confusion, PAT scopes, SSH vs MCP auth, tool-schema failures, stable server naming, and write-action approval boundaries.

It also now documents an OpenClaw-native MCP configuration path (`openclaw mcp set ...`) and rollback expectations.

## Google OAuth approach

This repo no longer carries its own Google OAuth instructions or helper scripts. Use the dedicated private Google OAuth skill repo instead:

- `https://github.com/mikepans1013/google-workspace-oauth-skill`
- Local canonical path when available: `/Users/henrykent/skills/google-workspace-oauth`

That repo owns scope selection, OAuth bootstrap/probe scripts, token storage guidance, Drive structure/routing, and Google write-action guardrails. Keep those instructions centralized there.

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

> Onboard a new OpenClaw bot with GitHub MCP and, if requested, hand off Google Workspace OAuth to the dedicated private OAuth skill repo.

The bot should load `SKILL.md`, determine whether the user wants prep-only or live setup, ask the first questions, and proceed only after the target account(s) and mode are confirmed.

## Extending

Keep this repo generic. Put customer/operator-specific account names and helper commands in that bot's local `TOOLS.md`, not in this public repo.
