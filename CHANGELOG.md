# Changelog

All notable changes to ccstat are documented here.

## [1.3.0] — 2026-04-15

- Generic badge system: `badge_file`, `badge_prefix`, `badge_default_mode` config keys replace hardcoded caveman logic — any plugin can show a badge by writing to `~/.claude/.ccstat-badge`
- Git: reduced 5 subprocess calls to 1 (`git status --porcelain -b` parses branch, ahead/behind, staged/modified/untracked in a single call)
- Windows: case-insensitive home directory replacement in path shortening
- Config validation: JSON parse errors and `bar_width` range violations logged to `~/.claude/.ccstat-errors.log` with a warning badge in the statusline
- Background update check errors now logged instead of silently swallowed
- `encoding='utf-8'` on all file opens

## [1.2.0] — 2026-04-14

- Renamed marketplace commands for consistency (`/ccstat-setup`, `/ccstat-update`, `/ccstat-remove`, `/ccstat-info`, `/ccstat-config`)
- Full cross-platform audit: Windows path separators, process spawning flags, UTF-8 encoding
- Added `.github` PR template and issue templates
- Added `CLAUDE.md` with development guidelines

## [1.1.0] — 2026-04-11

- Added user config system (`~/.claude/ccstat.json`) with `bar_width`, `show_tok_speed`, `show_lines_diff`, `update_check`
- Added `/ccstat-config` skill to view and edit config
- Added `/ccstat-info` skill to show version and install status
- Added `/ccstat-remove` skill to uninstall

## [1.0.0] — 2026-04-08

- Initial release
- Two-line statusline with token usage bar, git branch/diff stats, model name, session cost
- Auto-update check (fire-and-forget, once per day)
- `/ccstat-setup` and `/ccstat-update` skills
- `install.sh` one-liner fallback
