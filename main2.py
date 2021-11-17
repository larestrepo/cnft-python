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
    KEYS_FILE_PATH,
    wallet_id
    )
# node.query_protocol()
# result = node.query_tip_exec()

# transactions = node.get_transactions(wallet_id)
# print(transactions)

# balance = node.get_balance(wallet_id)
# print(balance)


metadata = {}
params = {
    "metadata": metadata,
    "mint": {
                        "with_quantity": False,
                        "NFT_handle": False,
                        "mint_wallet_id": "987f6d81f4f72c484f6d34c53e7d7f2719f40705",
                        "wallet_destin_addr": "addr_test1qzfxu7zhedzn86v95k84m7t94z3eek99al4xlyahkuw8ammjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvh5ndl",
                        "tokens_info":[
                            {
                                "name": "testtoken",
                                "amount": 20,
                                "PolicyID": '205a5880aebba0d1e330bb652114e3baea52542d4c0cb2defe26d5c9',
                            }
                        ]
                    }
}
wallet01 = 'addr_test1qzfxu7zhedzn86v95k84m7t94z3eek99al4xlyahkuw8ammjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvh5ndl'
wallet02 = 'addr_test1qzfxu7zhedzn86v95k84m7t94z3eek99al4xlyahkuw8ammjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvh5ndl'

node.transactions(wallet01,wallet02,params)



