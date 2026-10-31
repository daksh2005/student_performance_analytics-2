from pathlib import Path
import io
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Student Performance Analytics", page_icon="🎓", layout="wide")

from analytics import REQUIRED_COLUMNS, clean_data, build_review_table

@st.cache_data
def load_sample_data():
    path = Path(__file__).parent / "data" / "sample_performance.csv"
    return pd.read_csv(path)


def main():
    st.title("🎓 Student Performance Analytics")
    st.caption("Python Programming Mini Project | MCA Data Science | Academic prototype using synthetic data")
    with st.sidebar:
        st.header("Data & Filters")
        uploaded = st.file_uploader("Upload student CSV", type=["csv"])
        attendance_threshold = st.slider("Attendance review threshold (%)", 0, 100, 75)
        marks_threshold = st.slider("Marks review threshold (%)", 0, 100, 50)
        st.markdown("---")
        st.caption("Expected columns: " + ", ".join(REQUIRED_COLUMNS))

    try:
        raw = pd.read_csv(uploaded) if uploaded else load_sample_data()
        df = clean_data(raw)
    except Exception as exc:
        st.error(f"Could not process the dataset: {exc}")
        st.info("Upload a CSV with the required columns and valid numeric values.")
        st.stop()

    if df.empty:
        st.warning("No valid records remain after validation.")
        st.stop()

    with st.sidebar:
        semesters = sorted(df["semester"].dropna().unique().tolist())
        courses = sorted(df["course"].dropna().unique().tolist())
        selected_semesters = st.multiselect("Semester", semesters, default=semesters)
        selected_courses = st.multiselect("Course", courses, default=courses)

    filtered = df[df["semester"].isin(selected_semesters) & df["course"].isin(selected_courses)].copy()
    if filtered.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    students = filtered["student_id"].nunique()
    avg_marks = filtered["marks_pct"].mean()
    avg_att = filtered["attendance_pct"].mean()
    flagged = build_review_table(filtered, attendance_threshold, marks_threshold)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students represented", f"{students:,}")
    c2.metric("Average marks", f"{avg_marks:.1f}%")
    c3.metric("Average attendance", f"{avg_att:.1f}%")
    c4.metric("Records for review", f"{len(flagged):,}")

    st.subheader("Performance Overview")
    left, right = st.columns(2)
    course_summary = filtered.groupby("course", as_index=False).agg(
        average_marks=("marks_pct", "mean"), average_attendance=("attendance_pct", "mean")
    ).round(2)
    with left:
        fig = px.bar(course_summary, x="course", y="average_marks", color="average_marks",
                     range_y=[0, 100], title="Average Marks by Course",
                     labels={"course": "Course", "average_marks": "Average marks (%)"})
        st.plotly_chart(fig, use_container_width=True)
    with right:
        bands = filtered["performance_band"].value_counts().rename_axis("performance_band").reset_index(name="records")
        fig = px.pie(bands, names="performance_band", values="records", hole=0.45,
                     title="Performance Band Distribution")
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        attendance = filtered.assign(attendance_band=pd.cut(
            filtered["attendance_pct"], bins=[-0.01, 59.99, 74.99, 89.99, 100],
            labels=["Below 60%", "60–74%", "75–89%", "90–100%"]
        )).groupby("attendance_band", observed=False).size().reset_index(name="records")
        fig = px.bar(attendance, x="attendance_band", y="records", title="Attendance Distribution",
                     labels={"attendance_band": "Attendance band", "records": "Records"})
        st.plotly_chart(fig, use_container_width=True)
    with right:
        semester_summary = filtered.groupby("semester", as_index=False).agg(
            average_marks=("marks_pct", "mean"), average_attendance=("attendance_pct", "mean")
        ).round(2)
        semester_summary["semester_order"] = semester_summary["semester"].str.extract(r"(\d+)").astype(float)
        semester_summary = semester_summary.sort_values("semester_order", na_position="last")
        fig = px.line(semester_summary, x="semester", y="average_marks", markers=True,
                      title="Semester-wise Average Marks",
                      labels={"semester": "Semester", "average_marks": "Average marks (%)"})
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Student Records")
    st.caption("One row per student. Marks and attendance are averaged across the selected courses and semesters.")
    student_summary = filtered.groupby(["student_id", "student_name"], as_index=False).agg(
        courses=("course", "nunique"),
        semesters=("semester", "nunique"),
        average_attendance=("attendance_pct", "mean"),
        average_marks=("marks_pct", "mean"),
        assessment_records=("course", "size"),
    )
    student_summary["average_attendance"] = student_summary["average_attendance"].round(2)
    student_summary["average_marks"] = student_summary["average_marks"].round(2)
    student_summary = student_summary.sort_values(
        ["average_marks", "student_name"], ascending=[False, True]
    )
    st.dataframe(student_summary, use_container_width=True, hide_index=True)

    st.subheader("Academic Support Review")
    st.caption("Flags are transparent threshold-based prompts for human review, not predictions or final academic decisions.")
    if flagged.empty:
        st.success("No records meet the selected review thresholds.")
    else:
        # Consolidate multiple flagged course/semester records into one row per student.
        review_summary = flagged.groupby(["student_id", "student_name"], as_index=False).agg(
            courses_for_review=("course", lambda values: ", ".join(sorted(set(values)))),
            semesters_for_review=("semester", lambda values: ", ".join(sorted(set(values)))),
            lowest_marks_pct=("marks_pct", "min"),
            lowest_attendance_pct=("attendance_pct", "min"),
            review_reasons=("review_reason", lambda values: "; ".join(sorted(set(
                reason for item in values for reason in str(item).split("; ")
            )))),
        )
        review_summary["lowest_marks_pct"] = review_summary["lowest_marks_pct"].round(2)
        review_summary["lowest_attendance_pct"] = review_summary["lowest_attendance_pct"].round(2)
        st.dataframe(review_summary, use_container_width=True, hide_index=True)

    export_bytes = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download filtered analytics (CSV)", data=export_bytes,
                       file_name="student_performance_analytics.csv", mime="text/csv")
    st.markdown("---")
    st.caption("Demo dataset is synthetic. Do not upload identifiable student records to a public deployment.")

if __name__ == "__main__":
    main()
