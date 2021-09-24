import os
from decouple import config
from pinata import PinataPy

#Inputs
PINATA_API_KEY= config('PINATA_API_KEY')
PINATA_SECRET_API_KEY = config('PINATA_SECRET_API_KEY')
API_KEY = config('API_KEY')
path = ('/images/ARSSER/Serie2') # place of the images to be uploaded

dirname = os.path.dirname(__file__)
path = dirname + path
c = PinataPy(PINATA_API_KEY,PINATA_SECRET_API_KEY)
cid = c.pin_file_to_ipfs(path)
print(cid)

