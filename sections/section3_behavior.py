# ============================================================
#  sections/section3_behavior.py
#  Section 3: Behavioral & Soft Skills Intelligence
# ============================================================

from data_loader import load_data, get_stats, filter_rows, correlation, group_mean
from ai_engine import ask_gemini as ask_claude

def run(question_index=0):
    df = load_data()

    questions = [
        "Cluster employees based on soft skill ratings (Leadership, Teamwork, Adaptability, Creativity) and describe each cluster.",
        "Identify employees with high conflict resolution cases but low teamwork scores. Explain the contradiction.",
        "How does Employee Engagement Score impact Job Satisfaction and Retention?",
        "Detect employees with high initiative but low innovation contribution and explain possible blockers.",
    ]

    soft_cols = ['Leadership_Qualities_Rating', 'Teamwork_Skills_Rating',
                 'Adaptability_Rating', 'Creativity_Rating']

    resigned = filter_rows(df, 'Employee_Resignation_Status', 'eq', 'Yes')
    retained = filter_rows(df, 'Employee_Resignation_Status', 'eq', 'No')

    contexts = [
        # Q1
        f"""Soft skills statistics:\n{get_stats(df, soft_cols)}""",

        # Q2
        f"""Conflict Resolution vs Teamwork corr: {correlation(df, 'Conflict_Resolution_Cases', 'Teamwork_Skills_Rating')}
Stats:\n{get_stats(df, ['Conflict_Resolution_Cases', 'Teamwork_Skills_Rating'])}""",

        # Q3
        f"""Engagement vs Job Satisfaction corr : {correlation(df, 'Employee_Engagement_Score', 'Employee_Job_Satisfaction_Score')}
Avg Engagement — Resigned : {resigned['Employee_Engagement_Score'].mean():.2f}
Avg Engagement — Retained : {retained['Employee_Engagement_Score'].mean():.2f}
Avg Satisfaction — Resigned: {resigned['Employee_Job_Satisfaction_Score'].mean():.2f}
Avg Satisfaction — Retained: {retained['Employee_Job_Satisfaction_Score'].mean():.2f}""",

        # Q4
        f"""Initiative vs Innovation corr: {correlation(df, 'Initiative_Rating', 'Innovation_Projects_Involvement')}
Stats:\n{get_stats(df, ['Initiative_Rating', 'Innovation_Projects_Involvement'])}""",
    ]

    q   = questions[question_index]
    ctx = contexts[question_index]
    ans = ask_claude(q, ctx)
    return q, ctx, ans
