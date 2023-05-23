from typing import Dict, List, Tuple, Union

from core.utils import key_for_asset
from typing_extensions import TypedDict


class SpotAsset(TypedDict):
    type: str
    pair: Tuple[str, str]
    decimals: int


class OnchainDetail(TypedDict):
    asset_name: str
    asset_address: str
    metric: str


class OnchainAsset(TypedDict):
    type: str
    source: str
    key: str
    detail: OnchainDetail
    decimals: int


Asset = Union[SpotAsset, OnchainAsset]


ALL_ASSETS: List[Asset] = [
    {"type": "SPOT", "pair": ("BTC", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("WBTC", "BTC"), "decimals": 8},
    {"type": "SPOT", "pair": ("WBTC", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("BTC", "EUR"), "decimals": 8},
    {"type": "SPOT", "pair": ("ETH", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("SOL", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("AVAX", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("DOGE", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("SHIB", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("FIL", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("DAI", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("USDT", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("USDC", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("TUSD", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("BNB", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("ADA", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("XRP", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("MATIC", "USD"), "decimals": 8},
    {"type": "SPOT", "pair": ("AAVE", "USD"), "decimals": 8},
    {
        "type": "ONCHAIN",
        "source": "AAVE",
        "key": "AAVE-ON-BORROW",
        "detail": {
            "asset_name": "USD Coin",
            "asset_address": "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb480xb53c1a33016b2dc2ff3653530bff1848a515c8c5",
            "metric": "variableBorrowRate",
        },
        "decimals": 18,
    },
]

_ASSET_BY_KEY: Dict[str, SpotAsset] = {
    key_for_asset(asset): asset
    for asset in ALL_ASSETS
    if asset["type"] == "SPOT"
}


def get_spot_asset_spec_for_pair_id(pair_id: str) -> SpotAsset:
    if pair_id not in _ASSET_BY_KEY:
        raise ValueError(f"Pair ID not found: {pair_id}")
    return _ASSET_BY_KEY[pair_id]
