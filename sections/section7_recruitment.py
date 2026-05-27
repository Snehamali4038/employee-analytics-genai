# ============================================================
#  sections/section7_recruitment.py
#  Section 7: Recruitment & Hiring Effectiveness
# ============================================================

from data_loader import load_data, get_stats, group_mean
from ai_engine import ask_gemini as ask_claude

def run(question_index=0):
    df = load_data()

    questions = [
        "How do Hiring Source, Time to Hire, and Recruitment Cost impact employee performance, retention, and job satisfaction?",
        "Which hiring source produces the best long-term employee outcomes and why?",
        "Generate recommendations for optimizing the recruitment process based on cost, quality, and retention data.",
    ]

    contexts = [
        # Q1
        f"""Performance by Hiring Source:
{group_mean(df, 'Hiring_Source', 'Performance_Rating')}
Job Satisfaction by Hiring Source:
{group_mean(df, 'Hiring_Source', 'Employee_Job_Satisfaction_Score')}
Time to Hire stats:
{get_stats(df, ['Time_to_Hire'])}
Recruitment Cost stats:
{get_stats(df, ['Recruitment_Cost'])}""",

        # Q2
        f"""Performance by Hiring Source:
{group_mean(df, 'Hiring_Source', 'Performance_Rating')}
Resignation by Hiring Source:
{df.groupby('Hiring_Source')['Employee_Resignation_Status'].apply(lambda x: (x=='Yes').mean()*100).round(2).to_string()}
Satisfaction by Hiring Source:
{group_mean(df, 'Hiring_Source', 'Employee_Job_Satisfaction_Score')}""",

        # Q3
        f"""Full hiring source comparison:
Performance  : {group_mean(df, 'Hiring_Source', 'Performance_Rating')}
Satisfaction : {group_mean(df, 'Hiring_Source', 'Employee_Job_Satisfaction_Score')}
Resign Rate% : {df.groupby('Hiring_Source')['Employee_Resignation_Status'].apply(lambda x: round((x=='Yes').mean()*100,2)).to_string()}
Avg Cost     : {group_mean(df, 'Hiring_Source', 'Recruitment_Cost')}
Avg Time     : {group_mean(df, 'Hiring_Source', 'Time_to_Hire')}""",
    ]

    q   = questions[question_index]
    ctx = contexts[question_index]
    ans = ask_claude(q, ctx)
    return q, ctx, ans
