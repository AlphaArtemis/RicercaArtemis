import schedule
import time
import json
import os
import random

from search_api import google_search  # Assicurati che sia il file corretto per le ricerche

# Percorso file di parole chiave
parole_chiave_file = "parole_chiave.txt"
# Percorso file che tiene traccia delle ultime ricerche
ultime_ricerche_file = "ultime_ricerche.json"

# Carica tutte le parole chiave dal file
with open(parole_chiave_file, "r", encoding="utf-8") as f:
    all_keywords = [line.strip() for line in f.readlines() if line.strip()]

# Carica le ultime parole chiave usate per evitare ripetizioni
if os.path.exists(ultime_ricerche_file):
    with open(ultime_ricerche_file, "r", encoding="utf-8") as f:
        ultime_ricerche = json.load(f)
else:
    ultime_ricerche = []

# Se ci sono troppe parole esclude quelle già usate
parole_disponibili = [word for word in all_keywords if word not in ultime_ricerche]

# Se non ci sono abbastanza parole disponibili, resetta la memoria delle ultime ricerche
if len(parole_disponibili) < 4:
    parole_disponibili = all_keywords.copy()
    ultime_ricerche = []

# Seleziona 4 nuove parole chiave casuali senza ripetizioni
nuove_ricerche = random.sample(parole_disponibili, 4)

# Aggiorna la memoria delle ultime ricerche
ultime_ricerche = nuove_ricerche

# Salva le ultime ricerche per evitare ripetizioni nei prossimi cicli
with open(ultime_ricerche_file, "w", encoding="utf-8") as f:
    json.dump(ultime_ricerche, f, indent=2)

# Percorso del file di output
output_file = "ricerche.json"

def esegui_ricerche():
    risultati = []
    for keyword in nuove_ricerche:
        print(f"Eseguo ricerca per: {keyword}")
        risultati.append({
            "keyword": keyword,
            "risultati": google_search(keyword, num_results=5)
        })

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"results": risultati}, f, indent=2)

    print(f"✅ Ricerche salvate in {output_file}")

# Imposta la programmazione della ricerca
schedule.every(7).minutes.do(esegui_ricerche)  # Modifica l'intervallo se necessario

while True:
    schedule.run_pending()
    time.sleep(1)
