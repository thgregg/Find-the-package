from flask import Flask, jsonify, render_template
import csv
import os
from datetime import datetime, timedelta
import threading
import time

app = Flask(__name__)
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def get_balloon_filename():
    """ Génère le nom du fichier CSV en fonction de l'heure de lancement. """
    now = datetime.utcnow()
    launch_hour = 0 if now.hour < 12 else 12
    launch_time = now.replace(hour=launch_hour, minute=0, second=0, microsecond=0)
    return os.path.join(DATA_DIR, f"ballon_{launch_time.strftime('%Y-%m-%d_%H-%M')}.csv")

def simulate_balloon():
    """ Simule la trajectoire du ballon en ajoutant des points toutes les 10 secondes. """
    while True:
        filename = get_balloon_filename()
        lat, lon = 43.5775, 1.3766  # Coordonnées de départ

        if not os.path.exists(filename):  # Si le fichier n'existe pas, on le crée
            with open(filename, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["datetime", "lat", "lon"])

        # Ajouter une nouvelle position toutes les 10 secondes
        while datetime.utcnow().strftime("%H:%M") in ["00:00", "12:00"] or os.path.exists(filename):
            lat += 0.001  # Simulation de déplacement
            lon += 0.001
            with open(filename, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([datetime.utcnow().isoformat(), lat, lon])
            time.sleep(10)  # Mettre à jour toutes les 10 secondes

# Démarrer la simulation en arrière-plan
threading.Thread(target=simulate_balloon, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    """ Retourne les données du dernier fichier CSV actif. """
    filename = get_balloon_filename()
    if not os.path.exists(filename):
        return jsonify([])

    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({"datetime": row["datetime"], "lat": float(row["lat"]), "lon": float(row["lon"])})

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
