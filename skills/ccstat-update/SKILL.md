---
name: ccstat-update
description: >
  Update ccstat to the latest version. Checks current vs latest version,
  asks user to confirm, then downloads the update. Cross-platform, no curl
  dependency. Trigger: /ccstat-update, "update ccstat", "ccstat update".
---

Run this Python script to check versions:

```bash
python3 - <<'PYEOF'
import urllib.request, os, sys

script = os.path.join(os.path.expanduser("~"), ".claude", "statusline.py")
url    = "https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py"

# Get current version
current = None
if os.path.exists(script):
    with open(script) as f:
        for line in f:
            if line.startswith("VERSION"):
                current = line.split('"')[1]
                break

if not current:
    print("ccstat is not installed. Run /ccstat-setup first.")
    sys.exit(0)

# Get latest version
latest = None
try:
    data = urllib.request.urlopen(url, timeout=5).read().decode()
    for line in data.splitlines():
        if line.startswith("VERSION"):
            latest = line.split('"')[1]
            break
except Exception as e:
    print(f"Could not reach GitHub: {e}")
    sys.exit(1)

if not latest:
    print("Could not determine latest version.")
    sys.exit(1)

print(f"Current: v{current}")
print(f"Latest:  v{latest}")

if current == latest:
    print("Already on latest.")
else:
    print(f"UPDATE_AVAILABLE:{current}:{latest}")
PYEOF
```

If output contains `UPDATE_AVAILABLE`: ask user "ccstat vCURRENT → vLATEST. Update?"

If yes, run:

```bash
python3 - <<'PYEOF'
import urllib.request, os
script = os.path.join(os.path.expanduser("~"), ".claude", "statusline.py")
url    = "https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py"
urllib.request.urlretrieve(url, script)
print("✓ Updated. Changes take effect next prompt.")
PYEOF
```

If no: do nothing.
