import subprocess
from decouple import config
import json, os

# Import params
CARDANO_NETWORK_MAGIC = config('CARDANO_NETWORK_MAGIC')
CARDANO_CLI_PATH = config('CARDANO_CLI_PATH')
CARDANO_NETWORK = config('CARDANO_NETWORK')

if CARDANO_NETWORK == 'mainnet':
    CARDANO_NETWORK_MAGIC = ""

with open('./config_file.json') as file:
    params=json.load(file)

protocol_file_path = params['wallets']['protocol']
if not os.path.exists(protocol_file_path):
    os.makedirs(protocol_file_path)

keys_file_path = params['wallets']['keys_path']
if not os.path.exists(keys_file_path):
    os.makedirs(keys_file_path)

def wallet_to_address(wallet):
    if not wallet.startswith('addr' or 'DdzFF'):
        with open(keys_file_path + '/' + wallet + '/' + wallet + '.payment.addr','r') as file:
            wallet = file.readlines(1)[0]
    return wallet

try:
    """Executes query protocol parameters.
    Return: json file with protocol.json parameters"""
    command_string = [
        CARDANO_CLI_PATH,
        'query', 'protocol-parameters',
        '--testnet-magic', str(CARDANO_NETWORK_MAGIC),
        '--out-file', protocol_file_path+'/protocol.json']
    subprocess.check_output(command_string)
except:
    print('query protocol error')

def query_tip_exec():
    """Executes query tip. 
        No params needed
        Return: json with latest epoch, hash, slot, block, era, syncProgress
    """
    try:
        command_string = [
            CARDANO_CLI_PATH,
            'query', 'tip',
            '--testnet-magic', str(CARDANO_NETWORK_MAGIC)]
        rawResult = subprocess.check_output(command_string)
        rawResult = rawResult.decode('utf-8')
        return rawResult
    except:
        print('query tip error')

def build_raw_tx(TxHash, addr_origin, addr_destin, balance_origin, quantity, fee):
    """
    Transaction build raw.
    :param address: TxHash of the origin address, address origin and destin
    :return: tx_build file
    """
    try:
        command_string = [
            CARDANO_CLI_PATH,
            'transaction', 'build-raw',
            '--tx-in', TxHash,
            '--tx-out', addr_destin + '+' + str(quantity),
            '--tx-out', addr_origin + '+' + str(balance_origin) + '+' #+ "1 e1b35fa3a3293746a4d9980491df17575987fa119287e3993c499839.AN1744",
            '--fee', str(fee),
            '--out-file', protocol_file_path + '/tx.draft']
        print(command_string)
        subprocess.check_output(command_string)
    except:
        print('Tx build raw error')

def tx_min_fee():
    """Calculates the expected min fees . 
        No params needed
        Return: Min fees value
    """
    try:
        command_string = [
            CARDANO_CLI_PATH,
            'transaction', 'calculate-min-fee',
            '--tx-body-file', protocol_file_path + '/tx.draft',
            '--tx-in-count', str(1),
            '--tx-out-count', str(2),
            '--witness-count', str(1),
            '--testnet-magic', str(CARDANO_NETWORK_MAGIC),
            '--protocol-params-file', protocol_file_path+'/protocol.json']
        rawResult = subprocess.check_output(command_string)
        rawResult = rawResult.split()
        rawResult = rawResult[0]
        return rawResult
    except:
        print('Calculation of min fees error')

def get_transactions(address):
    """
    Get the list of transactions from the given addresses.
    :param address: Cardano Blockchain address to search for UTXOs
    :param tokens_amounts: Dictionary where all tokens amounts are saved
    :return: ada_transactions, token_transactions
            ada_transactions: list of transactions with lovelace only
            token_transactions: list of transactions including custom tokens
    """

    try:
        command_string = [
            CARDANO_CLI_PATH,
            'query', 'utxo',
            '--address', address,
            '--testnet-magic', str(CARDANO_NETWORK_MAGIC)]
        rawTipResult = subprocess.check_output(command_string)
        rawTipResult = rawTipResult.decode('utf-8')

        # Unpacking the results
        transactions = {}
        token_transactions = []
        for line in rawTipResult.splitlines():
            if 'lovelace' in line:
                transaction = {}
                trans = line.split()
                #if only lovelace
                if len(trans) == 4:
                    transaction['hash'] = trans[0]
                    transaction['id'] = trans[1]
                    transaction['amount'] = trans[2]
                    token_transactions.append(transaction)
                else:
                    transaction['hash'] = trans[0]
                    transaction['id'] = trans[1]
                    transaction['amounts'] = []
                    tr_amount = {}
                    tr_amount['token'] = trans[3]
                    tr_amount['amount'] = trans[2]
                    transaction['amounts'].append(tr_amount)
                    # for each token
                    for i in range(0, int((len(trans) - 4) / 3)):
                        tr_amount = {}
                        tr_amount['token'] = trans[3 + i * 3 + 3]
                        tr_amount['amount'] = trans[3 + i * 3 + 2]
                        transaction['amounts'].append(tr_amount)
                    token_transactions.append(transaction)
                    # add the tokens to total amounts to spend
                    # for t in transaction['amounts']:
                    #     if t['token'] in tokens_amounts:
                    #         tokens_amounts[t['token']] += int(t['amount'])
                    #     else:
                    #         tokens_amounts[t['token']] = int(t['amount'])
                transactions['transactions'] = token_transactions
        return transactions
    except:
        print('Query utxo error')


