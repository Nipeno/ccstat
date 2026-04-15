---
name: ccstat-info
description: >
  Show ccstat installation info — current version, latest available, config
  values, and file status. Trigger: /ccstat-info, "ccstat info", "what version
  is ccstat", "is ccstat up to date", "ccstat status".
---

Run this Python script and display the output:

```bash
python3 - <<'PYEOF'
import urllib.request, json, os, sys

home     = os.path.expanduser("~")
script   = os.path.join(home, ".claude", "statusline.py")
config   = os.path.join(home, ".claude", "ccstat.json")
cache    = os.path.join(home, ".claude", ".ccstat-update-cache")
settings = os.path.join(home, ".claude", "settings.json")

# Current version
current = None
if os.path.exists(script):
    with open(script) as f:
        for line in f:
            if line.startswith("VERSION"):
                current = line.split('"')[1]
                break

if not current:
    print("ccstat is not installed. Run /ccstat-setup to install.")
    sys.exit(0)

# Latest version
latest = None
try:
    data = urllib.request.urlopen(
        "https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py",
        timeout=5
    ).read().decode()
    for line in data.splitlines():
        if line.startswith("VERSION"):
            latest = line.split('"')[1]
            break
except Exception:
    latest = "(could not check)"

up_to_date = current == latest
status = "✓ up to date" if up_to_date else f"↑ v{latest} available"
print(f"ccstat v{current}  ({status})")
print()

# Config
defaults = {"bar_width": 12, "show_tok_speed": True, "show_lines_diff": True, "update_check": True, "badge_file": ".ccstat-badge", "badge_prefix": "", "badge_default_mode": "full"}
cfg = {}
if os.path.exists(config):
    try:
        with open(config) as f:
            cfg = json.load(f)
    except Exception:
        pass

print("Config:")
for key, default in defaults.items():
    val = cfg.get(key, default)
    marker = "" if val == default else " (custom)"
    print(f"  {key:<20} {json.dumps(val)}{marker}")
print()

# Files
print("Files:")
for label, path in [("statusline.py", script), ("ccstat.json", config), ("settings.json", settings)]:
    exists = "✓" if os.path.exists(path) else "✗"
    print(f"  {label:<20} {exists}  {path}")
PYEOF
```

Display the output as-is. If update available, suggest `/ccstat-update`.
