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

BOT_TOKEN = "8280673937:AAFl_wZ7-KrwJM7hqgnvmhQoJxsIKVapIp0"
CHAT_ID = 6552591095
BASE_COUPON = "FKGPTz"
COOKIES ="T=TI175183139606600189725678559092738797146168708042858256419461361772; AMCVS_17EB401053DAF4840A490D4C%40AdobeOrg=1; K-ACTION=null; ULSN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjb29raWUiLCJhdWQiOiJmbGlwa2FydCIsImlzcyI6ImF1dGguZmxpcGthcnQuY29tIiwiY2xhaW1zIjp7ImdlbiI6IjYiLCJ1bmlxdWVJZCI6IlVVSTI1MDgwMzE0MTIyNTcwMEtHNTgxOFAiLCJma0RldiI6bnVsbH0sImV4cCI6MTc3MDY5NDg2NCwiaWF0IjoxNzU0OTE0ODY0LCJqdGkiOiI0NTk3NGMwYi02NDQ1LTQyZWUtYTExNS1mYjViZmQyZjE5ZTkifQ.lKOmWMhBXqzvcnowIjIL_f9ZAbe5xgYc0A9rq3m4AVM; at=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNhNzdlZTgxLTRjNWYtNGU5Ni04ZmRlLWM3YWMyYjVlOTA1NSJ9.eyJleHAiOjE3NTQ5MTY2NjQsImlhdCI6MTc1NDkxNDg2NCwiaXNzIjoia2V2bGFyIiwianRpIjoiOWFiMzNmZDctOTc2Ny00NjhlLTlkODktMmZhNGY5ZTIzMzg2IiwidHlwZSI6IkFUIiwiZElkIjoiVEkxNzUxODMxMzk2MDY2MDAxODk3MjU2Nzg1NTkwOTI3Mzg3OTcxNDYxNjg3MDgwNDI4NTgyNTY0MTk0NjEzNjE3NzIiLCJiSWQiOiJJRlZaNkwiLCJrZXZJZCI6IlZJRTVFRkE5MzdFNERGNDFFNEFBRkY4Mjg1REE3Mjk2MDUiLCJ0SWQiOiJtYXBpIiwiZWFJZCI6ImgtNFc5alRjd0FRd3QxTGVUSXljLVhqUWZ4eG9qT3E1bXlqS2MwMTdiVjZ4VkdGSDBQZTF1Zz09IiwidnMiOiJMSSIsInoiOiJIWUQiLCJtIjp0cnVlLCJnZW4iOjR9.1Dc9p0ZIo6bzt5FzQKCWW-OSAC3_ge3sg4u8gJWW-_c; rt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjNhNzdlZTgxLTRjNWYtNGU5Ni04ZmRlLWM3YWMyYjVlOTA1NSJ9.eyJleHAiOjE3NzA4MTI0NjQsImlhdCI6MTc1NDkxNDg2NCwiaXNzIjoia2V2bGFyIiwianRpIjoiYjkzNGIzZjAtZjVjOS00YzY5LWIzMjgtZTM4NDAyZjY5ZjgwIiwidHlwZSI6IlJUIiwiZElkIjoiVEkxNzUxODMxMzk2MDY2MDAxODk3MjU2Nzg1NTkwOTI3Mzg3OTcxNDYxNjg3MDgwNDI4NTgyNTY0MTk0NjEzNjE3NzIiLCJiSWQiOiJJRlZaNkwiLCJrZXZJZCI6IlZJRTVFRkE5MzdFNERGNDFFNEFBRkY4Mjg1REE3Mjk2MDUiLCJ0SWQiOiJtYXBpIiwibSI6eyJ0eXBlIjoibiJ9LCJ2IjoiT0Q0Uk5VIn0.TlJI2QeL39zcxYZ6H5ikJSX0R8cQXtcnmgcO-A46gG0; vd=VIE5EFA937E4DF41E4AAFF8285DA729605-1754914827893-1.1754914888.1754914827.158218208; ud=0.kg-XnFW5gcfK9f7SstW1IHHzgOl-7yED0qEfCKj54P_aNfu7NMYAY9yPbBURSakHnfQTWuomtKUx6RMJIDKkCnv9z4ZI3ec0nhpgbalumM_LMnJmNR8gmDhgEUoO-CML97rRYXmoEz2nKjhD2cBvZ7o1Vl2AufsoYrVCp2QKD5tqcC5WGfGl_Z1kZkjuA_4piAWiWv4QcuHKNv5e-UAFAs7qcWLbfmGaOfX0oSfbxYfvvMLtnfnlhtLWyyjC9g_4Yh9MhZ2yoxt7dzUvfgY9Bw; gpv_pn=GPS%3AAddressInput; gpv_pn_t=GPS%3AAddressInput; AMCV_17EB401053DAF4840A490D4C%40AdobeOrg=-227196251%7CMCIDTS%7C20312%7CMCMID%7C90164886726208731467425828578759474554%7CMCAID%7CNONE%7CMCOPTOUT-1754922102s%7CNONE; s_sq=flipkart-mob-web%3D%2526pid%253DHyperlocal%25253A%252520Adjust%252520pin%252520on%252520map%2526pidt%253D1%2526oid%253DfunctionHr%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DA; vh=844; vw=390; dpr=3.0000001192092896; S=d1t15PztzTCFyPz8/RUo/Pz8/dk1ffqtcaZMaHMgis2a/HIfwuIu1ZY5UD4pCfdrMlGM2i1lwhxFsCH93rhAZQdutnw==; SN=VIE5EFA937E4DF41E4AAFF8285DA729605.TOK3A1728EDAF014C0E942449AD6BC74E58.1754914913937.LI"
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
