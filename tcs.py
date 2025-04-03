from tinkoff.invest import AccountStatus, InstrumentIdType, RequestError
from tinkoff.invest.services import Services

NANO = 10 ** (-9)
ASSETS_INFO_CACHE = {"uid": {"ticker": "", "name": "", "country": ""}}


class Asset:
    def __init__(
        self,
        asset_type: str,
        asset_value: float,
        asset_price: float,
        acc_id: str,
        acc_name: str,
        asset_uid: str,
        client: Services,
    ):
        self.acc_id = acc_id
        self.acc_name = acc_name
        self.type = asset_type
        self.uid = asset_uid
        self.ticker = ""
        self.name = ""
        self.country = ""
        self.value = asset_value
        self.price = asset_price
        self.total_price = self.value * self.price
        self._get_asset_info(asset_uid, client)

    def _get_asset_info(self, asset_uid: str, client: Services):
        if asset_uid in ASSETS_INFO_CACHE.keys():
            self.ticker = ASSETS_INFO_CACHE[asset_uid]["ticker"]
            self.name = ASSETS_INFO_CACHE[asset_uid]["name"]
            self.country = ASSETS_INFO_CACHE[asset_uid]["country"]
        else:
            try:
                info = client.instruments.get_instrument_by(
                    id_type=InstrumentIdType(3), id=asset_uid
                ).instrument
            except RequestError as er:
                print("\nGet Portfolio Request error")
                print("code:\n", er.code)
                print("details:\n", er.details)
                print("metadata:\n", er.metadata)
                print()
            else:
                self.ticker = info.ticker
                self.name = info.name
                self.country = info.country_of_risk_name
                ASSETS_INFO_CACHE[asset_uid] = {
                    "ticker": info.ticker,
                    "name": info.name,
                    "country": info.country_of_risk_name,
                }


class Portfolio:
    def __init__(self, client: Services):
        self.client = client
        self.assets = self._get_portfolio()

    def _get_accounts(self) -> list[dict]:
        return [
            {"id": acc.id, "name": acc.name, "status": acc.status}
            for acc in self.client.users.get_accounts().accounts
            if acc.status != AccountStatus(3)
        ]

    def _get_portfolio(self) -> list[Asset]:
        accounts = self._get_accounts()
        assets = []

        for acc in accounts:
            try:
                positions = self.client.operations.get_portfolio(
                    account_id=acc["id"]
                ).positions
            except RequestError as er:
                print("\nGet Portfolio Request error")
                print("code:\n", er.code)
                print("details:\n", er.details)
                print("metadata:\n", er.metadata)
                print()
            else:
                for position in positions:
                    assets.append(
                        Asset(
                            acc_id=acc["id"],
                            acc_name=acc["name"],
                            asset_type=position.instrument_type,
                            asset_value=position.quantity.units
                            + NANO * position.quantity.nano,
                            asset_price=position.current_price.units
                            + NANO * position.current_price.nano,
                            asset_uid=position.instrument_uid,
                            client=self.client,
                        )
                    )
        return assets

    def __repr__(self):
        s = ""
        for asset in self.assets:
            s += f"Account ID: {asset.acc_id}\n"
            s += f"Name: {asset.acc_name}\n"
            s += f"Type: {asset.type}\n"
            s += f"UID: {asset.uid}\n"
            s += f"Ticker: {asset.ticker}\n"
            s += f"Name: {asset.name}\n"
            s += f"Country: {asset.country}\n"
            s += f"Value: {asset.value}\n"
            s += f"Price: {asset.price}\n"
            s += f"Total price: {asset.total_price}\n\n"
        return s
