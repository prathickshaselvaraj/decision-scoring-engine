"""
This file generates a Markdown explanation report.
The report shows for each alternative:
- normalized score for each criterion
- weight
- contribution (normalized * weight)
- final score
This makes the ranking easy to understand.
"""
from typing import List, Dict
def format_float(x: float, digits: int = 4) -> str:
    return f"{x:.{digits}f}"

def write_explanation_report(
    path: str,
    ranked: List[Dict[str, object]],
    criteria: List[Dict],
) -> None:
    """
    writes the explanation report into a Markdown file.
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Explanation Report\n\n")
        f.write("This report explains how the final score was calculated for each alternative.\n\n")
        #criteria details
        f.write("## Criteria Information\n\n")
        for c in criteria:
            f.write(
                f"- **{c['criterion']}** | weight = {c['weight']} | direction = {c['direction']}\n"
            )
        f.write("\n---\n\n")
        #alternative wise report
        for item in ranked:
            alt = item["alternative"]
            rank = item["rank"]
            final_score = float(item["final_score"])
            contributions: Dict[str, float] = item["contributions"]
            normalized: Dict[str, float] = item["normalized"]
            f.write(f"## Rank {rank}: {alt}\n\n")
            f.write(f"**Final Score:** {format_float(final_score)}\n\n")
            f.write("| Criterion | Normalized Value | Weight | Contribution |\n")
            f.write("|---|---:|---:|---:|\n")
            for c in criteria:
                crit = c["criterion"]
                weight = float(c["weight"])
                f.write(
                    f"| {crit} | {format_float(normalized[crit])} | "
                    f"{format_float(weight)} | {format_float(contributions[crit])} |\n"
                )
            f.write("\n")
            #finding top contributing criterion
            top_crit = max(contributions, key=contributions.get)
            f.write(f"**Main contributing criterion:** `{top_crit}`\n\n")
            f.write("---\n\n")