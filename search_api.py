from fastapi import FastAPI
import requests
import json
from config import API_KEY, SEARCH_ENGINE_ID  # Assicurati che il file config.py esista e sia corretto

app = FastAPI()

@app.get("/search/")
def google_search(query: str, num_results: int = 5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "num": num_results
    }
    
    response = requests.get(url, params=params)
    results = response.json()

    if "items" in results:
        return {"results": [{"title": item["title"], "link": item["link"]} for item in results["items"]]}
    else:
        return {"error": "Nessun risultato trovato."}

# Per avviare il server:
# uvicorn search_api:app --host 0.0.0.0 --port 8000

