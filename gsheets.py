from gspread import Worksheet
from tcs import Portfolio

def update_portfolio_ws(worksheet: Worksheet, portfolio: Portfolio):
    values = [
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
    worksheet.clear()
    worksheet.update(values, f"A1:J{len(portfolio.assets) + 2}")