"""
io_utils.py
------------
Handles reading and writing CSV files.
No scoring logic here.
"""

import csv
from typing import Dict, List, Tuple


def read_csv_as_dicts(path: str) -> Tuple[List[str], List[Dict[str, str]]]:
    """
    Reads a CSV file and returns:
    - headers (list of column names)
    - rows (list of dicts)

    Each row is stored as strings.
    """
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = [row for row in reader]
    return headers, rows


def write_ranked_output_csv(path: str, rows: List[Dict[str, object]]) -> None:
    """
    Writes ranked results into a CSV file.
    """
    if not rows:
        raise ValueError("No ranked rows to write.")

    headers = list(rows[0].keys())

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
