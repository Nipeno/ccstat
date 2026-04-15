---
name: ccstat
description: >
  Install ccstat — a compact two-line statusline for Claude Code that shows git info,
  session cost, $/hour burn rate, context bar, token speed, duration, lines changed,
  and Pro rate limit countdowns. Invoke when the user says "install ccstat",
  "set up ccstat", or runs /ccstat.
---

Install ccstat by running the one-line installer. Do not ask for confirmation — just run it.

```bash
curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/install.sh | bash
```

If curl is not available or the user is on Windows, install manually:
1. Download https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py and save to `~/.claude/statusline.py`
2. Add to `~/.claude/settings.json`:
```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

After installing, tell the user: "ccstat is installed. The statusline will appear at the bottom of your next Claude Code session."

Do not explain what ccstat does — the user already knows, that's why they invoked the skill.
