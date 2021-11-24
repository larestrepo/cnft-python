import json
import library as lb
import wallet_lib as wallet
from node_lib import Node
from decouple import config
import os
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

node = Node(
CARDANO_NETWORK, 
CARDANO_CLI_PATH,
CARDANO_NETWORK_MAGIC,
TRANSACTION_PATH_FILE,
KEYS_FILE_PATH
)

def result_treatment(obj,client_id):

    """Main function that receives the object from the pubsub and defines which execution function to call"""
    main ={
        'client_id': client_id
    }

    if obj[0]['cmd_id'] == 'query_tip':
        print('Executing query tip')
        # result = lb.query_tip_exec()
        result = node.query_tip_exec()
        main.update(result)

    # elif obj[0]['cmd_id'] == 'query_utxo':
    #     print('Executing query utxo')
    #     address = obj[0]['message']['address']
    #     result = lb.get_transactions(address)
    #     main.update(result)
    
    elif obj[0]['cmd_id'] == 'generate_new_mnemonic_phrase':
        print('Executing generate_new_mnemonic_phrase')
        size = obj[0]['message']['size']    
        mnemonic = wallet.generate_mnemonic(size)
        main['wallet_mnemonic']=mnemonic
    
    elif obj[0]['cmd_id'] == 'generate_wallet':
        print('Executing generate wallet')
        name = obj[0]['message']['wallet_name']
        passphrase = obj[0]['message']['passphrase']
        mnemonic = obj[0]['message']['mnemonic']

        wallet_status = wallet.create_wallet(name, passphrase, mnemonic)
        main['wallet_status']=wallet_status
        id = wallet_status['id']
        utils.towallet(id, mnemonic)

        address = wallet.get_addresses(wallet_status['id'])
        main['address']=address

    elif obj[0]['cmd_id'] == 'wallet_info':
        print('Executing wallet info')
        id = obj[0]['message']['id']
        wallet_info = wallet.wallet_info(id)
        main['wallet_info']=wallet_info
        address = wallet.get_addresses(id)
        main['address']=address
    
    elif obj[0]['cmd_id'] == 'min_fees':
        print('Executing min fees')
        id = obj[0]['message']['id']
        tx_info = obj[0]['message']['tx_info']
        tx_info["time_to_live"]={
                        "quantity": 10,
                        "unit": "second"
                        }
        tx_info["withdrawal"]="self"
        tx_result = wallet.min_fees(id,tx_info)
        main['min_fees']= tx_result
    
    elif obj[0]['cmd_id'] == 'send_transaction':
        print('Executing send transaction')
        id = obj[0]['message']['id']
        tx_info = obj[0]['message']['tx_info']
        tx_info["time_to_live"]={
                        "quantity": 60,
                        "unit": "second"
                        }
        tx_info["withdrawal"]="self"
        tx_result = wallet.send_transaction(id,tx_info)
        main['tx_result']= tx_result
    
    elif obj[0]['cmd_id'] == 'confirm_transaction':
        print('Executing confirmation of the transaction')
        id = obj[0]['message']['id']
        tx_id = obj[0]['message']['tx_id']
        tx_result = wallet.confirm_transaction(id,tx_id)
        main['tx_result']= tx_result
    
    elif obj[0]['cmd_id'] == 'mint_asset':
        print('Executing mint asset')

        mint = node.transactions(obj[0])
        main['tx_result'] = mint
    
    elif obj[0]['cmd_id'] == 'delete_wallet':
        print('Executing wallet deletion')
        id = obj[0]['message']['id']
        print(id)
        wallet_info = wallet.delete_wallet(id)
        if wallet_info=={}:
            wallet_info={
                'message':"wallet succesfully deleted",
            }
        main['tx_result'] = wallet_info

    elif obj[0]['cmd_id'] == 'assets_balance':
        print('Executing assets info')
        id = obj[0]['message']['id']
        assets_balance = wallet.assets_balance(id)
        main['assets_balance']=assets_balance

    
    
    obj.pop(0)
    return main