import os
import subprocess
import sys
import time

VENV_DIR = "monenv"
PYTHON_EXEC = os.path.join(VENV_DIR, "bin", "python3") if os.name != "nt" else os.path.join(VENV_DIR, "Scripts", "python.exe")

if not os.path.isdir(VENV_DIR):
    print("[INFO] Création de l'environnement virtuel...")
    subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

print("[INFO] Installation des dépendances...")
print(f"[DEBUG] Installation avec : {PYTHON_EXEC} -m pip install -r requirements.txt")
subprocess.check_call([PYTHON_EXEC, "-m", "pip", "install", "-r", "requirements.txt"])

while True:
    print("[INFO] Lancement du bot Discord...")
    code = subprocess.call([PYTHON_EXEC, "bot.py"])
    print(f"[ERREUR] Le bot s'est arrêté avec le code {code}. Relance dans 5 secondes...")
    time.sleep(5)
