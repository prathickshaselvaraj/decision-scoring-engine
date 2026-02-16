"""
This file normalizes the scores so that all criteria values become comparable.
We use Min-Max Normalization (range 0 to 1)
If direction = benefit (higher is better):
    norm = (x - min) / (max - min)
If direction = cost (lower is better):
    norm = (max - x) / (max - min)
Special case:
If max == min (all values are same),
then we avoid division by zero and assign 1.0 for all.
"""
from typing import List, Dict, Tuple
def normalize_scores(
    score_rows: List[Dict[str, str]],
    criteria: List[Dict],
) -> Tuple[List[Dict[str, object]], Dict[str, Dict[str, float]]]:
    """
    Returns:
    1) normalized_rows:
       each row will have alternative name and normalized scores (0 to 1)
    2) stats:
       stores min and max used for each criterion
       example: {"Price": {"min": 10, "max": 50}}
    """
    stats: Dict[str, Dict[str, float]] = {}
    #Find min and max values for each criterion
    for c in criteria:
        crit = c["criterion"]
        values = []
        for row in score_rows:
            values.append(float(row[crit]))
        stats[crit] = {"min": min(values), "max": max(values)}
    normalized_rows: List[Dict[str, object]] = []
    #Normalize each alternative row
    for row in score_rows:
        new_row: Dict[str, object] = {}
        new_row["alternative"] = row["alternative"].strip()
        for c in criteria:
            crit = c["criterion"]
            direction = c["direction"]
            x=float(row[crit])
            mn=stats[crit]["min"]
            mx=stats[crit]["max"]
            if mx==mn:
                norm_value = 1.0
            else:
                if direction=="benefit":
                    norm_value = (x - mn) / (mx - mn)
                else:
                    norm_value = (mx - x) / (mx - mn)
            new_row[crit] = norm_value
        normalized_rows.append(new_row)
    return normalized_rows, stats
