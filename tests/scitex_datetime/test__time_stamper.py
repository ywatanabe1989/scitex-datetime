#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for scitex_datetime.TimeStamper."""
from __future__ import annotations

import time

import pandas as pd
import pytest

from scitex_datetime import TimeStamper


class TestTimeStamperBasics:
    def test_initial_state(self):
        ts = TimeStamper()
        assert ts.id == -1
        assert len(ts._df_record) == 0

    def test_call_returns_string(self):
        ts = TimeStamper()
        result = ts("first")
        assert isinstance(result, str)
        assert "first" in result

    def test_call_increments_id(self):
        ts = TimeStamper()
        ts("a")
        ts("b")
        ts("c")
        assert ts.id == 2

    def test_record_contents(self):
        ts = TimeStamper()
        ts("a")
        ts("b")
        rec = ts.record
        assert isinstance(rec, pd.DataFrame)
        assert len(rec) == 2
        assert list(rec.columns) == [
            "timestamp",
            "elapsed_since_start",
            "elapsed_since_prev",
            "comment",
        ]


class TestTimeStamperFormats:
    def test_simple_format(self, capsys):
        ts = TimeStamper(is_simple=True)
        out = ts("hello", verbose=True)
        assert "ID:" in out
        assert "hello" in out

    def test_detailed_format(self):
        ts = TimeStamper(is_simple=False)
        out = ts("hello")
        assert "Time" in out


class TestTimeStamperDelta:
    def test_delta_positive(self):
        ts = TimeStamper()
        ts("a")
        time.sleep(0.05)
        ts("b")
        d = ts.delta(1, 0)
        assert d > 0

    def test_delta_negative_index(self):
        ts = TimeStamper()
        ts("a")
        time.sleep(0.02)
        ts("b")
        # delta(-1, -2) == delta(1, 0)
        assert ts.delta(-1, -2) == ts.delta(1, 0)

    def test_delta_invalid_id_raises(self):
        ts = TimeStamper()
        ts("a")
        with pytest.raises(ValueError):
            ts.delta(5, 0)
