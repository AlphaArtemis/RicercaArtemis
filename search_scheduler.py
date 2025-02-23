import schedule
import time
import json
import os
from search_api import google_search  # Assicurati che sia il file corretto per le ricerche

# Lista delle ricerche da eseguire
keywords = ["Cyber Biologia", "Simbiosi AI e Umani", "Artemis Evoluzione"]

# Percorso del file di output
output_file = "ricerche.json"

def esegui_ricerche():
    risultati = []
    
    for keyword in keywords:
        print(f"Eseguo ricerca per: {keyword}")
        risultati.append({
            "keyword": keyword,
            "risultati": google_search(keyword, num_results=5)  # Modifica il numero di risultati se vuoi
        })

    # Salva i risultati nel file JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(risultati, f, indent=4, ensure_ascii=False)
    
    print(f"Ricerche salvate in {output_file}")

    # Caricamento automatico su GitHub
    push_to_github()

def push_to_github():
    """Esegue il push automatico delle ricerche su GitHub"""
    os.system("git add ricerche.json")
    os.system('git commit -m "Aggiornamento ricerche"')
    os.system("git push origin main")

# Programma la ricerca ogni minuto (puoi cambiare l'intervallo)
schedule.every(1).minutes.do(esegui_ricerche)  # Cambia il valore per impostare l'orario preferito

while True:
    schedule.run_pending()
    time.sleep(60)  # Controlla ogni minuto se è ora di eseguire la ricerca
