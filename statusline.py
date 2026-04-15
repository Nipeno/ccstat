#!/usr/bin/env python3
# ccstat — compact two-line statusline for Claude Code sessions
# Copyright (C) 2026 Nipeno
# SPDX-License-Identifier: GPL-3.0-or-later
VERSION = "1.3.1"
import json, sys, os, subprocess, time
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ── User config (~/.claude/ccstat.json) ──────────────────────────────────
_CONFIG_PATH = os.path.expanduser('~/.claude/ccstat.json')
_ERR_LOG     = os.path.expanduser('~/.claude/.ccstat-errors.log')
_cfg         = {}
_cfg_errors  = []

try:
    if os.path.exists(_CONFIG_PATH):
        with open(_CONFIG_PATH, encoding='utf-8') as _f:
            _cfg = json.load(_f)
except json.JSONDecodeError as _e:
    _cfg_errors.append(f'ccstat.json parse error: {_e}')
except Exception as _e:
    _cfg_errors.append(f'ccstat.json read error: {_e}')

_bar_width_raw = _cfg.get('bar_width', 12)
try:
    _bar_width_int = int(_bar_width_raw)
    if not (4 <= _bar_width_int <= 40):
        _cfg_errors.append(f'bar_width {_bar_width_raw!r} out of range 4–40, using 12')
        CFG_BAR_WIDTH = 12
    else:
        CFG_BAR_WIDTH = _bar_width_int
except (ValueError, TypeError):
    _cfg_errors.append(f'bar_width must be an integer, got {_bar_width_raw!r}')
    CFG_BAR_WIDTH = 12

CFG_SHOW_TOK_SPEED  = bool(_cfg.get('show_tok_speed', True))
CFG_SHOW_LINES_DIFF = bool(_cfg.get('show_lines_diff', True))
CFG_UPDATE_CHECK    = bool(_cfg.get('update_check', True))
CFG_BADGE_FILE         = str(_cfg.get('badge_file', '.ccstat-badge'))
CFG_BADGE_PREFIX       = str(_cfg.get('badge_prefix', ''))
CFG_BADGE_DEFAULT_MODE = str(_cfg.get('badge_default_mode', 'full'))

if _cfg_errors:
    try:
        with open(_ERR_LOG, 'w', encoding='utf-8') as _ef:
            _ef.write('\n'.join(_cfg_errors) + '\n')
    except Exception:
        pass

# ── Auto-update check (fire-and-forget, once per day) ─────────────────────
_UPDATE_CACHE = os.path.expanduser('~/.claude/.ccstat-update-cache')
_RAW_URL      = 'https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py'
_BG_FETCH     = (
    "import urllib.request,json,time,os\n"
    "cache=" + repr(_UPDATE_CACHE) + "\n"
    "log=" + repr(_ERR_LOG) + "\n"
    "url=" + repr(_RAW_URL) + "\n"
    "try:\n"
    " r=urllib.request.urlopen(url,timeout=4).read().decode('utf-8')\n"
    " ver=next((l.split('\"')[1] for l in r.splitlines() if l.startswith('VERSION')),None)\n"
    " ver and open(cache,'w',encoding='utf-8').write(json.dumps({'checked':time.time(),'latest':ver}))\n"
    "except Exception as e:\n"
    " open(log,'w',encoding='utf-8').write(f'[update check] {e}\\n')\n"
)

update_badge = ''
if CFG_UPDATE_CHECK:
    try:
        _cache = {}
        if os.path.exists(_UPDATE_CACHE):
            with open(_UPDATE_CACHE, encoding='utf-8') as _uf:
                _cache = json.load(_uf)
        _age   = time.time() - float(_cache.get('checked', 0))
        if _age > 86400:
            _kw = {'stdout': subprocess.DEVNULL, 'stderr': subprocess.DEVNULL}
            if os.name == 'posix':
                _kw['start_new_session'] = True
            else:
                _kw['creationflags'] = subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
            subprocess.Popen([sys.executable, '-c', _BG_FETCH], **_kw)
        _latest = _cache.get('latest', VERSION)
        if _latest and _latest != VERSION:
            update_badge = _latest
    except Exception:
        pass

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

# ── ANSI colors ──────────────────────────────────────────────────────────
R      = '\033[0m'
GRAY   = '\033[90m'
ORANGE = '\033[38;5;172m'
CYAN   = '\033[38;5;39m'
GREEN  = '\033[32m'
YELLOW = '\033[33m'
RED    = '\033[31m'
BLUE   = '\033[34m'
MAG    = '\033[35m'
WHITE  = '\033[97m'

# ── Safe nested get ──────────────────────────────────────────────────────
def g(path, default=None):
    v = data
    for k in path.split('.'):
        if not isinstance(v, dict): return default
        v = v.get(k)
        if v is None: return default
    return v

