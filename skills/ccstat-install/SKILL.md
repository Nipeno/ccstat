---
name: ccstat-install
description: >
  Final setup step after adding ccstat via the Claude Code plugin marketplace
  (`claude plugin marketplace add Nipeno/ccstat`). Downloads statusline.py and
  patches settings.json. Not needed if installed via the curl one-liner directly.
  Trigger: /ccstat-install, "install ccstat", "set up ccstat", "add ccstat".
---

Run the one-line installer without asking:

```bash
curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/install.sh | bash
```

If curl is unavailable or the user is on Windows, install manually:
1. Download `https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py` to:
   - macOS/Linux: `~/.claude/statusline.py`
   - Windows: `%USERPROFILE%\.claude\statusline.py`
2. Add to `settings.json` (`~/.claude/settings.json` or `%USERPROFILE%\.claude\settings.json`):

   **macOS/Linux:**
   ```json
   { "statusLine": { "type": "command", "command": "python3 ~/.claude/statusline.py" } }
   ```
   **Windows:**
   ```json
   { "statusLine": { "type": "command", "command": "python \"%USERPROFILE%\\.claude\\statusline.py\"" } }
   ```

Tell user: "ccstat installed. Statusline appears at the bottom of your next session."

Do not explain what ccstat does — the user already knows.
