import sqlite3
import json
import time
import schedule
from search_api import google_search  # Assicurati che il file search_api.py sia corretto

# Percorso del file JSON contenente le ricerche
RICERCHE_FILE = "ricerche.json"

# Nome del database SQLite
DB_NAME = "archivio_infinito.db"

# Creazione della tabella se non esiste
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ricerche (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parola_chiave TEXT NOT NULL,
            risultati TEXT NOT NULL,
            categoria TEXT,
            fonte TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database configurato correttamente.")

# Salva i risultati nel database
def salva_nel_database(keyword, risultati):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ricerche (parola_chiave, risultati, categoria, fonte)
        VALUES (?, ?, ?, ?)
    ''', (keyword, json.dumps(risultati), "AI", "Google Custom Search"))
    conn.commit()
    conn.close()
    print(f"✅ Salvata ricerca '{keyword}' nel database.")

# Carica le ricerche dal file JSON
def carica_ricerche():
    try:
        with open(RICERCHE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else data.get("results", [])
    except (FileNotFoundError, json.JSONDecodeError):
        print("⚠️ Nessun file ricerche.json trovato o file vuoto.")
        return []

# Esegue le ricerche e salva i risultati nel database
def esegui_ricerche():
    ricerche = carica_ricerche()
    if not ricerche:
        print("⚠️ Nessuna ricerca da eseguire.")
        return

    for ricerca in ricerche:
        keyword = ricerca.get("keyword", "")
        risultati = google_search(keyword, num_results=5)  # Modifica il numero di risultati se necessario
        salva_nel_database(keyword, risultati)

# Programma l'esecuzione automatica delle ricerche ogni X minuti
schedule.every(7.5).minutes.do(esegui_ricerche)  # Modifica il valore in base alla quota API disponibile

# Configura il database all'avvio
setup_database()

print("🟢 Sistema di ricerca e archiviazione avviato...")

# Loop infinito per eseguire le ricerche automaticamente
while True:
    schedule.run_pending()
    time.sleep(30)  # Controlla ogni 30 secondi se è il momento di eseguire una ricerca

