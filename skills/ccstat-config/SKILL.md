---
name: ccstat-config
description: >
  Configure ccstat — view or change settings in ~/.claude/ccstat.json.
  Trigger: /ccstat-config, "configure ccstat", "ccstat settings",
  "change ccstat bar width", "disable ccstat update check", etc.
---

## Config file

`~/.claude/ccstat.json` — all keys optional, defaults apply if absent.

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `bar_width` | int | `12` | Width of the context bar in characters |
| `show_tok_speed` | bool | `true` | Show output token speed (t/s) on line 2 |
| `show_lines_diff` | bool | `true` | Show +lines/-lines diff on line 2 |
| `update_check` | bool | `true` | Enable daily background update check |

## Behavior

1. Read current config:
   ```bash
   cat ~/.claude/ccstat.json 2>/dev/null || echo "{}"
   ```

2. If user specified a setting to change (e.g. "set bar_width to 20", "disable update check"):
   - Apply the change directly, write updated JSON back to `~/.claude/ccstat.json`
   - Confirm what changed

3. If user just ran `/ccstat-config` with no specifics:
   - Show current values vs defaults in a table
   - Ask which setting they want to change
   - Apply and confirm

4. After any change, tell user: "Takes effect next prompt."

## Writing the config

Use Python to safely read/merge/write:
```bash
python3 - <<'EOF'
import json, os
path = os.path.expanduser('~/.claude/ccstat.json')
cfg = json.loads(open(path).read()) if os.path.exists(path) else {}
# apply changes here, e.g. cfg['bar_width'] = 20
open(path, 'w').write(json.dumps(cfg, indent=2) + '\n')
print(json.dumps(cfg, indent=2))
EOF
```
