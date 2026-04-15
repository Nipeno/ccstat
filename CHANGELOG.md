# Changelog

All notable changes to ccstat are documented here.

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
