import time
import csv
import os
import gspread
from google.oauth2.service_account import Credentials
from config import GSHEET_CREDENTIALS, GSHEET_NAME, GSHEET_WORKSHEET

LOCAL_LOG = "logs/detections.csv"
_SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


class CloudLogger:
    def __init__(self, use_cloud: bool = True):
        self._use_cloud = use_cloud
        self._sheet = None
        os.makedirs("logs", exist_ok=True)

        if not os.path.exists(LOCAL_LOG):
            with open(LOCAL_LOG, "w", newline="") as f:
                csv.writer(f).writerow(
                    ["timestamp", "category", "raw_class", "confidence", "temp_c", "hum_pct", "fill_pct"]
                )

        if use_cloud:
            try:
                creds  = Credentials.from_service_account_file(GSHEET_CREDENTIALS, scopes=_SCOPES)
                client = gspread.authorize(creds)
                self._sheet = client.open(GSHEET_NAME).worksheet(GSHEET_WORKSHEET)
            except Exception as e:
                print(f"[CloudLogger] Google Sheets unavailable: {e}")
                self._use_cloud = False

    def log(
        self,
        category: str,
        raw_class: str = "",
        confidence: float = 0.0,
        temp_c: float = None,
        hum_pct: float = None,
        fill_pct: int = None,
    ):
        ts  = time.strftime("%Y-%m-%d %H:%M:%S")
        row = [ts, category, raw_class, confidence, temp_c, hum_pct, fill_pct]

        with open(LOCAL_LOG, "a", newline="") as f:
            csv.writer(f).writerow(row)

        if self._use_cloud and self._sheet:
            try:
                self._sheet.append_row(row)
            except Exception as e:
                print(f"[CloudLogger] Sheet write failed: {e}")

    def log_environment(self, temp_c: float, hum_pct: float):
        self.log("ENV_IDLE", temp_c=temp_c, hum_pct=hum_pct)
