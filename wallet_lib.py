
import subprocess
import requests
import sys



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


def create_wallet(name,passphrase,mnemonic):

    import utils
    utils.towallet(name,mnemonic)
    
    data = {
        'name': name,
        'mnemonic_sentence':mnemonic,
        'passphrase': passphrase
    }
    
    # Create wallet
    r = requests.post(URL,json=data)
    return r.json()

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
    r = requests.delete(request_status_url)
    return r.json()

def min_fees(id,data):
    request_address_url = URL + id + '/payment-fees'
    r = requests.post(request_address_url, json=data)
    r = r.json()
    return r

def send_transaction(id,data):
    request_address_url = URL + id + '/transactions'
    r = requests.post(request_address_url, json=data)
    r = r.json()
    return r

def confirm_transaction(id,tx_id):
    request_address_url = URL + id + '/transactions/' + tx_id
    r = requests.get(request_address_url)
    r = r.json()
    return r

def mint_token(id,mint_burn):
    request_address_url = URL + id + '/assets'
    r = requests.post(request_address_url,mint_burn)
    r = r.json()
    return r