def get_balance(wallet,token):
    if token=='ADA':
        token='lovelace'
    wallet = wallet_to_address(wallet)
    transactions = get_transactions(wallet)
    balance_dict = {}
    if transactions == {}:
        if token=='lovelace' or 'ADA':
            balance_dict['lovelace']=0
            balance_dict['ADA']=0
        else:
            balance_dict[token]=0
        return balance_dict
    else:
        balance = 0
        for utxo in transactions['transactions']:
            for amount in utxo['amounts']:
                if amount['token']==token:
                    balance = balance + int(amount['amount'])
        if token=='lovelace' or token=='ADA':
            balance_dict['lovelace']=balance
            balance_dict['ADA']=balance/1000000
        else:
            balance_dict[token]=balance
        return balance_dict

def send_funds(wallet_origin, wallet_destin, quantity, token):
    """Sign and submit. 
        :param address: TxHash of the origin address, address origin and destin
        Return: 
    """
    addr_origin = wallet_to_address(wallet_origin)
    addr_destin = wallet_to_address(wallet_destin)

    try:
        addr_origin_tx = get_transactions(addr_origin)
        if addr_origin_tx == {}: # not the only reason why we should print the no funds available
            print("No funds available in the origin wallet")
        else:
            if token=='ADA':
                token = 'lovelace'
                param = 1000000
            else:
                param = 1
            #Find utxo, for the time being not handling dust. The wallet should offer to unify the utxos with small balances.
            balance = 0
            for utxo in addr_origin_tx['transactions']:
                for amount in utxo['amounts']:
                    if amount['token']==token: 
                        balance = round(int(amount['amount'])) + balance
                        if int(amount['amount'])>= quantity*param:
                            TxHash = utxo['hash'] + '#' + utxo['id']
                
            balance_origin = balance - (quantity*param)
            
            #Create the tx_raw file to calculate the min fee
            build_raw_tx(TxHash, addr_origin, addr_destin, 0, 0, 0)
            #Calculate min fees based on previously tx_raw file
            fee = tx_min_fee()
            fee = int(fee.decode('utf-8'))
            print(fee)

            #Find utxo, for the time being not handling dust. The wallet should offer to unify the utxos with small balances. 
            #Exploring cardano-wallet to handle utxo pick up.
            for utxo in addr_origin_tx['transactions']:
                for amount in utxo['amounts']:
                    if amount['token']==token and int(amount['amount'])>= quantity*param + fee:
                        TxHash = utxo['hash'] + '#' + utxo['id']
                        balance_origin = round(int(amount['amount'])- (quantity*param) - fee)

            #Create the tx_raw file with the fees included
            build_raw_tx(TxHash, addr_origin, addr_destin, balance_origin, quantity*param, fee)

            print("################################")
            print("Sending '{}' from {} to {}. Fees are: {}".format(quantity*param, wallet_origin, wallet_destin,fee))
            print("################################")

            # Sign the transaction based on tx_raw file.
            # For the time being not handling multi-witness
            command_string = [
                CARDANO_CLI_PATH,
                'transaction', 'sign',
                '--tx-body-file', protocol_file_path + '/tx.draft',
                '--signing-key-file', keys_file_path + '/' + wallet_origin + '/' + wallet_origin + '.payment.skey',
                '--testnet-magic', str(CARDANO_NETWORK_MAGIC),
                '--out-file', protocol_file_path + '/tx.signed']
            subprocess.check_output(command_string)

            # Submit the transaction
            command_string = [
                CARDANO_CLI_PATH,
                'transaction', 'submit',
                '--tx-file', protocol_file_path + '/tx.signed',
                '--testnet-magic', str(CARDANO_NETWORK_MAGIC)]
                
            rawResult= subprocess.check_output(command_string)
            print(rawResult)
    except:
        print('Could not send the transaction')