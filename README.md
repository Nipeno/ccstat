# ccstat

Compact two-line status display for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) sessions.

```
~/Documents/GitHub/myproject  main ●3 ~1  claude-sonnet-4-6  14:22
$0.042  $1.23/h  ▓▓▓▓░░░░░░░░ 33%  ↑12k  18t/s  ⏱ 2m14s  +47 -12
```

**Line 1 — identity:** directory · git branch + status · model · effort level · time · alerts  
**Line 2 — resources:** cost + $/hour · context bar · tokens this turn · output speed · duration · lines changed · rate limits

---

## Install

**1. Copy the script:**

```bash
curl -o ~/.claude/statusline.py https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py
```

**2. Add to `~/.claude/settings.json`:**

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/statusline.py"
  }
}
```

That's it. The statusline appears at the bottom of every Claude Code session.

---

## What each segment shows

### Line 1

| Segment | Example | Notes |
|---|---|---|
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
|---|---|---|
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
