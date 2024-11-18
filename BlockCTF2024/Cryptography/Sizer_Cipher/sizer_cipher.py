'''
1 character: maps a-z, A-Z, 0-9 -> 000-03d
2 characters: 040 times first charcter + second character
Every 2 characters is represented by 3 hexadecimal digits
3 digits = char[0] * 040 + char[1]
Essentially just need to find quotient and remainder when dividing by 040 (hex).
'''
def dec2hex(x):
    return hex(x)[2:].zfill(2)

def hex2dec(s):
    return int(s, 16)

# a-z, A-Z, 0-9
chars = [chr(ord("a")+i) for i in range(26)] + [chr(ord("A")+i) for i in range(26)] + [chr(ord("0") + i) for i in range(10)] + ["{", "}"]

lookup = {}
for i, char in enumerate(chars):
    lookup[dec2hex(i)] = char

DIVISOR = hex2dec("040") # which is 64
def reverse_3_digits(digits):
    global DIVISOR, lookup
    # convert digits to decimal
    decimal = hex2dec(digits)
    
    quotient = decimal // DIVISOR
    remainder = decimal % DIVISOR
    
    return lookup[dec2hex(quotient)] + lookup[dec2hex(remainder)]

output = "0052c01be88c7f52cbdc3c084c7b1313828034370034dd13778342dff"
ans = ""

for i in range(0, len(output), 3):
    ans += reverse_3_digits(output[i:i+3])
    
print(ans)