"""
This file ranks the alternatives based on final score.
rule:higher final_score means better rank
If scores are equal, Python sorting keeps the same order (stable sort).
"""
from typing import List, Dict

def rank_alternatives(results: List[Dict[str, object]]) -> List[Dict[str, object]]:
    """
    Input:results list from scorer.py
    Output:ranked list with rank number added
    """
    sorted_results = sorted(results, key=lambda x: x["final_score"], reverse=True)
    ranked: List[Dict[str, object]] = []
    for i, item in enumerate(sorted_results, start=1):
        ranked.append(
            {
                "rank": i,
                "alternative": item["alternative"],
                "final_score": item["final_score"],
                "contributions": item["contributions"],
                "normalized": item["normalized"],
            }
        )
    return ranked
