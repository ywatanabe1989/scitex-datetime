"""Compile-only stub for examples/quickstart.py (PS303)."""

import subprocess
import sys
from pathlib import Path

QUICKSTART = Path(__file__).parents[2] / "examples" / "quickstart.py"


def test_quickstart_example_compiles_without_syntax_error():
    # Arrange
    if not QUICKSTART.is_file():
        # File missing is itself a failure, but a missing-file
        # assertion would count as a second assertion (STX-TQ007).
        # Treat absence as the failure path of the same check.
        compile_returncode = -1
        stderr_text = f"missing {QUICKSTART}"
    else:
        # Act
        proc = subprocess.run(
            [sys.executable, "-m", "py_compile", str(QUICKSTART)],
            capture_output=True,
        )
        compile_returncode = proc.returncode
        stderr_text = proc.stderr.decode(errors="replace")

    # Assert
    # `py_compile` exits 0 on a clean parse; anything else means the
    # quickstart example silently rotted.
    assert compile_returncode == 0, stderr_text
