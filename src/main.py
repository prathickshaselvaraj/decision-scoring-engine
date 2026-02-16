import os
import argparse

from src.io_utils import read_csv_as_dicts, write_ranked_output_csv
from src.validators import parse_and_validate_criteria, validate_scores_table
from src.normalizer import normalize_scores
from src.scorer import compute_scores
from src.ranker import rank_alternatives
from src.reporter import write_explanation_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-Criteria Decision Scoring Engine")

    parser.add_argument(
        "--criteria",
        type=str,
        default="data/criteria.csv",
        help="Path to criteria CSV file"
    )

    parser.add_argument(
        "--scores",
        type=str,
        default="data/scores.csv",
        help="Path to scores CSV file"
    )

    parser.add_argument(
        "--out",
        type=str,
        default="outputs",
        help="Output folder path"
    )

    args = parser.parse_args()

    criteria_path = args.criteria
    scores_path = args.scores
    out_folder = args.out

    #output folder+files
    os.makedirs(out_folder, exist_ok=True)
    ranked_csv_path = os.path.join(out_folder, "ranked_output.csv")
    report_path = os.path.join(out_folder, "explanation_report.md")

    #1)read csv files
    _, criteria_rows = read_csv_as_dicts(criteria_path)
    score_headers, score_rows = read_csv_as_dicts(scores_path)

    #2)validate inputs
    criteria = parse_and_validate_criteria(criteria_rows)
    validate_scores_table(score_headers, score_rows, criteria)

    #3)normalize
    normalized_rows, _stats = normalize_scores(score_rows, criteria)

    #4)compute scores
    results = compute_scores(normalized_rows, criteria)

    #5)rank
    ranked = rank_alternatives(results)

    #6)save ranked output csv
    ranked_csv_rows = []
    for r in ranked:
        ranked_csv_rows.append(
            {
                "rank": r["rank"],
                "alternative": r["alternative"],
                "final_score": round(float(r["final_score"]), 6),
            }
        )

    write_ranked_output_csv(ranked_csv_path, ranked_csv_rows)

    #7)save explanation report
    write_explanation_report(report_path, ranked, criteria)

    #console output
    print("Done! Files generated:")
    print(f"- {ranked_csv_path}")
    print(f"- {report_path}\n")
    print("Top 3 results:")
    for r in ranked[:3]:
        print(f"{r['rank']}. {r['alternative']} -> {float(r['final_score']):.4f}")
if __name__ == "__main__":
    main()
