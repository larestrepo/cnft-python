import subprocess
from itertools import groupby
from operator import add, itemgetter
import os
import json
import utils
import random


class Node():
    def __init__(self,
    CARDANO_NETWORK,
    CARDANO_CLI_PATH,
    CARDANO_NETWORK_MAGIC,
    TRANSACTION_PATH_FILE,
    KEYS_FILE_PATH,
    wallet_id,
    ):

        self.CARDANO_CLI_PATH = CARDANO_CLI_PATH
        self.CARDANO_NETWORK_MAGIC = CARDANO_NETWORK_MAGIC
        self.TRANSACTION_PATH_FILE = TRANSACTION_PATH_FILE
        self.CARDANO_NETWORK = CARDANO_NETWORK
        self.KEYS_FILE_PATH = KEYS_FILE_PATH
        self.wallet_id = wallet_id


    def insert_command(self, index, step, command_string, opt_commands):
        i = 0
        for opt_command in opt_commands:
            command_string.insert(index+i,str(opt_command))
            i += step
        print(command_string)
        return command_string, i

    def id_to_address(self, wallet_id):
        if not wallet_id.startswith('addr' or 'DdzFF'):
            with open(self.KEYS_FILE_PATH + '/' + wallet_id + '/' + wallet_id + '.payment.addr','r') as file:
                address = file.readlines(1)[0]
        else:
            address = wallet_id
        return address

    def query_protocol(self):
        """Executes query protocol parameters.
        Return: json file with protocol.json parameters"""
        command_string = [
            self.CARDANO_CLI_PATH,
            'query', 'protocol-parameters',
            '--out-file', self.TRANSACTION_PATH_FILE +'/protocol.json']
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(3,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        print(command_string)
        subprocess.check_output(command_string)

    def query_tip_exec(self):
        """Executes query tip. 
            No params needed
            Return: json with latest epoch, hash, slot, block, era, syncProgress
        """
        command_string = [
            self.CARDANO_CLI_PATH,
            'query', 'tip']
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(3,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])

        rawResult = subprocess.check_output(command_string)
        rawResult = rawResult.decode('utf-8')
        return rawResult
        
    def get_transactions(self, wallet_id):
        """
        Get the list of transactions from the given addresses.
        :param address: Cardano Blockchain address to search for UTXOs
        :param tokens_amounts: Dictionary where all tokens amounts are saved
        :return: ada_transactions, token_transactions
                ada_transactions: list of transactions with lovelace only
                token_transactions: list of transactions including custom tokens
        """
        address = self.id_to_address(wallet_id)
        command_string = [
            self.CARDANO_CLI_PATH,
            'query', 'utxo',
            '--address', address]
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(5,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
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

    def get_balance(self, wallet_id):
            wallet_id = self.id_to_address(wallet_id)
            transactions = self.get_transactions(wallet_id)
            balance_dict = {}

            balance = 0
            transactions = transactions['transactions']
            amounts = []
            for utxo in transactions:
                for amount in utxo['amounts']:
                    amounts.append(amount)
            amounts = sorted(amounts, key = itemgetter('token'))
            for key, value in groupby(amounts, key = itemgetter('token')):
                # print(f'The balance of "{key}" is: ')
                for k in value:
                    balance = balance + int(k['amount'])
                    # print(k)
                balance_dict[key]=balance
                print(f'Total balance of "{key}" is "{balance}"')

            return balance_dict

    def utxo_selection(self, addr_origin_tx, token, quantity, deplete):
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
        for utxo in transactions:
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
                TxHash.append('--tx-in')
                TxHash.append(TxHash_lower)
                amount_equal = sum(amount_lower)
            elif sum(amount_lower) < quantity:
                if amount_greater == []:
                    TxHash = []
                    amount_equal = 0
                amount_equal = min(amount_greater)
                index = [i for i, j in enumerate(amount_greater) if j == amount_equal][0]
                TxHash.append('--tx-in')
                TxHash.append(TxHash_greater[index])
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
                TxHash.append('--tx-in')
                TxHash.append(utxo_array)

        return TxHash, amount_equal

    def tx_min_fee(self, tx_in_count,tx_out_count):
        """Calculates the expected min fees . 
            No params needed
            Return: Min fees value
        """
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'calculate-min-fee',
            '--tx-body-file', self.TRANSACTION_PATH_FILE + '/tx.draft',
            '--tx-in-count', tx_in_count,
            '--tx-out-count', tx_out_count,
            '--witness-count', str(1),
            # '--testnet-magic', str(self.CARDANO_NETWORK_MAGIC),
            '--protocol-params-file', self.TRANSACTION_PATH_FILE + '/protocol.json']
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(11,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        rawResult = subprocess.check_output(command_string)
        rawResult = rawResult.split()
        rawResult = rawResult[0]
        return rawResult

    def build_raw_tx(self, TxHash, addr, fee, metadata_json_file, mint,script):
        """
        Transaction build raw.
        :param address: TxHash of the origin address, address origin and destin
        :return: tx_build file
        """
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'build-raw',
            '--fee', str(fee),
            '--out-file', self.TRANSACTION_PATH_FILE + '/tx.draft']
        i = 0
        command_string, index = self.insert_command(3+i,1,command_string,TxHash)
        i = i + index
        command_string, index = self.insert_command(3+i,1,command_string,addr)
        i = i + index
        metadata = []
        if metadata_json_file != '':
            metadata.append('--metadata-json-file')
            metadata.append(metadata_json_file)
            command_string, index = self.insert_command(3+i,1,command_string,addr)
        i = i + index
        mint_array = []
        if mint != []:
            mint_array.append(mint)
            mint_array.append('--minting-script-file')
            mint_array.append(script)
            command_string, index = self.insert_command(3+i,1,command_string,mint_array)
        
        # for address in addr:
        #     command_string.insert(3+i,'--tx-out')
        #     command_string.insert(4+i,address[0])
        #     i += 2
        # if metadata_json_file != '':
        #     command_string.insert(3+i, '--metadata-json-file')
        #     command_string.insert(4+i, metadata_json_file)
        #     i += 2
        # if mint != []:
        #     command_string.insert(3+i, mint)
        #     command_string.insert(4+i, '--minting-script-file')
        #     command_string.insert(5+i, script)
        # command_line = input()
        # args = shlex.split(command_line)
        # print(args)
        print(command_string)
        subprocess.check_output(command_string)

    # def utxo_selection(self, addr_origin_tx, assets, deplete):
    #     """ Function based on the coin selection algorithm to properly handle the use of utxos in the wallet. 
    #     Rules are:
    #     1. If any of your UTXO matches the Target it will be used.
    #     2. If the "sum of all your UTXO smaller than the Target" happens to match the Target, they will be used. (This is the case if you sweep a complete wallet.)
    #     3. If the "sum of all your UTXO smaller than the Target" doesn't surpass the target, the smallest UTXO greater than your Target will be used.
    #     4. Else Bitcoin Core does 1000 rounds of randomly combining unspent transaction outputs until their sum is greater than or equal to the Target. If it happens to find an exact match, it stops early and uses that.
    #         Otherwise it finally settles for the minimum of

    #             the smallest UTXO greater than the Target
    #             the smallest combination of UTXO it discovered in Step 4.

    #     https://github.com/bitcoin/bitcoin/blob/3015e0bca6bc2cb8beb747873fdf7b80e74d679f/src/wallet.cpp#L1276
    #     https://bitcoin.stackexchange.com/questions/1077/what-is-the-coin-selection-algorithm
    #     """

    #     #Applying the coin selection algorithm
    #     minUTXO = 1000000
    #     TXHash_lovelace = []
    #     TXHash_lovelace_lower = []
    #     amount_lovelace_lower = []
    #     TXHash_lovelace_greater = []
    #     amount_lovelace_greater = []
    #     TXHash_assets = []
    #     amount_assets = []
    #     utxo_found = False
    #     transactions = addr_origin_tx['transactions'][:]

    #     for asset, target in assets.items():
    #         balance_asset = 0
    #         for utxo in transactions:
    #             for amount in utxo['amounts']:
    #                 if asset == 'lovelace':
    #                     if int(amount['amount']) <= target + minUTXO:
    #                         TXHash_lovelace_lower.append(utxo['hash'] + '#' + utxo['id'])
    #                         amount_lovelace_lower.append(int(amount['amount']))
    #                     elif int(amount['amount']) > target + minUTXO:
    #                         TXHash_lovelace_greater.append(utxo['hash'] + '#' + utxo['id'])
    #                         amount_lovelace_greater.append(int(amount['amount']))
    #                     elif int(amount['amount']) == target:
    #                         TXHash_lovelace.append([utxo['hash'] + '#' + utxo['id']])
    #                         amount_equal = int(amount['amount'])
    #                         utxo_found = True
    #                         break
    #                 elif amount['token']==asset:
    #                     balance_asset = balance_asset + int(amount['amount'])
    #                     if balance_asset < target:
    #                         TXHash_assets.append({asset:{'utxo':utxo['hash'] + '#' + utxo['id'],'amount':int(amount['amount'])}})
    #     print(TXHash_lovelace_lower,TXHash_lovelace_greater,TXHash_assets)


        # for utxo in transactions:
        #     for amount in utxo['amounts']:
        #         amounts.append(amount)
        #     amounts = sorted(amounts, key = itemgetter('token'))
        #     for key, value in groupby(amounts, key = itemgetter('token')):
        #         # print(f'The balance of "{key}" is: ')
        #         for k in value:
        #             balance = balance + int(k['amount'])
        #             # print(k)
        #         balance_dict[key]=balance
        #         print(f'Total balance of "{key}" is "{balance}"')

        # for asset in TXHash_assets:
            

        # for utxo in addr_origin_tx['transactions']:
        #     for amount in utxo['amounts']:
        #         Tx
        #         TxHash.append(TxHash_ass)
        #         utxo_array.append([utxo['hash'] + '#' + utxo['id']])


        # for asset, target in assets.items():
        #     if asset in TXHash_assets:






        # for utxo in addr_origin_tx['transactions']:
        #     for amount in utxo['amounts']:
        #         if amount['token']=='lovelace': 
        #             if deplete:
        #                 TXHash_lovelace.append([utxo['hash'] + '#' + utxo['id']])
        #                 amount_equal = int(amount['amount'])
        #                 utxo_found = True
        #                 break
        #             if int(amount['amount']) == quantity:
        #                 TXHash_lovelace.append([utxo['hash'] + '#' + utxo['id']])
        #                 amount_equal = int(amount['amount'])
        #                 utxo_found = True
        #                 break
        #             elif int(amount['amount']) < quantity + minUTXO:
        #                 TXHash_lovelace_lower.append(utxo['hash'] + '#' + utxo['id'])
        #                 amount_lovelace_lower.append(int(amount['amount']))
        #             elif int(amount['amount']) > quantity + minUTXO:
        #                 TXHash_lovelace_greater.append(utxo['hash'] + '#' + utxo['id'])
        #                 amount_lovelace_greater.append(int(amount['amount']))
        #         # elif (amount['token'] != 'lovelace') and ()

        # if not utxo_found:
        #     if sum(amount_lower) == quantity:
        #         TxHash = TxHash_lower
        #         amount_equal = sum(amount_lower)
        #     elif sum(amount_lower) < quantity:
        #         if amount_greater == []:
        #             TxHash = []
        #             amount_equal = 0
        #         amount_equal = min(amount_greater)
        #         index = [i for i, j in enumerate(amount_greater) if j == amount_equal][0]
        #         TxHash.append([TxHash_greater[index]])
        #     else:
        #         utxo_array = []
        #         amount_array = []
        #         for _ in range(999):
        #             index_random = random.randint(0,len(transactions)-1)
        #             # utxo = addr_origin_tx['transactions'][index_random]
        #             utxo = transactions.pop(index_random)
        #             utxo_array.append([utxo['hash'] + '#' + utxo['id']])
        #             for amount in utxo['amounts']:
        #                 if amount['token']==token: 
        #                     amount_array.append(int(amount['amount']))
        #             if sum(amount_array) >= quantity + minUTXO:
        #                 amount_equal = sum(amount_array)
        #                 break
        #         TxHash = utxo_array

        # return TxHash, amount_equal

    def create_minting_policy(self, wallet_id):
        path = self.KEYS_FILE_PATH + '/' + wallet_id + '/' + 'minting/'
        if not os.path.exists(path):
            os.makedirs(path)
        
        # Generate key pairs for minting associated to specific policy script
        command_string = [
            'cardano-cli', 'address', 'key-gen', '--verification-key-file', path + wallet_id + '.policy.vkey',
        '--signing-key-file', path + wallet_id + '.policy.skey'
        ]
        subprocess.run(command_string)

        #Create policy script and save file policy.script
        command_string = [
        'cardano-cli', 'address', 'key-hash', '--payment-verification-key-file', path + wallet_id + '.policy.vkey'
        ]
        output = subprocess.Popen(command_string,stdout=subprocess.PIPE)

        policy_script = {
            "keyHash": str(output.communicate()[0].decode('utf-8')).rstrip(),
            "type": "sig"
        }


        with open(path + '/' + wallet_id + '.policy.script','w') as file:
            json.dump(policy_script, file, indent=4, ensure_ascii=True)

        # Generate policyID from the policy script file
        command_string = [
        'cardano-cli', 'transaction', 'policyid', '--script-file', path + wallet_id + '.policy.script'
        ]
        output = subprocess.Popen(command_string,stdout=subprocess.PIPE)
        policyID = str(output.communicate()[0].decode('utf-8')).rstrip()
        utils.save_files(path, wallet_id + '.policyID',str(policyID))
        return policyID

    def sign_transaction(self, wallet_id, mint):
        # Sign the transaction based on tx_raw file.
        # For the time being not handling multi-witness
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'sign',
            '--tx-body-file', self.TRANSACTION_PATH_FILE + '/tx.draft',
            '--signing-key-file', self.KEYS_FILE_PATH + '/' + wallet_id + '/' + wallet_id + '.payment.skey',
            # '--testnet-magic', str(CARDANO_NETWORK_MAGIC),
            '--out-file', self.TRANSACTION_PATH_FILE + '/tx.signed']
        i = 0
        mint_array = []
        if mint != []:
            mint_array.append('--signing-key-file')
            mint_array.append(self.KEYS_FILE_PATH + '/' + wallet_id + '/minting/' + wallet_id + '.policy.skey')
            command_string, index = self.insert_command(7+i,1,command_string,mint_array)  
        i = i + index       
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(7+i,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        
        subprocess.check_output(command_string)
    
    def submit_transaction(self):
        # Submit the transaction
        command_string = [
            self.CARDANO_CLI_PATH,
            'transaction', 'submit',
            '--tx-file', self.TRANSACTION_PATH_FILE + '/tx.signed']
        if self.CARDANO_NETWORK == 'testnet':
            command_string, index = self.insert_command(5,1,command_string,['--testnet-magic',self.CARDANO_NETWORK_MAGIC])
        
        rawResult= subprocess.check_output(command_string)
        print(rawResult)

    def transactions(self, wallet_origin, wallet_destin, params):
        """Sign and submit. 
            :param address: TxHash of the origin address, address origin and destin
            Return: 
        """
        minUTXOValue = 1000000
        addr_origin = self.id_to_address(wallet_origin)
        addr_destin = self.id_to_address(wallet_destin)
        addr_origin_tx = self.get_transactions(addr_origin)
        addr_zero = []
        # deplete = params['Tx']['Max']

        balance = self.get_balance(wallet_origin)
        print(balance)

        # Check for enough funds or minUTXOValue
        # TxHash_in, amount_equal = self.utxo_selection(addr_origin_tx,params['Tx']['assets'],deplete)

        # for asset, target in params['Tx']['assets'].items():
        #     if asset in balance:
        #         target = int(target)
        #         target_calculated =  target + 200000
        #         if int(balance[asset['name']]) < target_calculated: # Fee first aproximation
        #             print("No funds available in the origin wallet")
        #             break
        #         elif target < minUTXOValue:
        #             print('OutputTooSmallUTxo')
        #             break
        #         else:
        #             # For here when multiple destination address
        #             addr_zero.append([addr_origin + '+' + str(0)])
        #             TxHash_in, amount_equal = self.utxo_selection(addr_origin_tx,asset['name'],target_calculated, deplete)

        # Check if minting tokens as part of the transaction
        mint = []
        script_path = ''
        if params['mint'] is not {}:
            tokenamount_mint = params['mint']['tokens_info'][0]['amount']
            tokenname = params['mint']['tokens_info'][0]['name']
            wallet_id = params['mint']['mint_wallet_id']

            if params['mint']['tokens_info'][0]['PolicyID'] == None:
                # Create keys and policy IDs
                policyid = utils.create_minting_policy(wallet_id)
            else:
                policyid = params['mint']['tokens_info'][0]['PolicyID']

            # if params['mint']['with_quantity']:
            #     target = params['Tx']['assets'][0]['target']
            #     target_calculated = target + 200000
            # else:
            if policyid + '.' + tokenname in balance:
                tokenbalance = balance[policyid + '.' + tokenname]

            target = minUTXOValue
            target_calculated = target + 200000
            tokenbalance = tokenbalance + tokenamount_mint

            script_path = self.KEYS_FILE_PATH + '/' + wallet_id + '/minting/' + wallet_id + '.policy.script'
            mint = '--mint=' + str(tokenamount_mint) + ' ' + str(policyid) + '.' + str(tokenname)
            addr_zero.append('--tx-out')
            addr_zero.append(addr_destin + '+' + str(0) + '+' + str(tokenbalance) + ' ' + str(policyid) + '.' + str(tokenname))

        deplete = False
        TxHash_in, amount_equal = self.utxo_selection(addr_origin_tx,'lovelace',target_calculated,deplete)

        


        # if deplete:
        #     target = balance[0]['lovelace']
        #     target_calculated = target

        # elif params['mint']['flag']:
        #     # Minting tokens
            
        #     tokenamount = params['mint']['tokens_info'][0]['amount']
        #     tokenname = params['mint']['tokens_info'][0]['name']
        #     wallet_id = params['mint']['mint_wallet_id']

        #     if params['mint']['tokens_info'][0]['PolicyID'] == None:
        #         # Create keys and policy IDs
        #         policyid = utils.create_minting_policy(wallet_id)
        #     else:
        #         policyid = params['mint']['tokens_info'][0]['PolicyID']

        #     if params['mint']['with_quantity']:
        #         target = params['Tx']['assets'][0]['target']
        #         target_calculated = target + 200000
        #     else:
        #         target = minUTXOValue
        #         target_calculated = target + 200000

        #     script_path = keys_file_path + '/' + wallet_id + '/minting/' + wallet_id + '.policy.script'
        #     mint = '--mint=' + str(tokenamount) + ' ' + str(policyid) + '.' + str(tokenname)
        #     addr_zero.append([addr_destin + '+' + str(0) + '+' + str(tokenamount) + ' ' + str(policyid) + '.' + str(tokenname)])

        # else:
        #     target = params['Tx']['assets'][0]['target']
        #     target_calculated = target + 200000
        #     addr_zero.append([addr_origin + '+' + str(0)])

        # if balance[0]['lovelace'] < target_calculated:
        #     print("No funds available in the origin wallet")
        # elif target < minUTXOValue:
        #     print('OutputTooSmallUTxo')
        # else:
        
        
            

        metadata = params['metadata']
        metadata_json_file = utils.save_metadata(self.TRANSACTION_PATH_FILE, metadata)
                
        ###########################
        # Section to calculate min fees
        ###########################
        #Create the tx_raw file to calculate the min fee
        self.build_raw_tx(TxHash_in, addr_zero, 0, metadata_json_file, mint, script_path)
        #Calculate min fees based on previously tx_raw file
        fee = self.tx_min_fee(str(len(TxHash_in)),str(len(addr_zero)))
        fee = int(fee.decode('utf-8'))
        print(fee)
        

        ###########################
        # Section to build the actual transaction including fees
        ###########################
        addr = []
        target = amount_equal - fee
        addr.append('--tx-out')
        addr.append(addr_destin + '+' + str(int(target)) + '+' + str(tokenbalance) + ' ' + str(policyid) + '.' + str(tokenname))

        # #Create the tx_raw file with the fees included
            
        self.build_raw_tx(TxHash_in, addr, fee, metadata_json_file, mint, script_path)

        print("################################")
        print("Sending '{}' from {} to {}. Fees are: {}".format(target, wallet_origin, wallet_destin,fee))
        print("################################")

        self.sign_transaction(wallet_id,mint)
        self.submit_transaction()