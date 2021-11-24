import subprocess
from decouple import config
import json, os
import random
import utils
from node_lib import Node

CARDANO_NETWORK_MAGIC = config('CARDANO_NETWORK_MAGIC')
CARDANO_CLI_PATH = config('CARDANO_CLI_PATH')
CARDANO_NETWORK = config('CARDANO_NETWORK')

with open('./config_file.json') as file:
    params=json.load(file)

TRANSACTION_PATH_FILE = params['node']['transactions']
if not os.path.exists(TRANSACTION_PATH_FILE):
    os.makedirs(TRANSACTION_PATH_FILE)

KEYS_FILE_PATH = params['node']['keys_path']

if not os.path.exists(KEYS_FILE_PATH):
    os.makedirs(KEYS_FILE_PATH, exist_ok=True)

def wallet_to_address(wallet):
    if not wallet.startswith('addr' or 'DdzFF'):
        with open(KEYS_FILE_PATH + '/' + wallet + '/' + wallet + '.payment.addr','r') as file:
            wallet = file.readlines(1)[0]
    return wallet

def save_metadata( metadata):
    if metadata == {}:
        metadata_json_file = ''
    else:
        with open(TRANSACTION_PATH_FILE + '/' + 'metadata.json','w') as file:
            json.dump(metadata, file,indent=4,ensure_ascii=False)
        metadata_json_file = TRANSACTION_PATH_FILE + '/' + 'metadata.json'

    return metadata_json_file


wallet_id = 'addr_test1qzfxu7zhedzn86v95k84m7t94z3eek99al4xlyahkuw8ammjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvh5ndl'

node = Node(
    CARDANO_NETWORK, 
    CARDANO_CLI_PATH,
    CARDANO_NETWORK_MAGIC,
    TRANSACTION_PATH_FILE,
    KEYS_FILE_PATH
    )
# node.query_protocol()
# result = node.query_tip_exec()

# transactions = node.get_transactions(wallet_id)
# print(transactions)

# balance = node.get_balance(wallet_id)
# print(balance)


params = {
  "seq": 1,
  "cmd_id": "mint_asset",
  "message": {
    "tx_info": {
      "mint": {
        "id": "6c8eadf91ae46e93d953657ac968fbd4b8f0afed",
        "metadata": {},
        "address": "addr_test1qpjltzup7mjfk9vhrj4ltv6sduwv427nmjqf623jje7zt5qytthp9vmrx4y8t4kwk73jlxxsqwu75fd4dx5k5uzl54rsh4wu29",
        "tokens": [
          {
            "name": "testtokens2",
            "amount": 20,
            "policyID": ""
          }
        ]
      }
    }
  }
}

node.transactions(params)