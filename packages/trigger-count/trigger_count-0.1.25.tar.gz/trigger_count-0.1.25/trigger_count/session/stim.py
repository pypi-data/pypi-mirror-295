"""
Find stimulus info for each imaging frame.
"""
import multiprocessing
import time

import numpy as np
import pandas as pd
from tqdm import tqdm


DEFAULT_COLUMNS = ["i_flip", "i_epoch", "epoch_name"]


class StimProcessor:
    """Class to add stimulus info to imaging frame info."""
    def __init__(self, frame_info: pd.DataFrame, flip_info: pd.DataFrame, imaging_trigger: str, extra_columns: list | None = None) -> None:
        # params
        self.frame_info = frame_info
        self.flip_info = flip_info
        self.imaging_trigger = imaging_trigger
        self.extra_columns = extra_columns

        # go
        self.columns_to_extract = []
        self.trigger_col = None

    def run(self) -> pd.DataFrame:
        """Main method to call."""
        self.determine_stim_cols_to_extract()
        self.trigger_col = self.determine_trigger_col()
        stim_info = self.get_stim_info_per_frame()
        frame_info = pd.concat([self.frame_info, stim_info], axis=1)
        frame_info = frame_info.reset_index(drop=True)
        frame_info = frame_info.rename(columns={"i_flip": "i_stim_flip"})
        return frame_info

    def determine_trigger_col(self) -> str:
        """
        Determine trigger column in stimulus info.
        This column represents the current imaging trigger count.
        """
        if "counter" in self.flip_info.columns:
            trigger_col = "counter"
        elif "daq_count" in self.flip_info.columns:
            trigger_col = "daq_count"
        else:
            raise ValueError(f"Cannot determine trigger column in flip info.")
        print(f"Trigger col in flip info: {trigger_col}")
        return trigger_col

    def determine_stim_cols_to_extract(self) -> None:
        if isinstance(self.extra_columns, list):
            self.columns_to_extract = [*DEFAULT_COLUMNS, *self.extra_columns]
        else:
            self.columns_to_extract = DEFAULT_COLUMNS

    def get_stim_info_per_frame(self, use_multiprocessing: bool = True) -> pd.DataFrame:
        """
        Get stimulus info for each imaging frame.
        For long sessions, this may take over 1 min, therefore use multiprocessing.
        """
        print("Extracting stim info for each imaging frame.")
        self.assert_columns()
        t_start = time.time()
        if use_multiprocessing:
            print("Using multiprocessing.")
            pool = multiprocessing.Pool(6)
            rows = [x[1] for x in self.frame_info.iterrows()]
            stim_info = pool.map(self._get_stim_for_single_frame, rows)
            pool.close()
        else:
            stim_info = []
            n_total = self.frame_info.shape[0]
            for i_frame, frame_details in tqdm(self.frame_info.iterrows(), total=n_total):
                stim_details = self._get_stim_for_single_frame(frame_details)
                stim_info.append(stim_details)
        stim_info = pd.DataFrame(stim_info)
        stim_info = stim_info.sort_values(by=self.imaging_trigger).reset_index(drop=True)
        del stim_info[self.imaging_trigger]
        elapsed = time.time() - t_start
        print(f"Extracting stim info took {elapsed:.2f}s")
        return stim_info

    def assert_columns(self) -> None:
        for col in self.columns_to_extract:
            assert col in self.flip_info.columns, f"{col=} not in flip info."

    def _get_stim_for_single_frame(self, *args) -> dict:
        """Get stimulus info for a single imaging frame."""
        frame_details = args[0]
        i_frame = frame_details[self.imaging_trigger]
        trigger_count = i_frame + 1
        if trigger_count % 10000 == 0:
            print(f"\tFrame {trigger_count:,}")
        is_trigger = self.flip_info[self.trigger_col] == trigger_count
        stim_details = dict()
        stim_details["n_stim_flips"] = np.sum(is_trigger)
        stim_details[self.imaging_trigger] = i_frame
        if np.any(is_trigger):
            for col in self.columns_to_extract:
                stim_details[col] = self.flip_info.loc[is_trigger, col].values[0]
        return stim_details


