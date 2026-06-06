# Changelog

All notable changes to `scitex-datetime` are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.1.4] — 2026-01-05

- ci: resync integrated release pipeline from scitex-dev v0.11.20
- ci: standardize to scitex-dev canonical workflow set

## [0.1.3] — 2026-01-04

- deps: collapse to 3-tier pyproject (default + [all] + [dev])
- fix(_normalize_timestamp): use scitex_io peer instead of umbrella import
- deps: canonical version-pinning pattern in __init__
- deps: bump scitex-dev pin floor to 0.11.7
- deps: pin scitex-dev>=0.11.5 in [dev]
- quality: subprocess coverage wiring + codecov.yml + .scitex tracked
- test: cross-package import runtime gate (PS140), pytest.importorskip pattern
- test: integrate audit-all into the test suite
- docs: CHANGELOG.md + CONTRIBUTING.md (PS134/PS135)
- docs: Architecture + Demo sections in README (PS141/PS142)
- docs: skills leaves per SK105–107 template + SK706/709/710 fixes
- docs: canonical README layout per scitex-dev skill updates

## [0.1.2] — 2026-01-03

- chore: PS204 — test layout mirrors src/, examples → tests/integration/
- fix: PA501/PA201/PA203 — `from __future__ import annotations`, `__version__` in `__all__`
- fix: skills — strip trailing `<!-- EOF -->` (SK211)
- fix: release-safety — opt-in publish-pypi.yml (workflow_dispatch only)
- chore: switch __version__ to importlib.metadata to prevent version drift

## [0.1.1] — 2026-01-02

- feat: SKILL.md + _skills shipped via package-data (audit §E1)
- feat: quickstart example + test_examples smoke test

## [0.1.0]

- Initial CHANGELOG entry — see git log for prior history.
