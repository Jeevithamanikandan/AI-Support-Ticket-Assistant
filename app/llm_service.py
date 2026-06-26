# app/llm_service.py

import json
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-3.1-flash-lite")


PROMPT = """
You are a Python Pandas expert.

The dataframe name is df.

Columns:

ticket_id
created_at
category
priority
status
response_time_hrs
resolution_time_hrs
agent_id
customer_rating
issue_summary

Generate ONLY ONE valid pandas expression.

Rules:

1. Return JSON only.
2. Do not explain.
3. Do not use print().
4. Use ONLY dataframe df.
5. Output format:

{
 "code":"..."
}

Examples

Question:
How many tickets are open?

{
 "code":"len(df[df['status']=='Open'])"
}

Question:
Average customer rating for Technical category

{
 "code":"df[df['category']=='Technical']['customer_rating'].mean()"
}

Question:
Highest resolution time

{
 "code":"df['resolution_time_hrs'].max()"
}

Question:
Lowest customer rating

{
 "code":"df['customer_rating'].min()"
}

Question:
Which agent resolved the most tickets?

{
 "code":"df[df['status']=='Resolved'].groupby('agent_id').size().idxmax()"
}
"""


class GeminiService:

    def __init__(self):
        self.model = model

    def generate_code(self, question):

        response = self.model.generate_content(
            PROMPT + "\n\nQuestion:\n" + question
        )

        text = response.text.strip()

        text = text.replace("```json", "")
        text = text.replace("```", "")

        data = json.loads(text)

        return data["code"]

    def format_answer(self, question, result):

        prompt = f"""

Question:

{question}

Result:

{result}

Answer in one professional sentence.

"""

        response = self.model.generate_content(prompt)

        return response.text.strip()