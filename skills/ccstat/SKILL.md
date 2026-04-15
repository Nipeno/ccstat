---
name: ccstat
description: >
  Install or update ccstat — a compact two-line statusline for Claude Code that shows git info,
  session cost, $/hour burn rate, context bar, token speed, duration, lines changed,
  and Pro rate limit countdowns. Invoke when the user says "install ccstat",
  "set up ccstat", "add statusline", runs /ccstat, says "update ccstat", or runs /ccstat update.
---

## Install

If the user wants to install (no "update" mentioned), run the one-line installer without asking:

```bash
curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/install.sh | bash
```

After installing, tell the user: "ccstat is installed. The statusline will appear at the bottom of your next Claude Code session."

---

## Update (`/ccstat update` or "update ccstat")

1. Read the current version from `~/.claude/statusline.py` (look for the `VERSION = "..."` line).
2. Fetch the latest version from GitHub by reading the raw file and extracting the VERSION line:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py | grep '^VERSION'
   ```
3. If current == latest: tell the user "Already on latest (vX.Y.Z)." Stop.
4. If latest > current: show the user:
   > ccstat vCURRENT → vLATEST available. Update?
   Ask yes/no. If yes, run the installer:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/install.sh | bash
   ```
   Then tell the user: "Updated to vLATEST. Restart Claude Code to apply."
   If no: do nothing.

---

Do not explain what ccstat does — the user already knows.
