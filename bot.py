import requests
from telegram import Bot
import time
import os
TOKEN = os.getenv("7984815467:AAE-apCVpIILdnYyizB04EV9Iia3rarjNjw")
CHAT_ID = os.getenv("8325310989")
API_KEY = os.getenv("5b1a48954a206a6f0eb86f41bc8563fb")
bot = Bot(token=TOKEN)
sent_matches = set()
def get_live():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {"x-apisports-key": API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()
def analyze():
    try:
        data = get_live()
        for match in data['response']:
            fixture_id = match['fixture']['id']
            if fixture_id in sent_matches:
                continue
            minute = match['fixture']['status']['elapsed']
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            hg = match['goals']['home']
            ag = match['goals']['away']
            stats = match.get('statistics', [])
            shots = 0
            shots_on = 0
            attacks = 0
            for team in stats:
                for s in team['statistics']:
                    if s['type'] == "Total Shots":
                        shots += int(s['value'] or 0)
                    if s['type'] == "Shots on Goal":
                        shots_on += int(s['value'] or 0)
                    if s['type'] == "Dangerous Attacks":
                        attacks += int(s['value'] or 0)
            score = 0
            if shots >= 8:
                score += 1
            if shots_on >= 3:
                score += 1
            if attacks >= 20:
                score += 1
            if minute and 20 <= minute <= 40:
                if hg == 0 and ag == 0:
                    if score >= 3:
                        msg = f"""
🔥 PRO SİNYAL 🔥
⚽ {home} vs {away}
⏱ Dakika: {minute}
📊 Şut: {shots}
🎯 İsabetli: {shots_on}
⚡ Atak: {attacks}
💎 SKOR: {score}/3
🚀 0.5 ÜST GELME İHTİMALİ YÜKSEK
"""
bot.send_message(chat_id=CHAT_ID, text=msg)
                        sent_matches.add(fixture_id)
    except Exception as e:
        print("Hata:", e)
while True:
    analyze()
    time.sleep(60)
