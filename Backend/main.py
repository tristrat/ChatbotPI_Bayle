from openai import OpenAI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import string
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def analyze_texte(texte :str):
    mot_cle=nltk.word_tokenize(texte)
    return {"sujet":"vide","sentiments":[],"mot_cles":mot_cle}

def generer_reponse(texte: str):
    return {"reponse":"reponse vide"}

def formater_reponse(texte: str):
    return {"reponse_formater":"reponse vide formater"}

class AnalyseTexteInput(BaseModel):
    texte: str

@app.post("/analyse")
def analyse_endpoint(analyse_input: AnalyseTexteInput):
    #miniscule
    texte=(analyse_input.texte).lower()
    words=nltk.word_tokenize(texte)
    #stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in words if word not in stop_words]
    #suppression des ponctuations
    tokens = [word for word in tokens if word.lower() not in string.punctuation]

    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]

    query = " ".join(lemmatized_words)
    #OpenAI
    reponse=query_openai(query)
    return {"msg": reponse}

@app.post("/query_openai")
def query_openai(query: str):
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    if not openai_api_key:
        raise HTTPException(status_code=500, detail="API key not found in environment variables.")
    
    client = OpenAI(
    api_key=openai_api_key,
    )
    chat_completion = client.chat.completions.create(
model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a computer science university teacher"},
            {"role": "assistant", "content": "You are specialized in AI, machine learning, and deep learning"},
            {"role": "user", "content": query}
        ]
    )

    response = chat_completion.choices[0].message["content"]
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

