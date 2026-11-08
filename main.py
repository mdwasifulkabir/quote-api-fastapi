from fastapi import FastAPI
import json
import random
from pathlib import Path
from fastapi import HTTPException

from pydantic import BaseModel, Field

class Quote(BaseModel):
  quote: str = Field(min_length=5)
  author: str

class QuoteWithID(BaseModel):
  id: int
  quote: str = Field(min_length=5)
  author: str

app = FastAPI()

@app.get("/")
def root():
  return {"message": "Welcome to the quote api"}

path = Path(__file__).parent / "quotes.txt"

with open(path, "r", encoding="utf-8") as file:
  data = json.load(file)

quotes = data["quotes"]

@app.get("/quotes", response_model = Quote)
def all_quotes(author: str | None = None):
  if author is None:
    return quotes

  results = [
    quote for quote in quotes
    if author.lower() in quote["author"].lower()
  ]

  return results

@app.get("/quotes/{item_id}", response_model = Quote)
def get_quote(item_id: int):
  if item_id < 0 or item_id >= len(quotes):
    raise HTTPException(status_code=404, detail="Quote not found")

  return quotes[item_id]

@app.get("/quote", response_model= Quote)
def random_quote():
  return random.choice(quotes)

@app.post("/quotes/", response_model=QuoteWithID, status_code=201)
def post_quote(quote: Quote):
  quotes.append(quote.model_dump())

  return {
    id: len(quotes)-1
    **quote.model_dump()
  }

@app.put("/quotes/{item_id}", response_model=Quote)
def edit_quote(quote: Quote, item_id: int):
  if item_id < 0 or item_id >= len(quotes):
    raise HTTPException(
      status_code=404,
      detail= "Quote Not Found"
    )

  quotes[item_id] = quote.model_dump()
  return quote

@app.delete("/quotes/{item_id}")
def delete_quote(item_id: int):
  if item_id < 0 or item_id >= len(quotes):
    raise HTTPException(
      status_code= 404,
      detail= "Quote Not Found"
    )

  del quotes[item_id]