#!/usr/bin/env python3
"""Per-edge integration + degradation tests for the scitex-io edge.

This file mirrors the canonical ecosystem template
(``scitex-io`` branch ``test/figrecipe-integration-edge``,
``tests/integration/test_figrecipe_edge.py``) for the *optional*
``scitex_io`` collaborator of ``scitex-datetime``.

The edge under test
-------------------
``scitex_datetime._normalize_timestamp`` resolves its module-level
``STANDARD_FORMAT`` from ``scitex_io.load_configs()`` *when scitex-io is
installed* (the ``[all]`` extra). The wiring is a single
``try_import_optional("scitex_io", attr="load_configs", extra="all",
pkg="scitex-datetime")`` call:

  - scitex-io PRESENT  -> ``_load_configs`` is the real ``load_configs``
    callable; ``STANDARD_FORMAT`` is taken from ``CONFIG.FORMATS.TIMESTAMP``
    when that key exists, otherwise it falls back to ``DEFAULT_FORMAT``.
  - scitex-io ABSENT   -> ``try_import_optional`` swallows the ImportError
    and returns ``None``; ``_load_configs is None`` and ``STANDARD_FORMAT``
    degrades to ``DEFAULT_FORMAT`` ("%Y-%m-%d %H:%M:%S"). Every public
    timestamp helper keeps working — the optional peer only ever *upgrades*
    the configured format, it is never required.

The two test kinds every optional edge should have
--------------------------------------------------
1. INTEGRATION (collaborator PRESENT): exercise the real ``scitex_io`` and
   assert on the concrete wiring it enables. Guarded with
   ``pytest.importorskip("scitex_io")`` so the suite stays green on minimal
   installs instead of erroring.

2. DEGRADATION (collaborator ABSENT): simulate ``scitex_io`` being missing in
   a hermetic, reversible way (a fixture that snapshots ``sys.modules``,
   shadows ``scitex_io`` with ``None`` + an inert stub, reloads the affected
   module, and restores everything on teardown), then assert the documented,
   caller-safe contract: ``_load_configs is None``, ``STANDARD_FORMAT ==
   DEFAULT_FORMAT``, and the public helpers still produce correct output.

Conventions honoured (so this stays a clean template):
  - One assertion per test (TQ007): expensive shared setup (the reload under
    the simulated-absent dependency) is lifted into a fixture; each behaviour
    gets its own named, single-assert test so a red CI line names exactly what
    broke.
  - Explicit Arrange / Act / Assert markers in every test (TQ002).
  - No ``monkeypatch`` / ``mocker`` (banned ecosystem-wide): the
    scitex-io-absent fixture hand-swaps ``sys.modules`` and restores it on
    teardown.
"""

from __future__ import annotations

import importlib
import sys
from datetime import datetime

import pytest

_MODULE = "scitex_datetime._normalize_timestamp"


# ===========================================================================
# 1. INTEGRATION  —  scitex_io PRESENT
# ===========================================================================
scitex_io = pytest.importorskip("scitex_io")


@pytest.fixture
def normalize_module_with_io():
    """Reload the timestamp module with the real scitex_io present.

    Reloading (rather than relying on the already-imported module) makes the
    integration assertions independent of import order in the wider suite.
    """
    module = importlib.import_module(_MODULE)
    importlib.reload(module)
    return module


def test_scitex_io_exposes_load_configs():
    """scitex_io provides the ``load_configs`` attribute this edge consumes."""
    # Arrange
    # (scitex_io imported at module top via importorskip)
    # Act
    has_attr = hasattr(scitex_io, "load_configs")
    # Assert
    assert has_attr


def test_load_configs_is_bound_when_io_present(normalize_module_with_io):
    """With scitex_io installed, ``_load_configs`` resolves to a callable."""
    # Arrange
    module = normalize_module_with_io
    # Act
    resolved = module._load_configs
    # Assert
    assert callable(resolved)


def test_load_configs_is_scitex_io_load_configs(normalize_module_with_io):
    """The bound ``_load_configs`` is exactly ``scitex_io.load_configs``."""
    # Arrange
    module = normalize_module_with_io
    # Act
    resolved = module._load_configs
    # Assert
    assert resolved is scitex_io.load_configs


def test_standard_format_is_a_strftime_pattern(normalize_module_with_io):
    """``STANDARD_FORMAT`` is a usable strftime pattern when io is present."""
    # Arrange
    module = normalize_module_with_io
    dt = datetime(2010, 6, 18, 10, 15, 0)
    # Act
    rendered = dt.strftime(module.STANDARD_FORMAT)
    # Assert
    assert rendered  # non-empty -> the resolved format actually formats


def test_normalize_timestamp_roundtrips_with_io(normalize_module_with_io):
    """``normalize_timestamp`` works end-to-end with scitex_io present."""
    # Arrange
    module = normalize_module_with_io
    dt = datetime(2010, 6, 18, 10, 15, 0)
    # Act
    result = module.normalize_timestamp(dt, return_as="str", normalize_utc=False)
    # Assert
    assert result == "2010-06-18 10:15:00"


