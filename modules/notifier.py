import requests
import os


TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def send_telegram(message: str) -> bool:
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        resp = requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": message}, timeout=5)
        return resp.status_code == 200
    except Exception:
        return False


def notify_bin_full(category: str, fill_pct: int):
    msg = f"[SmartRecycle] {category.upper()} bin is {fill_pct}% full. Please empty it."
    send_telegram(msg)


def notify_sanitation_warning(temp_c: float, hum_pct: float):
    msg = f"[SmartRecycle] High temp/humidity alert: {temp_c}C / {hum_pct}%. Check bins."
    send_telegram(msg)
