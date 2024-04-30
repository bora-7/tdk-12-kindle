import sqlite3
from pydantic import BaseModel
from typing import List

from fastapi import (
    FastAPI,
    Query,
    HTTPException,
)
from fastapi.middleware.cors import CORSMiddleware


class WordDefinitionModel(BaseModel):
    type: str
    definitions: List[str]


app = FastAPI()

# Allow requests from these origins
origins = [
    "https://api.boraakyuz.me",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search_word")
def search_word(word: str = Query(..., min_length=2)):
    conn = sqlite3.connect("tdk12.db")
    cursor = conn.cursor()

    query = "SELECT word FROM dictionary WHERE word LIKE ? LIMIT 5"

    search_term = f"{word}%"

    cursor.execute(query, (search_term,))
    results = cursor.fetchall()

    matching_words = [row[0] for row in results]

    cursor.close()
    conn.close()
    return {"matching_words": matching_words}


@app.get("/get_definitions/{word}")
def get_definitions(word: str):
    conn = sqlite3.connect("tdk12.db")
    cursor = conn.cursor()

    cursor.execute("SELECT meanings FROM dictionary WHERE UPPER(word) = UPPER(?)", (word,))
    result = cursor.fetchone()

    if not result:
        raise HTTPException(status_code=400, detail="Definition not found!")

    cursor.close()
    conn.close()
    meanings = result[0]
    return {"definitions": meanings}
        
