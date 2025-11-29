from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class QuizRequest(BaseModel):
    task: str


@app.post("/quiz")
def quiz_endpoint(req: QuizRequest):

    # Call Groq LLM API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": req.task}
        ],
        "max_tokens": 200
    }

    try:
        r = requests.post(GROQ_URL, json=payload, headers=headers)
        result = r.json()

        reply = result["choices"][0]["message"]["content"]
        return {"answer": reply}

    except Exception as e:
        return {"error": str(e)}
