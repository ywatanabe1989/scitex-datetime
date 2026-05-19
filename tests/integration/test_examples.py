"""Smoke tests: every example script must run to completion.

Each example script is exercised independently via pytest parametrize so
that a failure points at the offending script rather than aborting the
whole suite on the first error.
"""

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).parents[2] / "examples"
EXAMPLE_SCRIPTS = sorted(EXAMPLES_DIR.glob("*.py"))


def test_examples_directory_is_populated():
    """Discovery sanity check: there must be at least one example script.

    Guards against an empty `examples/` directory silently turning the
    parametrized smoke test below into a no-op.
    """
    # Arrange
    discovered = EXAMPLE_SCRIPTS

    # Act
    count = len(discovered)

    # Assert
    assert count > 0, f"no example scripts found under {EXAMPLES_DIR}"


@pytest.mark.parametrize(
    "example_script",
    EXAMPLE_SCRIPTS,
    ids=[p.name for p in EXAMPLE_SCRIPTS],
)
def test_example_script_runs_to_completion(example_script, tmp_path):
    """Each example script must exit with returncode 0 within 60s.

    The script is launched in a fresh tmp_path cwd so that any artifacts
    it writes do not pollute the repository.
    """
    # Arrange
    cmd = [sys.executable, str(example_script)]

    # Act
    result = subprocess.run(
        cmd,
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=60,
    )

    # Assert
    assert result.returncode == 0, (
        f"{example_script.name} failed (rc={result.returncode}):\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )
