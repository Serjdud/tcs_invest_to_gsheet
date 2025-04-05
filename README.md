# About the Project
Python script downloads portfolio data from T-Bank Investments and uploads data to Google Sheet.

# Getting Started
## Prerequisites
Python 3 installed.

## Installation
### Settings for script
1. Get [T-Bank Invest API Key](https://tinkoff.github.io/investAPI/token/)
2. Put T-Bank API Key into `INVEST_TOKEN` variable in `settings.json` file
3. Setting your Google Cloud Project and Google Sheets Spreadsheet using Service Account ([How to setting](https://docs.gspread.org/en/v6.1.3/oauth2.html))
4. Save google credentials file to project directory as `g_credentials.json` file ([How to get](https://docs.gspread.org/en/v6.1.3/oauth2.html#for-bots-using-service-account))
5. Get Google Spreadsheet ID from URL: `https://docs.google.com/spreadsheets/d/<THIS IS SPREADSHEET ID>/edit?...`
6. Put Google Spreadsheet ID into `SPREADSHEET_ID` variable in `settings.json` file
7. Put Worksheet name into `WORKSHEET_NAME` variable in `settings.json` file

### Python environment
1. Create python virtual environment
```bash
python3 -m venv .venv
```
2. Activate python virtual environment
```bash
source .venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

# Usage
Run
```bash
python3 main.py
```