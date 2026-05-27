# ============================================================
#  sections/section5_attrition.py
#  Section 5: Attrition & Retention Intelligence
# ============================================================

from data_loader import load_data, get_stats, filter_rows, group_mean
from ai_engine import ask_gemini as ask_claude

def run(question_index=0):
    df = load_data()

    questions = [
        "Identify factors contributing to Employee Resignation using multi-variable reasoning.",
        "Generate a risk profile of employees likely to resign using behavioral and compensation features.",
        "Compare work-life balance, overtime, and engagement between resigned vs retained employees.",
    ]

    resigned = filter_rows(df, 'Employee_Resignation_Status', 'eq', 'Yes')
    retained = filter_rows(df, 'Employee_Resignation_Status', 'eq', 'No')

    compare_cols = ['Employee_Work_Life_Balance_Rating', 'Overtime_Hours_Per_Week',
                    'Employee_Engagement_Score', 'Annual_Salary_Increase_Percentage',
                    'Employee_Job_Satisfaction_Score']

    contexts = [
        # Q1
        f"""Resigned: {len(resigned)} | Retained: {len(retained)}
Resigned averages:\n{resigned[compare_cols].mean().round(2).to_string()}
Retained averages:\n{retained[compare_cols].mean().round(2).to_string()}""",

        # Q2
        f"""Resigned stats:\n{get_stats(resigned, compare_cols)}
Retained stats:\n{get_stats(retained, compare_cols)}
Department resignation counts:
{df.groupby('Department')['Employee_Resignation_Status'].apply(lambda x: (x=='Yes').sum()).sort_values(ascending=False).to_string()}""",

        # Q3
        f"""Comparison — Resigned vs Retained:
WLB Rating   : {resigned['Employee_Work_Life_Balance_Rating'].mean():.2f} vs {retained['Employee_Work_Life_Balance_Rating'].mean():.2f}
Overtime Hrs : {resigned['Overtime_Hours_Per_Week'].mean():.2f} vs {retained['Overtime_Hours_Per_Week'].mean():.2f}
Engagement   : {resigned['Employee_Engagement_Score'].mean():.2f} vs {retained['Employee_Engagement_Score'].mean():.2f}
Salary Raise : {resigned['Annual_Salary_Increase_Percentage'].mean():.2f}% vs {retained['Annual_Salary_Increase_Percentage'].mean():.2f}%""",
    ]

    q   = questions[question_index]
    ctx = contexts[question_index]
    ans = ask_claude(q, ctx)
    return q, ctx, ans
