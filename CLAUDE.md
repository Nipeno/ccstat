# ccstat — Claude instructions

## Version bumping

`VERSION` lives at the top of `statusline.py`. Bump it on every change to `statusline.py` using semver:

| Change | Bump |
|--------|------|
| Bug fix, refactor, cross-platform fix | patch `x.y.Z` |
| New feature, new config option, new segment | minor `x.Y.0` |
| Breaking change (removed segment, changed config schema) | major `X.0.0` |

**Always bump before committing.** If a session touches `statusline.py`, the version must be higher than it was before that session started. Never ship the same version with different code.

After bumping, sync the file to `~/.claude/statusline.py`:
```bash
cp statusline.py ~/.claude/statusline.py
```

## Skill files

Skill files live in `skills/` and mirror to `~/.claude/plugins/marketplaces/ccstat/skills/`. After editing any skill, sync it:
```bash
cp skills/<name>/SKILL.md ~/.claude/plugins/marketplaces/ccstat/skills/<name>/SKILL.md
```

## Repo layout

```
statusline.py          — the statusline script (versioned)
install.sh             — one-line installer
skills/
  ccstat/              → /ccstat        install
  ccstat-update/       → /ccstat-update
  ccstat-reinstall/    → /ccstat-reinstall
  ccstat-status/       → /ccstat-status
  ccstat-config/       → /ccstat-config
  ccstat-uninstall/    → /ccstat-uninstall
```
