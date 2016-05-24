#!/usr/bin/python
# Implement PKCS#7 padding
# A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of
# plaintext into ciphertext. But we almost never want to transform a single block;
# we encrypt irregularly-sized messages.
#
# One way we account for irregularly-sized messages is by padding, creating a
# plaintext that is an even multiple of the blocksize. The most popular padding
# scheme is called PKCS#7.
#
# So: pad any block to a specific block length, by appending the number of
# bytes of padding to the end of the block. For instance,
#
# "YELLOW SUBMARINE"
# ... padded to 20 bytes would be:
#
# "YELLOW SUBMARINE\x04\x04\x04\x04"

def pkcs7pad(string):
    blocksize = 16
    padlen = blocksize - (len(string) % blocksize)
    return string + (chr(padlen) * padlen)

def pkcs7unpad(s):
    if len(s) % 16 != 0:
        raise ValueError('Message length is not a multiple of 16 bytes.')
    p = ord(s[-1])
    if s[-p:] != p * chr(p):
        raise ValueError('PKCS7 Padding is incorrect.')
    return s[:-p]

if __name__ == '__main__':
    teststring = 'YELLOW SUBMARINEblah'
    padded = pkcs7pad(teststring)
    # print repr(pkcs7pad(teststring))
    # print repr(pkcs7unpad(pkcs7pad(teststring)))
    print repr(pkcs7unpad(padded))
