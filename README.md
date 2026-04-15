# ccstat

Compact two-line status display for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) sessions.

![ccstat screenshot](screenshot.png)

**Line 1 — identity:** directory · git branch + status · model · time · alerts  
**Line 2 — resources:** cost + $/hour · context bar · tokens · output speed · duration · lines changed · rate limits

---

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/Nipeno/ccstat/main/install.sh | bash
```

The script downloads `statusline.py` to `~/.claude/` and patches `~/.claude/settings.json`. If you already have a `statusLine` configured, it will print a warning and show you what it would replace — nothing is overwritten without confirmation.

---

## Uninstall

```bash
rm ~/.claude/statusline.py
```

Then remove the `statusLine` block from `~/.claude/settings.json`. The statusline stops appearing immediately.

---

## What each segment shows

### Line 1

| Segment | Example | Notes |
| --- | --- | --- |
| Directory | `~/projects/myapp` | Home-shortened path |
| Git branch | `main` | Current branch |
| Git ahead/behind | `↑2 ↓1` | Commits ahead/behind upstream |
| Git status | `●3 ~1 ?2` | Staged · modified · untracked |
| Model | `claude-sonnet-4-6` | Active model |
| Effort | `high` | Only shown if `effortLevel` is set |
| Time | `14:22` | Local clock |
| Caveman badge | `[CAVEMAN]` | Shown if [caveman](https://github.com/JuliusBrussee/caveman) plugin is active |
| Session name | `[my-session]` | Only shown if session is named |
| Context warning | `⚠ 200k` | When context exceeds 200k tokens |

### Line 2

| Segment | Example | Notes |
| --- | --- | --- |
| Cost | `$0.042` | Session total. Gray on Pro (quota not depleted) |
| Cost/hour | `$1.23/h` | Burn rate |
| Context bar | `▓▓▓▓░░░░░░░░ 33%` | Green → yellow → red at 70%/90% |
| Tokens this turn | `↑12k` | Input + cache tokens for current turn |
| Output speed | `18t/s` | Session average output tokens/sec |
| Duration | `⏱ 2m14s` | Total session wall time |
| Diff | `+47 -12` | Lines added/removed this session |
| Rate limits | `5h 42% ↺1h20m` | Pro plan quota usage + reset countdown |

---

## Requirements

- Python 3.8+
- Claude Code (any version with `statusLine` support)
- Git (optional — git segments are skipped if not in a repo)

**Platform notes:** ccstat works out of the box on macOS and Linux, which ship with Python 3. On Windows, Python isn't included by default — install it from [python.org](https://www.python.org/downloads/) first, then use the manual install below.

<details>
<summary>Manual install (Windows / no curl)</summary>

1. Download [`statusline.py`](https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py) and save it to `%USERPROFILE%\.claude\statusline.py`
2. Add to `%USERPROFILE%\.claude\settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

</details>

---

## Caveman integration

If you use the [caveman](https://github.com/JuliusBrussee/caveman) plugin, ccstat shows a badge indicating the active mode:

```
[CAVEMAN]        ← full mode
[CAVEMAN:LITE]   ← lite mode
[CAVEMAN:ULTRA]  ← ultra mode
```

---

## License

MIT
