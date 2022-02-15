import os
import subprocess
from decouple import config
import json


with open('./config_file.json') as file:
    params=json.load(file)
keys_file_path = params['node']['keys_path']
if not os.path.exists(keys_file_path):
    os.makedirs(keys_file_path)

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
    if os.path.exists(path+name):
        os.remove(path+name)
    # os.rmdir(path+name)
    # shutil.rmtree(path+name)

def save_metadata(path, metadata):
    if metadata == {}:
        metadata_json_file = ''
    else:
        with open(path + '/' + 'metadata.json','w') as file:
            json.dump(metadata, file,indent=4,ensure_ascii=False)
        metadata_json_file = path + '/' + 'metadata.json'

    return metadata_json_file


def towallet(wallet_id,mnemonic):
    try:
        ################################
        # generating additional keys before the actual creation
        ################################
        #Save temp mnemonic
        content = ' '.join(mnemonic)
        path = keys_file_path + '/' + wallet_id + '/'
        temp_mnemonic = wallet_id + '.temp_mnemonic'
        save_files(path, temp_mnemonic, content)

        # Generate master key
        output = cat_files(path,temp_mnemonic)
        command_string = [
            'cardano-address', 'key', 'from-recovery-phrase', 'Shelley'
        ]
        output2 = subprocess.Popen(command_string,stdin=output.stdout,stdout=subprocess.PIPE)
        output.stdout.close()

        content = output2.communicate()[0].decode('utf-8')
        # Save temp private keys files
        save_files(path,wallet_id + '.root.prv',str(content))
        # Delete file mnemonic
        remove_files(path, temp_mnemonic)

        output = cat_files(path, wallet_id + '.root.prv')
        # Generate stake key
        command_string = [
            'cardano-address', 'key', 'child', '1852H/1815H/0H/2/0'
        ]
        output3 = subprocess.Popen(command_string, stdin=output.stdout,stdout=subprocess.PIPE)
        output.stdout.close()
        # Generate payment key
        output = cat_files(path, wallet_id + '.root.prv')
        command_string = [
            'cardano-address', 'key', 'child', '1852H/1815H/0H/0/0'
        ]
        output4 = subprocess.Popen(command_string, stdin=output.stdout,stdout=subprocess.PIPE)
        output.stdout.close()
        stake_xprv = output3.communicate()[0].decode('utf-8')
        payment_xprv = output4.communicate()[0].decode('utf-8')
        output3.stdout.close()
        output4.stdout.close()

        # Save payment key into file
        save_files(path, wallet_id + '.stake.xprv',str(stake_xprv))
        save_files(path,wallet_id + '.payment.xprv',str(payment_xprv))

        # Generate payment verification key xpub
        output = cat_files(path,wallet_id + '.payment.xprv')
        command_string = [
            'cardano-address', 'key', 'public', '--with-chain-code'
        ]
        output1 = subprocess.Popen(command_string, stdin=output.stdout,stdout=subprocess.PIPE)
        output.stdout.close()
        payment_xpub = output1.communicate()[0].decode('utf-8')
        save_files(path, wallet_id + '.payment.xpub',str(payment_xpub))
        CARDANO_NETWORK = config('CARDANO_NETWORK')

        # Generate payment address from verification key
        output = cat_files(path, wallet_id + '.payment.xprv')
        command_string = [
            'cardano-address', 'address', 'payment', '--network-tag', CARDANO_NETWORK,
        ]
        output1 = subprocess.Popen(command_string,stdin=output.stdout,stdout=subprocess.PIPE)
        output.stdout.close()
        payment_addr = output1.communicate()[0].decode('utf-8')
        save_files(path, wallet_id + '.payment.addr',str(payment_addr))

        # Convert cardano-addresses extended signing keys to corresponding Shelley-format keys.

        command_string = [
            'cardano-cli', 'key', 'convert-cardano-address-key', '--shelley-payment-key', '--signing-key-file',
            path + wallet_id + '.payment.xprv', '--out-file', path + wallet_id + '.payment.skey'
        ]
        subprocess.run(command_string)
        command_string = [
            'cardano-cli', 'key', 'convert-cardano-address-key', '--shelley-stake-key', '--signing-key-file',
            path + wallet_id + '.stake.xprv', '--out-file', path + wallet_id + '.stake.skey'
        ]
        subprocess.run(command_string)

        # Get verification keys from signing keys.
        command_string = [
            'cardano-cli', 'key', 'verification-key', '--signing-key-file', path + wallet_id + '.stake.skey',
            '--verification-key-file', path + wallet_id + '.stake.evkey'
        ]
        subprocess.run(command_string)
        command_string = [
            'cardano-cli', 'key', 'verification-key', '--signing-key-file', path + wallet_id + '.payment.skey',
            '--verification-key-file', path + wallet_id + '.payment.evkey'
        ]
        subprocess.run(command_string)

        # Get non-extended verification keys from extended verification keys.
        command_string = [
            'cardano-cli', 'key', 'non-extended-key', '--extended-verification-key-file', path + wallet_id + '.stake.evkey',
            '--verification-key-file', path + wallet_id + '.stake.vkey'
                ]
        subprocess.run(command_string)
        command_string = [
            'cardano-cli', 'key', 'non-extended-key', '--extended-verification-key-file', path + wallet_id + '.payment.evkey',
            '--verification-key-file', path + wallet_id + '.payment.vkey'
                ]
        subprocess.run(command_string)

        # Build stake and payment addresses
        CARDANO_NETWORK_MAGIC = config('CARDANO_NETWORK_MAGIC')
        command_string = [
            'cardano-cli', 'stake-address', 'build', '--stake-verification-key-file', path + wallet_id + '.stake.vkey',
            '--testnet-magic', CARDANO_NETWORK_MAGIC, '--out-file', path + wallet_id + '.stake.addr'
                ]
        subprocess.run(command_string)
        command_string = [
            'cardano-cli', 'address', 'build', '--payment-verification-key-file', path + wallet_id + '.payment.vkey',
            '--testnet-magic', CARDANO_NETWORK_MAGIC, '--out-file', path + wallet_id + '.payment.addr'
            ]
        subprocess.run(command_string)
        command_string = [
            'cardano-cli', 'address', 'build', '--payment-verification-key-file', path + wallet_id + '.payment.vkey',
            '--stake-verification-key-file', path + wallet_id + '.stake.vkey',
            '--testnet-magic', CARDANO_NETWORK_MAGIC, '--out-file', path + wallet_id + '.base.addr'
            ]
        subprocess.run(command_string)



    except:
        print('problems generating the keys or saving the files')


def topayment_wallet(wallet_id, derivation_path):
        # Generate payment key
        path = keys_file_path + '/' + wallet_id + '/'
        derivation_path_concat = '/'.join(derivation_path)
        output = cat_files(path, wallet_id + '.root.prv')
        command_string = [
            'cardano-address', 'key', 'child', derivation_path_concat
        ]
        output1 = subprocess.Popen(command_string, stdin=output.stdout,stdout=subprocess.PIPE)
        output.stdout.close()
        payment_xprv = output1.communicate()[0].decode('utf-8')
        output1.stdout.close()
        save_files(path,wallet_id + '.payment.xprv',str(payment_xprv))

        # Convert cardano-addresses extended signing keys to corresponding Shelley-format keys.

        command_string = [
            'cardano-cli', 'key', 'convert-cardano-address-key', '--shelley-payment-key', '--signing-key-file',
            path + wallet_id + '.payment.xprv', '--out-file', path + wallet_id + '.payment.skey'
        ]
        subprocess.run(command_string)