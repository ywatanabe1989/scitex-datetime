#!/usr/bin/env python3
# Timestamp: "2026-05-23 (audit-cleanup)"
# File: tests/scitex_datetime/test__linspace.py

"""Tests for `scitex_datetime.linspace`.

Each test follows the SciTeX AAA pattern (`# Arrange`/`# Act`/`# Assert`
markers on separate lines), has a descriptive name (>=3 word-tokens
after `test_`), and makes exactly one assertion. See
`_skills/general/02_package_13_test-quality.md`. No mocks anywhere —
linspace is a pure datetime helper.
"""

import datetime
from datetime import timedelta, timezone

import numpy as np
import pytest


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


class TestLinspaceHappyPath:
    """Behavioural tests for the common `linspace` shapes."""

    def test_linspace_n_samples_returns_ndarray_of_requested_length(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 0, 0, 10)

        # Act
        result = linspace(start, end, n_samples=11)

        # Assert
        assert (isinstance(result, np.ndarray), len(result), result[0], result[-1]) == (
            True,
            11,
            start,
            end,
        )

    def test_linspace_n_samples_yields_datetime_dtype_entries(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 0, 0, 10)

        # Act
        result = linspace(start, end, n_samples=11)

        # Assert
        assert all(isinstance(dt, datetime.datetime) for dt in result)

    def test_linspace_sampling_rate_returns_inclusive_endpoint_count(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 0, 0, 1)

        # Act
        # 10 Hz over 1 s should be 10 intervals + 1 endpoint = 11 samples.
        result = linspace(start, end, sampling_rate=10)

        # Assert
        assert (len(result), result[0], result[-1]) == (11, start, end)

    def test_linspace_produces_uniform_one_second_spacing(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 0, 1, 0)

        # Act
        result = linspace(start, end, n_samples=61)
        deltas = [
            (result[i + 1] - result[i]).total_seconds() for i in range(len(result) - 1)
        ]

        # Assert
        assert all(pytest.approx(d, rel=1e-6) == 1.0 for d in deltas)


# ---------------------------------------------------------------------------
# Validation — parameter combinations
# ---------------------------------------------------------------------------


class TestLinspaceParameterValidation:
    """`linspace` rejects illegal parameter combinations."""

    def test_linspace_both_params_raises_value_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(
            ValueError,
            match="Provide either n_samples or sampling_rate, not both",
        ):
            linspace(start, end, n_samples=10, sampling_rate=1.0)

    def test_linspace_no_params_raises_value_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(
            ValueError,
            match="Either n_samples or sampling_rate must be provided",
        ):
            linspace(start, end)


# ---------------------------------------------------------------------------
# Validation — type checks (parametrised, one assert per row)
# ---------------------------------------------------------------------------


class TestLinspaceTypeChecks:
    """`linspace` rejects wrong-typed inputs with TypeError."""

    def test_linspace_string_start_raises_type_error(self):
        # Arrange
        from scitex_datetime import linspace

        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(TypeError, match="start_dt must be a datetime object"):
            linspace("2023-01-01", end, n_samples=10)

    def test_linspace_string_end_raises_type_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)

        # Act
        # Assert
        with pytest.raises(TypeError, match="end_dt must be a datetime object"):
            linspace(start, "2023-01-02", n_samples=10)

    def test_linspace_string_n_samples_raises_type_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(TypeError, match="n_samples must be a number"):
            linspace(start, end, n_samples="10")

    def test_linspace_string_sampling_rate_raises_type_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(TypeError, match="sampling_rate must be a number"):
            linspace(start, end, sampling_rate="10")


# ---------------------------------------------------------------------------
# Validation — value checks
# ---------------------------------------------------------------------------


