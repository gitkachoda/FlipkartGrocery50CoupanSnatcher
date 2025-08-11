import os
import time
import random
import string
import threading
import requests
from datetime import datetime
from flask import Flask, jsonify

# Environment variables (Render Dashboard → Environment)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_COUPON = os.getenv("BASE_COUPON")
COOKIES = os.getenv("FLIPKART_COOKIES")

# In-memory log buffer
LOGS = []
MAX_LOGS = 200
RUNNING = True

app = Flask(__name__)

def send_telegram_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram config missing, skipping send.")
        return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        r = requests.post(url, json=payload, timeout=10)
        print(f"📩 Telegram sent: {r.status_code}")
    except Exception as e:
        print("❌ Telegram Error:", e)

def generate_random_code():
    return BASE_COUPON + ''.join(random.choices(string.ascii_uppercase + string.digits, k=13))

def log_message(msg):
    """Store in memory and print to console."""
    timestamped = f"[{datetime.now()}] {msg}"
    LOGS.append(timestamped)
    if len(LOGS) > MAX_LOGS:
        LOGS.pop(0)
    print(timestamped)

def try_coupon(coupon_code):
    url = "https://2.rome.api.flipkart.com/api/1/action/view"
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

        log_message(f"CODE: {coupon_code} | SUCCESS: {action_success} | ERROR: {error_message}")

        # Notify only when max redemption limit reached
        if "You have reached maximum redemption limit" in error_message:
            telegram_text = (
                f"🟩 <b>Coupon Tried:</b> {coupon_code}\n"
                f"✅ <b>Success:</b> {action_success}\n"
                f"<b>Message:</b> {error_message}"
            )
            send_telegram_message(telegram_text)

    except Exception as e:
        log_message(f"Request Error: {e}")

def coupon_worker():
    log_message("⚙️ Worker started")
    while RUNNING:
        try:
            code = generate_random_code()
            try_coupon(code)
            delay = random.randint(1, 3)
            log_message(f"⏳ Waiting {delay} seconds...")
            time.sleep(delay)
        except Exception as e:
            log_message(f"❌ Worker crashed: {e}")
            time.sleep(5)

@app.route("/")
def home():
    return jsonify({"status": "running", "message": "Coupon bot active"})

@app.route("/logs")
def get_logs():
    return jsonify({"logs": LOGS[-50:]})

@app.route("/status")
def status():
    return jsonify({"running": RUNNING})

if __name__ == "__main__":
    send_telegram_message("✅ <b>Coupon Bot Started</b>\nServer is now running and trying coupons...")
    t = threading.Thread(target=coupon_worker, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
