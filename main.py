from fastapi import FastAPI
import json
import random
from pathlib import Path
from fastapi import HTTPException

app = FastAPI()

@app.get("/")
def root():
  return {"Welcome to the quote api"}

path = Path(__file__).parent / "quotes.txt"

with open(path, "r", encoding="utf-8") as file:
  data = json.load(file)

quotes = data["quotes"]

@app.get("/quotes")
def all_quotes(author: str | None = None, ):
  if author is None:
    return quotes

  results = [
    quote for quote in quotes
    if author.lower() in quote["author"].lower()
  ]

  return results

@app.get("/quotes/{item_id}")
def get_quote(item_id: str):
  try:
    return quotes[item_id]
  except:
    return HTTPException

@app.get("/quote")
def random_quote():
  return random.choice(quotes)

@app.get("/quote/{quote_id}")
def get_quote_by_id():
  return quotes[quote]