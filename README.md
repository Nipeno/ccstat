# ccstat for Claude Code

Compact two-line statusline for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) sessions.

![ccstat screenshot](screenshot.png)

**Line 1 — identity:** directory · git branch + status · model · time · alerts  
**Line 2 — resources:** cost + $/hour · context bar · tokens · output speed · duration · lines changed · rate limits

---

## Install

```bash
claude plugin marketplace add Nipeno/ccstat
claude plugin install ccstat@ccstat
```

Then run `/ccstat-setup` in any Claude Code session. Done.

This downloads `statusline.py`, configures `settings.json`, and verifies the install. Works on macOS, Linux, and Windows.

<details>
<summary>Alternative: install without the plugin marketplace</summary>

```bash
curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/install.sh | bash
```

This installs the statusline only. Slash commands (`/ccstat-update`, `/ccstat-config`, etc.) require the plugin.

</details>

---

## Commands

All commands are available as Claude Code slash commands after installing the plugin.

| Command | Description |
|---------|-------------|
| `/ccstat-setup` | Set up or repair ccstat |
| `/ccstat-update` | Check for updates and apply with confirmation |
| `/ccstat-remove` | Remove ccstat and clean up settings |
| `/ccstat-info` | Show version, update status, and current config |
| `/ccstat-config` | View or change settings in `~/.claude/ccstat.json` |

---

## Configuration

Create `~/.claude/ccstat.json` to override defaults (all keys optional):

```json
{
  "bar_width": 12,
  "show_tok_speed": true,
  "show_lines_diff": true,
  "update_check": true,
  "badge_file": ".ccstat-badge",
  "badge_prefix": "",
  "badge_default_mode": "full"
}
```

| Key | Default | Description |
|-----|---------|-------------|
| `bar_width` | `12` | Width of the context bar in characters (4–40) |
| `show_tok_speed` | `true` | Show output token speed (t/s) |
| `show_lines_diff` | `true` | Show +lines / -lines diff |
| `update_check` | `true` | Daily background update check |
| `badge_file` | `.ccstat-badge` | Filename inside `~/.claude/` that plugins write badges to |
| `badge_prefix` | `""` | If set, file content is treated as a mode name and displayed as `[PREFIX:MODE]` |
| `badge_default_mode` | `"full"` | Mode value that omits the suffix (shown as `[PREFIX]` not `[PREFIX:FULL]`) |

Or just use `/ccstat-config` and Claude will handle it.

---

## Auto-updates

ccstat checks for updates once per day in the background — a fire-and-forget subprocess with no tokens and no blocking. When a new version is available, a `↑ vX.Y.Z` badge appears on line 1. Run `/ccstat-update` to apply. Run `/ccstat-info` to check manually.

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
| Plugin badge | `[CAVEMAN]` | Generic badge slot — any plugin can write to `~/.claude/.ccstat-badge` |
| Session name | `[my-session]` | Shown if session is named |
| Context warning | `⚠ 200k` | When context exceeds 200k tokens |
| Update badge | `↑ v1.3.0` | New version available — run `/ccstat-update` |

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

## Plugin badge system

ccstat has a generic badge slot on line 1. Any plugin can show a badge by writing one line to `~/.claude/.ccstat-badge`. The caveman plugin does this automatically:

```
[CAVEMAN]        ← full mode
[CAVEMAN:LITE]   ← lite mode
[CAVEMAN:ULTRA]  ← ultra mode
```

To integrate your own plugin, write a line to `~/.claude/.ccstat-badge`. Configure the badge display with `badge_file`, `badge_prefix`, and `badge_default_mode` in `ccstat.json`.

---

## License

[GNU General Public License v3.0](LICENSE)
