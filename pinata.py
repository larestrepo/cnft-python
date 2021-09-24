import os
import typing as tp
import json

import requests

API_ENDPOINT = "https://api.pinata.cloud/"

class PinataPy:

    """ This library is mainly used to upload files to pinata. There are more functionalities
        available in the Pinata API but the most important is the function called pin_file_to_ipfs.
        For future work: pin_hash_to_ipfs, pin_json_to_ipfs and pin_list among others. It is also
        possible to provide metadata, but not yet implemented. 
    """
    def __init__(self, pinata_api_key, pinata_secret_api_key):
            self._auth_headers = {
                "pinata_api_key": pinata_api_key,
                "pinata_secret_api_key": pinata_secret_api_key,
            }

    @staticmethod
    def error(response):
        """Construct dict from response if an error has occurred"""
        return {"status": response.status_code, "reason": response.reason, "text": response.text}

    def pin_file_to_ipfs(self, path_to_file):
        """
        Pin any file, or directory, to Pinata's IPFS nodes

        More: https://docs.pinata.cloud/api-pinning/pin-file
        """
        url = API_ENDPOINT + "pinning/pinFileToIPFS"
        headers = self._auth_headers

        def get_all_files(directory):
            """get a list of absolute paths to every file located in the directory"""
            paths = []
            for root, dirs, files in os.walk(os.path.abspath(directory)):
                for file in files:
                    paths.append(os.path.join(root, file))
            return paths

        options = {
            'pinataOptions':{
                'cidVersion':0,
                'wrapWithDirectory': 'false',
                'customPinPolicy': {
                    'regions': [
                        {
                            'id': 'FRA1',
                            'desiredReplicationCount': 1
                        },
                        {
                            'id': 'NYC1',
                            'desiredReplicationCount': 2
                        }
                    ]
                }
            }
        }     
        all_files = get_all_files(path_to_file)       
        data = [('file', (open(file, "rb"))) for file in all_files]
        response = requests.post(url=url, files = data, headers = headers, json = options )
        return response.json() if response.ok else self.error(response)