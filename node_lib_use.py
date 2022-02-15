"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Section to interact with cardano node lib
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

from node_lib import Node

working_dir = "/home/cardanodatos/git/cnft-python/"

Node = Node(working_dir)

Node.query_protocol()

query_tip = Node.query_tip_exec()
print(query_tip)

list_wallets = IOT.list_wallets()
print(list_wallets)

transactions = Node.get_transactions('addr_test1qze9flv4z2k3pxf94cs9d33ky40qhlzcflv4s2ud7ayufh7skmwuaaukau6fgmer4a07zk0zdahsj2q4zaaayncsv5wqxcmcfs')
print(transactions)

balance = Node.get_balance('689f3a6a8132d58fbefe9673bcbe39f1cd8307c4')
print(balance)

params = {
"message": {
    "tx_info":{
        "id": "689f3a6a8132d58fbefe9673bcbe39f1cd8307c4",
        "metadata": {
            "4567":{
                "título": "Graduación",
                "Institución": "ACME"
            }
        },
        "mint": [
            {
                "name": "PruebaTolima1",
                "amount": 48,
                "policyID":"",
            },
        ],
    }
}
}
mint_info = Node.minting(params)

print(mint_info)

# params = {
# {
#   "seq": 1,
#   "cmd_id": "generate_wallet",
#   "message": {
#     "wallet_name": "asfgbb",
#     "mnemonic": [
#       "asdfd",
#       "df",
#       "fd"
#     ],
#     "passphrase": "sdfddd"
#   }
# }
# }


