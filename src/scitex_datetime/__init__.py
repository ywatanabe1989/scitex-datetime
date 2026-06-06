#!/usr/bin/env python3
# Timestamp: "2026-01-05 14:30:00 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-code/src/scitex/datetime/__init__.py

"""scitex-datetime — datetime helpers (standalone).

Provides utilities for datetime operations including:
- linspace: Create linearly spaced datetime arrays
- normalize_timestamp: Standardize timestamps to consistent format
- to_datetime: Convert various formats to datetime objects
- validate_timestamp_format: Validate timestamp string format
- format_for_filename: Format timestamps for filenames
- format_for_display: Format timestamps for display
- get_time_delta_seconds: Calculate time differences
"""

from __future__ import annotations

# importlib.metadata is stdlib since 3.8 and `requires-python = ">=3.9"`, so
# the only failure mode left is PackageNotFoundError (running from a source
# checkout that was never `pip install`-ed). Mirrors the canonical
# scitex-stats __init__.py version block.
from importlib.metadata import PackageNotFoundError as _PackageNotFoundError
from importlib.metadata import version as _version

try:
    __version__ = _version("scitex-datetime")
except _PackageNotFoundError:
    __version__ = "0.0.0+local"
del _version, _PackageNotFoundError

from ._linspace import linspace
from ._time_stamper import TimeStamper
from ._normalize_timestamp import (
    ALTERNATIVE_FORMATS,
    STANDARD_FORMAT,
    format_for_display,
    format_for_filename,
    get_time_delta_seconds,
    normalize_timestamp,
    parse_patient_recording_start_format,
    to_datetime,
    validate_timestamp_format,
)

__all__ = [
    "__version__",
    # Core functions
    "linspace",
    "TimeStamper",
    "normalize_timestamp",
    "to_datetime",
    # Formatting functions
    "format_for_filename",
    "format_for_display",
    "validate_timestamp_format",
    # Utility functions
    "get_time_delta_seconds",
    "parse_patient_recording_start_format",
    # Constants
    "STANDARD_FORMAT",
    "ALTERNATIVE_FORMATS",
]
