"""
Check a stream of triggers for irregularities.
"""

import pandas as pd
import numpy as np


class QualityChecker:
    """Check quality of triggers"""

    def __init__(self, triggers: pd.DataFrame, trigger_source: str) -> None:
        self.triggers = triggers
        self.trigger_source = trigger_source
        self.start_offsets = {}

    def run(self) -> None:
        print(f"---Quality check: {self.trigger_source}---")
        self.print_first_last_triggers()
        self.print_slowest_fastest_triggers()
        self.check_missing_intermediates()
        self.check_outliers()

    def print_first_last_triggers(self) -> None:
        """Print the first and last trigger intervals."""
        for ascending in [True, False]:
            prefix = "first" if ascending else "last"
            print(f"{prefix.capitalize()} triggers")
            sorted_df = self.triggers.sort_values(by="count", ascending=ascending)
            sorted_df = sorted_df.reset_index(drop=True)
            for i_row, row in sorted_df.iterrows():
                if i_row == 5:
                    break
                frame_interval = row[f"interval_{self.trigger_source}"]
                frame_interval = float(frame_interval)
                print(f"\t({i_row}) {self.trigger_source}: {row[self.trigger_source]:,} -> {frame_interval * 1000:.1f} ms")

    def print_slowest_fastest_triggers(self) -> None:
        """Print the slowest and fastest trigger intervals."""
        for ascending in [True, False]:
            prefix = "fastest" if ascending else "slowest"
            print(f"{prefix.capitalize()} trigger intervals")
            sorted_df = self.triggers.sort_values(by=f"interval_{self.trigger_source}", ascending=ascending)
            sorted_df = sorted_df.reset_index(drop=True)
            for i_row, row in sorted_df.iterrows():
                if i_row == 5:
                    break
                frame_interval = row[f"interval_{self.trigger_source}"]
                frame_interval = float(frame_interval)
                print(f"\t({i_row}) {self.trigger_source}: {row[self.trigger_source]:,} -> {frame_interval * 1000:.1f} ms")

    def check_outliers(self, threshold: float = 10) -> None:
        """Z-score trigger intervals to check for irregularieties."""
        intervals = self.triggers[f"interval_{self.trigger_source}"].values.astype(float)
        zscores = self.zscore_with_median(intervals)
        is_deviant = np.abs(zscores) > threshold
        n_deviant = np.sum(is_deviant)
        print(f"{n_deviant} outliers")
        for i_row, row in self.triggers.loc[is_deviant].iterrows():
            frame_interval = row[f"interval_{self.trigger_source}"]
            frame_interval = float(frame_interval)
            z = zscores[i_row]
            print(f"\t({i_row}) {self.trigger_source}: {row[self.trigger_source]:,} -> {frame_interval * 1000:.1f} ms ({z=:.1f})")
        start_offset, end_offset = self.determine_offsets(zscores)
        self.start_offsets[self.trigger_source] = start_offset

    @staticmethod
    def zscore_with_median(some_values: np.ndarray) -> np.ndarray:
        """
        Z-score a series of values with median.
        Take median and median absolute deviation instead of mean and standard deviation.
        """
        median_val = np.median(some_values)
        # print(f"Median: {median_val * 1000:.1f} ms")
        deviations = some_values - median_val
        absolute_deviations = np.abs(deviations)
        median_deviation = np.median(absolute_deviations)
        # print(f"Median deviation: {median_deviation * 1000:.1f} ms")
        z_values = (some_values - median_val) / median_deviation
        return z_values

    def check_missing_intermediates(self) -> None:
        """Check whether intermediate triggers were missed by the computer (but not the labjack)."""
        numbers = self.triggers[self.trigger_source].values
        min_val = np.min(numbers)
        max_val = np.max(numbers)
        all_possible = np.arange(min_val, max_val)
        is_there = np.isin(all_possible, numbers)
        is_missing = np.logical_not(is_there)
        n_missing = np.sum(is_missing)
        print(f"{n_missing} missed intermediate triggers.")

        if np.any(is_missing):
            missing_vals = all_possible[is_missing]
            for missed in missing_vals:
                is_before = self.triggers[self.trigger_source] == (missed - 1)
                is_after = self.triggers[self.trigger_source] == (missed + 1)
                if np.sum(is_before):
                    previous_interval = self.triggers.loc[is_before, f"interval_{self.trigger_source}"].values[0]
                    previous_interval = float(previous_interval)
                    previous_str = f"{previous_interval * 1000:.1f} ms"
                else:
                    previous_str = "also_missed"
                if np.sum(is_after):
                    following_interval = self.triggers.loc[is_after, f"interval_{self.trigger_source}"].values[0]
                    following_interval = float(following_interval)
                    following_str = f"{following_interval * 1000:.1f} ms"
                else:
                    following_str = "also_missed"
                print(f"\t {missed:,} (previous: {previous_str:}, following: {following_str:})")

    @staticmethod
    def determine_offsets(zscores: np.ndarray, threshold: float = 10) -> tuple:
        """
        Determine how many extra triggers could have occurred at the start or end of a recording.
        Somtimes, components can send extra triggers when turned on or off.
        These are detectable by having noticeably longer or shorter intervals to regular triggers.
        """
        start_offset = 0
        for i, z in enumerate(zscores):
            if i == 5:
                break
            if z > threshold:
                start_offset += 1

        end_offset = 0
        for i, z in enumerate(zscores[::-1]):
            if i == 5:
                break
            if z > threshold:
                end_offset += 1
        return start_offset, end_offset

