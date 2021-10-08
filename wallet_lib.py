
import subprocess
import requests
import json


URL = 'http://localhost:8090/v2/wallets/'

def generate_mnemonic(size=24):
    command_string = [
        'cardano-wallet', 'recovery-phrase', 'generate',
        '--size', str(size)
    ]
    mnemonic = subprocess.check_output(command_string)
    mnemonic = mnemonic.decode('utf-8')
    mnemonic = mnemonic.split()
    return mnemonic


def create_wallet(name,passphrase,mnemonic):
    
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
