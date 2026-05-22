#!/usr/bin/env python3
# Timestamp: "2026-05-23 (audit-cleanup)"
# File: tests/scitex_datetime/test__normalize_timestamp.py

"""Tests for `scitex_datetime` timestamp normalisation helpers.

Each test follows the SciTeX AAA pattern (`# Arrange`/`# Act`/`# Assert`
markers), has a descriptive name (≥3 word-tokens after `test_`), and
makes exactly one assertion — see `_skills/general/02_package_13_test-quality.md`.
No mocks anywhere: every input is a real datetime / str / number / etc.
"""

from datetime import datetime, timedelta, timezone

import pytest


# ---------------------------------------------------------------------------
# normalize_timestamp
# ---------------------------------------------------------------------------


class TestNormalizeTimestamp:
    """Behavioural tests for `normalize_timestamp`."""

    def test_normalize_datetime_returns_iso_string(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        dt = datetime(2010, 6, 18, 10, 15, 0)

        # Act
        result = normalize_timestamp(dt, return_as="str", normalize_utc=False)

        # Assert
        assert result == "2010-06-18 10:15:00"

    def test_normalize_naive_datetime_to_utc_aware(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        dt = datetime(2010, 6, 18, 10, 15, 0)

        # Act
        result = normalize_timestamp(dt, return_as="datetime", normalize_utc=True)

        # Assert
        assert result.tzinfo == timezone.utc

    def test_normalize_datetime_to_unix_timestamp(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        dt = datetime(2010, 6, 18, 10, 15, 0, tzinfo=timezone.utc)

        # Act
        result = normalize_timestamp(dt, return_as="timestamp")

        # Assert
        assert result == pytest.approx(dt.timestamp())

    def test_normalize_unix_timestamp_to_utc_datetime(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        unix_ts = 1276856100.0
        expected = datetime.fromtimestamp(unix_ts, tz=timezone.utc)

        # Act
        result = normalize_timestamp(unix_ts, return_as="datetime")

        # Assert
        assert result == expected

    def test_normalize_iso_string_to_datetime(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        ts_str = "2010-06-18T10:15:00"

        # Act
        result = normalize_timestamp(ts_str, return_as="datetime", normalize_utc=False)

        # Assert
        assert result == datetime(2010, 6, 18, 10, 15, 0)

    def test_normalize_string_preserves_microseconds(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        ts_str = "2010-06-18 10:15:00.123456"

        # Act
        result = normalize_timestamp(ts_str, return_as="datetime", normalize_utc=False)

        # Assert
        assert result.microsecond == 123456

    @pytest.mark.parametrize(
        "ts_str",
        [
            "2010-06-18 10:15:00",
            "2010/06/18 10:15:00",
            "18-06-2010 10:15:00",
            "18/06/2010 10:15:00",
        ],
    )
    def test_normalize_string_accepts_common_layouts(self, ts_str):
        # Arrange
        from scitex_datetime import normalize_timestamp

        # Act
        result = normalize_timestamp(ts_str, return_as="datetime", normalize_utc=False)

        # Assert
        assert isinstance(result, datetime)

    def test_normalize_without_utc_keeps_naive_tz(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        dt = datetime(2010, 6, 18, 10, 15, 0)

        # Act
        result = normalize_timestamp(dt, return_as="datetime", normalize_utc=False)

        # Assert
        assert result.tzinfo is None

    def test_normalize_aware_datetime_converts_to_utc_clock(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        # +05:00 zone at 10:15 should become 05:15 UTC.
        dt = datetime(2010, 6, 18, 10, 15, 0, tzinfo=timezone(timedelta(hours=5)))

        # Act
        result = normalize_timestamp(dt, return_as="datetime", normalize_utc=True)

        # Assert
        assert (result.tzinfo, result.hour) == (timezone.utc, 5)

    def test_normalize_invalid_return_as_raises_value_error(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        dt = datetime(2010, 6, 18, 10, 15, 0)

        # Act
        # Assert
        with pytest.raises(ValueError, match="return_as must be"):
            normalize_timestamp(dt, return_as="invalid")

    def test_normalize_int_unix_timestamp_returns_datetime(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        unix_ts = 1276856100

        # Act
        result = normalize_timestamp(unix_ts, return_as="datetime")

        # Assert
        assert isinstance(result, datetime)


# ---------------------------------------------------------------------------
# to_datetime
# ---------------------------------------------------------------------------


class TestToDatetime:
    """Behavioural tests for `to_datetime`."""

    def test_to_datetime_with_datetime_returns_same_object(self):
        # Arrange
        from scitex_datetime import to_datetime

        dt = datetime(2010, 6, 18, 10, 15, 0)

        # Act
        result = to_datetime(dt)

        # Assert
        assert result is dt

    def test_to_datetime_with_int_returns_utc_aware(self):
        # Arrange
        from scitex_datetime import to_datetime

        unix_ts = 1276856100
        expected = datetime.fromtimestamp(unix_ts, tz=timezone.utc)

        # Act
        result = to_datetime(unix_ts)

        # Assert
        assert result == expected

    def test_to_datetime_with_float_returns_utc_aware(self):
        # Arrange
        from scitex_datetime import to_datetime

        unix_ts = 1276856100.123456
        expected = datetime.fromtimestamp(unix_ts, tz=timezone.utc)

        # Act
        result = to_datetime(unix_ts)

        # Assert
        assert result == expected

    def test_to_datetime_with_iso_string_parses_fields(self):
        # Arrange
        from scitex_datetime import to_datetime

        ts_str = "2010-06-18T10:15:00"

        # Act
        result = to_datetime(ts_str)

        # Assert
        assert result == datetime(2010, 6, 18, 10, 15, 0)

    def test_to_datetime_with_standard_string_parses_fields(self):
        # Arrange
        from scitex_datetime import to_datetime

        ts_str = "2010-06-18 10:15:00"

        # Act
        result = to_datetime(ts_str)

        # Assert
        assert result == datetime(2010, 6, 18, 10, 15, 0)

    def test_to_datetime_truncates_nanosecond_to_microsecond(self):
        # Arrange
        from scitex_datetime import to_datetime

        ts_str = "2010-06-18 10:15:00.123456789"

        # Act
        result = to_datetime(ts_str)

        # Assert
        assert result.microsecond == 123456

    def test_to_datetime_unparseable_string_raises_value_error(self):
        # Arrange
        from scitex_datetime import to_datetime

        # Act
        # Assert
        with pytest.raises(ValueError, match="Could not parse timestamp string"):
            to_datetime("not-a-valid-timestamp")

    def test_to_datetime_unsupported_type_raises_type_error(self):
        # Arrange
        from scitex_datetime import to_datetime

        # Act
        # Assert
        with pytest.raises(TypeError, match="timestamp must be"):
            to_datetime([2010, 6, 18])

    @pytest.mark.parametrize(
        "ts_str, expected",
        [
            ("2010-06-18T10:15:00.123456", datetime(2010, 6, 18, 10, 15, 0, 123456)),
            ("2010/06/18 10:15:00", datetime(2010, 6, 18, 10, 15, 0)),
            ("18-06-2010 10:15:00", datetime(2010, 6, 18, 10, 15, 0)),
            ("18/06/2010 10:15:00", datetime(2010, 6, 18, 10, 15, 0)),
            ("18/06/2010, 10:15:00", datetime(2010, 6, 18, 10, 15, 0)),
            ("20100618 10:15:00", datetime(2010, 6, 18, 10, 15, 0)),
            ("2010-06-18_10:15:00", datetime(2010, 6, 18, 10, 15, 0)),
        ],
    )
    def test_to_datetime_alternative_format_parsed_correctly(self, ts_str, expected):
        # Arrange
        from scitex_datetime import to_datetime

        # Act
        result = to_datetime(ts_str)

        # Assert
        assert result == expected


# ---------------------------------------------------------------------------
# validate_timestamp_format
# ---------------------------------------------------------------------------


class TestValidateTimestampFormat:
    """Behavioural tests for `validate_timestamp_format`."""

    def test_validate_well_formed_standard_string_returns_true(self):
        # Arrange
        from scitex_datetime import STANDARD_FORMAT, validate_timestamp_format

        dt = datetime(2010, 6, 18, 10, 15, 0)
        ts_str = dt.strftime(STANDARD_FORMAT)

        # Act
        result = validate_timestamp_format(ts_str)

        # Assert
        assert result is True

    def test_validate_garbage_string_returns_false(self):
        # Arrange
        from scitex_datetime import validate_timestamp_format

        # Act
        result = validate_timestamp_format("not-a-timestamp")

        # Assert
        assert result is False

    def test_validate_iso_format_string_returns_false(self):
        # Arrange
        from scitex_datetime import validate_timestamp_format

        # ISO 8601 with `T` is not the STANDARD_FORMAT layout.
        # Act
        result = validate_timestamp_format("2010-06-18T10:15:00")

        # Assert
        assert result is False

    def test_validate_none_input_returns_false(self):
        # Arrange
        from scitex_datetime import validate_timestamp_format

        # Act
        result = validate_timestamp_format(None)

        # Assert
        assert result is False


# ---------------------------------------------------------------------------
# format_for_filename
# ---------------------------------------------------------------------------


class TestFormatForFilename:
    """Behavioural tests for `format_for_filename`."""

    def test_format_datetime_for_filename_returns_compact_string(self):
        # Arrange
        from scitex_datetime import format_for_filename

        dt = datetime(2010, 6, 18, 10, 15, 0)

        # Act
        result = format_for_filename(dt)

        # Assert
        assert result == "20100618_101500"

    def test_format_string_for_filename_returns_compact_string(self):
        # Arrange
        from scitex_datetime import format_for_filename

        ts_str = "2010-06-18 10:15:00"

        # Act
        result = format_for_filename(ts_str)

        # Assert
        assert result == "20100618_101500"

    def test_format_for_filename_contains_only_digit_underscore(self):
        # Arrange
        from scitex_datetime import format_for_filename

        dt = datetime(2010, 6, 18, 10, 15, 30)

        # Act
        result = format_for_filename(dt)

        # Assert
        assert all(c.isdigit() or c == "_" for c in result)


# ---------------------------------------------------------------------------
# format_for_display
# ---------------------------------------------------------------------------


class TestFormatForDisplay:
    """Behavioural tests for `format_for_display`."""

    def test_format_datetime_for_display_returns_readable(self):
        # Arrange
        from scitex_datetime import format_for_display

        dt = datetime(2010, 6, 18, 10, 15, 0)

        # Act
        result = format_for_display(dt)

        # Assert
        assert result == "2010-06-18 10:15:00"

    def test_format_slash_string_normalises_to_dash(self):
        # Arrange
        from scitex_datetime import format_for_display

        ts_str = "2010/06/18 10:15:00"

        # Act
        result = format_for_display(ts_str)

        # Assert
        assert result == "2010-06-18 10:15:00"

    def test_format_for_display_contains_space_and_separators(self):
        # Arrange
        from scitex_datetime import format_for_display

        dt = datetime(2010, 6, 18, 10, 15, 30)

        # Act
        result = format_for_display(dt)

        # Assert
        assert (" " in result, "-" in result, ":" in result) == (True, True, True)


# ---------------------------------------------------------------------------
# parse_patient_recording_start_format
# ---------------------------------------------------------------------------


class TestParsePatientRecordingStartFormat:
    """Behavioural tests for `parse_patient_recording_start_format`."""

    def test_parse_rec_start_returns_datetime_with_fields(self):
        # Arrange
        from scitex_datetime import parse_patient_recording_start_format

        ts_str = "10/06/2010, 07:40:34"

        # Act
        result = parse_patient_recording_start_format(ts_str)

        # Assert
        assert result == datetime(2010, 6, 10, 7, 40, 34)

    def test_parse_rec_start_wrong_format_raises_value_error(self):
        # Arrange
        from scitex_datetime import parse_patient_recording_start_format

        # Act
        # Assert
        with pytest.raises(ValueError):
            parse_patient_recording_start_format("2010-06-10 07:40:34")


# ---------------------------------------------------------------------------
# get_time_delta_seconds
# ---------------------------------------------------------------------------


class TestGetTimeDeltaSeconds:
    """Behavioural tests for `get_time_delta_seconds`."""

    def test_get_delta_positive_difference_returns_seconds(self):
        # Arrange
        from scitex_datetime import get_time_delta_seconds

        start = datetime(2010, 6, 18, 10, 0, 0)
        end = datetime(2010, 6, 18, 10, 1, 0)

        # Act
        result = get_time_delta_seconds(start, end)

        # Assert
        assert result == 60.0

    def test_get_delta_end_before_start_returns_negative(self):
        # Arrange
        from scitex_datetime import get_time_delta_seconds

        start = datetime(2010, 6, 18, 10, 1, 0)
        end = datetime(2010, 6, 18, 10, 0, 0)

        # Act
        result = get_time_delta_seconds(start, end)

        # Assert
        assert result == -60.0

    def test_get_delta_with_string_inputs_returns_seconds(self):
        # Arrange
        from scitex_datetime import get_time_delta_seconds

        start = "2010-06-18 10:00:00"
        end = "2010-06-18 10:01:00"

        # Act
        result = get_time_delta_seconds(start, end)

        # Assert
        assert result == 60.0

    def test_get_delta_mixed_string_and_datetime_inputs(self):
        # Arrange
        from scitex_datetime import get_time_delta_seconds

        start = datetime(2010, 6, 18, 10, 0, 0)
        end = "2010-06-18 11:00:00"

        # Act
        result = get_time_delta_seconds(start, end)

        # Assert
        assert result == 3600.0

    def test_get_delta_same_instant_returns_zero(self):
        # Arrange
        from scitex_datetime import get_time_delta_seconds

        dt = datetime(2010, 6, 18, 10, 0, 0)

        # Act
        result = get_time_delta_seconds(dt, dt)

        # Assert
        assert result == 0.0

    def test_get_delta_year_long_difference_is_about_31_536_000s(self):
        # Arrange
        from scitex_datetime import get_time_delta_seconds

        start = datetime(2010, 1, 1, 0, 0, 0)
        end = datetime(2011, 1, 1, 0, 0, 0)

        # Act
        result = get_time_delta_seconds(start, end)

        # Assert
        assert result == pytest.approx(365 * 24 * 60 * 60, rel=0.01)

    def test_get_delta_microsecond_precision_preserved(self):
        # Arrange
        from scitex_datetime import get_time_delta_seconds

        start = datetime(2010, 6, 18, 10, 0, 0, 0)
        end = datetime(2010, 6, 18, 10, 0, 0, 500000)

        # Act
        result = get_time_delta_seconds(start, end)

        # Assert
        assert result == 0.5


# ---------------------------------------------------------------------------
# Module constants
# ---------------------------------------------------------------------------


class TestConstants:
    """Behavioural tests for module constants."""

    def test_standard_format_is_strftime_compatible_string(self):
        # Arrange
        from scitex_datetime import STANDARD_FORMAT

        # Act
        result = (isinstance(STANDARD_FORMAT, str), "%" in STANDARD_FORMAT)

        # Assert
        assert result == (True, True)

    def test_alternative_formats_is_nonempty_list_of_strings(self):
        # Arrange
        from scitex_datetime import ALTERNATIVE_FORMATS

        # Act
        ok = (
            isinstance(ALTERNATIVE_FORMATS, list)
            and len(ALTERNATIVE_FORMATS) > 0
            and all(isinstance(fmt, str) for fmt in ALTERNATIVE_FORMATS)
        )

        # Assert
        assert ok is True


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    """Edge cases / boundary conditions."""

    def test_to_datetime_unix_epoch_returns_1970_01_01(self):
        # Arrange
        from scitex_datetime import to_datetime

        # Act
        result = to_datetime(0)

        # Assert
        assert (result.year, result.month, result.day) == (1970, 1, 1)

    def test_to_datetime_large_unix_timestamp_returns_2100(self):
        # Arrange
        from scitex_datetime import to_datetime

        # Year 2100
        large_ts = 4102444800

        # Act
        result = to_datetime(large_ts)

        # Assert
        assert result.year == 2100

    def test_to_datetime_negative_unix_timestamp_returns_1969(self):
        # Arrange
        from scitex_datetime import to_datetime

        # 1 year before epoch.
        neg_ts = -31536000

        # Act
        result = to_datetime(neg_ts)

        # Assert
        assert result.year == 1969

    def test_normalize_preserves_microsecond_field(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        dt = datetime(2010, 6, 18, 10, 15, 0, 123456)

        # Act
        result = normalize_timestamp(dt, return_as="datetime", normalize_utc=False)

        # Assert
        assert result.microsecond == 123456

    def test_roundtrip_datetime_to_timestamp_to_datetime_preserves_clock(self):
        # Arrange
        from scitex_datetime import normalize_timestamp

        original = datetime(2010, 6, 18, 10, 15, 0, tzinfo=timezone.utc)
        ts = normalize_timestamp(original, return_as="timestamp")

        # Act
        result = normalize_timestamp(ts, return_as="datetime")

        # Assert
        assert (
            result.year,
            result.month,
            result.day,
            result.hour,
            result.minute,
        ) == (
            original.year,
            original.month,
            original.day,
            original.hour,
            original.minute,
        )


# --------------------------------------------------------------------------------

if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__)])

# EOF
