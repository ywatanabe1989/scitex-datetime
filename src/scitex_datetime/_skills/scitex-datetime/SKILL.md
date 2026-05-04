---
name: scitex-datetime
description: |
  [WHAT] Datetime/duration helpers for SciTeX scripts — parsing, formatting, ISO round-trips, and ergonomic Δt arithmetic.
  [WHEN] Working with timestamps in logs, experiment metadata, or session bookkeeping.
  [HOW] `from scitex_datetime import ...` or `scitex-datetime --help`.
primary_interface: python
interfaces:
  python: 2
  cli: 0
  mcp: 0
  skills: 2
  hook: 0
  http: 0
canonical-location: scitex-datetime/src/scitex_datetime/_skills/scitex-datetime/SKILL.md
tags: [scitex-datetime]
---

> **Interfaces:** Python ⭐⭐ · CLI — · MCP — · Skills ⭐⭐ · Hook — · HTTP —

# scitex-datetime

Datetime helpers — `linspace(start, end, n)` for evenly-spaced datetime arrays, `normalize_timestamp(s)` for canonical strings, `to_datetime(any)` for permissive parsing, `format_for_filename(dt)` and `format_for_display(dt)`, `get_time_delta_seconds(a, b)`. Drop-in replacement for memorising pandas/numpy/dateutil format-string dance.

See README.md and the package's public `__init__.py` for the full
function list. This skill leaf exists so agents discover the package
exists and roughly what shape it has — refer to the source for
signatures.

## Sub-skills

### Core (01–09)
- [01_installation.md](01_installation.md) — install + import sanity check
- [02_quick-start.md](02_quick-start.md) — 30-second tour
- [03_python-api.md](03_python-api.md) — Python API surface
