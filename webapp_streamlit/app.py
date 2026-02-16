import sys
import os
import uuid
import streamlit as st

# this helps streamlit find the src folder when running app.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.io_utils import read_csv_as_dicts, write_ranked_output_csv
from src.validators import parse_and_validate_criteria, validate_scores_table
from src.normalizer import normalize_scores
from src.scorer import compute_scores
from src.ranker import rank_alternatives
from src.reporter import write_explanation_report


st.set_page_config(page_title="Decision Scoring Engine", layout="centered")

st.title("Multi-Criteria Decision Scoring & Ranking System")
st.write("Upload **criteria.csv** and **scores.csv**, then click run.")

criteria_file = st.file_uploader("Upload criteria.csv", type=["csv"])
scores_file = st.file_uploader("Upload scores.csv", type=["csv"])

OUT_ROOT = "streamlit_outputs"
os.makedirs(OUT_ROOT, exist_ok=True)


def run_engine(criteria_path: str, scores_path: str, out_folder: str):
    # create folder for this run
    os.makedirs(out_folder, exist_ok=True)

    ranked_csv_path = os.path.join(out_folder, "ranked_output.csv")
    report_path = os.path.join(out_folder, "explanation_report.md")

    # read csv files
    _, criteria_rows = read_csv_as_dicts(criteria_path)
    score_headers, score_rows = read_csv_as_dicts(scores_path)

    # validate + parse
    criteria = parse_and_validate_criteria(criteria_rows)
    validate_scores_table(score_headers, score_rows, criteria)

    # normalize + score + rank
    normalized_rows, _stats = normalize_scores(score_rows, criteria)
    results = compute_scores(normalized_rows, criteria)
    ranked_full = rank_alternatives(results)

    # save ranked csv (simple)
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

    # save report
    write_explanation_report(report_path, ranked_full, criteria)

    # read report for showing in app
    with open(report_path, "r", encoding="utf-8") as f:
        report_text = f.read()

    return criteria, ranked_csv_rows, ranked_full, report_text, ranked_csv_path, report_path


run_btn = st.button(
    "Run Scoring Engine",
    type="primary",
    disabled=(criteria_file is None or scores_file is None),
)

if run_btn:
    try:
        run_id = str(uuid.uuid4())[:8]
        run_folder = os.path.join(OUT_ROOT, f"run_{run_id}")
        os.makedirs(run_folder, exist_ok=True)

        # save uploaded files so csv reader can use them
        criteria_path = os.path.join(run_folder, "criteria.csv")
        scores_path = os.path.join(run_folder, "scores.csv")

        with open(criteria_path, "wb") as f:
            f.write(criteria_file.getbuffer())

        with open(scores_path, "wb") as f:
            f.write(scores_file.getbuffer())

        criteria, ranked_csv_rows, ranked_full, report_text, ranked_csv_path, report_path = run_engine(
            criteria_path, scores_path, run_folder
        )

        st.success("Run completed successfully!")

        st.subheader("Criteria Used")
        st.table(
            [
                {
                    "criterion": c["criterion"],
                    "weight": round(float(c["weight"]), 4),
                    "direction": c["direction"],
                }
                for c in criteria
            ]
        )

        st.subheader("Ranked Output")
        st.table(ranked_csv_rows)

        st.subheader("Top 3 Summary")
        for r in ranked_full[:3]:
            st.write(f"{r['rank']}. **{r['alternative']}** -> {float(r['final_score']):.4f}")

        st.subheader("Explanation (Criterion Contribution)")
        alt_names = [r["alternative"] for r in ranked_full]
        selected_alt = st.selectbox("Select an alternative", alt_names)

        selected_data = None
        for r in ranked_full:
            if r["alternative"] == selected_alt:
                selected_data = r
                break

        if selected_data is not None:
            contribs = selected_data["contributions"]
            norms = selected_data["normalized"]

            table_rows = []
            for c in criteria:
                crit = c["criterion"]
                table_rows.append(
                    {
                        "criterion": crit,
                        "direction": c["direction"],
                        "weight": round(float(c["weight"]), 4),
                        "normalized": round(float(norms[crit]), 4),
                        "contribution": round(float(contribs[crit]), 4),
                    }
                )

            st.table(table_rows)

            top_driver = max(contribs, key=contribs.get)
            st.info(f"Top contributing criterion for **{selected_alt}**: **{top_driver}**")

        st.subheader("Downloads")
        c1, c2 = st.columns(2)

        with c1:
            with open(ranked_csv_path, "rb") as f:
                st.download_button(
                    "Download ranked_output.csv",
                    data=f,
                    file_name="ranked_output.csv",
                    mime="text/csv",
                )

        with c2:
            with open(report_path, "rb") as f:
                st.download_button(
                    "Download explanation_report.md",
                    data=f,
                    file_name="explanation_report.md",
                    mime="text/markdown",
                )

        with st.expander("Show full explanation_report.md"):
            st.code(report_text)

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Check: weights sum to 1.0, directions are benefit/cost, and scores columns match criteria.")
