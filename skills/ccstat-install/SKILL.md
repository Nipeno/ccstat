---
name: ccstat-install
description: >
  Set up ccstat after adding the plugin via the Claude Code marketplace.
  Downloads statusline.py and configures settings.json. Cross-platform,
  no external dependencies. Trigger: /ccstat-install, "install ccstat",
  "set up ccstat", "add ccstat".
---

Run this Python script to download and configure ccstat. No confirmation needed.

```bash
python3 - <<'PYEOF'
import urllib.request, json, os, sys

home     = os.path.expanduser("~")
script   = os.path.join(home, ".claude", "statusline.py")
settings = os.path.join(home, ".claude", "settings.json")
url      = "https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py"
py       = "python" if sys.platform == "win32" else "python3"

# Download statusline.py
print("→ Downloading statusline.py...")
urllib.request.urlretrieve(url, script)

# Patch settings.json
print("→ Configuring settings.json...")
cfg = {}
if os.path.exists(settings):
    with open(settings) as f:
        cfg = json.load(f)
cfg["statusLine"] = {"type": "command", "command": f"{py} {script}"}
with open(settings, "w") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")

# Smoke test
print("→ Verifying...")
import subprocess
result = subprocess.run(
    [sys.executable, script],
    input=b"{}",
    capture_output=True,
    timeout=5,
)
lines = result.stdout.decode().strip().splitlines()
if len(lines) == 2:
    print("✓ ccstat installed and working.")
else:
    print("⚠ Installed but smoke test unexpected output. May need restart.")
PYEOF
```

Tell user: "ccstat installed. Statusline appears at the bottom of your next session."

Do not explain what ccstat does — the user already knows.
