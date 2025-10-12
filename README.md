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

### Other
1. Make run.sh executable
```bash
sudo chmod +x run.sh
```

# Usage
Run
```bash
./run.sh
```

# Scheduled auto-update
## Linux
(one of the options)
1. Make file /etc/systemd/system/portfolio-tracker.service
```ini
[Unit]
Description=Portfolio Tracker Update
After=network.target

[Service]
Type=oneshot
User=orangepi
Group=orangepi
WorkingDirectory=<PATH_TO_PROJECT>/tcs_invest_to_gsheet
ExecStart=/bin/bash <PATH_TO_PROJECT>/tcs_invest_to_gsheet/run.sh
Environment=PYTHONPATH=<PATH_TO_PROJECT>/tcs_invest_to_gsheet

# Logging
StandardOutput=journal
StandardError=journal

# Security
NoNewPrivileges=yes
PrivateTmp=yes
```
`<PATH_TO_PROJECT>` - path to `tcs_invest_to_gsheet` folder

2. Make file /etc/systemd/system/portfolio-tracker.timer
```ini
[Unit]
Description=Run Portfolio Tracker at 9:00 and 18:00 MSK
Requires=portfolio-tracker.service

[Timer]
# UTC time
OnCalendar=*-*-* 06:00:00
OnCalendar=*-*-* 15:00:00

# Settings
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
```
3. Enable and start `portfolio-tracker.timer` timer
```bash
sudo systemctl daemon-reload
sudo systemctl enable portfolio-tracker.timer
sudo systemctl start portfolio-tracker.timer
```
