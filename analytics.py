import pandas as pd

REQUIRED_COLUMNS = ["student_id", "student_name", "course", "semester", "attendance_pct", "marks", "max_marks"]

def clean_data(raw: pd.DataFrame):
    """Validate, standardise and clean student performance records."""
    df = raw.copy()
    df.columns = [str(c).strip().lower().replace(" ", "_") for c in df.columns]
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))

    for col in ["student_id", "student_name", "course", "semester"]:
        df[col] = df[col].astype("string").str.strip()
    for col in ["attendance_pct", "marks", "max_marks"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=REQUIRED_COLUMNS)
    df = df[(df["attendance_pct"].between(0, 100)) &
            (df["marks"] >= 0) &
            (df["max_marks"] > 0) &
            (df["marks"] <= df["max_marks"])]
    df = df[df["student_id"].str.len().fillna(0) > 0]
    df = df.drop_duplicates(subset=["student_id", "course", "semester"], keep="last")
    df["marks_pct"] = (df["marks"] / df["max_marks"] * 100).round(2)
    df["performance_band"] = pd.cut(
        df["marks_pct"], bins=[-0.01, 39.99, 59.99, 79.99, 100],
        labels=["Needs Improvement", "Satisfactory", "Good", "Excellent"]
    ).astype("string")
    return df.reset_index(drop=True)

def build_review_table(df, attendance_threshold=75, marks_threshold=50):
    if df.empty:
        return df.assign(review_reason=pd.Series(dtype="string"))
    out = df.copy()
    conditions = []
    for _, row in out.iterrows():
        reasons = []
        if row["attendance_pct"] < attendance_threshold:
            reasons.append("Attendance below threshold")
        if row["marks_pct"] < marks_threshold:
            reasons.append("Marks below threshold")
        conditions.append("; ".join(reasons) if reasons else "No threshold flag")
    out["review_reason"] = conditions
    return out[out["review_reason"] != "No threshold flag"].sort_values(
        ["marks_pct", "attendance_pct"], ascending=[True, True]
    )
