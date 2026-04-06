from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import get_table_file_map
from src.utils.logger import get_logger

logger = get_logger(__name__)


def extract_data(raw_dir: Path | None = None) -> dict[str, pd.DataFrame]:
    dataframes: dict[str, pd.DataFrame] = {}

    for table_name, file_path in get_table_file_map(raw_dir).items():
        logger.info("Reading %s from %s", table_name, file_path)
        dataframes[table_name] = pd.read_csv(file_path)

    return dataframes
