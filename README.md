# ccstat for Claude Code

Compact two-line statusline for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) sessions.

![ccstat screenshot](screenshot.png)

**Line 1 — identity:** directory · git branch + status · model · time · alerts  
**Line 2 — resources:** cost + $/hour · context bar · tokens · output speed · duration · lines changed · rate limits

---

## Install

### Via Claude Code plugin marketplace

```bash
claude plugin marketplace add Nipeno/ccstat
claude plugin install ccstat@ccstat
```

Then type `/ccstat` in any session and Claude installs it for you.

### Via one-liner

```bash
curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/install.sh | bash
```

Downloads `statusline.py` to `~/.claude/` and patches `~/.claude/settings.json`.

<details>
<summary>Manual install (Windows / no curl)</summary>

1. Download [`statusline.py`](https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py) and save to `%USERPROFILE%\.claude\statusline.py`
2. Add to `%USERPROFILE%\.claude\settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python \"%USERPROFILE%\\.claude\\statusline.py\""
  }
}
```

</details>

---

## Commands

All commands are available as Claude Code slash commands after installing the plugin.

| Command | Description |
|---------|-------------|
| `/ccstat-install` | Final setup step after `claude plugin install ccstat@ccstat` |
| `/ccstat-update` | Check for updates and apply with confirmation |
| `/ccstat-reinstall` | Force reinstall — overwrites everything, no prompts |
| `/ccstat-uninstall` | Remove ccstat and clean up settings |
| `/ccstat-status` | Show version, update status, and current config |
| `/ccstat-config` | View or change settings in `~/.claude/ccstat.json` |

---

## Configuration

Create `~/.claude/ccstat.json` to override defaults (all keys optional):

```json
{
  "bar_width": 12,
  "show_tok_speed": true,
  "show_lines_diff": true,
  "update_check": true
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `bar_width` | `12` | Width of the context bar in characters |
| `show_tok_speed` | `true` | Show output token speed (t/s) |
| `show_lines_diff` | `true` | Show +lines / -lines diff |
| `update_check` | `true` | Daily background update check |

Or just use `/ccstat-config` and Claude will handle it.

---

## Auto-updates

ccstat checks for updates once per day in the background — a fire-and-forget subprocess with no tokens and no blocking. When a new version is available, a `↑ vX.Y.Z` badge appears on line 1. Run `/ccstat-update` to apply.

To disable: set `"update_check": false` in `~/.claude/ccstat.json`.

---

## What each segment shows

### Line 1

| Segment | Example | Notes |
|---------|---------|-------|
| Directory | `~/projects/myapp` | Home-shortened path |
| Git branch | `main` | Current branch |
| Git ahead/behind | `↑2 ↓1` | Commits ahead/behind upstream |
| Git status | `●3 ~1 ?2` | Staged · modified · untracked |
| Model | `claude-sonnet-4-6` | Active model |
| Effort | `high` | Shown if `effortLevel` set in settings |
| Time | `14:22` | Local clock |
| Caveman badge | `[CAVEMAN]` | Shown if [caveman](https://github.com/JuliusBrussee/caveman) plugin active |
| Session name | `[my-session]` | Shown if session is named |
| Context warning | `⚠ 200k` | When context exceeds 200k tokens |
| Update badge | `↑ v1.2.0` | New version available — run `/ccstat-update` |

### Line 2

| Segment | Example | Notes |
|---------|---------|-------|
| Cost | `$0.042` | Session total. Gray on Pro (quota not depleted) |
| Cost/hour | `$1.23/h` | Burn rate |
| Context bar | `▓▓▓▓░░░░░░░░ 33%` | Green → yellow → red at 70% / 90% |
| Tokens this turn | `↑12k` | Input + cache tokens for current turn |
| Output speed | `18t/s` | Session average output tokens/sec |
| Duration | `⏱ 2m14s` | Total session wall time |
| Diff | `+47 -12` | Lines added/removed this session |
| Rate limits | `5h 42% ↺1h20m` | Pro plan quota + reset countdown |

---

## Requirements

- Python 3.8+
- Claude Code (any version with `statusLine` support)
- Git (optional — git segments skipped if not in a repo)

Works on macOS, Linux, and Windows. On Windows, install Python from [python.org](https://www.python.org/downloads/) first.

---

## Caveman integration

Works with the [caveman](https://github.com/JuliusBrussee/caveman) plugin. Active mode shown as a badge:

```
[CAVEMAN]        ← full mode
[CAVEMAN:LITE]   ← lite mode
[CAVEMAN:ULTRA]  ← ultra mode
```

---

## License

[GNU General Public License v3.0](LICENSE)
