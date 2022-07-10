from typing import Union

from fastapi import FastAPI

app = FastAPI()

class Sentence(BaseModel):
    sentence: str

@app.get("/")
def index():
    return {"ping": "pong"}


@app.put("/correct")
def read_item(sentence: Sentence, q: Union[str, None] = None):
    return {"sentence": sentence, "corrected": sentence}
