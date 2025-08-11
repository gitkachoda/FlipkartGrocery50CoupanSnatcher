import os
import time
import random
import string
import threading
import requests
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, jsonify

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_COUPON = os.getenv("BASE_COUPON")
COOKIES ="T=TI175183139606600189725678559092738797146168708042858256419461361772; AMCVS_17EB401053DAF4840A490D4C%40AdobeOrg=1; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C20312%7CMCMID%7C90164886726208731467425828578759474554%7CMCAID%7CNONE%7CMCOPTOUT-1754896321s%7CNONE; vh=915; vw=412; dpr=2.6249998807907104; K-ACTION=null; vd=VIFC2C21C09F074A73B5A41C063F536BBC-1754908986134-1.1754908986.1754908986.154511199; ULSN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjb29raWUiLCJhdWQiOiJmbGlwa2FydCIsImlzcyI6ImF1dGguZmxpcGthcnQuY29tIiwiY2xhaW1zIjp7ImdlbiI6IjUiLCJ1bmlxdWVJZCI6IlVVSTI1MDgwMzE0MTIyNTcwMEtHNTgxOFAiLCJma0RldiI6bnVsbH0sImV4cCI6MTc3MDY4OTAxNCwiaWF0IjoxNzU0OTA5MDE0LCJqdGkiOiI0ODk5NTZmZS1jMzI3LTQ0NmUtYjQzNi03ZWFlYzQ3NmQ2MDkifQ.vU_SwzSvAsN7smhVDUrY2lJfsOsdN8uomv2_17mCeio; at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNhNzdlZTgxLTRjNWYtNGU5Ni04ZmRlLWM3YWMyYjVlOTA1NSJ9.eyJleHAiOjE3NTQ5MTA4MTQsImlhdCI6MTc1NDkwOTAxNCwiaXNzIjoia2V2bGFyIiwianRpIjoiZTBkODZiMzktMjdmMC00OGZkLTk4MTctMzBiZDM1YWM0ZWM4IiwidHlwZSI6IkFUIiwiZElkIjoiVEkxNzUxODMxMzk2MDY2MDAxODk3MjU2Nzg1NTkwOTI3Mzg3OTcxNDYxNjg3MDgwNDI4NTgyNTY0MTk0NjEzNjE3NzIiLCJiSWQiOiJXWTlYUVciLCJrZXZJZCI6IlZJRkMyQzIxQzA5RjA3NEE3M0I1QTQxQzA2M0Y1MzZCQkMiLCJ0SWQiOiJtYXBpIiwiZWFJZCI6Ik9vQ3JMQ0NFYUZJVEloeUZrVmJwLXZfYVVNd19kUGdXenVuMGhwMnpKQTR5R2xNRDIyWWxVdz09IiwidnMiOiJMSSIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjN9.vKqq3vIzdKAPcjA5yiF6fiQ1_pFtB3jm0oYN0Z23D5Q; rt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhlM2ZhMGE3LTJmZDMtNGNiMi05MWRjLTZlNTMxOGU1YTkxZiJ9.eyJleHAiOjE3NzA4MDY2MTQsImlhdCI6MTc1NDkwOTAxNCwiaXNzIjoia2V2bGFyIiwianRpIjoiODlhM2Y2MzYtODdjMy00ZmU2LWE3MWUtMDdmNTIzZjcwYjI4IiwidHlwZSI6IlJUIiwiZElkIjoiVEkxNzUxODMxMzk2MDY2MDAxODk3MjU2Nzg1NTkwOTI3Mzg3OTcxNDYxNjg3MDgwNDI4NTgyNTY0MTk0NjEzNjE3NzIiLCJiSWQiOiJXWTlYUVciLCJrZXZJZCI6IlZJRkMyQzIxQzA5RjA3NEE3M0I1QTQxQzA2M0Y1MzZCQkMiLCJ0SWQiOiJtYXBpIiwibSI6eyJ0eXBlIjoibiJ9LCJ2IjoiUDJSR0dWIn0.PGiRwYbO9mbFK-JWRP6NbmHTDhOV0Q-hxK_bkepklPs; ud=3.-hCuLDZfVJf9kwEcWhK4aoBwDJGEECSIrdcVIpy1i7xnA9ufoMNSLvu_MarqMGLxoZWdLIeeNoRhMdCveDfQD-CoZ7oQa45_NpQIaUJBL6YjUr1yDz2gtGUQbcNRHgPSY6HBbC2r_JknxJHaHrnz4PVRUIOlTXAtQC_1EOnr2l9uX_znfNb67vtHFcZdJJY-Ph9rQJEcYeMxsalOFCNMQnztN9vAMLE5unVXJmDjYcNrD_GhkMf8Gpf4H16hitVK; S=d1t17Pz8/Pz96Pz8/PzIUBhg/LU+jjSa6LaLLpXcrNC32yftwba2SdAeNLqo9zp/bU7S/tufAt36/gJemjQBVJXDJbg==; SN=VIFC2C21C09F074A73B5A41C063F536BBC.TOK169EDD8669274E7180B390EF4B56CB41.1754909031608.LI"
RUNNING = True

app = Flask(__name__)

def log_to_console(msg):
    """Instant print with timestamp"""
    timestamped = f"[{datetime.now()}] {msg}"
    print(timestamped)

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        log_to_console(f"Telegram Error: {e}")

def generate_random_code():
    return BASE_COUPON + ''.join(random.choices(string.ascii_uppercase + string.digits, k=13))

def try_coupon(coupon_code):
    url = "https://1.rome.api.flipkart.com/api/1/action/view"
    headers = {
        "content-type": "application/json",
        "cookie": COOKIES,
        "flipkart_secure": "true",
        "host": "1.rome.api.flipkart.com",
        "origin": "https://www.flipkart.com",
        "User-Agent": "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36",
        "referer": "https://www.flipkart.com/",
        "x-user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36 FKUA/msite/0.0.3/msite/Mobile"
    }
    payload = {
        "actionRequestContext": {
            "type": "CLAIM_COUPON",
            "couponCode": coupon_code
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        data = response.json()

        action_success = data.get("RESPONSE", {}).get("actionSuccess", None)
        error_message = data.get("RESPONSE", {}).get("errorMessage", "")

        log_entry = f"CODE: {coupon_code} | SUCCESS: {action_success} | ERROR: {error_message}"
        log_to_console(log_entry)

        telegram_text = (
            f"💥 <b>Coupon Tried:</b> {coupon_code}\n"
            f"🔗 <b>Request URL:</b> {url}\n"
            f"📨 <b>Request Payload:</b> {payload}\n"
            f"📥 <b>Response:</b> {data}\n"
            f"✅ <b>Success:</b> {action_success}\n"
            f"❗ <b>Error Message:</b> {error_message}"
        )
        send_telegram_message(telegram_text)

    except Exception as e:
        log_to_console(f"Request Error: {e}")
        send_telegram_message(f"⚠️ <b>Request Error:</b> {e}")

def coupon_worker():
    while RUNNING:
        code = generate_random_code()
        try_coupon(code)
        delay = random.randint(1, 3)
        time.sleep(delay)

@app.route("/")
def home():
    return jsonify({"status": "running", "message": "Coupon bot active"})

@app.route("/status")
def status():
    return jsonify({"running": RUNNING})

if __name__ == "__main__":
    send_telegram_message("✅ <b>Coupon Bot Started</b>\nServer is now running and trying coupons...")
    t = threading.Thread(target=coupon_worker, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=8000)
