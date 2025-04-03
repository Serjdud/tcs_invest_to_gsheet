import os
import gspread
import json
from tcs import Portfolio
from tinkoff.invest import Client
from gsheets import update_portfolio_ws

INVEST_TOKEN = ""
GOOGLE_CREDENTIALS_FILE = ""
SPREADSHEET_ID = ""
WORKSHEET_NAME = ""

with open("settings.json", "r") as file:
    settings = json.load(file)
    INVEST_TOKEN = settings["INVEST_TOKEN"]
    GOOGLE_CREDENTIALS_FILE = settings["GOOGLE_CREDENTIALS_FILE"]
    SPREADSHEET_ID = settings["SPREADSHEET_ID"]
    WORKSHEET_NAME = settings["WORKSHEET_NAME"]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def main():
    with Client(INVEST_TOKEN) as client:
        gs = gspread.service_account(filename=GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
        sh = gs.open_by_key(SPREADSHEET_ID)
        ws = sh.worksheet(WORKSHEET_NAME)

        portfolio = Portfolio(client)

        update_portfolio_ws(ws, portfolio)


if __name__ == "__main__":
    main()
