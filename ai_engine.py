# ============================================================
#  ai_engine.py  —  Talks to Google Gemini API (FREE)
# ============================================================

from google import genai
from config import GEMINI_API_KEY
import time

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(question: str, data_context: str) -> str:
    prompt = f"""You are an expert HR Data Analyst.
Analyze the following real employee data statistics and answer the question.

DATA FROM CSV:
{data_context}

QUESTION:
{question}

Give a clear, business-ready answer with:
1. Key finding from the data
2. Why this pattern exists (reasoning)
3. 2-3 actionable recommendations

Be specific with numbers. Keep it under 300 words."""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model    = "gemini-2.5-flash",
                contents = prompt
            )
            return response.text

        except Exception as e:
            err = str(e)
            if "429" in err or "quota" in err.lower():
                time.sleep(30)
                continue
            else:
                return f"Error: {err}"

    return "Gemini is busy. Please wait 1 minute and try again."