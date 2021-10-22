import json
import library as lb
import wallet_lib as wallet

def result_treatment(obj,client_id):

    """Main function that receives the object from the pubsub and defines which execution function to call"""

    if obj[0]['cmd_id'] == 'query_tip':
        print('Executing {}'.format(obj.pop(0)))
        main ={
            'client-id': client_id
        }
        result = lb.query_tip_exec()
        result = result.decode('utf-8')
        result = json.loads(result)
        main.update(result)

    elif obj[0]['cmd_id'] == 'query_utxo':
        #print('Executing {}'.format(obj.pop(0)))
        print('Executing query utxo')
        main ={
            'client-id': client_id
        }
        address = obj[0]['message']['address']
        result = lb.get_transactions(address)
        main.update(result)
        print(main)
    
    elif obj[0]['cmd_id'] == 'generate_new_mnemonic_phrase':
        print('Executing generate_new_mnemonic_phrase')
        main ={
            'client-id': client_id
        }
        size = obj[0]['message']['size']    
        size = 24
        mnemonic = wallet.generate_mnemonic(size)
        main['wallet_mnemonic']=mnemonic
        print(main['wallet_mnemonic'])

    return main


# mnemonic = subprocess.check_output([
#     'cardano-wallet', 'recovery-phrase', 'generate'
# ])

# print(mnemonic)

# s = subprocess.check_output(["echo", "Hello World!"])
# print("s = " + str(s))