
import csv
import os
import re
from utils.loggerUtil import getLogger

logger = getLogger("app")

def csvReader(file_path, score_name):
    values = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader, None)

            if not headers:
                logger.error(f"No header found in file: {file_path}")
                return None

            headers = [h.strip() for h in headers]
            if score_name not in headers:
                logger.error(f"Score column '{score_name}' not found in {file_path}")
                return None

            col_index = headers.index(score_name)

            for row in reader:
                if not row or len(row) <= col_index:
                    logger.warning(f"Row too short or empty in {file_path}: {row}")
                    continue

                cell = row[col_index].strip()

                # Skip blank cells silently
                if cell == "":
                    continue

                try:
                    value = float(cell)
                    values.append(value)
                except ValueError:
                    if not hasattr(csvReader, "_warned_files"):
                        csvReader._warned_files = set()
                    if file_path not in csvReader._warned_files:
                        logger.warning(f"Non-numeric values encountered in {file_path}. Some rows skipped.")
                        csvReader._warned_files.add(file_path)
                    continue

        if values:
            return sum(values) / len(values)
        else:
            logger.error(f"No valid numeric values found in file: {file_path}")
            return None

    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
    except Exception as e:
        logger.error(f"Error opening or processing file {file_path}: {str(e)}")

    return None


def read_uniqueness_score(csv_files):
    csv_scores = {}
    file_path = csv_files[0]

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            headers = file.readline().strip().split(',')

            if "Uniqueness Score" not in headers:
                logger.error(f"'Uniqueness Score' column not found in {file_path}")
                return csv_scores

            score_index = headers.index("Uniqueness Score")

            for line in file:
                row_values = re.split(r",(?!(?:[^\"']*[\"'][^\"']*[\"'])*[^\"']*$)", line.strip())

                if len(row_values) <= score_index:
                    logger.warning(f"Row too short in uniqueness file {file_path}: {line.strip()}")
                    continue

                try:
                    key = row_values[0].strip()
                    value = float(row_values[score_index])
                    csv_scores[key] = value
                except ValueError:
                    logger.warning(f"Ignoring non-numeric value in {file_path}: {row_values[score_index]}")
                    continue

    except Exception as e:
        logger.error(f"Failed to process uniqueness file {file_path}: {str(e)}")

    return csv_scores
