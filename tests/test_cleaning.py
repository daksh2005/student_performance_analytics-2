import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from analytics import clean_data, build_review_table

def test_clean_data_calculates_percentage_and_deduplicates():
    df = pd.DataFrame([
        ["S1","A","Python","Semester 1",80,40,50],
        ["S1","A","Python","Semester 1",82,45,50],
        ["S2","B","Stats","Semester 1",110,70,100],
        ["S3","C","DB","Semester 1",70,30,0],
    ], columns=["student_id","student_name","course","semester","attendance_pct","marks","max_marks"])
    clean = clean_data(df)
    assert len(clean) == 1
    assert clean.iloc[0]["marks_pct"] == 90.0
    assert clean.iloc[0]["attendance_pct"] == 82

def test_review_table_flags_low_attendance_or_marks():
    df = pd.DataFrame([
        ["S1","A","Python","Semester 1",60,70,100],
        ["S2","B","Stats","Semester 1",90,35,100],
    ], columns=["student_id","student_name","course","semester","attendance_pct","marks","max_marks"])
    clean = clean_data(df)
    flagged = build_review_table(clean, attendance_threshold=75, marks_threshold=50)
    assert len(flagged) == 2
