# ============================================================
#  sections/section6_compensation.py
#  Section 6: Compensation & Benefits Analysis
# ============================================================

from data_loader import load_data, get_stats, filter_rows, correlation, group_mean
from ai_engine import ask_gemini as ask_claude

def run(question_index=0):
    df = load_data()

    questions = [
        "Analyze the relationship between Salary Increase %, Bonus %, and Performance Rating.",
        "Identify employees who are underpaid relative to their performance and skills.",
        "Evaluate whether compensation benefits influence retention and satisfaction.",
    ]

    underpaid = df[(df['Performance_Rating'] >= 12) &
                   (df['Annual_Salary_Increase_Percentage'] <= 3)]

    resigned = filter_rows(df, 'Employee_Resignation_Status', 'eq', 'Yes')
    retained = filter_rows(df, 'Employee_Resignation_Status', 'eq', 'No')

    benefit_cols = ['Employee_Stock_Options', 'Employee_Health_Insurance_Coverage',
                    'Employee_Compensation_Benefits', 'Employee_Savings_Plans']
    # only use benefit cols that exist
    benefit_cols = [c for c in benefit_cols if c in df.columns]

    contexts = [
        # Q1
        f"""Salary Increase % vs Performance corr : {correlation(df, 'Annual_Salary_Increase_Percentage', 'Performance_Rating')}
Bonus % vs Performance corr        : {correlation(df, 'Performance_Bonus_Percentage', 'Performance_Rating')}
Stats:\n{get_stats(df, ['Annual_Salary_Increase_Percentage', 'Performance_Bonus_Percentage', 'Performance_Rating'])}""",

        # Q2
        f"""Underpaid high performers (Perf>=12, Raise<=3%): {len(underpaid)}
By Department:\n{underpaid['Department'].value_counts().to_string()}
Their avg performance: {underpaid['Performance_Rating'].mean():.2f}
Their avg raise: {underpaid['Annual_Salary_Increase_Percentage'].mean():.2f}%""",

        # Q3
        f"""Avg salary raise — Resigned: {resigned['Annual_Salary_Increase_Percentage'].mean():.2f}% | Retained: {retained['Annual_Salary_Increase_Percentage'].mean():.2f}%
Avg bonus     — Resigned: {resigned['Performance_Bonus_Percentage'].mean():.2f}% | Retained: {retained['Performance_Bonus_Percentage'].mean():.2f}%
{f"Benefit availability stats:{chr(10)}{get_stats(df, benefit_cols)}" if benefit_cols else "No benefit columns found."}""",
    ]

    q   = questions[question_index]
    ctx = contexts[question_index]
    ans = ask_claude(q, ctx)
    return q, ctx, ans
