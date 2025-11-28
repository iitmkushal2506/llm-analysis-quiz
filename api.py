from fastapi import FastAPI, Request

app = FastAPI()

SECRET = "XYZ123"   # your secret value

@app.post("/quiz")
async def quiz_endpoint(request: Request):
    data = await request.json()
    return {"received": data}

