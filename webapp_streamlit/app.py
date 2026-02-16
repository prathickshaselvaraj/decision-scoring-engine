
import sys
import os
import tempfile
import streamlit as st

# to make sure streamlit can import from src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.main import run_pipeline

st.set_page_config(page_title="Decision Scoring Engine", layout="centered")

st.title("Multi-Criteria Decision Scoring & Ranking System")
st.write("Upload **criteria.csv** and **scores.csv**, then click Run.")

criteria_file = st.file_uploader("Upload criteria.csv", type=["csv"])
scores_file = st.file_uploader("Upload scores.csv", type=["csv"])

# store results so dropdown changes won't force us to run again
if "results" not in st.session_state:
    st.session_state["results"] = None

run_btn = st.button(
    "Run Scoring Engine",
    type="primary",
    disabled=(criteria_file is None or scores_file is None),
)

if run_btn:
    try:
        # using temp folder so we don't permanently save user uploads
        with tempfile.TemporaryDirectory() as tmp:
            criteria_path = os.path.join(tmp, "criteria.csv")
            scores_path = os.path.join(tmp, "scores.csv")
            out_folder = os.path.join(tmp, "out")

            # save uploaded files to temp
            with open(criteria_path, "wb") as f:
                f.write(criteria_file.getbuffer())

            with open(scores_path, "wb") as f:
                f.write(scores_file.getbuffer())

            # run pipeline
            criteria, ranked_csv_rows, ranked_full, ranked_csv_path, report_path = run_pipeline(
                criteria_path, scores_path, out_folder
            )

            # read outputs before temp folder disappears
            with open(ranked_csv_path, "rb") as f:
                ranked_bytes = f.read()

            with open(report_path, "r", encoding="utf-8") as f:
                report_text = f.read()

            with open(report_path, "rb") as f:
                report_bytes = f.read()

        # save everything in session state
        st.session_state["results"] = {
            "criteria": criteria,
            "ranked_csv_rows": ranked_csv_rows,
            "ranked_full": ranked_full,
            "ranked_bytes": ranked_bytes,
            "report_text": report_text,
            "report_bytes": report_bytes,
        }

        st.success("Run completed successfully!")

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Check: weights sum to 1.0, directions are benefit/cost, and score columns match criteria names.")


# show results if we have them
res = st.session_state["results"]

if res is not None:
    criteria = res["criteria"]
    ranked_csv_rows = res["ranked_csv_rows"]
    ranked_full = res["ranked_full"]
    ranked_bytes = res["ranked_bytes"]
    report_text = res["report_text"]
    report_bytes = res["report_bytes"]

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

    if selected_data:
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
        st.download_button(
            "Download ranked_output.csv",
            data=ranked_bytes,
            file_name="ranked_output.csv",
            mime="text/csv",
        )

    with c2:
        st.download_button(
            "Download explanation_report.md",
            data=report_bytes,
            file_name="explanation_report.md",
            mime="text/markdown",
        )

    with st.expander("Show full explanation_report.md"):
        st.code(report_text)
