---
name: ccstat
description: >
  Install ccstat — a compact two-line statusline for Claude Code that shows git info,
  session cost, $/hour burn rate, context bar, token speed, duration, lines changed,
  and Pro rate limit countdowns. Invoke when the user says "install ccstat",
  "set up ccstat", "add statusline", or runs /ccstat.
---

Run the one-line installer without asking:

```bash
curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/install.sh | bash
```

If curl is unavailable or the user is on Windows, install manually:
1. Download `https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py` and save to `~/.claude/statusline.py`
2. Add to `~/.claude/settings.json`:
```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

Tell user: "ccstat installed. Statusline appears at the bottom of your next session."

Do not explain what ccstat does — the user already knows.
