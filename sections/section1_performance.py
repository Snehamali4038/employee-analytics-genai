# ============================================================
#  sections/section1_performance.py
#  Section 1: Employee Performance & Skill Analytics
# ============================================================

from data_loader import (load_data, get_stats, filter_rows,
                          correlation, group_mean)
from ai_engine import ask_gemini as ask_claude

def run(question_index=0):
    """
    Run a question from Section 1.
    question_index: 0 to 4
    Returns: (question_text, data_context, ai_answer)
    """
    df = load_data()

    questions = [
        "How do Technical, Communication, and Problem Solving skills collectively influence Performance Rating? Build a weighted scoring model.",
        "Identify employees with high performance but low leadership potential. What are the possible reasons?",
        "Compare employees with Performance >= 10 vs <= 5. What behavioral patterns exist?",
        "Detect inconsistencies where high skill ratings do not align with project outcomes.",
        "Generate a profile of the ideal employee using the top 10% performers.",
    ]

    # Prepare data context for each question
    skill_cols = ['Technical_Skills_Rating', 'Communication_Skills_Rating',
                  'Problem_Solving_Skills_Rating', 'Performance_Rating']

    high = filter_rows(df, 'Performance_Rating', 'gte', 10)
    low  = filter_rows(df, 'Performance_Rating', 'lte', 5)
    top10 = filter_rows(df, 'Performance_Rating', 'gte',
                        df['Performance_Rating'].quantile(0.9))

    soft_cols = ['Technical_Skills_Rating', 'Communication_Skills_Rating',
                 'Problem_Solving_Skills_Rating', 'Leadership_Qualities_Rating',
                 'Teamwork_Skills_Rating', 'Adaptability_Rating', 'Creativity_Rating']

    contexts = [
        # Q1
        f"""Skill stats:\n{get_stats(df, skill_cols)}
Correlations with Performance:
  Technical    : {correlation(df, 'Technical_Skills_Rating', 'Performance_Rating')}
  Communication: {correlation(df, 'Communication_Skills_Rating', 'Performance_Rating')}
  ProblemSolving: {correlation(df, 'Problem_Solving_Skills_Rating', 'Performance_Rating')}""",

        # Q2
        f"""Total employees: {len(df)}
High performers (>=10): {len(high)}
Leadership Potential distribution:
{df['Leadership_Potential'].value_counts().to_string()}
High performers by leadership:
{high['Leadership_Potential'].value_counts().to_string()}""",

        # Q3
        f"""High performers (>=10): {len(high)}
  Avg skills: {high[skill_cols[:-1]].mean().round(2).to_dict()}
Low performers (<=5): {len(low)}
  Avg skills: {low[skill_cols[:-1]].mean().round(2).to_dict()}""",

        # Q4
        f"""Performance by Project Outcome:
{group_mean(df, 'Project_Outcome', 'Performance_Rating')}
Project outcome counts:
{df['Project_Outcome'].value_counts().to_string()}""",

        # Q5
        f"""Top 10% performers ({len(top10)} employees):
{top10[soft_cols].mean().round(2).to_string()}""",
    ]

    q   = questions[question_index]
    ctx = contexts[question_index]
    ans = ask_claude(q, ctx)

    return q, ctx, ans
