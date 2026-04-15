# Contributing to ccstat

Thanks for your interest in contributing.

## Before You Start

- Check existing [issues](https://github.com/Nipeno/ccstat/issues) and [PRs](https://github.com/Nipeno/ccstat/pulls) to avoid duplicate work.
- For large changes, open an issue first to discuss the approach.

## Setup

```bash
git clone https://github.com/Nipeno/ccstat.git
cd ccstat
```

No dependencies beyond Python 3.8+ and Claude Code.

## Making Changes

### `statusline.py`

This script runs on every Claude Code prompt on users' machines. Hold it to a high standard.

- **Bump the version** at the top of the file before committing (semver: patch/minor/major).
- **Smoke test** before committing:
  ```bash
  echo '{}' | python3 statusline.py
  ```
- **Cross-platform**: use `os.path.join`, not hardcoded `/`. Test mentally against macOS, Linux, Windows.
- **No `eval()`/`exec()`** on external data. No HTTP (use HTTPS). No shell injection.

### Skill files

Skill files live in `skills/<name>/SKILL.md`. Changes here don't require a version bump.

### README / CHANGELOG

If you add a feature or config option, update `README.md`. Add an entry to `CHANGELOG.md` under the new version.

## Submitting a PR

1. Fork and create a branch: `git checkout -b fix/my-fix`
2. Make your changes following the guidelines above
3. Fill out the pull request template completely
4. Submit — a maintainer will review promptly

## Reporting Bugs

Use the [bug report issue template](https://github.com/Nipeno/ccstat/issues/new/choose). Include your OS, Python version, and the exact error output.

## Security Issues

Do **not** open a public issue for security vulnerabilities. See [SECURITY.md](SECURITY.md).
