import gspread
from google.oauth2.service_account import Credentials
import random

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

import os
import json

credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])

creds = Credentials.from_service_account_info(
    credentials,
    scopes=SCOPES
)

client = gspread.authorize(creds)

sheet = client.open_by_key(
    "1aQAEq-cc8DR9BNQT3s_QAzx86PTGLGI0jnWZ3mpeQCg"
).worksheet("Licenses")


# Generate 8 digit license
def generate_license():
    while True:
        key = str(random.randint(10000000, 99999999))
        try:
            sheet.find(key)
        except:
            return key


# Check Trader already active
def is_active(trader_id):
    values = sheet.get_all_values()

    for row in values[1:]:
        if len(row) >= 2 and row[1] == str(trader_id):
            return True

    return False


# Save Trader
def save_license(trader_id, country, deposit, plan):

    sheet.append_row([
        trader_id,      # License Key
        trader_id,      # Quotex ID
        plan,           # Membership
        "active"        # Status
    ])

    return trader_id
    