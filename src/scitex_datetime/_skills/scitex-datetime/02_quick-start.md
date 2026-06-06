---
description: |
  [TOPIC] Quick Start
  [DETAILS] Smallest useful example demonstrating the primary use case in
  under 30 seconds.
tags: [scitex-datetime-quick-start]
---

# Quick Start

```python
import scitex_datetime as sxd

# Parse heterogeneous timestamps
dt = sxd.to_datetime("2026/04/27 10:30:00")

# Format for filenames (no spaces or colons)
print(sxd.format_for_filename(dt))   # "2026-04-27_103000"

# Format for display
print(sxd.format_for_display(dt))    # "2026-04-27 10:30:00"

# Standardise any timestamp format
ts = sxd.normalize_timestamp("2026-04-27T10:30:00")
print(ts)                            # "2026-04-27 10:30:00"

# Linearly spaced datetimes
from datetime import datetime, timedelta
start = datetime(2026, 4, 27, 10, 0, 0)
end = start + timedelta(hours=1)
grid = sxd.linspace(start, end, n_samples=5)
print(grid)                          # [datetime, ..., datetime]  (5 evenly spaced)
```
