import os
import json
from modules.scoreProcessor import ScoreProcessor
from utils.loggerUtil import getLogger

logger = getLogger("app")

def main():
    base_path = r"C:\office\belden"
    output_path = r"C:\office\TASK1\dbScores.json"

    processor = ScoreProcessor()
    final_scores = {}

    if not os.path.exists(base_path):
        logger.error(f"Base directory does not exist: {base_path}")
        return

    for schema in os.listdir(base_path):
        schema_path = os.path.join(base_path, schema, "Scoring")
        if not os.path.isdir(schema_path):
            logger.warning(f"No 'Scoring' folder found in schema: {schema}")
            continue

        table_scores = {}

        # Clean column mapping
        score_column_map = {
            "accuracy scoring": "Record_Score",
            "completeness": "Complete_Score",
            "data formating": "DF_Score",
            "data quality": "DQ_Score",
            "uniqueness scoring": "Uniqueness Score"
        }

        for score_type in os.listdir(schema_path):
            score_path = os.path.join(schema_path, score_type)
            score_key = score_type.lower()

            if not os.path.isdir(score_path):
                continue

            column_name = score_column_map.get(score_key)
            if not column_name:
                logger.warning(f"No column mapping found for: {score_type}")
                continue

            logger.info(f"Processing: {schema} -> {score_type}")
            scores = processor.process_table_scores(schema, score_path, column_name)
            if scores:
                table_scores[score_key] = scores

        schema_avg, table_count = processor.average_schema_scores(table_scores)

        if schema_avg:
            final_scores[schema] = {
                "Scores": schema_avg,
                "Summary": {"Table Count": table_count}
            }

    if final_scores:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(final_scores, f, indent=4)
            logger.info(f"Scoring JSON generated successfully at {output_path}")
        except Exception as e:
            logger.error(f"Failed to write JSON file: {str(e)}")
    else:
        logger.warning("No valid scores processed. JSON file was not created.")

if __name__ == "__main__":
    main()
