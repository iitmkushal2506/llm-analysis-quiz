from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# ⬇️ Add this
@app.get("/")
def home():
    return {"message": "LLM Quiz API is running 🚀"}

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

class QuizRequest(BaseModel):
    task: str

@app.post("/quiz")
async def quiz_endpoint(data: QuizRequest):
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [{"role": "user", "content": data.task}]
    }
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}

    response = requests.post(GROQ_URL, json=payload, headers=headers).json()
    answer = response["choices"][0]["message"]["content"]

    return {"answer": answer}
