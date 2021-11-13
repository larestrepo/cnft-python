import unittest
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
            wallet02 = 'addr_test1qza83ygkg0kn5pzaya8wakmsd3j5678v3l3yju9sng7r6ad0yzn06hf399g6wmcqce90gxqujpzu7duaenk2t2vy3gjskjmdyn'
            quantity = 6
            deplete = False
            token = 'ADA'

            lb.send_funds(wallet01,wallet02,quantity,token,deplete)

    if test_id==2: #new method
        def test_create_wallet(self):
            wallet_name = 'Forminting'
            passphrase = 'Forminting'
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

        

            




unittest.main()
