#!/usr/bin/python
# Implement CBC mode
# CBC mode is a block cipher mode that allows us to encrypt irregularly-sized
# messages, despite the fact that a block cipher natively only transforms
# individual blocks.
#
# In CBC mode, each ciphertext block is added to the next plaintext block before
# the next call to the cipher core.
#
# The first plaintext block, which has no associated previous ciphertext block, is
# added to a "fake 0th ciphertext block" called the initialization vector, or IV.
#
# Implement CBC mode by hand by taking the ECB function you wrote earlier, making
# it encrypt instead of decrypt (verify this by decrypting whatever you encrypt to
# test), and using your XOR function from the previous exercise to combine them.
#
# The file here is intelligible (somewhat) when CBC decrypted against
# "YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)
#
# Don't cheat.
# Do not use OpenSSL's CBC code to do CBC mode, even to verify your results.
# What's the point of even doing this stuff if you aren't going to learn from it?

# pseudocode
#
# Encrypt:
# Assign IV vector
# XOR together
# ECB first block
# XOR together
# ECB second block
# repeat until done

# Decrypt:
# Read last block
# ECB decrypt it
# Read previous block
# XOR against plaintext
# Continue until done

from Crypto.Cipher import AES
from base64 import b64decode

aeskey = 'YELLOW SUBMARINE'
ciphertext = b64decode(open('10.txt', 'r').read())
iv = chr(0)*16


if len(ciphertext) % 16 != 0:
    raise Exception('String is not a list of 16-byte blocks')

def xor(s1, s2):
    result = ''
    if len(s1) != len(s2):
        raise Exception('Strings to XOR are different lengths')
    for i in range(len(s1)):
        result += chr(ord(s1[i]) ^ ord(s2[i]))
    return result

def blockify(s, blocklen):
    return [s[i:i+blocklen] for i in range(0, len(s), blocklen)]

def aescbc_decrypt(iv, s, key):
    aesobj = AES.new(key, AES.MODE_ECB)
    blocks = blockify(s, 16)
    blocks.insert(0,iv)
    ret = []
    for i in range(1, len(blocks), 1):
        a = aesobj.decrypt(blocks[len(blocks)-i])
        b = blocks[len(blocks)-i-1]
        ret.insert(0,xor(a, b))
    return ''.join(ret)

if __name__ == '__main__':
    print aescbc_decrypt(iv, ciphertext, aeskey)
