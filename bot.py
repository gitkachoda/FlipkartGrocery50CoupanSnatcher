import os
import time
import random
import string
import threading
import requests
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, jsonify

# ================= Load .env =================
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
BASE_COUPON = os.getenv("BASE_COUPON")
COOKIES = os.getenv("COOKIES")

RUNNING = True
app = Flask(__name__)

# ================= Logger =================
def log_to_console(msg):
    timestamped = f"[{datetime.now()}] {msg}"
    print(timestamped, flush=True)  # flush added

# ================= Telegram Sender =================
def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        log_to_console(f"Telegram Error: {e}")

# ================= Code Generator =================
def generate_random_code():
    return BASE_COUPON + ''.join(random.choices(string.ascii_uppercase + string.digits, k=13))

# ================= Coupon Worker =================
def try_coupon(coupon_code):
    url = "https://2.rome.api.flipkart.com/api/1/action/view"
    headers = {
        "content-type": "application/json",
        "cookie": COOKIES,
        "flipkart_secure": "true",
        "host": "2.rome.api.flipkart.com",
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

        # ================= Safe JSON Handling =================
        if response.headers.get("content-type", "").startswith("application/json"):
            data = response.json()
        else:
            log_to_console(f"❌ Non-JSON Response (status {response.status_code}): {response.text[:200]}")
            return

        action_success = data.get("RESPONSE", {}).get("actionSuccess", None)
        error_message = data.get("RESPONSE", {}).get("errorMessage", "")

        # Console log sirf response ka
        log_to_console(f"CODE: {coupon_code} | SUCCESS: {action_success} | ERROR: {error_message}")
        log_to_console(f"RESPONSE: {data}")

        # Agar sirf invalid code wala error hai to telegram par mat bhej
        if error_message == "The code you have entered is invalid":
            return

        # Baaki sab kuch turant telegram par bhejna hai
        telegram_text = (
            f"💥 <b>Coupon Tried:</b> {coupon_code}\n"
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
        # har request ke beech 20-30 second rukna
        delay = random.randint(20, 30)
        log_to_console(f"⏳ Waiting {delay} seconds before next request...")
        time.sleep(delay)

# ================= Flask Routes =================
@app.route("/")
def home():
    return jsonify({"status": "running", "message": "Coupon bot active"})

@app.route("/status")
def status():
    return jsonify({"running": RUNNING})

# ================= Main =================
if __name__ == "__main__":
    send_telegram_message("✅ <b>Coupon Bot Started</b>\nServer is now running and trying coupons...")
    t = threading.Thread(target=coupon_worker, daemon=True)
    t.start()
    port = int(os.environ.get("PORT", 10000))  # Render ke liye port fix
    app.run(host="0.0.0.0", port=port)
