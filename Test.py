import unittest
import library as lb
import time


class TestLibrary (unittest.TestCase):


    def test_send_funds(self):

        walletName = 'acdc'
        wallet01 = 'main'
        wallet02 = 'Will_Cotrino_2'
        quantity = 10
        token = 'ADA'
        # Verify initial funds from the wallets to test
        if token=='ADA':
            token = 'lovelace'
            param = 1000000
        else:
            param = 1

        balance01 = round(lb.get_balance(wallet01,token)[token])
        balance02 = round(lb.get_balance(wallet02,token)[token])

        addr_origin = lb.wallet_to_address(wallet01)
        addr_destin = lb.wallet_to_address(wallet02)
        fees = lb.tx_min_fee(addr_origin,addr_destin)
        fees = int(fees.decode('utf-8'))

        send_funds = lb.send_funds(wallet01,wallet02,quantity*param,token)

        new_balance01 = balance01 - quantity*param - fees
        new_balance02 = balance02 + quantity*param
        # 60 seconds to allow the blockchain to process and confirm the transaction
        time.sleep(60)
        actual_balance01 = lb.get_balance(wallet01,token)
        actual_balance02 = lb.get_balance(wallet02,token)

        #self.assertTrue (type(test_transactions) is dict)
        self.assertEqual(actual_balance01['lovelace'],new_balance01,"There must be some problem with the transaction")
        self.assertEqual(actual_balance02['lovelace'],new_balance02,"There must be some problem with the transaction")



unittest.main()