class TestLinspaceValueChecks:
    """`linspace` rejects illegal datetime / sample-count values."""

    def test_linspace_start_after_end_raises_value_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(ValueError, match="start_dt must be earlier than end_dt"):
            linspace(end, start, n_samples=10)

    def test_linspace_start_equals_end_raises_value_error(self):
        # Arrange
        from scitex_datetime import linspace

        same = datetime.datetime(2023, 1, 1)

        # Act
        # Assert
        with pytest.raises(ValueError, match="start_dt must be earlier than end_dt"):
            linspace(same, same, n_samples=10)

    def test_linspace_negative_n_samples_raises_value_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(ValueError, match="n_samples must be positive"):
            linspace(start, end, n_samples=-1)

    def test_linspace_zero_n_samples_raises_value_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(ValueError, match="n_samples must be positive"):
            linspace(start, end, n_samples=0)

    def test_linspace_negative_sampling_rate_raises_value_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(ValueError, match="sampling_rate must be positive"):
            linspace(start, end, sampling_rate=-1.0)

    def test_linspace_zero_sampling_rate_raises_value_error(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # Assert
        with pytest.raises(ValueError, match="sampling_rate must be positive"):
            linspace(start, end, sampling_rate=0.0)


# ---------------------------------------------------------------------------
# Precision / range edge cases
# ---------------------------------------------------------------------------


class TestLinspacePrecisionAndRange:
    """`linspace` precision + range behaviour."""

    def test_linspace_microsecond_precision_step_is_one_millisecond(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 0, 0, 0, 10000)  # 10 ms

        # Act
        result = linspace(start, end, n_samples=11)

        # Assert
        assert [dt.microsecond for dt in result] == [i * 1000 for i in range(11)]

    def test_linspace_year_scale_endpoint_count_is_six(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2020, 1, 1)
        end = datetime.datetime(2025, 1, 1)

        # Act
        result = linspace(start, end, n_samples=6)

        # Assert
        assert (len(result), result[0], result[-1]) == (6, start, end)

    def test_linspace_year_scale_inter_sample_step_is_about_one_year(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2020, 1, 1)
        end = datetime.datetime(2025, 1, 1)

        # Act
        result = linspace(start, end, n_samples=6)
        deltas_days = [(result[i + 1] - result[i]).days for i in range(len(result) - 1)]

        # Assert
        assert all(364 <= d <= 366 for d in deltas_days)

    def test_linspace_one_microsecond_range_returns_two_endpoints(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 0, 0, 0, 1)

        # Act
        result = linspace(start, end, n_samples=2)

        # Assert
        assert (len(result), result[0], result[-1]) == (2, start, end)

    def test_linspace_dense_microsecond_grid_step_is_one(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 0, 0, 0, 100)

        # Act
        result = linspace(start, end, n_samples=101)

        # Assert
        assert [dt.microsecond for dt in result] == list(range(101))


# ---------------------------------------------------------------------------
# Sampling-rate parametrised checks
# ---------------------------------------------------------------------------


class TestLinspaceSamplingRate:
    """`linspace` sampling-rate -> sample-count math."""

    @pytest.mark.parametrize(
        "rate, expected_samples",
        [(100, 101), (256, 257), (512, 513), (1000, 1001)],
    )
    def test_linspace_one_second_at_rate_yields_rate_plus_one_samples(
        self, rate, expected_samples
    ):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 0, 0, 1)

        # Act
        result = linspace(start, end, sampling_rate=rate)

        # Assert
        assert len(result) == expected_samples

    @pytest.mark.parametrize(
        "duration_seconds, rate, expected_samples",
        [
            (1, 256, 1 * 256 + 1),
            (10, 100, 10 * 100 + 1),
            (0.5, 1000, int(0.5 * 1000) + 1),
            (60, 1, 60 * 1 + 1),
        ],
    )
    def test_linspace_duration_times_rate_plus_one_samples(
        self, duration_seconds, rate, expected_samples
    ):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0)
        end = start + timedelta(seconds=duration_seconds)

        # Act
        result = linspace(start, end, sampling_rate=rate)

        # Assert
        assert len(result) == expected_samples

    def test_linspace_step_matches_one_over_sampling_rate(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 0, 0, 1)
        rate = 256

        # Act
        result = linspace(start, end, sampling_rate=rate)
        delta = (result[1] - result[0]).total_seconds()

        # Assert
        assert pytest.approx(1.0 / rate, rel=1e-4) == delta


