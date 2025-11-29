from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

class QuizRequest(BaseModel):
    task: str

@app.post("/quiz")
async def quiz_endpoint(data: QuizRequest):
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful quiz assistant."},
            {"role": "user", "content": data.task}
        ]
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # send request to Groq API
    response = requests.post(GROQ_URL, json=payload, headers=headers)
    result = response.json()

    answer = result["choices"][0]["message"]["content"]

    return {"answer": answer}

@app.get("/")
def home():
    return "Quiz system running with Groq LLM!"

