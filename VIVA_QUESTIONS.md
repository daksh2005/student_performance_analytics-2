# Viva Questions and Answers

1. **What is the aim of the project?**  
   To organise student marks and attendance into an interactive dashboard for descriptive academic analysis.

2. **Why is Python used?**  
   Python has readable syntax and a strong ecosystem for data processing, visualisation, and rapid application development.

3. **What is Pandas?**  
   Pandas is a Python library for working with structured data using Series and DataFrames.

4. **What is data cleaning?**  
   Data cleaning identifies and handles missing, invalid, inconsistent, or duplicate records before analysis.

5. **Why is marks percentage calculated?**  
   It allows fairer comparison when assessments have different maximum marks: marks / max_marks × 100.

6. **What does Streamlit do?**  
   Streamlit converts a Python script into an interactive web application with widgets and charts.

7. **What does Plotly provide?**  
   Plotly creates interactive charts that support hover, zoom, and exploration.

8. **How are duplicate records handled?**  
   The project keeps the latest row for each student_id, course, and semester combination.

9. **What is a KPI?**  
   A key performance indicator is a concise metric used to monitor a relevant aspect of a system.

10. **How are review flags generated?**  
    A record is flagged if its attendance is below the selected attendance threshold or marks percentage is below the selected marks threshold.

11. **Is the system using machine learning?**  
    No. The current review flag is rule-based. Machine learning could be added as future work.

12. **What are the limitations?**  
    The sample data is synthetic; there is no authentication or live university integration; and flags do not replace academic judgement.

13. **What is CSV?**  
    Comma-Separated Values is a simple text format for tabular data exchange.

14. **What is a DataFrame?**  
    A two-dimensional labelled data structure provided by Pandas.

15. **How can the project be improved?**  
    Add authentication, a database, role-based access, more indicators, accessibility features, and carefully validated predictive models.
