import logging
from typing import Optional, List
import json
from web3 import Web3, HTTPProvider

from config.chain import Networks
from core.entry import SpotEntry
from core.utils import str_to_bytes32

logger = logging.getLogger(__name__)

class CoreClient:
    def __init__(
        self,
        network,
        client_address: str,
        client_private_key: str
    ):
        if network not in Networks.keys():
            raise NotImplementedError(f"Network {network} not recognized")

        self.client_address = client_address
        self.client_private_key = client_private_key
        self.network = Networks[network]
        self.web3 = Web3(HTTPProvider(self.network['RPC'], request_kwargs={'timeout': 30}))
        self._setup_contracts()
        print("Oracle Contract Address: " + self.network["Oracle Contract Address"])
        print("Publisher Registry Contract Address: " + self.network["Publisher Registry Contract Address"])

    def _setup_contracts(self):
        oracle_abis = json.load(open("abis/Oracle.json", "r"))['abi']
        self.oracle = self.web3.eth.contract(
            address=self.network["Oracle Contract Address"], 
            abi=oracle_abis)

        publisher_registry_abis =  json.load(open("abis/PublisherRegistry.json", "r"))['abi']
        self.publisher_registry = self.web3.eth.contract(
            address=self.network["Publisher Registry Contract Address"], 
            abi=publisher_registry_abis)

    def get_nonce(self):
        return self.web3.eth.getTransactionCount(self.client_address)

    def get_timestamp(self):
        return self.web3.eth.get_block('latest').timestamp

    def publish_spot_entry(self, spot_entry: SpotEntry):
        nonce = self.get_nonce()
        call_function = self.oracle.functions.publishSpotEntry([
          [
            spot_entry.base.timestamp,                                #"timestamp"
            str_to_bytes32(spot_entry.base.source),                   #"source"
            str_to_bytes32(spot_entry.base.publisher)                 #"publisher"
          ],
          str_to_bytes32(spot_entry.pair_id),                         #"pairId"
          spot_entry.price,                                           #"price"
          spot_entry.volume                                           #"volume"
        ]).buildTransaction({"chainId": self.web3.eth.chain_id, "from": self.client_address, "nonce": nonce, 'maxFeePerGas': 20000000000})

        signed_tx = self.web3.eth.account.sign_transaction(call_function, private_key = self.client_private_key)
        send_tx = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(send_tx)
        return tx_receipt

    def publish_spot_entries(self, spot_entries:List[SpotEntry]):
        nonce = self.get_nonce()
        call_function = self.oracle.functions.publishSpotEntries([[
          [
            spot_entry.base.timestamp,                                #"timestamp"
            str_to_bytes32(spot_entry.base.source),                   #"source"
            str_to_bytes32(spot_entry.base.publisher)                 #"publisher"
          ],
          str_to_bytes32(spot_entry.pair_id),                         #"pairId"
          spot_entry.price,                                           #"price"
          spot_entry.volume                                           #"volume"
        ] for spot_entry in spot_entries]).buildTransaction({"chainId": self.web3.eth.chain_id, "from": self.client_address, "nonce": nonce, 'maxFeePerGas': 20000000000})
        
        signed_tx = self.web3.eth.account.sign_transaction(call_function, private_key = self.client_private_key)
        send_tx = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(send_tx)
        return tx_receipt

