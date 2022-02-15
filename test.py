from base64 import b16encode
  
s = 'PruebaTolima'
s = s.encode('utf-8')
# Using base64.b16encode() method
gfg = b16encode(s)
gfg = gfg.decode('utf-8')

print(gfg)