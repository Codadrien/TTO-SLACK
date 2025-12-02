import requests
import os
import json
import sys
from datetime import datetime
import pytz

# Webhook Slack (sera défini dans les secrets GitHub)
WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK")

# Fuseau horaire Paris
PARIS_TZ = pytz.timezone("Europe/Paris")

# Mapping des noms vers les User IDs Slack
USER_IDS = {
    "Arnaud": "<@U04JBM2N285>",
    "Arthur": "<@U05D4LENHEE>",
    "Lou": "<@U05B1HZ6AU9>",
    "Camille G": "<@U04H95BL2GN>",
    "Adrien": "<@U08A2348NTS>",
    "Nicolas": "<@U0768DLD5PG>",
    "Camille L": "<@U0764ABCC14>",
    "Pierre": "<@U072Y1NSDF0>",
    "Lucas": "<@U07MC2TBLKY>",
    "Tobias": "<@U0764AAM4MU>",
    "Maëlan": "<@U04MD04GW94>",
    "Kevin": "<@U04BTKLK5KK>",
    "JC": "<@U07T534C2P8>",
}

def load_rotation():
    with open("rotation.json", "r", encoding="utf-8") as f:
        return json.load(f)

def get_people_for_date(date_str):
    data = load_rotation()
    if date_str in data:
        return data[date_str]["personnes"]
    return None

def send_reminder(test_date=None):
    # Utilise la date de test si fournie, sinon la date actuelle
    if test_date:
        date_str = test_date
    else:
        now = datetime.now(PARIS_TZ)
        date_str = now.strftime("%Y-%m-%d")

    print(f"📅 Date: {date_str}")

    # Récupère les personnes du jour
    personnes = get_people_for_date(date_str)

    if personnes is None:
        print("❌ Pas de rotation prévue pour cette date")
        return

    # Convertit les noms en mentions Slack
    mentions = " ".join([USER_IDS.get(p, p) for p in personnes])
    noms = ", ".join(personnes)

    # Construit le message
    message = {
        "text": f"🔔 *RAPPEL TEST SITE*\n\nAujourd'hui c'est au tour de {mentions} de faire les tests.\n\n📋 <https://docs.google.com/spreadsheets/d/1IN12Idjt2yikYdtEAutw6Ko9FMWjzVIrj0TdLgFPVHg/edit|Lien du doc à remplir>\n\nMerci de mettre un ✅ quand c'est fait !"
    }

    print(f"👥 Personnes du jour: {noms}")

    # Envoie vers Slack
    response = requests.post(WEBHOOK_URL, json=message)

    if response.status_code == 200:
        print("✅ Rappel envoyé avec succès !")
    else:
        print(f"❌ Erreur: {response.status_code}")

if __name__ == "__main__":
    # Récupère la date de test depuis les arguments ou variable d'env
    test_date = os.environ.get("TEST_DATE") or (sys.argv[1] if len(sys.argv) > 1 else None)
    send_reminder(test_date)
