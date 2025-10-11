from gspread import Worksheet
from tcs import Portfolio
from logger_setup import logger


def update_portfolio_ws(worksheet: Worksheet, portfolio: Portfolio):
    """Update Google Sheets with portfolio data"""
    try:
        logger.info("Starting Google Sheets update")

        values: list[list[str | float]] = [
            [
                "Account ID",
                "Account Name",
                "Type",
                "UID",
                "Ticker",
                "Name",
                "Country",
                "Value",
                "Price",
                "Total Price",
            ]
        ]

        logger.info(f"Processing {len(portfolio.assets)} assets")

        for asset in portfolio.assets:
            values.append(
                [
                    asset.acc_id,
                    asset.acc_name,
                    asset.type,
                    asset.uid,
                    asset.ticker,
                    asset.name,
                    asset.country,
                    asset.value,
                    asset.price,
                    asset.total_price,
                ]
            )

        logger.info("Clearing worksheet")
        worksheet.clear()

        logger.info("Updating data in Google Sheets")
        worksheet.update(values, f"A1:J{len(portfolio.assets) + 2}")

        logger.info("Google Sheets updated successfully")

    except Exception as e:
        logger.error(f"Error updating Google Sheets: {e}")
        raise
