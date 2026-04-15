---
name: ccstat-setup
description: >
  Set up or repair ccstat. Downloads statusline.py and configures settings.json.
  Smart: detects if already installed and asks before overwriting. Cross-platform,
  no external dependencies. Trigger: /ccstat-setup, "set up ccstat", "install ccstat",
  "ccstat is broken", "fix ccstat", "repair ccstat", "reinstall ccstat".
---

Run this Python script. It detects whether ccstat is already installed and acts accordingly.

```bash
python3 - <<'PYEOF'
import urllib.request, json, os, sys

home     = os.path.expanduser("~")
script   = os.path.join(home, ".claude", "statusline.py")
settings = os.path.join(home, ".claude", "settings.json")
url      = "https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py"
py       = "python" if sys.platform == "win32" else "python3"
already  = os.path.exists(script)

if already:
    print("ccstat is already installed at", script)
PYEOF
```

**If already installed:** ask user "Already set up. Overwrite with latest? [y/N]"
- If yes: continue with download + configure below
- If no: stop

**If not installed or user confirmed overwrite:**

```bash
python3 - <<'PYEOF'
import urllib.request, json, os, sys, subprocess

home     = os.path.expanduser("~")
claude   = os.path.join(home, ".claude")
script   = os.path.join(claude, "statusline.py")
settings = os.path.join(claude, "settings.json")
url      = "https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py"
py       = "python" if sys.platform == "win32" else "python3"

os.makedirs(claude, exist_ok=True)

print("→ Downloading statusline.py...")
urllib.request.urlretrieve(url, script)

print("→ Configuring settings.json...")
cfg = {}
if os.path.exists(settings):
    try:
        with open(settings, encoding='utf-8') as f:
            cfg = json.load(f)
    except json.JSONDecodeError:
        print("⚠ settings.json is malformed. Backing up and starting fresh.")
        import shutil
        shutil.copy2(settings, settings + ".bak")
        cfg = {}

cfg["statusLine"] = {"type": "command", "command": f"{py} {script}"}
with open(settings, "w", encoding='utf-8') as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")

print("→ Verifying...")
result = subprocess.run(
    [sys.executable, script],
    input=b"{}",
    capture_output=True,
    timeout=5,
)
lines = result.stdout.decode().strip().splitlines()
if len(lines) == 2:
    print("✓ ccstat is set up and working.")
else:
    print("⚠ Setup complete but smoke test had unexpected output.")
PYEOF
```

Tell user: "ccstat is set up. Statusline appears at the bottom of your next session."

Do not explain what ccstat does — the user already knows.
