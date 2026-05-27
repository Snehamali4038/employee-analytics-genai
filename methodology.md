# Methodology & Approach

## Project Overview

This project solves the Quantiphi GenAI Data Analytics use case. The goal was to build an AI-powered tool that analyzes employee data and generates business insights using a Large Language Model (LLM).

The dataset contains 4000 employee records with 109 columns covering performance ratings, skills, salary, training, project outcomes, attrition and recruitment data.

---

## Approach — RAG (Retrieval Augmented Generation)

I used the RAG approach to make sure the AI answers are grounded in real data and not based on guesswork.

### What is RAG?

RAG stands for Retrieval Augmented Generation. It has 3 steps:

1. **Retrieve** — fetch relevant data from the source (CSV file)
2. **Augment** — add that data as context to the AI prompt
3. **Generate** — AI generates answers based on that real data

### Why RAG?

Without RAG, the AI would answer from its training knowledge which may be wrong or generic. With RAG, we pass actual numbers from the CSV so the AI can only reason on real data.

---

## How RAG Works in This Project

```
User selects a Section and Question
        ↓
section file loads the CSV using pandas
        ↓
Relevant columns are filtered and stats are calculated
(mean, correlation, group averages, counts etc.)
        ↓
Those real stats are added into the prompt as context
        ↓
Gemini API receives: context + question
        ↓
Gemini reasons only on the provided data
        ↓
Business insight with recommendations is shown in UI
```

---

## Data Retrieval — What Was Retrieved for Each Section

### Section 1 — Performance & Skills
- Columns used: Technical_Skills_Rating, Communication_Skills_Rating, Problem_Solving_Skills_Rating, Performance_Rating, Leadership_Potential
- Operations: correlation, group mean, describe stats, top 10% filter

### Section 2 — Training & Mentorship
- Columns used: Professional_Development_Hours, Training_Program, Mentor_Rating, Mentor_Experience_Level, Internship_Conversion_Status, Number_Of_Promotions
- Operations: correlation, group mean by training type, internship conversion counts

### Section 3 — Behavioral & Soft Skills
- Columns used: Leadership_Qualities_Rating, Teamwork_Skills_Rating, Adaptability_Rating, Creativity_Rating, Conflict_Resolution_Cases, Employee_Engagement_Score, Employee_Job_Satisfaction_Score, Initiative_Rating, Innovation_Projects_Involvement
- Operations: describe stats, correlation, group mean by resignation status

### Section 4 — Project Performance
- Columns used: Project_Complexity, Project_Size, Project_Outcome, Project_Role, Performance_Rating, Technical_Skills_Rating
- Operations: crosstab (complexity vs outcome), group mean by role, skill comparison by outcome

### Section 5 — Attrition & Retention
- Columns used: Employee_Resignation_Status, Employee_Work_Life_Balance_Rating, Overtime_Hours_Per_Week, Employee_Engagement_Score, Annual_Salary_Increase_Percentage, Employee_Job_Satisfaction_Score, Department
- Operations: filter resigned vs retained, compare averages, department-wise resignation count

### Section 6 — Compensation & Benefits
- Columns used: Annual_Salary_Increase_Percentage, Performance_Bonus_Percentage, Performance_Rating, Employee_Stock_Options, Employee_Health_Insurance_Coverage
- Operations: correlation, filter underpaid high performers, department breakdown

### Section 7 — Recruitment
- Columns used: Hiring_Source, Time_to_Hire, Recruitment_Cost, Performance_Rating, Employee_Job_Satisfaction_Score, Employee_Resignation_Status
- Operations: group mean by hiring source, resignation rate by source, cost comparison

---

## Assumptions Made

1. High performers are defined as employees with Performance_Rating >= 10
2. Low performers are defined as employees with Performance_Rating <= 5
3. Top 10% performers are employees above the 90th percentile of Performance_Rating
4. Underpaid high performers are defined as employees with Performance_Rating >= 12 AND Annual_Salary_Increase_Percentage <= 3%
5. All correlations are Pearson correlations calculated using pandas
6. Missing values are dropped before calculating statistics
7. Text columns like Yes/No are excluded from numeric operations

---

## Tools and Technologies Used

| Tool | Purpose |
|------|---------|
| Python | Main programming language |
| Pandas | Data loading, filtering, statistics |
| Streamlit | Web UI framework |
| Google Gemini API (gemini-2.5-flash) | LLM for reasoning and insight generation |
| Google GenAI Python SDK | Official library to call Gemini API |
| VS Code | Development environment |
| GitHub | Code repository and submission |

---

## Project Structure

Each section is kept in a separate file to make the code clean, readable and easy to maintain. This follows the Single Responsibility Principle — each file does only one job.

```
config.py          → stores API key and settings
data_loader.py     → all data reading and filtering functions
ai_engine.py       → all Gemini API calls
ui.py              → Streamlit UI
sections/          → one file per section (7 files)
```

---

---


