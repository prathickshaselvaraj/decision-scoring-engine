"""
This file validates the input CSV files.

Why validation is important:
- If weights are wrong -> final ranking will be wrong
- If columns are missing -> program may crash later
- If scores are not numeric -> normalization fails
"""

from typing import List, Dict

ALLOWED_DIRECTIONS = {"benefit", "cost"}


def parse_and_validate_criteria(criteria_rows: List[Dict[str, str]]) -> List[Dict]:
    """
    Input: criteria.csv rows (as string values)
    Output: parsed list with correct types:
        [{"criterion": str, "weight": float, "direction": str}, ...]

    Checks:
    - criterion name should not be empty
    - no duplicate criterion names
    - direction should be benefit or cost
    - weight should be numeric and non-negative
    - weights must sum to 1.0
    """
    if not criteria_rows:
        raise ValueError("criteria.csv is empty.")

    parsed = []
    total_weight = 0.0
    seen_criteria = set()

    for row in criteria_rows:
        crit = row.get("criterion", "").strip()
        weight_str = row.get("weight", "").strip()
        direction = row.get("direction", "").strip().lower()

        if crit == "":
            raise ValueError("Criterion name cannot be empty in criteria.csv.")

        if crit in seen_criteria:
            raise ValueError(f"Duplicate criterion found: '{crit}'")
        seen_criteria.add(crit)

        if direction not in ALLOWED_DIRECTIONS:
            raise ValueError(
                f"Invalid direction '{direction}' for '{crit}'. "
                "Direction must be 'benefit' or 'cost'."
            )

        try:
            weight = float(weight_str)
        except:
            raise ValueError(f"Invalid weight '{weight_str}' for '{crit}'.")

        if weight < 0:
            raise ValueError(f"Weight cannot be negative for '{crit}'.")

        total_weight += weight
        parsed.append({"criterion": crit, "weight": weight, "direction": direction})

    if abs(total_weight - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1.0, but current sum = {total_weight}")

    return parsed


def validate_scores_table(
    score_headers: List[str],
    score_rows: List[Dict[str, str]],
    criteria: List[Dict],
) -> None:
    """
    Validates scores.csv file.

    Checks:
    - scores.csv should not be empty
    - must contain 'alternative' column
    - all criteria columns must exist in scores.csv
    - alternative name must not be empty
    - scores must be numeric
    """
    if not score_rows:
        raise ValueError("scores.csv is empty.")

    if "alternative" not in score_headers:
        raise ValueError("scores.csv must contain an 'alternative' column.")

    required_criteria = [c["criterion"] for c in criteria]

    for crit in required_criteria:
        if crit not in score_headers:
            raise ValueError(f"scores.csv is missing required column: '{crit}'")

    for i, row in enumerate(score_rows, start=1):
        alt = row.get("alternative", "").strip()

        if alt == "":
            raise ValueError(f"Row {i} has an empty alternative name.")

        for crit in required_criteria:
            value = row.get(crit, "").strip()

            try:
                float(value)
            except:
                raise ValueError(
                    f"Invalid score in row {i} (alternative '{alt}'), "
                    f"criterion '{crit}': '{value}'"
                )
