import subprocess
from decouple import config
import json

# Import params
CARDANO_NETWORK_MAGIC = config('CARDANO_NETWORK_MAGIC')
CARDANO_CLI_PATH = config('CARDANO_CLI_PATH')

def query_tip_exec():
    # We tell python to execute cardano-cli shell command to query the blockhain and read the output data
    try:
        command_string = [
            CARDANO_CLI_PATH,
            'query', 'tip',
            '--testnet-magic', str(CARDANO_NETWORK_MAGIC)]
        rawTipResult = subprocess.check_output(command_string)
        return rawTipResult
    except:
        print('error in command')


def result_treatment(obj):

    """Main function that receives the object from the pubsub and defines which execution function to call"""

    if obj[0]['cmd_id'] == 'query_tip':
        print('Executing {}'.format(obj.pop(0)))
        result = query_tip_exec()
        result = result.decode('utf-8')
        result = json.loads(result)
        print('Command result {}'.format(result))

    return result

    # while len(obj)>0:
    #     print(obj.pop(0))
    # while not q.empty():    
    #     message = q.get()
    #     print("queue: ",message)


# mnemonic = subprocess.check_output([
#     'cardano-wallet', 'recovery-phrase', 'generate'
# ])

# print(mnemonic)

# s = subprocess.check_output(["echo", "Hello World!"])
# print("s = " + str(s))