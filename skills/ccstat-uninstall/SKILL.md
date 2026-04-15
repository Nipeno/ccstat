---
name: ccstat-uninstall
description: >
  Uninstall ccstat — removes statusline.py and ccstat.json, clears statusLine
  from settings.json. Asks confirmation before proceeding. Trigger: /ccstat-uninstall,
  "uninstall ccstat", "remove ccstat".
---

Ask user to confirm: "Remove ccstat and clear statusLine from settings.json?"

If yes:

1. Delete files if they exist:
   ```bash
   rm -f ~/.claude/statusline.py ~/.claude/ccstat.json ~/.claude/.ccstat-update-cache
   ```

2. Remove `statusLine` key from `~/.claude/settings.json` using Python:
   ```bash
   python3 - ~/.claude/settings.json <<'EOF'
   import json, sys
   path = sys.argv[1]
   try:
       cfg = json.loads(open(path).read())
       cfg.pop('statusLine', None)
       open(path, 'w').write(json.dumps(cfg, indent=2) + '\n')
       print("✓ statusLine removed from settings.json")
   except Exception as e:
       print(f"⚠ Could not patch settings.json: {e}")
   EOF
   ```

3. Tell user: "ccstat uninstalled. Statusline gone next session."

If no: do nothing.
