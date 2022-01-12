# CardanoPython

There are 2 ways to interact with this library.

1. With Cardano node and Cardano wallet installed (installation instruction in separate file) you can just simply install the CardanoPython SDK and start using it:
[Cardano_installation.md](https://github.com/larestrepo/cnft-python/blob/main/cardano_installation.md).

2. If you want to use this library but don't have installed Cardano node or Cardano wallet, then you need to configure your server/interface as a client API. We are using IOT core to open a websocket subscription to allow communication with our infrastructure. Instructions below.
##

### Prerequesites

1. Cardano-node running
2. Cardano wallet running. Some of the built-in functionalities can be covered from CLI but there are some functionalities that we want to make them through the API wallet.



This library relies on a file called config_file.json

```json
{"node":{
        "keys_path": "./priv/wallets",
        "transactions": "./priv/transactions",
        "CARDANO_NETWORK": "testnet",
        "CARDANO_NETWORK_MAGIC": 1097911063,
        "CARDANO_CLI_PATH": "cardano-cli",
        "URL": "http://localhost:8090/v2/wallets/"
    }
}
```

There are 3 classes in the library all contained in the file node_lib.py: Node, Wallet, IOT

a. Wallet class

List of methods:

- list_wallets
- generate_mnemonic
- create_wallet
- wallet_info
- get_addresses
- delete_wallet
- min_fees
- send_transaction
- confirm_transaction
- assets_balance

b. Node class

- query_protocol
- query_tip
- get_transactions
- get_balance
- minting

To instantiate the class, just call it with the working directory param. The working directory path must contain the config_file.json file.

For example:

```python
from node_lib import Wallet

working_dir = "/home/cardanodatos/git/cnft-python/"

wallet = Wallet(working_dir)

list_wallets = wallet.list_wallets()
print(list_wallets)

mnemonic = wallet.generate_mnemonic(24)
print(mnemonic)
```

For a full list of methods available and the usage see:
[wallet_lib_use](https://github.com/larestrepo/cnft-python/blob/main/wallet_lib_use.py)


3. AWS IOT Core configure. Basic instructions are explained here. 

#

### AWS IoT basic setup

Steps to configure basic communication (subscribe and connect)

In AWS account: 

1. Create a thing
2. Create certificates and attach to thing
3. Create policyID and attach to the certificates

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iot:Connect",
      "Resource": "arn:<your specific end_point>:client/${iot:Connection.Thing.ThingName}"
    },
    {
      "Effect": "Allow",
      "Action": "iot:Publish",
      "Resource": "arn:aws:<your specific end_point>:topic/sensor/data"
    }
  ]
}
```
4. Upload certificates to the remote "sensor" (Private and public keys, and root CA certificates Starfield Root CA Certificate) 

Ref: https://docs.aws.amazon.com/iot/latest/developerguide/server-authentication.html?icmpid=docs_iot_console#server-authentication-certs

5. (Optional) Start the app (AWS-thing.py) 

If you subscribe in AWS IoT, you should see a return message similar to: 

```json
{
  "deviceid": "1",
  "datatime": "2021-09-24 10:48:41",
  "temperature": "11",
  "humidity": "90",
  "windDirection": "5",
  "windIntensity": "28",
  "rainHeight": "23"
}
```

##

### AWS IoT with sdk-python-v2 setup

Use this file as reference:

https://github.com/aws/aws-iot-device-sdk-python-v2/blob/main/samples/pubsub.py


#### In addition to the previous steps in the basic setup and to start the pubsub using the websocket option 

1. Configure IAM user to allow the use of websockets with the sdk according to this guideline:

 Ref: https://docs.aws.amazon.com/iot/latest/developerguide/device-advisor-setting-up.html

2. Create the files in ~/.aws/credentials and ~/.aws/config

#### credentials:

    [default]
    aws_access_key_id=AKIAIOSFODNN7EXAMPLE
    aws_secret_access_key=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY

#### config

    [default]
    region=us-west-2
    output=json

Ref: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html

3. (Optional) In AWS CloudShell you could do:

    aws configure

And follow the steps from the shell. 

4. Create additional folders to contain certificates and secrets

It is needed cert, key and root-ca files. (Similar to Point 4 of the AWS basic setup)


### Publish command from AWS IOT Core to Cardano-node

Source CARDANO_NODE_SOCKET_PATH to bashrc

    echo "export CARDANO_NODE_SOCKET_PATH=/opt/cardano/cnode/sockets/node0.socket" >> ~/.bashrc

Commands are sent in json format. The fields are:

seq (type: int): Indicates the number of messages to receive to build the command. Currently 1 is used which means that all the information needed to build the command is sent in one json.

cmd_id (type: string): command identifier

message (type: string): in case any additional parameter is needed to build the command i.e. wallet address.

1. Query tip

```json
{
  "seq": 1,
  "cmd_id": "query_tip",
  "message": ""
}
```
2. generate_new_mnemonic_phrase
```json
{
  "seq": 1,
  "cmd_id": "generate_new_mnemonic_phrase",
  "message": { 
		"size": 24
  }
}
```
3. generate wallet
```json
{
  "seq": 1,
  "cmd_id": "generate_wallet",
  "message": {
		"wallet_name": "wallet_name",
		"passphrase": "passphrase",
		"mnemonic": "mnemonic",
  }
}
```
4. wallet info
```json
{
  "seq": 1,
  "cmd_id": "wallet_info",
  "message": {
		"id": "id"
  }
}
```
5. min fees
```json
{
    "seq": 1,
    "cmd_id": "min_fees",
    "message": {
            "id": "2781d44e82ad834750c8fd2654faccd2db912eaa",
            "tx_info": {
            "payments": [
            {
                "address": "addr_test1qp09lnuch5vgswuxcjlta78mlp88taudhgymyktu3qy44pk8tuvg9dmy75z2dpj0e4kzw642e3hpjt937e4t3jun3l3sftz57e",
                "amount": {
                    "quantity": 5000000,
                    "unit": "lovelace"
                },
                "assets": null
            }
            ],
            "metadata": null
        }
    }
}
```
6. Send transactions
```json
{
    "seq": 1,
    "cmd_id": "send_transaction",
    "passphrase": "Contraseña de gastos",
    "message": {
            "id": "987f6d81f4f72c484f6d34c53e7d7f2719f40705",
            "tx_info": {
            "payments": [
            {
                "address": "addr_test1qp09lnuch5vgswuxcjlta78mlp88taudhgymyktu3qy44pk8tuvg9dmy75z2dpj0e4kzw642e3hpjt937e4t3jun3l3sftz57e",
                "amount": {
                    "quantity": 5000000,
                    "unit": "lovelace"
                },
                "assets": null
            }
            ],
            "metadata": null
        }
    }
}
```
7. Confirm transaction
```json
{
        "seq": 1,
        "cmd_id": "confirm_transaction",
        "message": {
            "id": "2781d44e82ad834750c8fd2654faccd2db912eaa"
        }
}


```
8. Confirm transaction by tx id
```json
{
        "seq": 1,
        "cmd_id": "confirm_transaction_by_tx",
        "message": {
            "id": "2781d44e82ad834750c8fd2654faccd2db912eaa",
            "tx_id": "b9f044b9c1f4f981ede4f576b0aee37a2b3b0d153c924d69763daa392822c0ae"
        }
}


```

9. Mint token
```json

{
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
            "amount": 35,
            "policyID": "1f4df2e4cb4c94705bed1312646d95c9b0f4ec342445619c65593601"
          }
        ]
      }
    }
  }
}

```
10. Delete wallet

```json
{
  "seq": 1,
  "cmd_id": "delete_wallet",
  "message": {
		"id": "id"
  }
}
```
11. assets info
```json
{
  "seq": 1,
  "cmd_id": "assets_balance",
  "message": {
		"id": "id"
  }
}
```
12. Get transactions
```json
{
  "seq": 1,
  "cmd_id": "get_transactions",
  "message": {
		"address": "address"
  }
}
```



