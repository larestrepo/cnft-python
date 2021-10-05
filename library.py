import subprocess
from decouple import config

# Import params
CARDANO_NETWORK_MAGIC = config('CARDANO_NETWORK_MAGIC')
CARDANO_CLI_PATH = config('CARDANO_CLI_PATH')
CARDANO_NETWORK = config('CARDANO_NETWORK')

if CARDANO_NETWORK == 'mainnet':
    CARDANO_NETWORK_MAGIC = ""

def query_tip_exec():
    """Executes query tip. 
        No params needed
        Return: json file with latest epoch, hash, slot, block, era, syncProgress
    """
    try:
        command_string = [
            CARDANO_CLI_PATH,
            'query', 'tip',
            '--testnet-magic', str(CARDANO_NETWORK_MAGIC)]
        rawTipResult = subprocess.check_output(command_string)
        return rawTipResult
    except:
        print('query tip error')

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
                # if only lovelace
                # if len(trans) == 4:
                #     transaction['hash'] = trans[0]
                #     transaction['id'] = trans[1]
                #     transaction['amount'] = trans[2]
                #     ada_transactions.append(transaction)
                # else:
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


# Next: query protocol params, calculate min fees, Tx build raw, Sign and submit Tx, Verify Tx, generate keys, cardano-wallet

