"""
This file calculates final score for each alternative.
Steps:
- Multiply normalized value with weight
- Add all contributions to get final score
formula:
contribution = normalized_score * weight
final_score = sum of all contributions
"""
from typing import List, Dict
def compute_scores(
    normalized_rows: List[Dict[str, object]],
    criteria: List[Dict],
) -> List[Dict[str, object]]:
    """
    returns results for each alternative:
    {
        "alternative": str,
        "final_score": float,
        "contributions": {criterion: float},
        "normalized": {criterion: float}
    }
    """
    results: List[Dict[str, object]] = []
    for row in normalized_rows:
        alt = row["alternative"]
        total_score = 0.0
        contributions: Dict[str, float] = {}
        normalized_values: Dict[str, float] = {}
        for c in criteria:
            crit = c["criterion"]
            weight = c["weight"]
            norm_val = float(row[crit])
            normalized_values[crit] = norm_val
            contrib = norm_val * weight
            contributions[crit] = contrib
            total_score += contrib
        results.append(
            {
                "alternative": alt,
                "final_score": total_score,
                "contributions": contributions,
                "normalized": normalized_values,
            }
        )
    return results
