
import os
from modules.csvReader import csvReader, read_uniqueness_score
from utils.loggerUtil import getLogger
from modules.fileHandler import getCsvFiles

class ScoreProcessor:
    def __init__(self):
        self.logger = getLogger("app")

    def process_table_scores(self, schema_name, score_path, score_name):
        csv_scores = {}
        csv_files = getCsvFiles(score_path)

        if not csv_files:
            self.logger.warning(f"No CSV files found in: {score_path}")
            return csv_scores

        if score_name == "uniqueness scoring":
            csv_scores = read_uniqueness_score(csv_files)
        else:
            for file_path in csv_files:
                key = os.path.basename(file_path)
                try:
                    avg = csvReader(file_path, score_name)
                    if avg is not None:
                        csv_scores[key] = avg
                except Exception as e:
                    self.logger.error(f"Error processing {file_path}: {str(e)}")
                    continue

        return csv_scores

    def average_schema_scores(self, table_scores):
        avg_scores = {}
        table_count = 0

        if not table_scores:
            return avg_scores, table_count

        all_scores = {}
        for score_type, score_dict in table_scores.items():
            for _, val in score_dict.items():
                if score_type not in all_scores:
                    all_scores[score_type] = []
                all_scores[score_type].append(val)

        for score_type, values in all_scores.items():
            if values:
                avg_scores[score_type] = sum(values) / len(values)

        table_count = max(len(score_dict) for score_dict in table_scores.values())
        return avg_scores, table_count
