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
| `badge_file` | string | `".ccstat-badge"` | Filename inside `~/.claude/` that plugins write badges to |
| `badge_prefix` | string | `""` | If set, file content is treated as a mode name and displayed as `[PREFIX:MODE]` |
| `badge_default_mode` | string | `"full"` | Mode value that omits the suffix (shown as `[PREFIX]` not `[PREFIX:FULL]`) |

## Behavior

1. Read current config:
   ```bash
   python3 -c "
   import json, os
   path = os.path.join(os.path.expanduser('~'), '.claude', 'ccstat.json')
   cfg = {}
   if os.path.exists(path):
       with open(path) as f: cfg = json.load(f)
   defaults = {'bar_width': 12, 'show_tok_speed': True, 'show_lines_diff': True, 'update_check': True, 'badge_file': '.ccstat-badge', 'badge_prefix': '', 'badge_default_mode': 'full'}
   for k, d in defaults.items():
       v = cfg.get(k, d)
       marker = ' (custom)' if v != d else ''
       print(f'  {k:<20} {json.dumps(v)}{marker}')
   "
   ```

2. If user specified a setting to change (e.g. "set bar_width to 20", "disable update check"):
   - Apply the change directly using the write script below
   - Confirm what changed

3. If user just ran `/ccstat-config` with no specifics:
   - Show current values vs defaults in a table
   - Ask which setting they want to change
   - Apply and confirm

4. After any change, tell user: "Takes effect next prompt."

## Writing the config

Use Python to safely read/merge/write:
```bash
python3 - <<'PYEOF'
import json, os
path = os.path.join(os.path.expanduser("~"), ".claude", "ccstat.json")
cfg = {}
if os.path.exists(path):
    with open(path) as f:
        cfg = json.load(f)
# apply changes here, e.g. cfg["bar_width"] = 20
with open(path, "w") as f:
    json.dump(cfg, f, indent=2)
    f.write("\n")
print(json.dumps(cfg, indent=2))
PYEOF
```
