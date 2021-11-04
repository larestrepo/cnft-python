
import subprocess
import requests
import sys
import os


URL = 'http://localhost:8090/v2/wallets/'

def list_wallets():
    request_status_url = URL
    wallets_info = requests.get(request_status_url)
    return wallets_info.json()

def generate_mnemonic(size=24):
    try:
        # Generate mnemonic
        command_string = [
            'cardano-wallet', 'recovery-phrase', 'generate',
            '--size', str(size)
        ]
        mnemonic = subprocess.check_output(command_string)
        mnemonic = mnemonic.decode('utf-8')
        mnemonic = mnemonic.split()
        return mnemonic

    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)


    # with open('./temp_keys','w') as file:
    #     file.write(str(mnemonic))

def save_files(path,name,content):
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + name,'w') as file:
        file.write(content)

def cat_files(path,name):
    # Generate master key
    command_string = [
        'cat', path + name
    ]
    output = subprocess.Popen(command_string, stdout=subprocess.PIPE)
    return output

def remove_files(path,name):
    os.remove(path+name)


def create_wallet(name,passphrase,mnemonic):
    # try: 
    #     ################################
    #     # generating additional keys before the actual creation
    #     ################################
    #     #Save temp mnemonic
    #     content = ' '.join(mnemonic)
    #     path = './priv/' + name + '/'
    #     name = 'temp_mnemonic'
    #     save_files(path, 'temp_mnemonic', content)

    #     # Generate master key
    #     output = cat_files(path,'temp_mnemonic')
    #     # command_string = [
    #     #     'cat', 'temp_mnemonic'
    #     # ]
    #     # output = subprocess.Popen(command_string, stdout=subprocess.PIPE)
    #     command_string2 = [
    #         'cardano-address', 'key', 'from-recovery-phrase', 'Shelley'
    #     ]
    #     output2 = subprocess.Popen(command_string2,stdin=output.stdout,stdout=subprocess.PIPE)
    #     output.stdout.close()

    #     # Delete file mnemonic
    #     remove_files(path,'temp_mnemonic')
    #     content = output2.communicate()[0].decode('utf-8')
    #     # Save temp private keys files
    #     save_files(path,'root.prv',str(content))

    #     output = cat_files(path,'root.prv')
    #     # Generate stake key
    #     command_string3 = [
    #         'cardano-address', 'key', 'child', '1852H/1815H/0H/2/0'
    #     ]
    #     output3 = subprocess.Popen(command_string3, stdin=output.stdout,stdout=subprocess.PIPE)
    #     output.stdout.close()
    #     # Generate payment key
    #     output = cat_files(path,'root.prv')
    #     command_string4 = [
    #         'cardano-address', 'key', 'child', '1852H/1815H/0H/0/0'
    #     ]
    #     output4 = subprocess.Popen(command_string4, stdin=output.stdout,stdout=subprocess.PIPE)
    #     output.stdout.close()
    #     stake_xprv = output3.communicate()[0].decode('utf-8')
    #     payment_xprv = output4.communicate()[0].decode('utf-8')

    #     # Save payment key into file
    #     save_files(path,'stake.xprv',str(stake_xprv))
    #     save_files(path,'payment.xprv',str(payment_xprv))

    # except:
    #     print('problems generating the keys or saving the files')
    # finally:
    # # Wallet from seed mnemonic
    data = {
        'name': name,
        'mnemonic_sentence':mnemonic,
        'passphrase': passphrase
    }
    
    # Implement mnemonic second factor
    # Create wallet
    r = requests.post(URL,json=data)
    r = r.json()

    return r

def wallet_info(id):
    request_status_url = URL + id
    wallet_info = requests.get(request_status_url)
    return wallet_info.json()

def get_addresses(id):
    #Get only unused addresses
    request_address_url = URL + id + '/addresses?state=unused'
    addresses = requests.get (request_address_url)
    return addresses.json()

def delete_wallet(id):
    request_status_url = URL + id
    wallet_info = requests.delete(request_status_url)
    return wallet_info.json()

def min_fees(id,data):
    request_address_url = URL + id + '/payment-fees'
    r = requests.post(request_address_url, json=data)
    r = r.json()
    print(r)
    return r

def send_transaction(id,data):
    request_address_url = URL + id + '/transactions'
    r = requests.post(request_address_url, json=data)
    r = r.json()
    print(r)
    return r
