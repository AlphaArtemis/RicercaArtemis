import schedule
import time
import json
import os
from search_api import google_search  # Assicurati che sia il file corretto per le ricerche

# Lista delle ricerche da eseguire
with open("parole_chiave.txt", "r", encoding="utf-8") as f:
    all_keywords = [line.strip().replace("[", "").replace("]", "") for line in f.readlines() if line.strip()]

# Prendi solo 4 ricerche alla volta, cambiandole ad ogni ciclo
from random import sample
keywords = sample(all_keywords, 4) if len(all_keywords) >= 4 else all_keywords

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
    time.sleep(450)  # 450 secondi = 7.5 minuti per 8 ricerche all'ora

import os

# Dopo aver salvato i risultati
os.system("git add ricerche.json")
os.system('git commit -m "Aggiornamento ricerche notturne"')
os.system("git push origin main")

import subprocess

# Dopo aver salvato i risultati, aggiorniamo GitHub
subprocess.run(["python", "update_git.py"])

import json
import os
from datetime import datetime

ARCHIVE_FILE = "archivio_ricerche.json"
SEARCH_RESULTS_FILE = "ricerche.json"

def salva_in_archivio():
    """Aggiunge le nuove ricerche all'archivio senza sovrascrivere i vecchi dati"""
    if not os.path.exists(ARCHIVE_FILE):
        with open(ARCHIVE_FILE, "w") as f:
            json.dump([], f)

    with open(SEARCH_RESULTS_FILE, "r") as f:
        nuovi_dati = json.load(f)

    with open(ARCHIVE_FILE, "r+") as f:
        archivio = json.load(f)
        for ricerca in nuovi_dati:
            ricerca["timestamp"] = datetime.now().isoformat()
            archivio.append(ricerca)

        f.seek(0)
        json.dump(archivio, f, indent=4)

if __name__ == "__main__":
    salva_in_archivio()
    print("Archivio aggiornato con le nuove ricerche!")

import os

# Dopo aver salvato le ricerche
os.system("python archivio.py")

import os
os.system("python archivio.py")
