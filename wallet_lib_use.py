"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Section to interact with cardano wallet lib
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

from node_lib import Wallet

working_dir = "/home/cardanodatos/git/cnft-python/"

wallet = Wallet(working_dir)

list_wallets = wallet.list_wallets()
print(list_wallets)

#Steps to create a wallet

#Generate mnemonic
# mnemonic = wallet.generate_mnemonic(24)
# print(mnemonic)

# #Create wallet
# wallet_created = wallet.create_wallet('my_wallet_name','my_wallet_password',mnemonic)
# print(wallet_created)


# id = wallet_created['id']
# id = "689f3a6a8132d58fbefe9673bcbe39f1cd8307c4"
# #Wallet info
# wallet_info = wallet.wallet_info(id)
# print(wallet_info)

# # Get list of addresses associated to the wallet
# wallet_addresses = wallet.get_addresses(id,'unused')
# print(wallet_addresses)

# # Delete wallet
# wallet_deleted = wallet.delete_wallet(id)
# print(wallet_deleted)

# # Estimate min fees, in the data json file can be specified
# # address as destination with quantity, assets and metadata
# assets = [{
#   "policy_id": "65ab82542b0ca20391caaf66a4d4d7897d281f9c136cd3513136945b",
#   "asset_name": "",
#   "quantity": 0
# }]
# metadata = {
#   "0": {
#       "string": "cardano"
#       },
# }

# data = {
#         "payments": [
#         {
#             "address": "addr_test1qp09lnuch5vgswuxcjlta78mlp88taudhgymyktu3qy44pk8tuvg9dmy75z2dpj0e4kzw642e3hpjt937e4t3jun3l3sftz57e",
#             "amount": {
#                 "quantity": 5000000,
#                 "unit": "lovelace"
#             },
#             "assets": assets
#         }
#         ],
#         "metadata": metadata
#         }

# min_fees = wallet.min_fees(id, data)
# print(min_fees)

# # Send a transaction from previously created data json adding passphrase

# data['passphrase'] = 'my_wallet_password'

# transaction = wallet.send_transaction(id, data)

# # Confirm transaction

# transaction_confirmation = wallet.confirm_transaction(id)

# # Get asset balance

# # asset_balance = wallet.assets_balance(id)
# name='asfgbb'
# mnemonic = ['asdfd', 'df', 'fd']

# passphrase = 'sdfddd'

# generate_wallet = wallet.create_wallet(name, passphrase, mnemonic)