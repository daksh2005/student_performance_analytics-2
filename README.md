# Student Performance Analytics System

**Course:** MCA Data Science — Python Programming  
**Type:** Academic prototype using synthetic data

## Features
- Loads built-in sample CSV or an uploaded CSV
- Validates required columns and numeric ranges
- Standardises columns, removes duplicate student-course-semester records, and derives marks percentage
- KPI cards for students, average marks, average attendance, and review flags
- Interactive Plotly charts for course marks, performance bands, attendance distribution, and semester trends
- Filters by semester and course
- Transparent academic-support review thresholds
- CSV export of filtered analytics

## Requirements
- Python 3.10 or newer (Python 3.11 recommended)
- Internet connection for first-time dependency installation

## Run on Windows
1. Extract the ZIP.
2. Open the project folder in VS Code.
3. Open Terminal and run:
   ```powershell
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```
4. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## CSV format
Required columns:
`student_id, student_name, course, semester, attendance_pct, marks, max_marks`

- `attendance_pct`: 0–100
- `marks`: 0 or greater, and no greater than `max_marks`
- `max_marks`: positive number
- One unique record per student, course, and semester

## Test data cleaning
Run:
```bash
pytest -q
```

## Project structure
```text
student_performance_analytics/
├── app.py
├── analytics.py
├── requirements.txt
├── README.md
├── data/
│   └── sample_performance.csv
├── tests/
│   └── test_cleaning.py
└── screenshots/
    └── dashboard_preview.png
```

## Important academic note
All included student names and records are synthetic demonstration data. Review flags are threshold-based prompts for human follow-up, not machine-learning predictions or final academic decisions. Do not upload identifiable student information to a public hosting service.
