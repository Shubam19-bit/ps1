
import os
from utils.loggerUtil import getLogger

logger = getLogger("app")

def getCsvFiles(folder_path):
    csv_files = []

    if not os.path.exists(folder_path):
        logger.error(f"Score folder does not exist: {folder_path}")
        return csv_files

    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(".csv"):
                full_path = os.path.abspath(os.path.join(folder_path, filename))
                csv_files.append(full_path)
    except Exception as e:
        logger.error(f"Failed to list files in {folder_path}: {str(e)}")

    if not csv_files:
        logger.warning(f"No CSV files found in folder: {folder_path}")

    return csv_files
