"""
Basic file functions.
"""
import cv2
import tkinter as tk
from pathlib import Path
from tkinter import filedialog

import tifffile


def ask_for_folder_path(base_folder: Path | None = None) -> Path:
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(initialdir=base_folder)
    folder_path = Path(folder_path)
    root.destroy()  # Destroy the root window after getting the folder path
    if not folder_path.is_dir():
        raise FileNotFoundError(f"{folder_path}")
    return folder_path


def find_mp4_files(some_folder: Path) -> list:
    """Find .mp4 files in a folder."""
    mp4_files = []
    for element in some_folder.iterdir():
        if element.suffix == ".mp4":
            mp4_files.append(element)
    return mp4_files


def find_csv_files(some_folder: Path) -> list:
    """List .csv files in a folder."""
    csv_files = []
    for element in some_folder.iterdir():
        if element.suffix == ".csv":
            csv_files.append(element)
    return csv_files


def get_n_frames_from_mp4(file_path: Path) -> int:
    """Get number of frames from a .mp4 file without loading file into memory."""
    cap = cv2.VideoCapture(str(file_path))
    if not cap.isOpened():
        raise IOError(f"Unable to open video file {file_path}.")

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    cap.release()  # Release the video capture object
    return total_frames


def get_n_frames_from_tif(file_path: Path) -> int:
    """Get number of frames of a .tif without loading file into memory."""
    file = tifffile.TiffFile(file_path)
    n_frames = len(file.pages)
    if n_frames == 1:
        n_frames = file.imagej_metadata["images"]
    return n_frames
