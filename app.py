from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


# ------------------------------
# Homepage (HTML UI)
# ------------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>
        <title>LLM Quiz System</title>
        <style>
            body { font-family: Arial; background: #f2f2f2; padding: 40px; }
            h1 { text-align: center; }
            .box { width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; }
            input, textarea, button { width: 100%; padding: 10px; margin-top: 10px; }
            button { background: #4CAF50; color: white; border: none; cursor: pointer; }
            button:hover { background: #45a049; }
        </style>
    </head>
    <body>
        <h1>LLM Quiz System</h1>
        <div class="box">
            <form method="post" action="/ask">
                <label>Enter your question:</label>
                <textarea name="query" rows="4" required></textarea>
                <button type="submit">Ask AI</button>
            </form>
        </div>
    </body>
    </html>
    """


# ------------------------------
# Handles Form Submission from UI
# ------------------------------
@app.post("/ask", response_class=HTMLResponse)
def ask_ai_ui(query: str = Form(...)):

    answer = call_groq(query)

    return f"""
    <html>
    <body style='font-family: Arial; padding: 40px;'>
        <h2>Your Question:</h2>
        <p>{query}</p>

        <h2>AI Answer:</h2>
        <p>{answer}</p>

        <br><br>
        <a href="/">Ask Another Question</a>
    </body>
    </html>
    """


# ------------------------------
# API endpoint (for the assignment)
# ------------------------------
class QuizRequest(BaseModel):
    task: str

@app.post("/quiz")
def quiz_endpoint(req: QuizRequest):
    result = call_groq(req.task)
    return {"answer": result}


# ------------------------------
# Groq API Caller Function
# ------------------------------
def call_groq(text):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": text}]
        }

        r = requests.post(GROQ_URL, json=payload, headers=headers)
        data = r.json()

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error calling AI: {str(e)}"
