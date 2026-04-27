# scitex-datetime

<!-- scitex-badges:start -->
[![PyPI](https://img.shields.io/pypi/v/scitex-datetime.svg)](https://pypi.org/project/scitex-datetime/)
[![Python](https://img.shields.io/pypi/pyversions/scitex-datetime.svg)](https://pypi.org/project/scitex-datetime/)
[![Tests](https://github.com/ywatanabe1989/scitex-datetime/actions/workflows/test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-datetime/actions/workflows/test.yml)
[![Install Test](https://github.com/ywatanabe1989/scitex-datetime/actions/workflows/install-test.yml/badge.svg)](https://github.com/ywatanabe1989/scitex-datetime/actions/workflows/install-test.yml)
[![Coverage](https://codecov.io/gh/ywatanabe1989/scitex-datetime/graph/badge.svg)](https://codecov.io/gh/ywatanabe1989/scitex-datetime)
[![Docs](https://readthedocs.org/projects/scitex-datetime/badge/?version=latest)](https://scitex-datetime.readthedocs.io/en/latest/)
[![License: AGPL v3](https://img.shields.io/badge/license-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
<!-- scitex-badges:end -->


Small datetime helpers extracted from the [SciTeX](https://github.com/ywatanabe1989/scitex-python) ecosystem as a standalone package.

## Install

```bash
pip install scitex-datetime
```

## API

```python
import scitex_datetime as sxd

# Linearly spaced timestamps
sxd.linspace(start, stop, num=100)

# Parse and standardize timestamps
sxd.normalize_timestamp("2026-04-27T10:30:00")
sxd.to_datetime("2026/04/27 10:30:00")
sxd.validate_timestamp_format("2026-04-27 10:30:00")

# Format
sxd.format_for_display(dt)       # "2026-04-27 10:30:00"
sxd.format_for_filename(dt)      # "2026-04-27_103000"

# Time deltas
sxd.get_time_delta_seconds(dt1, dt2)
```

## Status

Standalone fork of `scitex.datetime`. The umbrella package's `scitex.datetime`
import path is preserved via a `sys.modules`-alias bridge. `STANDARD_FORMAT`
is read from a scitex CONFIG when available, falling back to `"%Y-%m-%d %H:%M:%S"`.

## License

AGPL-3.0-only (see [LICENSE](./LICENSE)).
