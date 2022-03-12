"""
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Section to interact with cardano node lib
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

from node_lib import Node

working_dir = "/home/cardanodatos/git/cnft-python/"

Node = Node(working_dir)

# Node.query_protocol()

# query_tip = Node.query_tip_exec()
# print(query_tip)

# list_wallets = IOT.list_wallets()
# print(list_wallets)

# transactions = Node.get_transactions('addr_test1qze9flv4z2k3pxf94cs9d33ky40qhlzcflv4s2ud7ayufh7skmwuaaukau6fgmer4a07zk0zdahsj2q4zaaayncsv5wqxcmcfs')
# print(transactions)

# balance = Node.get_balance('689f3a6a8132d58fbefe9673bcbe39f1cd8307c4')
# print(balance)

params = {
  "message": {
    "tx_info": {
      "id": "1703ef5f85048194efa2686c22e145c0ae146c11",
      "metadata": {
        "4567": {
          "título": "Para el curso",
          "Institución": "ACME"
        }
      },
      "mint": [
        {
          "name": "556Prueba",
          "amount": 45122333365,
          "policyID": "f2a5629e0c50614a1aa805c56de5537a55957eca4c02f0ad002ba981"
        }
      ]
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


