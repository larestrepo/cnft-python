import json
import library as lb
import wallet_lib as wallet

def result_treatment(obj,client_id):

    """Main function that receives the object from the pubsub and defines which execution function to call"""
    main ={
        'client_id': client_id
    }

    if obj[0]['cmd_id'] == 'query_tip':
        print('Executing query tip')
        result = lb.query_tip_exec()
        result = result.decode('utf-8')
        result = json.loads(result)
        main.update(result)

    elif obj[0]['cmd_id'] == 'query_utxo':
        print('Executing query utxo')
        address = obj[0]['message']['address']
        result = lb.get_transactions(address)
        main.update(result)
    
    elif obj[0]['cmd_id'] == 'generate_new_mnemonic_phrase':
        print('Executing generate_new_mnemonic_phrase')
        size = obj[0]['message']['size']    
        mnemonic = wallet.generate_mnemonic(size)
        main['wallet_mnemonic']=mnemonic
    
    elif obj[0]['cmd_id'] == 'generate_wallet':
        print('Executing generate wallet')
        wallet_status = wallet.create_wallet(obj[0]['message']['wallet_name'], obj[0]['message']['passphrase'],obj[0]['message']['mnemonic'])
        main['wallet_status']=wallet_status
        address = wallet.get_addresses(wallet_status['id'])
        main['address']=address

    elif obj[0]['cmd_id'] == 'wallet_info':
        print('Executing wallet info')
        id = obj[0]['message']['id']
        wallet_info = wallet.wallet_info(id)
        main['wallet_info']=wallet_info
        address = wallet.get_addresses(id)
        main['address']=address
    
    elif obj[0]['cmd_id'] == 'min_fees':
        print('Executing min fees')
        id = obj[0]['message']['id']
        tx_info = obj[0]['message']['tx_info']
        tx_info["time_to_live"]={
                        "quantity": 10,
                        "unit": "second"
                        }
        tx_info["withdrawal"]="self"
        tx_result = wallet.min_fees(id,tx_info)
        main['min_fees']= tx_result
    
    elif obj[0]['cmd_id'] == 'send_transaction':
        print('Executing send transaction')
        id = obj[0]['message']['id']
        tx_info = obj[0]['message']['tx_info']
        tx_info["time_to_live"]={
                        "quantity": 60,
                        "unit": "second"
                        }
        tx_info["withdrawal"]="self"
        tx_result = wallet.send_transaction(id,tx_info)
        main['tx_result']= tx_result
    
    elif obj[0]['cmd_id'] == 'confirm_transaction':
        print('Executing confirmation of the transaction')
        id = obj[0]['message']['id']
        tx_id = obj[0]['message']['tx_id']
        tx_result = wallet.confirm_transaction(id,tx_id)
        main['tx_result']= tx_result
    
    elif obj[0]['cmd_id'] == 'mint_asset':
        print('Executing mint asset')
        id = obj[0]['message']['id']
        print(id)
        tx_info = obj[0]['message']['tx_info']
        print('##########1',tx_info)
        tx_info['time_to_live']={
                        "quantity": 60,
                        "unit": "second"
                        }
        tx_result = wallet.mint_token(id,tx_info)
        main['tx_result']= tx_result
    
    elif obj[0]['cmd_id'] == 'delete_wallet':
        print('Executing wallet deletion')
        id = obj[0]['message']['id']
        wallet_info = wallet.delete_wallet(id)

    
    
    obj.pop(0)
    return main