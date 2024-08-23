from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.scrape import scrape
from src.analyze import analyze_document

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlInput(BaseModel):
    url: str

@app.post("/analyze")
async def analyze(input: UrlInput):
    doc = await scrape(input.url)
    analysis = analyze_document(doc['content'])
    return analysis["user_friendly_summary"]

    