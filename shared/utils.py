import logging, os, requests
from dotenv import load_dotenv

load_dotenv()

def log(msg):
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    logging.info(msg)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram(message: str):
    if not TG_TOKEN or not TG_CHAT_ID:
        log("⚠️ Telegram not configured")
        return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload, timeout=5)
    except Exception as e:
        log(f"Telegram send error: {e}")
