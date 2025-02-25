import sqlite3

conn = sqlite3.connect("archivio_infinito.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tabelle nel database:", tables)

conn.close()
