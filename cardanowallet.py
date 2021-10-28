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
        #size = 24
        mnemonic = wallet.generate_mnemonic(size)
        main['wallet_mnemonic']=mnemonic
    
    elif obj[0]['cmd_id'] == 'generate_wallet':
        print('Executing generate wallet')
        #print(obj[0]['message']['wallet_name'])
        wallet_status = wallet.create_wallet(obj[0]['message']['wallet_name'], obj[0]['message']['passphrase'],obj[0]['message']['mnemonic'])
        main['wallet_status']=wallet_status
        address = wallet.get_addresses(wallet_status['id'])
        main['address']=address

    elif obj[0]['cmd_id'] == 'wallet_info':
        print('Executing wallet info')
        wallet_info = wallet.wallet_info(obj[0]['id'])
        main['wallet_info']=wallet_info
    
    
    obj.pop(0)
    return main