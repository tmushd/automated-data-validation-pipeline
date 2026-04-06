from __future__ import annotations

from pathlib import Path

from src.pipeline.extract import extract_data
from src.pipeline.load import load_to_sqlite
from src.pipeline.transform import transform_data
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_pipeline(raw_dir: Path | None = None) -> Path:
    logger.info("Starting pipeline run")
    raw_data = extract_data(raw_dir=raw_dir)
    transformed_data = transform_data(raw_data)
    db_path = load_to_sqlite(transformed_data)
    logger.info("Pipeline completed successfully")
    return db_path


if __name__ == "__main__":
    run_pipeline()
