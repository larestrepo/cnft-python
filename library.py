import subprocess
from decouple import config
import json, os
import random
import shlex

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

def build_raw_tx(TxHash, addr, fee):
    """
    Transaction build raw.
    :param address: TxHash of the origin address, address origin and destin
    :return: tx_build file
    """
    try:
        command_string = [
            CARDANO_CLI_PATH,
            'transaction', 'build-raw',
            '--fee', str(fee),
            '--out-file', protocol_file_path + '/tx.draft']

        i = 0
        for utxo in TxHash:
            command_string.insert(3+i,'--tx-in')
            command_string.insert(4+i,utxo[0])
            i += 2
        for address in addr:
            command_string.insert(3+i,'--tx-out')
            command_string.insert(4+i,address[0])
            i += 2
        print(command_string)
        subprocess.check_output(command_string)
    except:
        print('Tx build raw error')

def tx_min_fee(tx_in_count,tx_out_count):
    """Calculates the expected min fees . 
        No params needed
        Return: Min fees value
    """
    command_string = [
        CARDANO_CLI_PATH,
        'transaction', 'calculate-min-fee',
        '--tx-body-file', protocol_file_path + '/tx.draft',
        '--tx-in-count', tx_in_count,
        '--tx-out-count', tx_out_count,
        '--witness-count', str(1),
        '--testnet-magic', str(CARDANO_NETWORK_MAGIC),
        '--protocol-params-file', protocol_file_path+'/protocol.json']
    rawResult = subprocess.check_output(command_string)
    rawResult = rawResult.split()
    rawResult = rawResult[0]
    return rawResult

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

def utxo_selection(addr_origin_tx, token, quantity, deplete):
    """ Function based on the coin selection algorithm to properly handle the use of utxos in the wallet. 
    Rules are:
    1. If any of your UTXO matches the Target it will be used.
    2. If the "sum of all your UTXO smaller than the Target" happens to match the Target, they will be used. (This is the case if you sweep a complete wallet.)
    3. If the "sum of all your UTXO smaller than the Target" doesn't surpass the target, the smallest UTXO greater than your Target will be used.
    4. Else Bitcoin Core does 1000 rounds of randomly combining unspent transaction outputs until their sum is greater than or equal to the Target. If it happens to find an exact match, it stops early and uses that.
        Otherwise it finally settles for the minimum of

            the smallest UTXO greater than the Target
            the smallest combination of UTXO it discovered in Step 4.

    https://github.com/bitcoin/bitcoin/blob/3015e0bca6bc2cb8beb747873fdf7b80e74d679f/src/wallet.cpp#L1276
    https://bitcoin.stackexchange.com/questions/1077/what-is-the-coin-selection-algorithm
    """

    #Applying the coin selection algorithm
    minUTXO = 1000000
    TxHash = []
    TxHash_lower = []
    amount_lower = []
    TxHash_greater = []
    amount_greater = []
    utxo_found = False
    transactions = addr_origin_tx['transactions'][:]
    for utxo in addr_origin_tx['transactions']:
        for amount in utxo['amounts']:
            if amount['token']==token: 
                if deplete:
                    TxHash.append([utxo['hash'] + '#' + utxo['id']])
                    amount_equal = int(amount['amount'])
                    utxo_found = True
                    break
                if int(amount['amount']) == quantity:
                    TxHash.append([utxo['hash'] + '#' + utxo['id']])
                    amount_equal = int(amount['amount'])
                    utxo_found = True
                    break
                elif int(amount['amount']) < quantity + minUTXO:
                    TxHash_lower.append(utxo['hash'] + '#' + utxo['id'])
                    amount_lower.append(int(amount['amount']))
                elif int(amount['amount']) > quantity + minUTXO:
                    TxHash_greater.append(utxo['hash'] + '#' + utxo['id'])
                    amount_greater.append(int(amount['amount']))

    if not utxo_found:
        if sum(amount_lower) == quantity:
            TxHash = TxHash_lower
            amount_equal = sum(amount_lower)
        elif sum(amount_lower) < quantity:
            if amount_greater == []:
                TxHash = []
                amount_equal = 0
            amount_equal = min(amount_greater)
            index = [i for i, j in enumerate(amount_greater) if j == amount_equal][0]
            TxHash.append([TxHash_greater[index]])
        else:
            utxo_array = []
            amount_array = []
            for _ in range(999):
                index_random = random.randint(0,len(transactions)-1)
                # utxo = addr_origin_tx['transactions'][index_random]
                utxo = transactions.pop(index_random)
                utxo_array.append([utxo['hash'] + '#' + utxo['id']])
                for amount in utxo['amounts']:
                    if amount['token']==token: 
                        amount_array.append(int(amount['amount']))
                if sum(amount_array) >= quantity + minUTXO:
                    amount_equal = sum(amount_array)
                    break
            TxHash = utxo_array

    return TxHash, amount_equal

