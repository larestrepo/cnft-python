
from collections import defaultdict

test_dict = 
    {
      "hash": "32fbd9488e244ff71a88bf313b15d5b3b6a97257742fa89808e4e2297bf3cd1e",
      "id": "0",
      "amounts": [
        {
          "token": "lovelace",
          "amount": "13322526"
        },
        {
          "token": "0b57a5ace42fb9a8d9e8edd6cd1550f0cd7385989e7128f5328c7dd1.AN0929",
          "amount": "1"
        },
        {
          "token": "105d2c05ad4b3be5b3cbe09bb4c2a10d13198989aa1c785eaadd8a89.AN1047",
          "amount": "1"
        },
        {
          "token": "1513b0aa6c324a5d027ff5c7039b102b9293d7e952a383a524819392.AN1004",
          "amount": "1"
        },
        {
          "token": "1f6122a63bd449b18b2698bed5eee0e705376aac1f00ef5f46683dc5.ACME",
          "amount": "1"
        },
        {
          "token": "233f14849ee70cb92ca5440fb2fa963595db6e9f876f286f1f20bed4.AN1033",
          "amount": "1"
        },
        {
          "token": "289eef47cb5fad3eab0f377db7965d7dc6059e4143e220f79a7771ac.AN0908",
          "amount": "1"
        },
        {
          "token": "29e94d7c4cf98f8047585dbcc2d96d3bd630279ecb9534b9752a84e0.AN1036",
          "amount": "1"
        },
        {
          "token": "64d11f99e09ab304033a996944785c7d5f067e2943ed088c39e9427b.AN1004",
          "amount": "1"
        },
        {
          "token": "812d57fc81fb3ffb0211ac1acbfafd5ab975884d9688883eb87505af.AN0908",
          "amount": "1"
        },
        {
          "token": "82d764d7835332b4d342c8a5b1a8d387c0feb3415f3b20b088e3a45d.ACME",
          "amount": "1"
        },
        {
          "token": "904ed71464de22f07f9fdaf8828d2eba15430b3ee1ea5df61a7e376d.ACME",
          "amount": "1"
        },
        {
          "token": "c817d82cee3ca8b82ae05f678119c1aa3f73b58ba39b15f56a5b970b.ACME",
          "amount": "1"
        },
        {
          "token": "d17e2c1c95787347a900394c1973a2197b87516b7d9343bcab8a2e82.AN0929",
          "amount": "1"
        },
        {
          "token": "d76e760cbaa5a76e60f5acb74cc317dd53dc25e1429a3230096b5688.AN1049",
          "amount": "1"
        },
        {
          "token": "e4590e33bbc91984ba861e209d04f65237309c9373f758344cf9db58.AN0956",
          "amount": "1"
        },
        {
          "token": "fc2ec4b8d62bfe680fbcbb4f932d80a7d029ec84cce93a7de54926a4.AN1103",
          "amount": "1"
        }
        
    }

res = defaultdict(list)
print(str(res))
for key, val in sorted(test_dict.items()):
    res[val].append(key)
     
# printing result
print("Grouped dictionary is : " + str(dict(res)))