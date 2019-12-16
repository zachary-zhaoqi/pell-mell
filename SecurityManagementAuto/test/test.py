import json

a=0x16
print(a)

b=json.dumps(a)
print(b)

def str_to_hex(s):
    return ' '.join([hex(ord(c)).replace('0x', '') for c in s])

c=hex(22)
#d=hex(b)#
# print(d)