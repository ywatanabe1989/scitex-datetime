---
description: |
  [TOPIC] Python API
  [DETAILS] Public Python API of scitex-datetime — exported functions, signatures,
  return types, and minimal usage examples per function.
tags: [scitex-datetime-python-api]
---

# Python API

```python
import scitex_datetime as sxd
```

## Constants

### STANDARD_FORMAT -> str
Default: `"%Y-%m-%d %H:%M:%S"`. Overridden by `CONFIG.FORMATS.TIMESTAMP`
when `scitex_io` is installed (the `[all]` extra).

### ALTERNATIVE_FORMATS -> list[str]
List of format strings tried sequentially by `to_datetime()` when parsing
string timestamps. Includes ISO 8601, US, European, and compact variants.

---

## Core Functions

### to_datetime(timestamp) -> datetime

Convert various timestamp formats to a `datetime` object.

```python
sxd.to_datetime("2026/04/27 10:30:00")          # string
sxd.to_datetime("2026-04-27T10:30:00")           # ISO 8601
sxd.to_datetime(1714208400)                      # Unix seconds (int)
sxd.to_datetime(1714208400.5)                    # Unix seconds (float)
sxd.to_datetime(datetime(2026, 4, 27, 10, 30))  # already datetime
```

**Parameters:**
- `timestamp: datetime | str | int | float` — input in any supported format

**Returns:** `datetime` — parsed datetime object

**Raises:**
- `ValueError` if string format cannot be parsed
- `TypeError` if type is not supported

---

### normalize_timestamp(timestamp, return_as="str", normalize_utc=True) -> str | datetime | float

Standardize any timestamp format to a consistent output.

```python
sxd.normalize_timestamp("2026-04-27T10:30:00")
# → "2026-04-27 10:30:00"

sxd.normalize_timestamp("2026-04-27T10:30:00", return_as="datetime")
# → datetime(2026, 4, 27, 10, 30)

sxd.normalize_timestamp("2026-04-27T10:30:00", return_as="timestamp")
# → 1714208400.0
```

**Parameters:**
- `timestamp: datetime | str | int | float` — input timestamp
- `return_as: str` — `"str"` (default), `"datetime"`, or `"timestamp"`
- `normalize_utc: bool` — if True (default), normalize to UTC timezone

**Returns:** `str`, `datetime`, or `float` depending on `return_as`

---

### validate_timestamp_format(timestamp_str) -> bool

Check whether a string matches the standard format (`STANDARD_FORMAT`).

```python
sxd.validate_timestamp_format("2026-04-27 10:30:00")   # True
sxd.validate_timestamp_format("2026/04/27 10:30:00")   # False
```

**Parameters:**
- `timestamp_str: str` — string to validate

**Returns:** `bool`

---

## Formatting Functions

### format_for_filename(timestamp) -> str

Format a timestamp for use in filenames (no spaces or colons).

```python
sxd.format_for_filename("2026-04-27 10:30:00")
# → "20260427_103000"
```

**Parameters:**
- `timestamp: datetime | str` — input timestamp

**Returns:** `str` — `"%Y%m%d_%H%M%S"` format

---

### format_for_display(timestamp) -> str

Format a timestamp for human-readable display.

```python
sxd.format_for_display("2026/04/27 10:30:00")
# → "2026-04-27 10:30:00"
```

**Parameters:**
- `timestamp: datetime | str` — input timestamp

**Returns:** `str` — `"%Y-%m-%d %H:%M:%S"` format

---

## Utility Functions

### linspace(start_dt, end_dt, n_samples=None, sampling_rate=None) -> np.ndarray

Create a linearly spaced array of `datetime` objects between two endpoints.

```python
from datetime import datetime
start = datetime(2026, 4, 27, 10, 0, 0)
end   = datetime(2026, 4, 27, 11, 0, 0)

# Fixed number of samples
grid = sxd.linspace(start, end, n_samples=5)       # 5 evenly spaced

# Sampling rate in Hz
grid = sxd.linspace(start, end, sampling_rate=4.0)  # 4 Hz over 1 hour
```

**Parameters:**
- `start_dt: datetime` — start of the range
- `end_dt: datetime` — end of the range (must be later than start_dt)
- `n_samples: int, optional` — number of samples (mutually exclusive with sampling_rate)
- `sampling_rate: float, optional` — sampling rate in Hz (mutually exclusive with n_samples)

**Returns:** `np.ndarray` — array of `datetime` objects

**Raises:**
- `TypeError` if start_dt or end_dt is not a datetime
- `ValueError` if start_dt >= end_dt, or if both/neither n_samples and sampling_rate provided

---

### get_time_delta_seconds(start, end) -> float

Calculate the time difference in seconds between two timestamps.

```python
sxd.get_time_delta_seconds("2026-04-27 10:00:00", "2026-04-27 11:30:00")
# → 5400.0
```

**Parameters:**
- `start: datetime | str` — start timestamp
- `end: datetime | str` — end timestamp

**Returns:** `float` — time difference in seconds

---

### parse_patient_recording_start_format(str) -> datetime

Parse a recording-start string in the `"DD/MM/YYYY, HH:MM:SS"` format.

```python
sxd.parse_patient_recording_start_format("10/06/2010, 07:40:34")
# → datetime(2010, 6, 10, 7, 40, 34)
```

**Parameters:**
- `patient_recording_start_str: str` — string in `%d/%m/%Y, %H:%M:%S` format

**Returns:** `datetime`
