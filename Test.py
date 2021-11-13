import unittest

from requests import NullHandler
import library as lb
import wallet_lib as wallet
import time
import utils

test_id = 1 # pick between test functions

class TestLibrary (unittest.TestCase):

    if test_id == 1: #old method
        def test_send_funds(self):

            walletName = 'acdc'
            wallet01 = 'main'
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
                    "token": "ADA",
                    "assets":[
                        {"name":"lovelace",
                        "target":3_000_000,
                        },
                        ],
                },
                "metadata": metadata,
                "mint": {
                    "Flag": True,
                    "with_quantity": True,
                    "NFT_handle": False,
                    "tokens_info":[
                        {
                            "name": "test_token",
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
            list_wallets=wallet.list_wallets()
            print(list_wallets)
            for k, v in list_wallets.items():
                if k==[id]:
                    wallet.delete_wallet(k)
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
            name='forminting'
            nmemonic = wallet.generate_mnemonic(24)

            utils.towallet(name,nmemonic)
    
    if test_id==7:
        def test_minting(self):
            wallet_name = 'Mint_wallet'
            utils.create_minting_policy(wallet_name)


        

            




unittest.main()
