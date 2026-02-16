import os
import argparse

from src.io_utils import read_csv_as_dicts, write_ranked_output_csv
from src.validators import parse_and_validate_criteria, validate_scores_table
from src.normalizer import normalize_scores
from src.scorer import compute_scores
from src.ranker import rank_alternatives
from src.reporter import write_explanation_report

def run_pipeline(criteria_path: str, scores_path: str, out_folder: str):
    """
    runs the complete decision scoring pipeline.
    steps:
    -read csv files
    -validate inputs
    -normalize scores
    -calculate final scores
    -rank alternatives
    -save output csv + explanation report
    returns the generated results for reuse.
    """
    os.makedirs(out_folder, exist_ok=True)

    ranked_csv_path = os.path.join(out_folder, "ranked_output.csv")
    report_path = os.path.join(out_folder, "explanation_report.md")

    # 1)read inputs
    _, criteria_rows = read_csv_as_dicts(criteria_path)
    score_headers, score_rows = read_csv_as_dicts(scores_path)

    # 2)validate
    criteria = parse_and_validate_criteria(criteria_rows)
    validate_scores_table(score_headers, score_rows, criteria)

    # 3)normalize
    normalized_rows, _stats = normalize_scores(score_rows, criteria)

    # 4)compute scores
    results = compute_scores(normalized_rows, criteria)

    # 5)rank
    ranked_full = rank_alternatives(results)

    # 6)write ranked output csv
    ranked_csv_rows = []
    for r in ranked_full:
        ranked_csv_rows.append(
            {
                "rank": r["rank"],
                "alternative": r["alternative"],
                "final_score": round(float(r["final_score"]), 6),
            }
        )
    write_ranked_output_csv(ranked_csv_path, ranked_csv_rows)

    # 7)write explanation report
    write_explanation_report(report_path, ranked_full, criteria)
    return criteria, ranked_csv_rows, ranked_full, ranked_csv_path, report_path


def main():
    parser = argparse.ArgumentParser(
        description="Multi-Criteria Decision Scoring and Ranking System"
    )
    parser.add_argument(
        "--criteria",
        type=str,
        default="data/criteria.csv",
        help="Path of criteria.csv file",
    )
    parser.add_argument(
        "--scores",
        type=str,
        default="data/scores.csv",
        help="Path of scores.csv file",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="outputs",
        help="Output folder name",
    )

    args = parser.parse_args()
    criteria_path = args.criteria
    scores_path = args.scores
    out_folder = args.out
    criteria, ranked_csv_rows, ranked_full, ranked_csv_path, report_path = run_pipeline(
        criteria_path, scores_path, out_folder
    )
    print("Done! Output files created:")
    print(f"- {ranked_csv_path}")
    print(f"- {report_path}\n")

    print("Top 3 alternatives:")
    for r in ranked_full[:3]:
        print(f"{r['rank']}. {r['alternative']} -> {float(r['final_score']):.4f}")
if __name__ == "__main__":
    main()
