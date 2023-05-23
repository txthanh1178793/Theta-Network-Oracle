from dataclasses import dataclass
from enum import Enum
from typing import Literal


@dataclass
class Network:
    chain_id: int
    chain_name: str
    rpc: str


# contract address configuration
@dataclass
class ContractAddresses:
    publisher_registry_address: bytes
    oracle_proxy_address: bytes