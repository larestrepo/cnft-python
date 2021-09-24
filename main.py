import os
from decouple import config
from pinata import PinataPy

#Inputs
PINATA_API_KEY= config('PINATA_API_KEY')
PINATA_SECRET_API_KEY = config('PINATA_SECRET_API_KEY')
API_KEY = config('API_KEY')
#path = ('./images/ARSSER') # place of the images to be uploaded

# def file_reading(path):
#     """ Generates dict with the list of images to be uploaded into IPFS """

#     dirs = sorted([f for f in os.listdir(path) if not f.startswith('.')])
#     img = {}
#     for i in dirs:
#         sub_dirs = os.path.join(path, i)
#         files = sorted([sub_dir for sub_dir in os.listdir(sub_dirs) if not sub_dir.startswith('.')])
#         img[i] = [s for s in files]
#     return (img)

#all_images = file_reading(path)
#print(all_images)

# image_list = []
# for k, v in all_images.items():
#     abs_path = path + '/' + k
#     for i in v:
#         image_path = abs_path + '/' + i
#         image_list.append(image_path)
# print(image_list)

dirname = os.path.dirname(__file__)
path = dirname + '/images/ARSSER/Serie2'
c = PinataPy(PINATA_API_KEY,PINATA_SECRET_API_KEY)
cid = c.pin_file_to_ipfs(path)
print(cid)

