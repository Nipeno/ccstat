---
name: ccstat-status
description: >
  Show ccstat installation status — current version, latest available, config
  values, and file paths. Trigger: /ccstat-status, "ccstat status", "what version
  is ccstat", "is ccstat up to date".
---

Run the following and display a clean summary:

1. Get current version:
   ```bash
   grep '^VERSION' ~/.claude/statusline.py 2>/dev/null || echo "not installed"
   ```

2. Get latest version from GitHub:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py 2>/dev/null | grep '^VERSION'
   ```

3. Show update cache if present:
   ```bash
   cat ~/.claude/.ccstat-update-cache 2>/dev/null
   ```

4. Show current config:
   ```bash
   cat ~/.claude/ccstat.json 2>/dev/null || echo "(no config — all defaults)"
   ```

5. Show statusLine entry from settings.json:
   ```bash
   python3 -c "import json; cfg=json.load(open('$HOME/.claude/settings.json')); print(json.dumps(cfg.get('statusLine','not set'), indent=2))"
   ```

Format output as a compact status card:

```
ccstat vX.Y.Z  (latest: vX.Y.Z ✓ or ↑ vX.Y.Z available)

Config (~/.claude/ccstat.json):
  bar_width       12
  show_tok_speed  true
  show_lines_diff true
  update_check    true

Files:
  ~/.claude/statusline.py       ✓
  ~/.claude/ccstat.json         ✓ / (default)
  ~/.claude/settings.json       statusLine configured ✓
```

If not installed, say so clearly and suggest `/ccstat` to install.
