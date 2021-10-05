import library as lb
import json

address = "addr_test1qpsa3y56lrztf9kup73z7taz82hmyzl7y22jgjxd5ytdv7y3r8hcsm9t6est7r3ftqmgx65g69u8hyjvqc99l9cnkp4s4vr73g"

token_transactions = lb.get_transactions(address)
main ={
            'client-id': 'any number'
        }
main.update(token_transactions)
print(main)
print (main)