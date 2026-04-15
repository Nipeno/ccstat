---
name: ccstat-reinstall
description: >
  Force reinstall ccstat from scratch — overwrites statusline.py and resets
  settings.json statusLine config. No confirmation needed. Trigger: /ccstat-reinstall,
  "reinstall ccstat", "ccstat is broken", "fix ccstat".
---

Force reinstall without prompting. Run this Python script:

```bash
python3 - <<'PYEOF'
import urllib.request, json, os, sys

home     = os.path.expanduser("~")
script   = os.path.join(home, ".claude", "statusline.py")
settings = os.path.join(home, ".claude", "settings.json")
url      = "https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py"
py       = "python" if sys.platform == "win32" else "python3"

print("→ Downloading statusline.py...")
urllib.request.urlretrieve(url, script)

print("→ Configuring settings.json...")
cfg = {}
if os.path.exists(settings):
    with open(settings) as f:
        cfg = json.load(f)
cfg["statusLine"] = {"type": "command", "command": f"{py} {script}"}
with open(settings, "w") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")

print("✓ ccstat reinstalled.")
PYEOF
```

Tell user: "ccstat reinstalled. Changes take effect next prompt."
