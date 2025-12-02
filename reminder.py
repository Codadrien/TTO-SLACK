import requests
import os
from datetime import datetime
import pytz

# Webhook Slack (sera défini dans les secrets GitHub)
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK")

# Fuseau horaire Paris
PARIS_TZ = pytz.timezone("Europe/Paris")

# ROTATION PAR JOUR - Remplace les User IDs par les vrais
# Format: jour -> liste des personnes du jour
ROTATION = {
    0: ["<@U08A2348NTS>"],  # Lundi
    1: ["<@U08A2348NTS>"],  # Mardi
    2: ["<@U08A2348NTS>"],  # Mercredi
    3: ["<@U08A2348NTS>"],  # Jeudi
    4: ["<@U08A2348NTS>"],  # Vendredi
}

def send_reminder():
    # Récupère le jour actuel (0=lundi, 4=vendredi)
    now = datetime.now(PARIS_TZ)
    jour = now.weekday()

    # Vérifie que c'est un jour de semaine
    if jour > 4:
        print("Weekend - pas d'envoi")
        return

    # Récupère les personnes du jour
    personnes = ROTATION.get(jour, [])
    mentions = " ".join(personnes)

    # Construit le message
    message = {
        "text": f"🔔 *RAPPEL TEST SITE*\n\nAujourd'hui c'est au tour de {mentions} de faire les tests.\n\nMerci de mettre une coche ✅ *Valider* quand c'est fait !"
    }

    # Envoie vers Slack
    response = requests.post(WEBHOOK_URL, json=message)

    if response.status_code == 200:
        print("✅ Rappel envoyé avec succès !")
    else:
        print(f"❌ Erreur: {response.status_code}")

if __name__ == "__main__":
    send_reminder()
