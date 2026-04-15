# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | ✅ Yes    |
| Older   | ❌ No     |

Always run the latest version. Updates via `/ccstat-update` in Claude Code.

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Email: **nipenogamer@gmail.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Your suggested fix (optional)

Fixes for confirmed vulnerabilities are prioritized and released promptly.

## Scope

`statusline.py` runs on every Claude Code prompt on users' machines. Vulnerabilities in this file are treated as critical.

In-scope:
- Code execution via malicious Claude Code session data
- Path traversal or arbitrary file writes
- Credential or token exposure

Out-of-scope:
- Issues in dependencies not bundled with ccstat
- Social engineering