# ---------------------------------------------------------------------------
# Timezone / return type / edge sample counts
# ---------------------------------------------------------------------------


class TestLinspaceTimezoneAndReturnShape:
    """`linspace` timezone preservation and return-shape contract."""

    def test_linspace_preserves_utc_timezone_on_all_entries(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        end = datetime.datetime(2023, 1, 1, 1, 0, 0, tzinfo=timezone.utc)

        # Act
        result = linspace(start, end, n_samples=5)

        # Assert
        assert all(dt.tzinfo == timezone.utc for dt in result)

    def test_linspace_returns_object_dtype_ndarray_from_n_samples(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        result = linspace(start, end, n_samples=10)

        # Assert
        assert (isinstance(result, np.ndarray), result.dtype) == (True, np.dtype("O"))

    def test_linspace_returns_object_dtype_ndarray_from_sampling_rate(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        result = linspace(start, end, sampling_rate=1.0)

        # Assert
        assert (isinstance(result, np.ndarray), result.dtype) == (True, np.dtype("O"))

    def test_linspace_n_samples_equal_to_one_returns_only_start(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 1, 2)

        # Act
        # `np.linspace(0, d, 1)` returns just `[0]` -> only `start`.
        result = linspace(start, end, n_samples=1)

        # Assert
        assert (len(result), result[0]) == (1, start)


# ---------------------------------------------------------------------------
# Practical scenarios
# ---------------------------------------------------------------------------


class TestLinspacePracticalScenarios:
    """Practical-use checks (still single-assert per test)."""

    @pytest.mark.parametrize(
        "rate, duration_seconds",
        [(256, 10), (512, 10)],
    )
    def test_linspace_eeg_sampling_yields_expected_sample_count(
        self, rate, duration_seconds
    ):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 12, 0, 0)
        end = start + timedelta(seconds=duration_seconds)

        # Act
        timestamps = linspace(start, end, sampling_rate=rate)

        # Assert
        assert len(timestamps) == duration_seconds * rate + 1

    @pytest.mark.parametrize("rate", [256, 512])
    def test_linspace_eeg_inter_sample_step_matches_inverse_rate(self, rate):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 12, 0, 0)
        end = start + timedelta(seconds=10)
        expected_interval = 1.0 / rate

        # Act
        timestamps = linspace(start, end, sampling_rate=rate)
        first_interval = (timestamps[1] - timestamps[0]).total_seconds()

        # Assert
        assert pytest.approx(expected_interval, rel=1e-3) == first_interval

    def test_linspace_hourly_schedule_hours_are_zero_to_twenty_three(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 0, 0, 0)
        end = datetime.datetime(2023, 1, 1, 23, 0, 0)

        # Act
        hourly = linspace(start, end, n_samples=24)
        observed_hours = [ts.hour for ts in hourly]

        # Assert
        assert observed_hours == list(range(24))

    def test_linspace_five_minute_logging_intervals_are_five(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1, 9, 0, 0)
        end = datetime.datetime(2023, 1, 1, 10, 0, 0)

        # Act
        timestamps = linspace(start, end, n_samples=13)
        deltas_minutes = [
            (timestamps[i + 1] - timestamps[i]).total_seconds() / 60
            for i in range(len(timestamps) - 1)
        ]

        # Assert
        assert all(pytest.approx(d, rel=1e-6) == 5.0 for d in deltas_minutes)

    def test_linspace_million_samples_full_year_returns_million_entries(self):
        # Arrange
        from scitex_datetime import linspace

        start = datetime.datetime(2023, 1, 1)
        end = datetime.datetime(2023, 12, 31)

        # Act
        result = linspace(start, end, n_samples=1_000_000)

        # Assert
        assert (len(result), result[0], result[-1]) == (1_000_000, start, end)


# --------------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])

# EOF
