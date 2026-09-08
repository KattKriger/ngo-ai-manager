import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(prompt):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": "You are an expert NGO data analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return completion.choices[0].message.content
