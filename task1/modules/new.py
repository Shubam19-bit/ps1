import os
import re
from utils.loggerUtil import getLogger

logger = getLogger("app")

def csvReader(file_path, score_name):
    values = []
    warned = False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            header_line = f.readline()
            if not header_line:
                logger.error(f"No header found in file: {file_path}")
                return None

            headers_raw = re.split(r",(?!(?:[^\"]*\"[^\"]*\")*[^\"]*$)", header_line.strip())
            headers = [h.strip().lower() for h in headers_raw]
            score_name_normalized = score_name.strip().lower()

            if score_name_normalized not in headers:
                logger.error(f"Score column '{score_name}' not found in {file_path}")
                logger.warning(f"Actual headers found: {headers_raw}")
                return None

            col_index = headers.index(score_name_normalized)

            for line_num, line in enumerate(f, start=2):
                line = line.strip()
                if not line:
                    continue

                row = re.split(r",(?!(?:[^\"]*\"[^\"]*\")*[^\"]*$)", line)
                if len(row) <= col_index:
                    logger.warning(f"Row too short or empty in {file_path} at line {line_num}: {row}")
                    continue

                cell = row[col_index].strip()
                if cell == "":
                    continue

                try:
                    value = float(cell)
                    values.append(value)
                except ValueError:
                    if not warned:
                        logger.warning(f"Non-numeric values encountered in {file_path}. Some rows skipped.")
                        warned = True
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
