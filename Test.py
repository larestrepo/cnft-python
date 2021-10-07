import unittest
import library as lb

utxoHash = 'edfe874cfcb0ac5d0d4d9c14248abc374c6d2683a4a518332b18be9999bba9a0#0'
walletName = 'acdc'
wallet01 = 'main'
wallet02 = 'Will_Cotrino_2'
quantity = 3000000
token = 'ADA'


class TestLibrary (unittest.TestCase):

    
    """Steps to send funds
        1.Check the balance of the source wallet
        2. Pick Utxo hash 
        2. Build raw tx file 
        3. Calculate min fees
        4. Build raw tx file including min fees
        5. Sign the transaction
        6. Submit the transaction
    """

    # def test_querytip(self):
    #     query_tip = lb.query_tip_exec()
    #     print(query_tip)
    #     self.assertFalse(query_tip == {})

    # def test_getbalance(self):
    #     #pending testing with different tokens
    #     balance = lb.get_balance(walletName,token)
    #     print(balance)
    #     self.assertTrue(type(balance) is dict)

    # def test_get_transactions(self):
    #     test_transactions = lb.get_transactions(wallet01)
    #     print(test_transactions)
    #     self.assertTrue(type(test_transactions) is dict)


    # def test_min_fee(self):
    #     test_fee = lb.tx_min_fee(utxoHash,wallet01,wallet02)
    #     print (test_fee)
    #     self.assertFalse(test_fee=={})
    
    # def test_tx_submmit(self):
    #     test_submmit = lb.sign_submmit(utxoHash, quantity, token, wallet01, wallet02)


    def test_send_funds(self):
        send_funds = lb.send_funds(wallet01,wallet02,2,'ADA')



unittest.main()
