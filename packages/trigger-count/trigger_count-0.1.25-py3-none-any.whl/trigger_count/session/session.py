"""
Organize all triggers in one go.
"""
import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
import polars as pl

from trigger_count.files import get_n_frames_from_tif, find_csv_files, find_mp4_files, get_n_frames_from_mp4
from trigger_count.session.stim import StimProcessor
from trigger_count.session.quality import QualityChecker
from trigger_count.log import get_file_logger


# classes
class RecordingSession:
    """Class to process triggers of one recording session.
    """
    def __init__(
            self,
            source_folder: Path,
            stim_columns: list,
            require_flip: bool = True,
            require_daq: bool = True,
    ) -> None:
        # params
        self.source_folder = source_folder
        self.stim_columns = stim_columns
        self.require_flip = require_flip
        self.require_daq = require_daq

        # state
        self.daq_df: pl.DataFrame | None = None  # use polars to speed this up
        self.flip_info: pd.DataFrame | None = None
        self.vitals_df: pd.DataFrame | None = None

        self.imaging_type = None
        self.n_daq_samples = None
        self.n_stim_flips = None
        self.n_imaging_frames = None
        self.n_vitals_samples = None
        self.n_eyetracking_frames = None
        self.frame_info: pd.DataFrame | None = None
        self.imaging_trigger = None
        self.start_offsets = {}
        self.end_offsets = {}
        self.all_columns = None
        
        self.logger = get_file_logger("session", source_folder / "triggers.log")

        # go!
        self.check_folders()
        self.check_dtypes()

    def check_folders(self) -> None:
        if not self.source_folder.is_dir():
            raise FileNotFoundError(f"{self.source_folder}")
        self.check_stim_folder_name()
        self.check_2p_folder_name()

    def check_stim_folder_name(self) -> None:
        """
        Identify the folder with stim information.
        Rename to 'stim'.
        """
        target_folder = self.source_folder / "stim"
        if not target_folder.is_dir():
            for element in self.source_folder.iterdir():
                if element.is_dir():
                    flip_path = element / "flip_info.csv"
                    if flip_path.is_file():
                        print(f"{element} contains flip_info.csv")
                        source = element
                        target = element.parent / "stim"
                        os.rename(source, target)
                        self.logger.info(f"Renamed {source.name} to {target.name}")

    def check_2p_folder_name(self) -> None:
        target_folder = self.source_folder / "suite2p"
        if not target_folder.is_dir():
            for element in self.source_folder.iterdir():
                if element.is_dir():
                    f_path = element / "F.npy"
                    if f_path.is_file():
                        print(f"{element} contains flip_info.csv")
                        source = element
                        target = element.parent / "suite2p"
                        os.rename(source, target)
                        self.logger.info(f"Renamed {source.name} to {target.name}")

    def check_dtypes(self) -> None:
        """
        Check which dtypes are available:
        - stim
        - 2p
        - widefield
        - eyetracking (LE, RE)
        - vitals
        """
        self.check_2p_files()
        self.check_wf_files()
        self.assert_imaging()
        self.check_daq_files()
        self.check_stim_files()
        self.check_vitals_files()
        self.check_eyetracking_files()

    def check_2p_files(self) -> None:
        """Check what 2p related files exist."""
        suite2p_folder = self.source_folder / "suite2p"
        if suite2p_folder.is_dir():
            traces_file = suite2p_folder / "F.npy"
            if traces_file.is_file():
                traces = np.load(traces_file)
                self.n_imaging_frames = traces.shape[1]
                self.logger.info(f"Twophoton frames (suite2p): {self.n_imaging_frames:,}")
                self.imaging_type = "twophoton"

    def check_wf_files(self) -> None:
        """Check what widefield-related files exist."""
        widefield_file = self.source_folder / "dataset" / "recording.tif"
        if widefield_file.is_file():
            self.logger.info(f"Widefield data available: {widefield_file}")
            self.n_imaging_frames = get_n_frames_from_tif(widefield_file)
            self.logger.info(f"Widefield frames (TIFF): {self.n_imaging_frames:,}")
            self.imaging_type = "widefield"

    def assert_imaging(self) -> None:
        """Assert that we identified whether a session has 2p or WF imaging"""
        assert self.imaging_type is not None



    def check_stim_files(self) -> None:
        """Check whether a stimulus file exists."""
        stim_file = self.source_folder / "stim" / "flip_info.csv"
        if stim_file.is_file():
            self.flip_info = pd.read_csv(stim_file)
            self.n_stim_flips = self.flip_info.shape[0]
            self.logger.info(f"Stim screen flips: {self.n_stim_flips:,}")
        else:
            if self.require_flip:
                raise FileNotFoundError(f"{stim_file} does not exist.")

    def check_daq_files(self) -> None:
        """Check what stim-related files exist."""
        stim_folder = self.source_folder / "stim"
        possible_names = ["daq.csv", "labjack.csv"]

        daq_file = None
        if stim_folder.is_dir():
            for name in possible_names:
                daq_candidate = stim_folder / name
                if daq_candidate.is_file():
                    daq_file = daq_candidate
                    self.daq_df = pl.read_csv(daq_file)  # pd.read_csv(daq_file)
                    self.n_daq_samples = self.daq_df.shape[0]
                    self.logger.info(f"DAQ samples: {self.n_daq_samples:,}")
        if (daq_file is None) and self.require_daq:
            raise FileNotFoundError(f"No DAQ file found.")

    def check_vitals_files(self) -> None:
        """Check what vitals-related files exist."""
        vitals_folder = self.source_folder / "vitals"
        if vitals_folder.is_dir():
            csv_files = find_csv_files(vitals_folder)
            if len(csv_files) == 1:
                self.vitals_df = pd.read_csv(csv_files[0])
                self.n_vitals_samples = self.vitals_df.shape[0]
                self.logger.info(f"{self.n_vitals_samples:,} vitals samples")
            else:
                raise ValueError(f"{len(csv_files)} CSV files in vitals folder.")

    def check_eyetracking_files(self) -> None:
        """Check what eye tracking related files exist."""
        eyetracking_folder = self.source_folder / "eyetracking"
        if eyetracking_folder.is_dir():
            left_eye_folder = eyetracking_folder / "left_eye"
            right_eye_folder = eyetracking_folder / "right_eye"
            self.n_eyetracking_frames = {}
            for name, folder in {"left": left_eye_folder, "right": right_eye_folder}.items():
                mp4_file = find_mp4_files(folder)
                if len(mp4_file) == 1:
                    mp4_file = mp4_file[0]
                    n_frames = get_n_frames_from_mp4(mp4_file)
                    self.n_eyetracking_frames[name] = n_frames
                    self.logger.info(f"{name.capitalize()} eye tracking frames: {n_frames:,}")
                else:
                    raise ValueError(f"{len(mp4_file)} mp4 files in {folder}")

    def make_frame_info(self, overwrite: bool = False) -> pd.DataFrame:
        """
        Main method to call.
        Creates a table with info for each 2p or WF frame.
        """
        frame_info_file = self.source_folder / "dataset" / "frame_info.csv"
        if frame_info_file.is_file() and not overwrite:
            raise FileExistsError(f"Frame info file already exists: {frame_info_file}")
        else:
            if isinstance(self.daq_df, (pd.DataFrame, pl.DataFrame)):
                self.make_frame_info_from_daq()
            else:
                self.logger.info("No DAQ file - is this an older session?")
                raise NotImplementedError()
        if self.n_stim_flips:
            self.add_stim_info()
        if self.n_eyetracking_frames:
            self.add_eye_tracking_triggers()
        self.apply_trigger_offsets()
        # self.add_elapsed()
        self.print_summary()
        return self.frame_info

    def make_frame_info_from_daq(self) -> None:
        """
        Get table with one row per imaging frame by subsampling DAQ file.
        TODO: fill in missing intermediates so that table always has as many rows as there are imaging frames.
        """
        if self.imaging_type == "twophoton":
            self.imaging_trigger = "twophoton_scanner"
        elif self.imaging_type == "widefield":
            self.imaging_trigger = "widefield_camera"
        subsampled = self.subsample_daq(self.imaging_trigger)
        self.quality_check(subsampled, self.imaging_trigger)
        frame_info = dict()
        frame_info["datetime"] = subsampled["datetime"]
        frame_info[f"i_{self.imaging_type}_frame"] = subsampled[self.imaging_trigger] - 1
        frame_info[f"{self.imaging_type}_frame_interval"] = subsampled[f"interval_{self.imaging_trigger}"]
        frame_info = pd.DataFrame(frame_info)
        self.frame_info = frame_info

    def subsample_daq(self, trigger_source: str) -> pl.DataFrame:
        """Subsample DAQ file to only rows where a new trigger was received."""
        column = f"interval_{trigger_source}"
        if column not in self.daq_df.columns:
            self.logger.info("DAQ table columns:")
            for col in self.daq_df.columns:
                self.logger.info(f"\t{col}")
            raise KeyError(f"{column=} not in DAQ table.")
        is_selected = self.daq_df[column].is_not_null()
        subset = self.daq_df.filter(is_selected)
        n_triggers = subset.shape[0]
        self.logger.info(f"{trigger_source}: {n_triggers:,} triggers")
        subset = subset.to_pandas()
        return subset

    def quality_check(self, triggers: pd.DataFrame, trigger_source: str) -> None:
        """Check whether a certain trigger source has consistent trigger intervals."""
        checker = QualityChecker(triggers, trigger_source)
        checker.run()
        self.start_offsets[trigger_source] = checker.start_offsets[trigger_source]

    def add_stim_info(self) -> None:
        """
        Add stimulus info to info per imaging frame.
        This step takes the most time.
        """
        processor = StimProcessor(
            frame_info=self.frame_info,
            flip_info=self.flip_info,
            imaging_trigger=f"i_{self.imaging_type}_frame",
            extra_columns=self.stim_columns,
        )
        self.frame_info = processor.run()

    def add_eye_tracking_triggers(self) -> None:
        """Add eye tracking info to frame info."""
        for eye in ["left", "right"]:
            trigger_source = f"{eye}_eye_camera"
            subset = self.subsample_daq(trigger_source)
            self.quality_check(subset, trigger_source)
            subset = self.subsample_daq(self.imaging_trigger)
            self.frame_info[f"i_{eye}_eye_frame"] = subset[trigger_source] - 1

    def apply_trigger_offsets(self) -> None:
        """To account for extra triggers at start, subtract possible offsets."""
        self.logger.info("---Applying imaging offsets---")
        for trigger_source, start_offset in self.start_offsets.items():
            if start_offset != 0:
                if trigger_source == self.imaging_trigger:
                    self.logger.info(f"{trigger_source}: Subtracting {start_offset} triggers.")
                    col = f"i_{self.imaging_type}_frame"
                    self.frame_info[col] = self.frame_info[col] - start_offset
                    is_negative = self.frame_info[col] < 0
                    if np.any(is_negative):
                        n_removed = np.sum(is_negative)
                        self.logger.info(f"Removing {n_removed} rows from frame info")
                        is_positive = self.frame_info[col] >= 0
                        self.frame_info = self.frame_info.loc[is_positive].reset_index(drop=True)
                else:
                    if trigger_source == "left_eye_camera":
                        col = "i_left_eye_frame"
                    elif trigger_source == "right_eye_camera":
                        col = "i_right_eye_frame"
                    else:
                        raise ValueError(f"{trigger_source}")
                    self.frame_info[col] = self.frame_info[col] - start_offset

    def add_elapsed(self) -> None:
        """Compute frame interval."""
        timestamps = pd.to_datetime(self.frame_info["datetime"], format="%Y-%m-%d %H:%M:%S.%f")
        relative_time = timestamps - timestamps.min()
        relative_time = [x.total_seconds() for x in relative_time]
        self.frame_info["elapsed"] = relative_time

    def print_summary(self) -> None:
        i_last = self.frame_info[f"i_{self.imaging_type}_frame"].max()
        max_count = i_last + 1
        n_rows = self.frame_info.shape[0]
        self.logger.info(f"Imaging frames (max count): {max_count:,}")
        self.logger.info(f"Rows in table: {n_rows:,}")
