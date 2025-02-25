import sqlite3

# Connessione al database (se non esiste, lo crea)
conn = sqlite3.connect("archivio_infinito.db")
cursor = conn.cursor()

# Creazione della tabella per memorizzare le ricerche
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ricerche (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        parola_chiave TEXT,
        risultati TEXT,
        categoria TEXT,
        fonte TEXT
    )
''')

# Salva le modifiche e chiude la connessione
conn.commit()
conn.close()

print("✅ Database 'archivio_infinito.db' creato con successo!")
