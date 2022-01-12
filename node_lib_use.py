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

transactions = Node.get_transactions('addr_test1qq3nkre520rashkeq843mptpz3wq0l8c4lzw2gpzg0mv3urjkcctzvtrmt0chuqgaphal08kaqhn0gn295v7wefe95eq23ruet')
print(transactions)

balance = Node.get_balance('76619605f95582f288daf4bd8b6188dad8c898d7')
print(balance)

params = {
"message": {
    "tx_info":{
        "id": "987f6d81f4f72c484f6d34c53e7d7f2719f40705",
        "metadata": {
            "4567":{
                "título": "Graduación",
                "Institución": "ACME"
            }
        },
        "mint": [
            {
                "name": "PruebaACME1119",
                "amount": 1,
                "policyID":"",
            },
        ],
    }
}
}
mint_info = Node.minting(params)

print(mint_info)


