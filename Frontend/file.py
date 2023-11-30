from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class AnalyseTexteInput(BaseModel):
    texte: str

@app.post("/analyse")
def analyse_endpoint(analyse_input: AnalyseTexteInput):
    print(analyse_input)
    return {"msg": analyse_input}
