---
name: ccstat-reinstall
description: >
  Force reinstall ccstat from scratch — overwrites statusline.py and resets
  settings.json statusLine config. No confirmation needed. Trigger: /ccstat-reinstall,
  "reinstall ccstat", "ccstat is broken", "fix ccstat".
---

Force reinstall without prompting. Run both commands:

```bash
curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py -o ~/.claude/statusline.py
```

Then patch settings.json to ensure the statusLine config is correct. Read `~/.claude/settings.json`, set:
```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

Tell user: "ccstat reinstalled. Changes take effect next prompt."
