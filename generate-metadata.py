import json

def generate_numbers(amount):
    nums=[]
    for i in range(1,amount+1):
        if i < 10:
            num = '00' + str(i)
        elif i == 100:
            num = i
        else:
            num = '0' + str(i)
        
        nums.append(num)
    return nums

def generate_metadata(amount):

    numbers = generate_numbers(amount)
    name="Yuca(Mahihot-esculenta)Var1."
    asset_name = {}
    metadata = {}
    for i in range(amount):
        asset_name = {
            name + numbers[i]: {
                "name": name +  numbers[i],
                "nsfw": "False",
                "files": [
                {
                    "src": "ipfs://QmUPJZGxEUtnaaPybS9G7AJfX2i29pnSgT7vohUyRGrGdE",
                    "mediaType": "image/jpg"
                }
                ],
                "image": "ipfs://QmaNrhkn3aAYpd5vqfwzpsSr6svYkNgQLgQ7AZBCvva4vP",
                "description": {
                "en": [
                    "Pictorial phytotropism of nutritious plants of native character.",
                    "Consequence of differential growth in thinking and conception of reality.",
                    "#" + numbers[i] + " of a serie of 100 pieces"
                ],
                "es": [
                    "Fitotropismo pictórico de plantas nutritivas de caracter nativo.",
                    "Consecuencia de un crecimiento diferencial en el pensamiento y la concepción de la realidad.",
                    "#" + numbers[i] + " de una serie de 100 piezas"
                ]
                },
                "collection": "Tubérculos",
                "artist": "Ser Jiménez",
                "url": "www.arsser.com",
                "instagram": "@serjimenezars",
                "facebook": "ser.jimenez.ars",
                "year": "2019",
                "golden_ticket": "c106c5d98885bae6d0c658c3d1f80c624655d5f707b8b6c6b479742dc126f8ff"
            }
        }
        metadata.update(asset_name)

    metadata = {
        '721': {
            'PolicyID': metadata
        }
    }
        
    #return json.dumps(metadata,indent=4,ensure_ascii=False)
    return metadata

amount= 10
metadata = generate_metadata(amount)
with open("./metadata.json",'w') as file:
    json.dump(metadata, file,indent=4,ensure_ascii=False)