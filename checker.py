import os
import requests
import datetime
import json

# --- CONFIG ---
DEBUG = 0  # Set to 1 for local debug/test, 0 for GitHub Actions
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def main():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    date_str = yesterday.strftime("%Y-%m-%d")

    if DEBUG:
        print(f"[DEBUG] Checking games for: {date_str}")

    resp = requests.get("https://statsapi.mlb.com/api/v1/schedule",
                        params={'teamId': 119, 'sportId': 1, 'startDate': date_str, 'endDate': date_str})
    data = resp.json()
    

    games = data.get('dates', [])
    if not games:
        msg = f"No Dodgers game found on {date_str}."
        if DEBUG:
            print(f"[DEBUG] {msg}")
        return

    game = games[0]['games'][0]
    home_id = game['teams']['home']['team']['id']
    home_score = game['teams']['home']['score']
    away_score = game['teams']['away']['score']
    is_home = home_id == 119
    dodgers_won = home_score > away_score if is_home else away_score > home_score

    if DEBUG:
        print(f"[DEBUG] API response: {json.dumps(data, indent=4)}")
        print(f"[DEBUG] Game Info:")
        print(f"[DEBUG]  Dodgers were home: {is_home}")
        print(f"[DEBUG]  Final Score: Home {home_score} – Away {away_score}")
        print(f"[DEBUG]  Dodgers won: {dodgers_won}")

    coupon_active = False
    if is_home and home_score > away_score:
        msg = f"⚾ @here **Dodgers won at home yesterday!** Coupon active today 🍜"
        coupon_active = True
    elif is_home and home_score <= away_score:
        msg = f"⚾ Dodgers **played at home on {date_str}** but lost. No coupon today."
    else:
        msg = f"🚫 Dodgers **didn't play at home** on {date_str}. No coupon today. 🚫 "

    if DEBUG and WEBHOOK_URL:
        print(f"[DEBUG] Sending message to Discord: {msg}")
        requests.post(WEBHOOK_URL, json={"content": msg})
    elif coupon_active and WEBHOOK_URL:
        print(f"[DEBUG] Sending message to Discord: {msg}")
        requests.post(WEBHOOK_URL, json={"content": msg})
        requests.post(WEBHOOK_URL, json={"content": "dodgerswin"})
    else:
        print(f"No webhook url, no message sent. {msg}")
        

if __name__ == "__main__":
    main()
