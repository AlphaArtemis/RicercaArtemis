import schedule
import time
import json
import os
import random
from search_api import google_search  # Assicurati che search_api.py sia corretto
from archivio_infinito import salva_nel_database  # Importa la funzione per salvare nel database

# Percorso del file delle parole chiave
PAROLE_CHIAVE_FILE = "parole_chiave.txt"

# Percorso del file JSON dove salvare i risultati temporanei
RICERCHE_FILE = "ricerche.json"

# Carica le parole chiave dal file
def carica_parole_chiave():
    try:
        with open(PAROLE_CHIAVE_FILE, "r", encoding="utf-8") as file:
            keywords = [line.strip() for line in file.readlines() if line.strip()]
        return keywords
    except FileNotFoundError:
        print("⚠️ File parole_chiave.txt non trovato!")
        return []

# Esegue le ricerche selezionando casualmente 4 parole chiave diverse ogni ciclo
def esegui_ricerche():
    keywords = carica_parole_chiave()

    if len(keywords) < 4:
        print("⚠️ Non ci sono abbastanza parole chiave per eseguire 4 ricerche.")
        return

    keywords_da_cercare = random.sample(keywords, 4)  # Prende 4 parole casuali

    risultati = []
    for keyword in keywords_da_cercare:
        print(f"🔎 Eseguo ricerca per: {keyword}")
        risultati_query = google_search(keyword, num_results=5)  # Modifica il numero di risultati se necessario
        risultati.append({"keyword": keyword, "risultati": risultati_query})

        # Salva immediatamente nel database
        salva_nel_database(keyword, risultati_query)

    # Salva i risultati temporanei in ricerche.json
    with open(RICERCHE_FILE, "w", encoding="utf-8") as file:
        json.dump({"results": risultati}, file, indent=4, ensure_ascii=False)

    print("✅ Ricerche completate e salvate.")

# Programma l'esecuzione automatica ogni 7.5 minuti
schedule.every(7.5).minutes.do(esegui_ricerche)  # Modifica il valore se necessario

print("🟢 Search Scheduler avviato...")

# Loop infinito per gestire le ricerche pianificate
while True:
    schedule.run_pending()
    time.sleep(30)  # Controlla ogni 30 secondi se è il momento di eseguire una ricerca
