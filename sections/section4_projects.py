# ============================================================
#  sections/section4_projects.py
#  Section 4: Project & Work Performance Analysis
# ============================================================

from data_loader import load_data, get_stats, filter_rows, group_mean
from ai_engine import ask_gemini as ask_claude

def run(question_index=0):
    df = load_data()

    questions = [
        "How do Project Complexity and Project Size influence Project Outcome?",
        "Identify patterns among employees involved in successful vs failed projects.",
        "What combination of skills and ratings leads to successful project outcomes?",
        "Compare performance of employees across different Project Roles (Manager vs Developer vs Analyst).",
    ]

    contexts = [
        # Q1
        f"""Project Complexity vs Outcome:\n{df.groupby(['Project_Complexity','Project_Outcome']).size().unstack(fill_value=0).to_string()}
Project Size vs Outcome:\n{df.groupby(['Project_Size','Project_Outcome']).size().unstack(fill_value=0).to_string()}""",

        # Q2
        f"""Performance by Project Outcome:
{group_mean(df, 'Project_Outcome', 'Performance_Rating')}
Skill ratings by outcome:
{df.groupby('Project_Outcome')[['Technical_Skills_Rating','Communication_Skills_Rating','Problem_Solving_Skills_Rating']].mean().round(2).to_string()}""",

        # Q3
        f"""Project outcome counts:
{df['Project_Outcome'].value_counts().to_string()}
Avg skills for Successful projects:
{df[df['Project_Outcome']=='Successful'][['Technical_Skills_Rating','Communication_Skills_Rating','Problem_Solving_Skills_Rating','Leadership_Qualities_Rating','Teamwork_Skills_Rating']].mean().round(2).to_string()}
Avg skills for Failed projects:
{df[df['Project_Outcome']=='Failed'][['Technical_Skills_Rating','Communication_Skills_Rating','Problem_Solving_Skills_Rating','Leadership_Qualities_Rating','Teamwork_Skills_Rating']].mean().round(2).to_string()}""",

        # Q4
        f"""Project Role vs Outcome:\n{df.groupby(['Project_Role','Project_Outcome']).size().unstack(fill_value=0).to_string()}
Avg Performance by Role:
{group_mean(df, 'Project_Role', 'Performance_Rating')}""",
    ]

    q   = questions[question_index]
    ctx = contexts[question_index]
    ans = ask_claude(q, ctx)
    return q, ctx, ans
