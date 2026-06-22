# GitHub MCP for OpenClaw Bot Onboarding

Use GitHub's official MCP server as the source of truth:

- https://github.com/github/github-mcp-server

Do not copy stale install snippets into this skill. The official repo changes faster than a skill should. Link to it, then document OpenClaw-specific decisions, verification, and gotchas.

## OpenClaw setup guidance

1. Confirm the target GitHub identity:
   - personal user or org?
   - which repos should the bot access?
   - is public-only enough, or are private repos needed?
   - should write actions be allowed after approval?

2. Follow the official GitHub MCP server docs for the current transport/auth method.

3. Store credentials outside the repo:
   - Prefer OpenClaw/Gateway secret handling when available.
   - Otherwise use a local secret file under `~/.openclaw/secrets/` with `chmod 600`.
   - For local stdio installs, a good default is `~/.openclaw/secrets/github-mcp-pat` plus a `~/.openclaw/bin/github-mcp-wrapper` script that exports `GITHUB_PERSONAL_ACCESS_TOKEN` and execs `github-mcp-server stdio`. Configure OpenClaw to call only the wrapper, not the token.
   - Never commit PATs, OAuth tokens, private keys, or generated config containing secrets.

4. Add the MCP server with a stable name such as `github` or `github-official`.
   - If installing the official release binary, verify the published sha256 checksum from `github/github-mcp-server` before linking it into `~/.openclaw/bin/`.

5. Reload/restart OpenClaw only as required by the current OpenClaw MCP configuration path.

6. Verify tool loading before doing work.
   - If GitHub tools do not show up in the current assistant turn yet, run a direct stdio MCP smoke test against the wrapper with `initialize`, `notifications/initialized`, and `tools/list`.
   - After any OpenClaw MCP config change, run `node scripts/r2-runtime-healthcheck.js --healthcheck`, `openclaw gateway status`, and a safe status/tool-loading check before reporting done.

## Nuances we ran into / guardrails

- **Auth identity confusion:** `gh`, SSH remotes, HTTPS remotes, GitHub MCP, and GitHub API tools can all authenticate differently. Always verify which account the MCP is actually using before assuming repo access.
- **SSH success does not mean MCP success:** SSH keys can allow `git push` while the MCP still lacks an API token or app installation permissions.
- **HTTPS remotes may fail silently later:** a repo can be cloned locally while pushes fail because `gh` or credential helper is not authenticated. Verify a harmless read/list and, when needed, a controlled write on a test repo.
- **PAT scopes matter:** missing repo/project/workflow scopes show up as confusing 404/403 failures. Prefer the minimum scopes needed, but make private repo access explicit.
- **Fine-grained PAT headers can look empty:** fine-grained PATs may return an empty `x-oauth-scopes` header even when valid. Verify identity with `GET /user`, repo permissions with `GET /repos/{owner}/{repo}`, and MCP access with a harmless read.
- **Tool-schema failures can affect OpenClaw broadly:** a broken MCP server can prevent tools from loading cleanly. After adding any MCP, check OpenClaw status/tool list. If the server breaks schema loading, disable or remove it before continuing.
- **Server name stability matters:** downstream instructions and tool routing may depend on the configured MCP name. Pick a boring stable name and document it.
- **Destructive GitHub actions need approval:** deleting repos, changing visibility, force-pushing, merging, closing issues/PRs, publishing releases, and changing repo settings should never be automatic.

## Verification checklist

- Official repo referenced: `github/github-mcp-server`.
- MCP server appears in OpenClaw status/tool list.
- Authenticated account is the intended GitHub user/app installation.
- Expected repos are visible and repo metadata shows expected permissions.
- A harmless read operation works, such as listing branches or reading a README file.
- Runtime health and gateway status pass after the MCP config change.
- If writes are needed, use a test repo/branch first.
- Document safe details in `TOOLS.md`; never document tokens.
