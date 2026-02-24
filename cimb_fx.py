import json
import os
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

SPREADSHEET_NAME = "ใส่ชื่อไฟล์ Google Sheet ของคุณ"
WORKSHEET_NAME = "CIMBT 11015"
API_URL = "https://www.cimbthai.com/api/services/app-service/v1/exchange-rate"

# โหลด Service Account จาก GitHub Secret
service_account_info = json.loads(os.environ["GSHEET_SERVICE_ACCOUNT"])

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    service_account_info, scope)

client = gspread.authorize(creds)

# ดึงข้อมูลจาก CIMB
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

response = requests.get(API_URL, headers=headers, timeout=30)
response.raise_for_status()

data = response.json()["data"]

spreadsheet = client.open(SPREADSHEET_NAME)

try:
    sheet = spreadsheet.worksheet(WORKSHEET_NAME)
    sheet.clear()
except:
    sheet = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows="200", cols="10")

sheet.append_row([
    "Currency Name",
    "Currency Code",
    "Buy OD",
    "Buy TT",
    "Sell OD",
    "Last Update"
])

now = datetime.now().strftime("%Y-%m-%d %H:%M")

for r in data:
    sheet.append_row([
        r.get("rowName"),
        r.get("backendCode"),
        r.get("buyOD"),
        r.get("buyTT"),
        r.get("sellOD"),
        now
    ])

print("CIMB FX updated successfully")
