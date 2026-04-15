#!/usr/bin/env python3
# ccstat — compact two-line statusline for Claude Code sessions
# Copyright (C) 2026 Nipeno
# SPDX-License-Identifier: GPL-3.0-or-later
VERSION = "1.1.0"
import json, sys, os, subprocess, time
from datetime import datetime

# ── User config (~/.claude/ccstat.json) ──────────────────────────────────
_CONFIG_PATH = os.path.expanduser('~/.claude/ccstat.json')
_cfg = {}
try:
    if os.path.exists(_CONFIG_PATH):
        with open(_CONFIG_PATH) as _f:
            _cfg = json.load(_f)
except Exception:
    pass

CFG_BAR_WIDTH       = int(_cfg.get('bar_width', 12))
CFG_SHOW_TOK_SPEED  = bool(_cfg.get('show_tok_speed', True))
CFG_SHOW_LINES_DIFF = bool(_cfg.get('show_lines_diff', True))
CFG_UPDATE_CHECK    = bool(_cfg.get('update_check', True))

# ── Auto-update check (fire-and-forget, once per day) ─────────────────────
_UPDATE_CACHE = os.path.expanduser('~/.claude/.ccstat-update-cache')
_RAW_URL      = 'https://raw.githubusercontent.com/Nipeno/ccstat/main/statusline.py'
_BG_FETCH     = (
    "import urllib.request,json,time\n"
    "cache=" + repr(_UPDATE_CACHE) + "\n"
    "url=" + repr(_RAW_URL) + "\n"
    "try:\n"
    " r=urllib.request.urlopen(url,timeout=4).read().decode()\n"
    " ver=next((l.split('\"')[1] for l in r.splitlines() if l.startswith('VERSION')),None)\n"
    " ver and open(cache,'w').write(json.dumps({'checked':time.time(),'latest':ver}))\n"
    "except:pass\n"
)

update_badge = ''
if CFG_UPDATE_CHECK:
    try:
        _cache = json.loads(open(_UPDATE_CACHE).read()) if os.path.exists(_UPDATE_CACHE) else {}
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

# ── Caveman badge ─────────────────────────────────────────────────────────
badge = ''
flag = os.path.expanduser('~/.claude/.caveman-active')
if os.path.exists(flag):
    try:
        with open(flag) as _ff:
            mode = _ff.read().strip()
        if not mode or mode == 'full':
            badge = f'{ORANGE}[CAVEMAN]{R}'
        else:
            badge = f'{ORANGE}[CAVEMAN:{mode.upper()}]{R}'
    except Exception:
        badge = f'{ORANGE}[CAVEMAN]{R}'

# ── Effort level ──────────────────────────────────────────────────────────
effort = ''
settings_path = os.path.expanduser('~/.claude/settings.json')
try:
    with open(settings_path) as f:
        effort = json.load(f).get('effortLevel', '')
except Exception:
    pass

# ── Shorten path ──────────────────────────────────────────────────────────
home = os.path.expanduser('~')
short_dir = cwd.replace(home, '~', 1)

# ── Git ───────────────────────────────────────────────────────────────────
branch = git_status = ahead_behind = ''
try:
    subprocess.check_output(['git','-C',cwd,'rev-parse','--git-dir'], stderr=subprocess.DEVNULL)
    branch = subprocess.check_output(
        ['git','-C',cwd,'branch','--show-current'], text=True, stderr=subprocess.DEVNULL).strip()

    staged_out    = subprocess.check_output(['git','-C',cwd,'diff','--cached','--numstat'],    text=True, stderr=subprocess.DEVNULL).strip()
    modified_out  = subprocess.check_output(['git','-C',cwd,'diff','--numstat'],               text=True, stderr=subprocess.DEVNULL).strip()
    untracked_out = subprocess.check_output(['git','-C',cwd,'ls-files','--others','--exclude-standard'], text=True, stderr=subprocess.DEVNULL).strip()

    n_staged    = len([l for l in staged_out.split('\n')    if l])
    n_modified  = len([l for l in modified_out.split('\n')  if l])
    n_untracked = len([l for l in untracked_out.split('\n') if l])

    if n_staged or n_modified or n_untracked:
        parts = []
        if n_staged:    parts.append(f'{GREEN}●{n_staged}{R}')
        if n_modified:  parts.append(f'{YELLOW}~{n_modified}{R}')
        if n_untracked: parts.append(f'{GRAY}?{n_untracked}{R}')
        git_status = ' '.join(parts)
    else:
        git_status = f'{GREEN}●{R}'

    # Commits ahead/behind upstream
    try:
        ab = subprocess.check_output(
            ['git','-C',cwd,'rev-list','--left-right','--count','HEAD...@{u}'],
            text=True, stderr=subprocess.DEVNULL).strip().split()
        ahead, behind = int(ab[0]), int(ab[1])
        ab_parts = []
        if ahead:  ab_parts.append(f'{CYAN}↑{ahead}{R}')
        if behind: ab_parts.append(f'{RED}↓{behind}{R}')
        ahead_behind = ' '.join(ab_parts)
    except Exception:
        pass
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
