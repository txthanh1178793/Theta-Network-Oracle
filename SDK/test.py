
import logging
from typing import Optional, List
import json
from web3 import Web3, HTTPProvider


abi = [
	{
		"inputs": [
			{
				"components": [
					{
						"components": [
							{
								"internalType": "uint256",
								"name": "a",
								"type": "uint256"
							},
							{
								"internalType": "uint256",
								"name": "b",
								"type": "uint256"
							},
							{
								"internalType": "uint256",
								"name": "c",
								"type": "uint256"
							}
						],
						"internalType": "struct sub_struct",
						"name": "sstruct",
						"type": "tuple"
					},
					{
						"internalType": "uint256",
						"name": "d",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "e",
						"type": "uint256"
					}
				],
				"internalType": "struct test_struct",
				"name": "input",
				"type": "tuple"
			}
		],
		"name": "write",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "data",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "a",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "b",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "c",
						"type": "uint256"
					}
				],
				"internalType": "struct sub_struct",
				"name": "sstruct",
				"type": "tuple"
			},
			{
				"internalType": "uint256",
				"name": "d",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "e",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]

client_address= "0x18E9a5eE2342C93f80036a6DD7A931Ebaf07BbC9"
client_private_key ="1dd3a5652ee5590dca9f6afef8340fab052a144c710505bd2341bb9387b3a23f"
web3 = Web3(HTTPProvider("https://rpc.ankr.com/filecoin_testnet"))


nonce = web3.eth.getTransactionCount(client_address)
contract = web3.eth.contract(address="0x614EA1546f54192c713d2fcC516E4a74cF282fA0", abi = abi)
call_function = contract.functions.write(
	[[2,3,4],5,6]
).buildTransaction({"chainId": web3.eth.chain_id, "from": client_address, "nonce": nonce, 'maxFeePerGas': 2000000000})
signed_tx = web3.eth.account.sign_transaction(call_function, private_key = client_private_key)
send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)

print(tx_receipt)