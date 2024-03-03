from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pln import search

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