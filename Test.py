import unittest

from requests import NullHandler
import library as lb
import wallet_lib as wallet
import time
import utils
from node_lib import Node
from decouple import config
import json
import os


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

test_id = 9 # pick between test functions

class TestLibrary (unittest.TestCase):

    if test_id == 1: #old method
        def test_send_funds(self):

            walletName = 'acdc'
            wallet01 = 'addr_test1qzfxu7zhedzn86v95k84m7t94z3eek99al4xlyahkuw8ammjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvh5ndl'
            wallet02 = 'addr_test1qzfxu7zhedzn86v95k84m7t94z3eek99al4xlyahkuw8ammjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eqvh5ndl'
            quantity = 3
            deplete = False
            token = 'ADA'
            # metadata = {
            #     "1337": {
            #         "name": "hello world",
            #         "completed": 0
            #     }
            # }
            metadata = {}
            params = {
                "Tx": {
                    "Max": False,
                    "assets":
                        {"lovelace": 3_000_000,
                        "testtoken": 10,
                        },
                },
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
                            "PolicyID": None,
                        }
                    ]
                }
                
            }

            lb.transactions(wallet01,wallet02,params)

    if test_id==2: #new method
        def test_create_wallet(self):
            wallet_name = 'Mint_wallet'
            passphrase = 'Mint_wallet'
            size = 24
            main ={
            'client-id': 'asjfdkjfnfdnmdlk'
            }
            mnemonic = wallet.generate_mnemonic(size)
            print(mnemonic)

            response = wallet.create_wallet(wallet_name, passphrase,mnemonic)
            print(response)
            print('id: ',response['id'],'/n', 'name: ', response['name'] )
 
            wallet_info = wallet.wallet_info(response['id'])
            print(wallet_info)
            status = wallet_info['state']['status']
            print(status)
            
            addresses = wallet.get_addresses(response['id'])
            print(addresses[0]['id'])
    if test_id==3: # new method
        def test_delete_wallet(self):
            # list_wallets=wallet.list_wallets()
            # print(list_wallets)
            # for k, v in list_wallets.items():
            #     if k==[id]:
            #         wallet.delete_wallet(k)
            id = '8b94dab0fa6c5ff737b19d9dba7faca095ce1480'
            response = wallet.delete_wallet(id)
            print(response)
    if test_id==4: # old method
        def test_get_balance(self):
            wallet01 = 'acdc'
            token = 'ADA'
            actual_balance01 = lb.get_balance(wallet01,token)
            print(actual_balance01)

    if test_id==5: #new method
        def test_generate_nmemonic(self):
            wallet.generate_mnemonic(24)
    
    if test_id==6:

        def test_generate_wallet_from_nmemonic(self):
            wallet_id='987f6d81f4f72c484f6d34c53e7d7f2719f40705'
            # nmemonic = wallet.generate_mnemonic(24)
            nmemonic = ['canal', 'issue', 'there', 'cricket', 'sand', 'develop', 'oak', 'erode', 'antenna', 'flock', 'invite', 'power', 'cheese', 'retreat', 'tennis', 'scout', 'swallow', 'found', 'never', 'spice', 'inch', 'artwork', 'cupboard', 'lumber']

            utils.towallet(wallet_id,nmemonic)
    
    if test_id==7:
        def test_minting(self):
            params= {
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
    
    if test_id==8:
        def test_get_addresses(self):
            print('executing get address')
            id='af807b9bf120667b5fadd9e7bdee4a6dab71623f'
            addresses = wallet.get_addresses(id)
            print(addresses)

    if test_id==9:
        
        def test_get_balance_new(self):
            address='addr_test1qpjltzup7mjfk9vhrj4ltv6sduwv427nmjqf623jje7zt5qytthp9vmrx4y8t4kwk73jlxxsqwu75fd4dx5k5uzl54rsh4wu29'
            balance = node.get_balance(address)
            print(balance)

        # def test_full_cycle(self):
        #     """ 1. Create wallet
        #     {
        #         "seq": 1,
        #         "cmd_id": "generate_new_mnemonic_phrase",
        #         "message": { 
        #                 "size": 24
        #         }
        #         }

        #     """

        #     # 1.a Create nmemonic
        #     size = 24
        #     mnemonic = wallet.generate_mnemonic(size)

    


        

            




unittest.main()