def get_balance(wallet,token):
    if token=='ADA':
        token='lovelace'
    wallet = wallet_to_address(wallet)
    transactions = get_transactions(wallet)
    balance_dict = {}
    if transactions == {}:
        if token=='lovelace':
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
        if token=='lovelace':
            balance_dict['lovelace']=balance
            balance_dict['ADA']=balance/1000000
        else:
            balance_dict[token]=balance
        return balance_dict

def send_funds(wallet_origin, wallet_destin, quantity, token, deplete):
    """Sign and submit. 
        :param address: TxHash of the origin address, address origin and destin
        Return: 
    """
    minUTXOValue = 1000000
    addr_origin = wallet_to_address(wallet_origin)
    addr_destin = wallet_to_address(wallet_destin)
    if token=='ADA':
        token = 'lovelace'
        param = 1000000
    else:
        param = 1
    quantity = quantity*param
    addr_origin_tx = get_transactions(addr_origin)
    balance = get_balance(addr_origin,token)

    addr_zero = []
    if deplete: 
        quantity_calculated = balance['lovelace']
    else:
        quantity_calculated = quantity + 200000
        addr_zero.append([addr_origin + '+' + str(0)])
    
    addr_zero.append([addr_destin + '+' + str(0)])
    
    if addr_origin_tx == {} or balance['lovelace'] < quantity_calculated:
        print("No funds available in the origin wallet")
    elif quantity < minUTXOValue:
        print('OutputTooSmallUTxo')
    else:
        TxHash_in, amount_equal = utxo_selection(addr_origin_tx,token,quantity_calculated,deplete)

        if TxHash_in==[]:
            print("No funds available in the origin wallet")
        else:
            ###########################
            # Section to calculate min fees
            ###########################
            #Create the tx_raw file to calculate the min fee
            build_raw_tx(TxHash_in, addr_zero, 0)
            #Calculate min fees based on previously tx_raw file
            fee = tx_min_fee(str(len(TxHash_in)),str(len(addr_zero)))
            fee = int(fee.decode('utf-8'))
            print(fee)
            
            ###########################
            # Section to build the actual transaction including fees
            ###########################
            addr = []
            if deplete: 
                # quantity_fee = balance['lovelace'] - fee
                TxHash_in, amount_equal = utxo_selection(addr_origin_tx,token,0, deplete)
            else:
                quantity_fee = quantity + fee
                TxHash_in, amount_equal = utxo_selection(addr_origin_tx,token,quantity_fee,deplete)
                final_balance = amount_equal - quantity_fee
                addr.append([addr_origin + '+' + str(int(final_balance))])

            addr.append([addr_destin + '+' + str(int(quantity))])
            
            
            #Create the tx_raw file with the fees included
            
            build_raw_tx(TxHash_in, addr, fee)

            print("################################")
            print("Sending '{}' from {} to {}. Fees are: {}".format(quantity, wallet_origin, wallet_destin,fee))
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