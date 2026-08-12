import os
from pathlib import Path
from datetime import datetime

from config.settings import RAW_PATH, PROCESSED_PATH


def _cleanup_files_by_date_pattern(directory, prefix, suffix, max_files=5, file_type_label="file"):
    dir_path = Path(directory)
    if not dir_path.exists():
        return

    matching_files = []

    for file_path in dir_path.glob(f"{prefix}*{suffix}"):
        filename = file_path.name
        if filename.startswith(prefix) and filename.endswith(suffix):
            date_str = filename[len(prefix):-len(suffix)]
            try:
                file_date = datetime.strptime(date_str, "%Y_%m_%d")
                matching_files.append((file_date, file_path))
            except ValueError:
                # Ignore files that do not strictly match the expected YYYY_MM_DD date format
                continue

    # Sort files by parsed date ascending (oldest first)
    matching_files.sort(key=lambda item: item[0])

    # Delete oldest files if total count exceeds max_files
    if len(matching_files) > max_files:
        files_to_delete = matching_files[:len(matching_files) - max_files]
        for _, file_path in files_to_delete:
            print(f"Removing old {file_type_label}: {file_path}")
            try:
                file_path.unlink()
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")


def cleanup_raw_files(max_files=5):
    _cleanup_files_by_date_pattern(
        directory=RAW_PATH,
        prefix="humana_",
        suffix=".json",
        max_files=max_files,
        file_type_label="raw file",
    )


def cleanup_processed_files(max_files=5):
    _cleanup_files_by_date_pattern(
        directory=PROCESSED_PATH,
        prefix="humana_financial_metrics_",
        suffix=".csv",
        max_files=max_files,
        file_type_label="processed file",
    )


def cleanup_old_files(max_files=5):
    cleanup_raw_files(max_files=max_files)
    cleanup_processed_files(max_files=max_files)


if __name__ == "__main__":
    cleanup_old_files()
