---
name: ccstat-remove
description: >
  Remove ccstat — deletes statusline.py and ccstat.json, clears statusLine
  from settings.json. Asks confirmation before proceeding. Trigger: /ccstat-remove,
  "remove ccstat", "uninstall ccstat", "delete ccstat".
---

Ask user to confirm: "Remove ccstat and clear statusLine from settings.json?"

If yes, run this Python script:

```bash
python3 - <<'PYEOF'
import json, os

home     = os.path.expanduser("~")
script   = os.path.join(home, ".claude", "statusline.py")
config   = os.path.join(home, ".claude", "ccstat.json")
cache    = os.path.join(home, ".claude", ".ccstat-update-cache")
settings = os.path.join(home, ".claude", "settings.json")

for path in [script, config, cache]:
    if os.path.exists(path):
        os.remove(path)
        print(f"  Removed {path}")

if os.path.exists(settings):
    try:
        with open(settings) as f:
            cfg = json.load(f)
        cfg.pop("statusLine", None)
        with open(settings, "w") as f:
            json.dump(cfg, f, indent=2)
            f.write("\n")
        print("  Cleared statusLine from settings.json")
    except json.JSONDecodeError:
        print("  ⚠ settings.json is malformed — could not patch. Remove statusLine manually.")

print("✓ ccstat removed. Statusline gone next session.")
PYEOF
```

If no: do nothing.
