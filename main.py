from fastapi import FastAPI
import json
import random
from pathlib import Path

app = FastAPI()

@app.get("/")
def root():
  return {"Welcome to the quote api"}

path = Path(__file__).parent / "quotes.txt"

with open(path, "r", encoding="utf-8") as file:
  data = json.load(file)

quotes = data["quotes"]

@app.get("/quote")
def random_quote():
  return random.choice(quotes)