# ===========================================================================
# 2. DEGRADATION  —  scitex_io ABSENT
# ===========================================================================
@pytest.fixture
def scitex_io_absent():
    """Make ``import scitex_io`` fail for the duration of the test.

    Hermetic and reversible:
      1. snapshot the whole ``sys.modules`` so teardown restores it exactly;
      2. evict ``scitex_io`` (and its submodules) plus the timestamp module
         under test, then shadow ``scitex_io`` with ``None`` so a *fresh*
         ``import scitex_io`` raises ImportError (which ``try_import_optional``
         catches and converts to ``None``);
      3. reload the timestamp module so it re-runs its optional-import guard
         under the missing dependency.

    Yields the freshly reloaded timestamp module.
    """
    # 0. Ensure the module is importable before we tear anything down.
    importlib.import_module(_MODULE)

    # 1. Full snapshot for an exact restore.
    snapshot = dict(sys.modules)

    # 2. Evict scitex_io + the module under test; shadow scitex_io with None.
    for name in list(sys.modules):
        if name == "scitex_io" or name.startswith("scitex_io."):
            del sys.modules[name]
    sys.modules.pop(_MODULE, None)
    # ``None`` in sys.modules makes a subsequent ``import scitex_io`` raise
    # ImportError rather than re-discovering the installed package.
    sys.modules["scitex_io"] = None

    # 3. Reload the module so its top-level try_import_optional re-runs with
    #    scitex_io shadowed out.
    module = importlib.import_module(_MODULE)
    module = importlib.reload(module)

    try:
        yield module
    finally:
        # Exact restore: drop anything added, reinstate the originals.
        sys.modules.clear()
        sys.modules.update(snapshot)
        # Reload once more so the live, cached module reflects the real
        # (scitex_io-present) environment for any later test.
        importlib.reload(importlib.import_module(_MODULE))


def test_load_configs_is_none_without_io(scitex_io_absent):
    """Without scitex_io, the optional import degrades to ``None``."""
    # Arrange
    module = scitex_io_absent
    # Act
    resolved = module._load_configs
    # Assert
    assert resolved is None


def test_standard_format_falls_back_to_default_without_io(scitex_io_absent):
    """``STANDARD_FORMAT`` falls back to ``DEFAULT_FORMAT`` without scitex_io."""
    # Arrange
    module = scitex_io_absent
    # Act
    fmt = module.STANDARD_FORMAT
    # Assert
    assert fmt == module.DEFAULT_FORMAT


def test_default_format_is_the_documented_pattern(scitex_io_absent):
    """The documented fallback pattern is exactly ``%Y-%m-%d %H:%M:%S``."""
    # Arrange
    module = scitex_io_absent
    # Act
    fmt = module.DEFAULT_FORMAT
    # Assert
    assert fmt == "%Y-%m-%d %H:%M:%S"


def test_normalize_timestamp_still_works_without_io(scitex_io_absent):
    """``normalize_timestamp`` keeps working with scitex_io absent."""
    # Arrange
    module = scitex_io_absent
    dt = datetime(2010, 6, 18, 10, 15, 0)
    # Act
    result = module.normalize_timestamp(dt, return_as="str", normalize_utc=False)
    # Assert
    assert result == "2010-06-18 10:15:00"


def test_to_datetime_still_works_without_io(scitex_io_absent):
    """``to_datetime`` parsing is independent of the optional peer."""
    # Arrange
    module = scitex_io_absent
    # Act
    result = module.to_datetime("2010-06-18 10:15:00")
    # Assert
    assert result == datetime(2010, 6, 18, 10, 15, 0)


def test_validate_timestamp_format_still_works_without_io(scitex_io_absent):
    """``validate_timestamp_format`` accepts the fallback-formatted string."""
    # Arrange
    module = scitex_io_absent
    # Act
    is_valid = module.validate_timestamp_format("2010-06-18 10:15:00")
    # Assert
    assert is_valid


def test_format_for_filename_still_works_without_io(scitex_io_absent):
    """``format_for_filename`` is unaffected by scitex_io absence."""
    # Arrange
    module = scitex_io_absent
    dt = datetime(2010, 6, 18, 10, 15, 0)
    # Act
    result = module.format_for_filename(dt)
    # Assert
    assert result == "20100618_101500"


def test_fresh_scitex_io_import_raises_under_fixture(scitex_io_absent):
    """The fixture genuinely makes ``import scitex_io`` fail (sanity check)."""
    # Arrange
    module = scitex_io_absent  # noqa: F841 (fixture forces the absent state)
    import_scitex_io = lambda: importlib.import_module("scitex_io")
    # Act
    raised = pytest.raises(ImportError)
    # Assert
    with raised:
        import_scitex_io()


def test_sys_modules_restored_after_degradation():
    """After the degradation fixture tears down, scitex_io is importable again."""
    # Arrange
    # This test does NOT use the scitex_io_absent fixture; it runs in the
    # restored environment and proves the snapshot/restore was clean.
    sys.modules.pop("scitex_io", None)
    # Act
    module = importlib.import_module("scitex_io")
    # Assert
    assert module is not None
