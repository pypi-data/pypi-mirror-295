from gemnify_sdk.scripts.instance import ContractInstance
from gemnify_sdk.scripts.http import HTTP
import time

class Reader:
    def __init__(self, config) -> None:
        self.config = config
        self.reader = ContractInstance(config, 'Reader')
        self.vault = ContractInstance(config, 'Vault')

    def get_aum(self):
        return self.reader.call_function("getAum")

    def get_global_OI(self):
        result = self.reader.call_function("getGlobalOI")
        if isinstance(result, list) and len(result) == 2:
            keys = [
                "max_global_OI",
                "available_global_OI"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")

    def get_pool_info(self, *args):
        result = self.vault.call_function("getPoolInfo", args)
        if isinstance(result, tuple) and len(result) == 8:
            keys = [
                "pool_amount",
                "reserved_amount",
                "buffer_amount",
                "global_long_size",
                "global_long_average_price",
                "global_short_size",
                "global_short_average_price",
                "usdg_amount"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")

    def get_max_price(self, *args):
        return self.vault.call_function("getMaxPrice", args)

    def get_min_price(self, *args):
        return self.vault.call_function("getMinPrice", args)

    def get_market_price(self, token_address):
        http = HTTP(self.config)

        market_price = http.post(
            "getMarketPrice",
            payload={
                'market': token_address
            }
        )
        return market_price['price']

    def get_position(self, *args):
        instance = ContractInstance(self.config, 'Vault')
        result = instance.call_function("getPosition", args)
        if isinstance(result, tuple) and len(result) == 9:
            keys = [
                "size",
                "collateral",
                "average_price",
                "entry_borrowing_rate",
                "funding_fee_amount_per_size",
                "claimable_funding_amount_per_size",
                "reserve_amount",
                "realised_pnl",
                "last_increased_time"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")

    def get_positions(self, account, market = "", status = 20000, page_index = 1, page_size = 10):
        http = HTTP(self.config)
        positions = http.post(
            "getPositionsByAccount",
            payload={
                'account': account,
                'status': status,
                "market": market,
                'pageIndex': page_index,
                'pageSize': page_size
            }
        )
        return positions

    def get_position_pnl_and_fees(self, *args):
        result = self.vault.call_function("getPositionDeltaAndFees", args)
        if isinstance(result, list) and len(result) == 5:
            keys = [
                "has_profit",
                "delta",
                "borrowing_fee",
                "funding_fee_amount",
                "claimable_amount"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")