# ── Parse fields ─────────────────────────────────────────────────────────
model         = g('model.display_name') or 'unknown'
cwd           = g('workspace.current_dir') or os.getcwd()
cost          = float(g('cost.total_cost_usd') or 0)
dur_ms        = int(g('cost.total_duration_ms') or 0)
api_ms        = int(g('cost.total_api_duration_ms') or 0)
lines_add     = int(g('cost.total_lines_added') or 0)
lines_rem     = int(g('cost.total_lines_removed') or 0)
ctx_pct       = int(float(g('context_window.used_percentage') or 0))
total_out_tok = int(g('context_window.total_output_tokens') or 0)
curr_in       = int(g('context_window.current_usage.input_tokens') or 0)
curr_cc       = int(g('context_window.current_usage.cache_creation_input_tokens') or 0)
curr_cr       = int(g('context_window.current_usage.cache_read_input_tokens') or 0)
exceeds_200k  = g('exceeds_200k_tokens') is True
session_name  = g('session_name')
worktree      = g('workspace.git_worktree')
rl_5h_pct     = g('rate_limits.five_hour.used_percentage')
rl_5h_reset   = g('rate_limits.five_hour.resets_at')
rl_7d_pct     = g('rate_limits.seven_day.used_percentage')
rl_7d_reset   = g('rate_limits.seven_day.resets_at')

# ── Custom badge ──────────────────────────────────────────────────────────
# Any plugin can show a badge by writing one line to ~/.claude/<badge_file>.
#
# badge_file         — filename inside ~/.claude/ to read (default: .ccstat-badge)
# badge_prefix       — if set, content is treated as a mode name:
#                        default mode → [PREFIX]
#                        other modes  → [PREFIX:MODE]
# badge_default_mode — which mode value omits the suffix (default: "full")
#
# Content with ANSI escape codes is displayed as-is.
# Without a prefix, content is shown as [CONTENT].
badge = ''
_badge_path = os.path.join(os.path.expanduser('~/.claude'), CFG_BADGE_FILE)
if os.path.exists(_badge_path):
    try:
        with open(_badge_path, encoding='utf-8') as _bf:
            _raw = _bf.readline().strip()[:80]
        if _raw:
            if '\033' in _raw:
                badge = _raw
            elif CFG_BADGE_PREFIX:
                _prefix = CFG_BADGE_PREFIX.upper()
                _mode   = _raw.upper()
                if _mode == CFG_BADGE_DEFAULT_MODE.upper():
                    badge = f'{ORANGE}[{_prefix}]{R}'
                else:
                    badge = f'{ORANGE}[{_prefix}:{_mode}]{R}'
            else:
                badge = f'{ORANGE}[{_raw.upper()}]{R}'
    except Exception:
        pass

# ── Effort level ──────────────────────────────────────────────────────────
effort = ''
_settings_path = os.path.expanduser('~/.claude/settings.json')
try:
    with open(_settings_path, encoding='utf-8') as f:
        effort = json.load(f).get('effortLevel', '')
except Exception:
    pass

# ── Shorten path ──────────────────────────────────────────────────────────
_home     = os.path.normpath(os.path.expanduser('~'))
_norm_cwd = os.path.normpath(cwd)
if os.name == 'nt':
    # Case-insensitive home replacement on Windows
    if _norm_cwd.lower().startswith(_home.lower()):
        short_dir = '~' + _norm_cwd[len(_home):]
    else:
        short_dir = _norm_cwd
else:
    short_dir = _norm_cwd.replace(_home, '~', 1)

# ── Git (single subprocess call via --porcelain -b) ───────────────────────
branch = git_status = ahead_behind = ''
try:
    _status_lines = subprocess.check_output(
        ['git', '-C', cwd, 'status', '--porcelain', '-b'],
        text=True, encoding='utf-8', stderr=subprocess.DEVNULL
    ).splitlines()

    _n_staged = _n_modified = _n_untracked = 0
    _ahead = _behind = 0

    for _line in _status_lines:
        if _line.startswith('## '):
            _ref = _line[3:].split('...')[0].strip()
            if _ref.startswith('No commits yet on '):
                branch = _ref[18:]
            elif _ref.startswith('HEAD'):
                branch = ''  # detached HEAD
            else:
                branch = _ref
            # Ahead/behind lives in the same branch line: [ahead N, behind N]
            if '[' in _line and ']' in _line:
                _bracket = _line[_line.index('[')+1:_line.rindex(']')]
                for _part in _bracket.split(','):
                    _part = _part.strip()
                    if _part.startswith('ahead '):
                        try: _ahead = int(_part[6:])
                        except ValueError: pass
                    elif _part.startswith('behind '):
                        try: _behind = int(_part[7:])
                        except ValueError: pass
        elif len(_line) >= 2:
            if _line[:2] == '??':
                _n_untracked += 1
            else:
                if _line[0] not in (' ', '?'): _n_staged += 1
                if _line[1] not in (' ', '?'): _n_modified += 1

    if _n_staged or _n_modified or _n_untracked:
        _parts = []
        if _n_staged:    _parts.append(f'{GREEN}●{_n_staged}{R}')
        if _n_modified:  _parts.append(f'{YELLOW}~{_n_modified}{R}')
        if _n_untracked: _parts.append(f'{GRAY}?{_n_untracked}{R}')
        git_status = ' '.join(_parts)
    else:
        git_status = f'{GREEN}●{R}'

    _ab_parts = []
    if _ahead:  _ab_parts.append(f'{CYAN}↑{_ahead}{R}')
    if _behind: _ab_parts.append(f'{RED}↓{_behind}{R}')
    ahead_behind = ' '.join(_ab_parts)

