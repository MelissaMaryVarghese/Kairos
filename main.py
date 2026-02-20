from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import analyze_text

app = FastAPI()

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze(input: TextInput):
    result = analyze_text(input.text)
    return result

@app.get("/")
def home():
    return {"message": "SynapseCX API Running"}