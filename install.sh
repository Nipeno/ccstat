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

existing = cfg.get("statusLine")
new_entry = {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
}

# Already pointing at our statusline.py (any path form) — silent overwrite
already_ours = (
    isinstance(existing, dict) and
    "statusline.py" in existing.get("command", "")
)

if existing and not already_ours:
    print(f"⚠  statusLine is already set in {path}:")
    print(f"   {json.dumps(existing)}")
    try:
        answer = input("   Overwrite? [y/N] ").strip().lower()
    except EOFError:
        answer = "n"
    if answer != "y":
        print("Aborted — settings unchanged.")
        sys.exit(0)

cfg["statusLine"] = new_entry

with open(path, "w") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")
PYEOF

echo "✓ Done. ccstat is active in your next Claude Code session."