except Exception:
    pass

# ── Duration formatter ────────────────────────────────────────────────────
def dur_fmt(ms):
    s = ms // 1000
    m = s // 60; s = s % 60
    h = m // 60; m = m % 60
    if h > 0:  return f'{h}h{m}m'
    if m > 0:  return f'{m}m{s}s'
    return f'{s}s'

# ── Countdown formatter ───────────────────────────────────────────────────
def countdown(ts):
    if not ts: return ''
    diff = int(ts) - int(time.time())
    if diff <= 0: return 'now'
    d = diff // 86400
    h = (diff % 86400) // 3600
    m = (diff % 3600) // 60
    if d > 0: return f'{d}d{h}h'
    if h > 0: return f'{h}h{m}m'
    return f'{m}m'

# ── Rate limit color ──────────────────────────────────────────────────────
def rl_color(pct):
    if pct >= 80: return RED
    if pct >= 50: return YELLOW
    return GREEN

# ── Cost color + per-hour ─────────────────────────────────────────────────
# on_pro: inferred from rate limit data presence — API users don't receive
# rate_limits fields; Pro/Max plan users do.
on_pro     = rl_5h_pct is not None or rl_7d_pct is not None
quota_gone = on_pro and (rl_5h_pct is not None and float(rl_5h_pct) >= 100)
cost_real  = not on_pro or quota_gone
cost_color = YELLOW if cost_real else GRAY
cost_ph    = (cost / dur_ms * 3_600_000) if dur_ms > 0 else 0
cost_fmt   = f'{cost_color}${cost:.3f}{R}  {cost_color}${cost_ph:.2f}/h{R}'

# ── Token speed (session avg output tok/s) ────────────────────────────────
tok_speed     = int(total_out_tok / (api_ms / 1000)) if api_ms > 0 else 0
tok_speed_fmt = f'{GRAY}{tok_speed}t/s{R}' if tok_speed > 0 else ''

# ── Context bar ───────────────────────────────────────────────────────────
filled = min(ctx_pct * CFG_BAR_WIDTH // 100, CFG_BAR_WIDTH)
empty  = CFG_BAR_WIDTH - filled
bc     = RED if ctx_pct >= 90 else YELLOW if ctx_pct >= 70 else GREEN
bar    = f'{bc}{"▓" * filled}{R}{GRAY}{"░" * empty}{R}'

# ── Tokens this turn ──────────────────────────────────────────────────────
curr_total = curr_in + curr_cc + curr_cr
curr_fmt   = f'↑{curr_total // 1000}k' if curr_total >= 1000 else f'↑{curr_total}'

# ── Rate limits ───────────────────────────────────────────────────────────
rl_parts = []
if rl_5h_pct is not None:
    p  = int(float(rl_5h_pct))
    cd = countdown(rl_5h_reset)
    rl_parts.append(f'5h {rl_color(p)}{p}%{R} ↺{cd}')
if rl_7d_pct is not None:
    p  = int(float(rl_7d_pct))
    cd = countdown(rl_7d_reset)
    rl_parts.append(f'7d {rl_color(p)}{p}%{R} ↺{cd}')
rl_str = (f'  {GRAY}│{R}  ' + f'  {GRAY}·{R}  '.join(rl_parts)) if rl_parts else ''

# ── Build line 1 — identity (where → what → mode → time → alerts) ────────
l1 = []
l1.append(f'{CYAN}{short_dir}{R}')
if branch:
    git_seg = f'{GREEN}{branch}{R}'
    if ahead_behind: git_seg += f' {ahead_behind}'
    git_seg += f' {git_status}'
    l1.append(git_seg)
if worktree:     l1.append(f'{GRAY}wt:{worktree}{R}')
l1.append(f'{WHITE}{model}{R}')
if effort:       l1.append(f'{BLUE}{effort}{R}')
l1.append(f'{GRAY}{datetime.now().strftime("%H:%M")}{R}')
if badge:        l1.append(badge)
if session_name: l1.append(f'{MAG}[{session_name}]{R}')
if exceeds_200k: l1.append(f'{RED}⚠ 200k{R}')
if update_badge: l1.append(f'{YELLOW}↑ v{update_badge}{R}')
if _cfg_errors:  l1.append(f'{RED}⚠ cfg{R}')

# ── Build line 2 — resources (cost → context → tokens → speed → time → diff → limits) ──
l2 = [
    cost_fmt,
    f'{bar} {ctx_pct}%',
    curr_fmt,
]
if CFG_SHOW_TOK_SPEED and tok_speed_fmt: l2.append(tok_speed_fmt)
l2.append(f'⏱ {dur_fmt(dur_ms)}')
if CFG_SHOW_LINES_DIFF: l2.append(f'{GREEN}+{lines_add}{R} {RED}-{lines_rem}{R}')

print('  '.join(l1))
print('  '.join(l2) + rl_str)
