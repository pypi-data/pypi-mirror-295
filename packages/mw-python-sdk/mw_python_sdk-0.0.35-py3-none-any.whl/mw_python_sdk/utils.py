"""
Utility functions.
"""

import logging
import time
from typing import List
from datetime import datetime
from .core import DatasetFile

# Create a logger for your library
logger = logging.getLogger(__name__)


def parse_datetime(date_string: str) -> datetime:
    """
    Parse a datetime string into a datetime object.

    Args:
        date_string (str): The datetime string to parse.

    Returns:
        datetime: A datetime object.

    """
    if date_string is None:
        return datetime.now()
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def convert_to_dataset_file(files) -> List[DatasetFile]:
    """
    将给定的文件列表转换为 DatasetFile 对象的列表。

    Args:
        files (List[Dict]): 文件列表，每个元素为字典类型，包含 "_id"、"Token"、"Size" 和 "SubPath" 等字段。

    Returns:
        List[DatasetFile]: 转换后的 DatasetFile 对象列表。

    """
    if files is None:
        return []
    dataset_files = [
        DatasetFile(
            file.get("_id"),
            file.get("Token"),
            file.get("Size"),
            "" if file.get("SubPath") is None else file.get("SubPath"),
        )
        for file in files
    ]
    return dataset_files

def generate_timestamped_string(revision: int) -> str:
    """
    Generates a timestamped string based on the current time and a revision number.

    :param revision: The revision number.
    :return: A timestamped string.
    """
    timestamp = int(time.time() * 1000)
    result = f"{timestamp}_{revision}"
    return result