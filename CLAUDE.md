# ccstat — Claude instructions

## Production context

This is a **public, production repository**. Real users install and run this code directly on their machines. Every change must be safe, correct, and professional before it reaches `main`.

- **Never auto-push** unless the change is critical (security fix, broken install). All other commits stay local until the user reviews and approves a push.
- **Quality bar**: code must look like it was written by a careful human developer. No debug prints, no `except: pass` silently swallowing errors, no sloppy variable names, no leftover TODOs.
- **When unsure** whether something is ready for public — don't push. Ask first.

## Security requirements

`statusline.py` runs on every Claude Code prompt on the user's machine. Treat it like privileged code.

Hard blockers — never ship:
- `eval()` or `exec()` on any external or user-supplied data
- HTTP (non-TLS) fetches
- Shell injection via `subprocess` with unsanitized input
- Writing attacker-controlled data to paths outside `~/.claude/`
- Silently ignoring exceptions that could mask a security failure

Always verify:
- External data written to disk is sanitized or safely serialized (e.g. `json.dump`, not raw write)
- File paths constructed with `os.path.join` + `os.path.expanduser`, never string concatenation
- Network requests use HTTPS to known, hardcoded URLs only

## Cross-platform compatibility

`statusline.py` must work on macOS, Linux, and Windows. Check every change against:

- Path separators — always use `os.path.join`, never hardcode `/`
- Process spawning — `start_new_session` (POSIX) vs `DETACHED_PROCESS` flags (Windows); both branches must exist
- File encoding — always specify `encoding='utf-8'` when opening text files
- Python version — target Python 3.8+; avoid newer syntax or stdlib additions

Skill files (`.md`) are platform-agnostic — no special handling needed.

## Version bumping

`VERSION` lives at the top of `statusline.py`. Bump on every change to `statusline.py` using semver:

| Change | Bump |
|--------|------|
| Bug fix, refactor, cross-platform fix | patch `x.y.Z` |
| New feature, new config option, new segment | minor `x.Y.0` |
| Breaking change (removed segment, changed config schema) | major `X.0.0` |

**Always bump before committing.** Never ship the same version string with different code.

After bumping, sync to local install:
```bash
cp statusline.py ~/.claude/statusline.py
```

`CHANGELOG.md` is the canonical release history. No GitHub releases required — the install always pulls from `main` directly.

## Skill files

Skill files live in `skills/` and mirror to `~/.claude/plugins/marketplaces/ccstat/skills/`. After editing any skill, sync:
```bash
cp skills/<name>/SKILL.md ~/.claude/plugins/marketplaces/ccstat/skills/<name>/SKILL.md
```

## Before committing `statusline.py`

Always run the smoke test to catch syntax errors, import failures, and broken JSON handling:
```bash
echo '{}' | python3 statusline.py
```
If it crashes or exits with an error, do not commit.

## README and CHANGELOG sync

If a change adds a new feature, config option, or segment — update `README.md` to reflect it before committing. Don't ship undocumented user-facing changes.

Add an entry to `CHANGELOG.md` for every version bump. Format: `## [x.y.z] — YYYY-MM-DD` followed by bullet points. Keep it user-facing (what changed, not how).

## Committing and pushing

- **Commit freely** when work is complete and correct.
- **Do not auto-push** low-priority or non-essential changes — stage and commit locally, then tell the user what's ready.
- **Auto-push only** for: critical security fixes or broken install fixes where delay causes active harm.
- Before any push, confirm the diff is clean, professional, and safe for public eyes.

## External contributions

Others submit PRs. The `.github/pull_request_template.md` and issue templates handle contributor guidance — don't duplicate that here. When reviewing or merging PRs, apply the same security and cross-platform checklist above.

## Repo layout

```
statusline.py          — the statusline script (versioned, runs on user machines)
install.sh             — fallback installer (curl one-liner)
skills/
  ccstat-setup/        → /ccstat-setup   (primary setup via marketplace)
  ccstat-update/       → /ccstat-update
  ccstat-remove/       → /ccstat-remove
  ccstat-info/         → /ccstat-info
  ccstat-config/       → /ccstat-config
.github/
  pull_request_template.md
  ISSUE_TEMPLATE/
```
