#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TimeStamper — pandas-backed stopwatch.

Ported from scitex-gen ``_legacy/_TimeStamper.py`` as part of the
scitex-gen full retirement wave. Each call records a timestamp,
elapsed-since-start, elapsed-since-prev, an optional comment, and the
formatted text string into an internal ``pandas.DataFrame``.
"""
from __future__ import annotations

import time

import pandas as pd


class TimeStamper:
    """Pandas-backed stopwatch / timestamp recorder.

    Functionality
    -------------
    - Generates timestamps with comments and tracks elapsed time.
    - Records timestamps in a DataFrame for analysis.
    - Calculates time differences between any two recorded stamps.

    Example
    -------
    >>> ts = TimeStamper(is_simple=True)
    >>> _ = ts("Starting process")  # doctest: +SKIP
    """

    def __init__(self, is_simple: bool = True) -> None:
        self.id: int = -1
        self.start_time: float = time.time()
        self._is_simple: bool = is_simple
        self._prev: float = self.start_time
        self._df_record: pd.DataFrame = pd.DataFrame(
            columns=[
                "timestamp",
                "elapsed_since_start",
                "elapsed_since_prev",
                "comment",
                "formatted_text",
            ]
        )

    def __call__(self, comment: str = "", verbose: bool = False) -> str:
        now: float = time.time()
        from_start: float = now - self.start_time
        from_prev: float = now - self._prev

        formatted_from_start: str = time.strftime(
            "%H:%M:%S", time.gmtime(from_start)
        )
        formatted_from_prev: str = time.strftime(
            "%H:%M:%S", time.gmtime(from_prev)
        )

        self.id += 1
        self._prev = now

        text: str = (
            f"ID:{self.id} | {formatted_from_start} {comment} | "
            if self._is_simple
            else (
                f"Time (id:{self.id}): total {formatted_from_start}, "
                f"prev {formatted_from_prev} [hh:mm:ss]: {comment}\n"
            )
        )

        self._df_record.loc[self.id] = [
            now,
            from_start,
            from_prev,
            comment,
            text,
        ]

        if verbose:
            print(text)
        return text

    @property
    def record(self) -> pd.DataFrame:
        """Recorded stamps without the ``formatted_text`` column."""
        return self._df_record[
            [
                "timestamp",
                "elapsed_since_start",
                "elapsed_since_prev",
                "comment",
            ]
        ]

    def delta(self, id1: int, id2: int) -> float:
        """Time difference (seconds) between two recorded stamps.

        Negative indices count from the end (Python list-style).
        """
        if id1 < 0:
            id1 = len(self._df_record) + id1
        if id2 < 0:
            id2 = len(self._df_record) + id2

        if not all(idx in self._df_record.index for idx in [id1, id2]):
            raise ValueError("Invalid timestamp ID(s)")

        return (
            self._df_record.loc[id1, "timestamp"]
            - self._df_record.loc[id2, "timestamp"]
        )
