import subprocess
from decouple import config

# Import params
CARDANO_NETWORK_MAGIC = config('CARDANO_NETWORK_MAGIC')

def query_tip_exec():
    # We tell python to execute cardano-cli shell command to query the blockhain and read the output data
    try:
        rawTipTable = subprocess.check_output([
            CARDANO_CLI_PATH,
            'query', 'tip',
            '--testnet-magic', str(CARDANO_NETWORK_MAGIC)])
        return rawTipTable
    except:
        print('error')

def result_treatment(obj):

    if obj[0]['cmd_id'] == 'query_tip':
        query_tip_exec()

    while len(obj)>0:
        print(obj.pop(0))
    # while not q.empty():    
    #     message = q.get()
    #     print("queue: ",message)


# mnemonic = subprocess.check_output([
#     'cardano-wallet', 'recovery-phrase', 'generate'
# ])

# print(mnemonic)

# s = subprocess.check_output(["echo", "Hello World!"])
# print("s = " + str(s))