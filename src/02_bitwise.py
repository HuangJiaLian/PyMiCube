from base64 import decode

def print_hex(bytes):
    l = [hex(int(i)) for i in bytes]
    return(" ".join(l))

# t = 0b1001
# print(bin(t>>3))

# a = 0b11111111
# b = 0b00000001
# c = a + b 
# print(a, b)
# print(c, bin(c))
# print(bin(a&b), bin(a|b))


# d = 0x11
# print(d)

value = b'\xb9\xd8\xd3\xd3=C"\x9f9*c A\xe6\xf4\x81\xbc3\xa7\xf2'
# e = r_data
# print(e)
# print(e[0], e[-2])
# print(type(e))
# print(len(e))
# print(list(e))





key = [176,  81, 104, 224,  86, 137,
       237, 119,  38,  26, 193, 161,
       210, 126, 150,  81,  93,  13, 
       236, 249,  89, 235,  88,  24, 
       113,  81, 214, 131, 130, 199, 
         2, 169,  39, 165, 171, 41]


def toHexVal(value, key):
    raw = list(value)
    k1 = raw[-1] >> 4 & 0xf
    k2 = raw[-1] & 0xf
    for i in range(18):
        raw[i] += key[i + k1] + key[i + k2]
    raw = raw[:18]

    valhex = []
    for i in range(len(raw)):
        valhex.append(raw[i] >> 4 & 0xf)
        valhex.append(raw[i]  & 0xf)
    return valhex

valhex = toHexVal(value, key)
print(len(valhex),valhex)







# print(r_data)
# print(d_data)
# print(print_hex(d_data))


# faces = ['Front', 'Bottom', 'Right', 'Top', 'Left', 'Back']
# direction = ['Clockwise', 'Anti-clockwise']

# print(d_data[32], d_data[33])




# key = [176,  81, 104, 224,  86, 137,
#        237, 119,  38,  26, 193, 161,
#        210, 126, 150,  81,  93,  13, 
#        236, 249,  89, 235,  88,  24, 
#        113,  81, 214, 131, 130, 199, 
#          2, 169,  39, 165, 171, 41]

# print('Key:')
# for k in key:
#     print(hex(k))