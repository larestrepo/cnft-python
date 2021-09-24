import os
import typing as tp
import json

import requests

API_ENDPOINT = "https://api.pinata.cloud/"

class PinataPy:
    def __init__(self, pinata_api_key, pinata_secret_api_key):
            self._auth_headers: Headers = {
                "pinata_api_key": pinata_api_key,
                "pinata_secret_api_key": pinata_secret_api_key,
            }

    #@staticmethod
    def pin_file_to_ipfs(self, path_to_file):
        """
        Pin any file, or directory, to Pinata's IPFS nodes

        More: https://docs.pinata.cloud/api-pinning/pin-file
        """
        url = API_ENDPOINT + "pinning/pinFileToIPFS"
        headers: Headers = self._auth_headers

        def get_all_files(directory):
            """get a list of absolute paths to every file located in the directory"""
            paths = []
            for root, dirs, files_ in os.walk(os.path.abspath(directory)):
                for file in files_:
                    paths.append(os.path.join(root, file))
            return paths

        #files: tp.Dict[str, tp.Any]
        # pinataOptions= {'pinataOptions':{
            
        #                         'customPinPolicy': {
        #                             'regions': [
        #                                 {
        #                                     'id': 'FRA1',
        #                                     'desiredReplicationCount': 1
        #                                 },
        #                                 {
        #                                     'id': 'NYC1',
        #                                     'desiredReplicationCount': 2
        #                                 }
        #                             ]
        #                         }
        #                     }
        # }
        #options = {}
        options = {'pinataOptions':{'cidVersion':0}}
        
                
        print(json.dumps(options))        
        all_files = get_all_files(path_to_file)       
        data = [('file', (file, open(file, "rb"))) for file in all_files]
        #data = [('file',(file,open(all_files[0],'rb')))]
        #data = [('file',(all_files[0],open(all_files[0],'rb')))]
        #headers['pinataOptions'] = options['pinataOptions']

        #data.append(json.dumps(options))
        print(data)
        # if options is not None:
        #     if "pinataMetadata" in options:
        #         headers["pinataMetadata"] = options["pinataMetadata"]
        #     if "pinataOptions" in options:
        #         headers["pinataOptions"] = options["pinataOptions"]
        response = requests.post(url=url, files = data, headers = headers )
        #response = requests.post(self.url, files=files, headers=headers)
        return response.json() if response.ok else self._error(response)  # type: ignore








class NftStorage:
    def __init__(self, api_key):
        self.api_key = api_key
        # self.pinata_api_key = pinata_api_key
        # self.pinata_secret_api_key = pinata_secret_api_key
        self.url = 'https://api.pinata.cloud/pinning/pinFileToIPFS'
        # self.headers = {
        #     'pinata_api_key': pinata_api_key,
        #     'pinata_secret_api_key': pinata_secret_api_key

        # }
        #self.url = 'https://api.nft.storage/upload'
        self.headers = {'Authorization': 'Bearer ' + self.api_key}
        
    
    def upload(self, file_list, file_type):
        files = []
        for i in file_list:
            data = open(i, 'rb').read()
            #files.append(('file', (i.split('/')[2], open(i, 'rb').read(), file_type)))
            response = requests.post(self.url, headers = self.headers, data = data)
            if response.json()['ok'] == True:
                return response.json()['value']['cid']
        # try:
        #     response = requests.post(self.url, headers = self.headers, files = files)
        #     if response.json()['ok'] == True:
        #         return response.json()['value']['cid']
        # except:
        #     print("Something went wrong with the upload")
            
    # def upload(self, file):
    #     data = open(file, 'rb').read()
    #     try:
    #         response = requests.post(self.url, headers = self.headers, data = data)
    #         if response.json()['ok'] == True:
    #             return response.json()['value']['cid']
    #     except:
    #         print("Something went wrong with the upload")