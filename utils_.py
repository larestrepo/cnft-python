import subprocess
from decouple import config
import json, os
import random
import utils

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