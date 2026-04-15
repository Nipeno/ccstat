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

Then patch settings.json using Python to ensure the statusLine config is correct:

```bash
python3 - <<'EOF'
import json, os, sys
settings = os.path.join(os.path.expanduser("~"), ".claude", "settings.json")
script   = os.path.join(os.path.expanduser("~"), ".claude", "statusline.py")
py       = "python" if sys.platform == "win32" else "python3"
cfg = json.loads(open(settings).read()) if os.path.exists(settings) else {}
cfg["statusLine"] = {"type": "command", "command": f"{py} {script}"}
open(settings, "w").write(json.dumps(cfg, indent=2) + "\n")
EOF
```

Tell user: "ccstat reinstalled. Changes take effect next prompt."
