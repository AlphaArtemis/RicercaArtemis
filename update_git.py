import os
import subprocess

def aggiorna_github():
    try:
        # Aggiunge il file ricerche.json al commit
        subprocess.run(["git", "add", "ricerche.json"], check=True)
        
        # Crea il commit con un messaggio automatico
        subprocess.run(["git", "commit", "-m", "Aggiornamento automatico ricerche"], check=True)
        
        # Pusha le modifiche su GitHub
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("✅ Aggiornamento completato e caricato su GitHub!")
    
    except subprocess.CalledProcessError as e:
        print("❌ Errore durante l'aggiornamento:", e)

if __name__ == "__main__":
    aggiorna_github()
