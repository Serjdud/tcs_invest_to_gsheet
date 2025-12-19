import gspread
import json
import sys
from tcs import Portfolio
from t_tech.invest import Client
from gsheets import update_portfolio_ws
from logger_setup import logger

INVEST_TOKEN = ""
GOOGLE_CREDENTIALS_FILE = ""
SPREADSHEET_ID = ""
WORKSHEET_NAME = ""


def load_settings():
    """Load settings from file"""
    try:
        logger.info("Loading settings from settings.json")
        with open("settings.json", "r") as file:
            settings = json.load(file)
            INVEST_TOKEN = settings["INVEST_TOKEN"]
            GOOGLE_CREDENTIALS_FILE = settings["GOOGLE_CREDENTIALS_FILE"]
            SPREADSHEET_ID = settings["SPREADSHEET_ID"]
            WORKSHEET_NAME = settings["WORKSHEET_NAME"]
        logger.info("Settings loaded successfully")
        return INVEST_TOKEN, GOOGLE_CREDENTIALS_FILE, SPREADSHEET_ID, WORKSHEET_NAME
    except FileNotFoundError:
        logger.error("settings.json file not found")
        raise
    except KeyError as e:
        logger.error(f"Missing required parameter in settings: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"JSON format error in settings.json: {e}")
        raise


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def main():
    try:
        logger.info("=== Starting portfolio update ===")

        # Load settings
        INVEST_TOKEN, GOOGLE_CREDENTIALS_FILE, SPREADSHEET_ID, WORKSHEET_NAME = (
            load_settings()
        )

        logger.info("Initializing Tinkoff Invest client")
        with Client(INVEST_TOKEN) as client:
            logger.info("Authenticating with Google Sheets")
            gs = gspread.service_account(
                filename=GOOGLE_CREDENTIALS_FILE, scopes=SCOPES
            )

            logger.info(f"Opening spreadsheet with ID: {SPREADSHEET_ID}")
            sh = gs.open_by_key(SPREADSHEET_ID)

            logger.info(f"Getting worksheet: {WORKSHEET_NAME}")
            ws = sh.worksheet(WORKSHEET_NAME)

            logger.info("Getting portfolio data")
            portfolio = Portfolio(client)

            logger.info("Updating Google Sheets")
            update_portfolio_ws(ws, portfolio)

        logger.info("=== Portfolio update completed successfully ===")

    except Exception as e:
        logger.error(f"Critical error in main: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
