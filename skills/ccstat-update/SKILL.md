---
name: ccstat-update
description: >
  Update ccstat to the latest version. Checks current vs latest version,
  asks user to confirm, then runs the installer. Trigger: /ccstat-update,
  "update ccstat", "ccstat update".
---

1. Read current version from `~/.claude/statusline.py` (look for `VERSION = "..."` line).
2. Fetch latest version from GitHub:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py | grep '^VERSION'
   ```
3. If current == latest: tell user "Already on latest (vX.Y.Z)." Stop.
4. If latest > current: show the user:
   > ccstat vCURRENT → vLATEST available. Update?
   Ask yes/no. If yes, run:
   ```bash
   curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py -o ~/.claude/statusline.py
   ```
   Tell user: "Updated to vLATEST. Changes take effect next prompt."
   If no: do nothing.
