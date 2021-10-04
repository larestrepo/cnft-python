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


def result_treatment(obj,client_id):

    """Main function that receives the object from the pubsub and defines which execution function to call"""

    if obj[0]['cmd_id'] == 'query_tip':
        print('Executing {}'.format(obj.pop(0)))
        main ={
            'client-id': client_id
        }
        result = query_tip_exec()
        result = result.decode('utf-8')
        result = json.loads(result)
        main.update(result)

    return main


# mnemonic = subprocess.check_output([
#     'cardano-wallet', 'recovery-phrase', 'generate'
# ])

# print(mnemonic)

# s = subprocess.check_output(["echo", "Hello World!"])
# print("s = " + str(s))