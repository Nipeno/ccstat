#!/usr/bin/env bash
set -euo pipefail

SETTINGS="$HOME/.claude/settings.json"
SCRIPT="$HOME/.claude/statusline.py"
RAW="https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py"

echo "→ Downloading statusline.py..."
curl -fsSL "$RAW" -o "$SCRIPT"

echo "→ Patching ~/.claude/settings.json..."

if [ ! -f "$SETTINGS" ]; then
    echo '{}' > "$SETTINGS"
fi

# Use Python to safely patch the JSON (avoids sed/jq dependency)
python3 - "$SETTINGS" <<'PYEOF'
import json, sys

path = sys.argv[1]
with open(path) as f:
    cfg = json.load(f)

cfg["statusLine"] = {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
}

with open(path, 'w') as f:
    json.dump(cfg, f, indent=2)
    f.write('\n')
PYEOF

echo "✓ Done. ccstat is active in your next Claude Code session."
