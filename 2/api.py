from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pln import search
import json

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def get_search_query(q: str):
  response = search(q)
  
  return response

@app.get("/search/{article}")
def get_search_article(article: str):
    with open("results.json", "r") as f:
        data = json.load(f)

    result = [obj for obj in data if obj['article'].split("/")[1] == article]
  
    return result