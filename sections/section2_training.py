# ============================================================
#  sections/section2_training.py
#  Section 2: Training, Mentorship & Development
# ============================================================

from data_loader import load_data, get_stats, filter_rows, correlation, group_mean
from ai_engine import ask_gemini as ask_claude

def run(question_index=0):
    df = load_data()

    questions = [
        "Do Professional Development Hours correlate with Performance Rating and Promotions?",
        "What is the impact of Mentor Rating and Mentor Experience Level on Internship Conversion and Performance?",
        "Identify employees who received training but show low performance. Generate hypotheses.",
        "Compare Basic vs Advanced Training Program effects on performance and career growth.",
        "Predict which employees are likely to benefit most from advanced training programs.",
    ]

    converted     = filter_rows(df, 'Internship_Conversion_Status', 'eq', 'Converted')
    not_converted = filter_rows(df, 'Internship_Conversion_Status', 'eq', 'Not Converted')

    contexts = [
        # Q1
        f"""Dev Hours vs Performance corr : {correlation(df, 'Professional_Development_Hours', 'Performance_Rating')}
Dev Hours vs Promotions corr   : {correlation(df, 'Professional_Development_Hours', 'Number_Of_Promotions')}
Stats:\n{get_stats(df, ['Professional_Development_Hours', 'Performance_Rating', 'Number_Of_Promotions'])}""",

        # Q2
        f"""Internship Conversion counts:
{df['Internship_Conversion_Status'].value_counts().to_string()}
Avg Mentor Rating — Converted    : {converted['Mentor_Rating'].mean():.2f}
Avg Mentor Rating — Not Converted: {not_converted['Mentor_Rating'].mean():.2f}
Mentor Experience vs Conversion:
{group_mean(df, 'Mentor_Experience_Level', 'Performance_Rating')}""",

        # Q3
        f"""Training program avg performance:
{group_mean(df, 'Training_Program', 'Performance_Rating')}
Low performers (<=5) who had Advanced training:
{len(filter_rows(df[df['Training_Program']=='Advanced'], 'Performance_Rating', 'lte', 5))}""",

        # Q4
        f"""Training program performance comparison:
{group_mean(df, 'Training_Program', 'Performance_Rating')}
Training program promotion comparison:
{group_mean(df, 'Training_Program', 'Number_Of_Promotions')}""",

        # Q5
        f"""Performance distribution:
{df['Performance_Rating'].describe().round(2).to_string()}
Training program counts:
{df['Training_Program'].value_counts().to_string()}
Dev hours stats:
{get_stats(df, ['Professional_Development_Hours'])}""",
    ]

    q   = questions[question_index]
    ctx = contexts[question_index]
    ans = ask_claude(q, ctx)
    return q, ctx, ans
