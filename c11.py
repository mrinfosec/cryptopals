#!/usr/bin/python
# An ECB/CBC detection oracle Now that you have ECB and CBC
# #working:
#
# Write a function to generate a random AES key; that's just 16 random bytes.
#
# Write a function that encrypts data under an unknown key --- that is, a function
# that generates a random key and encrypts under it.
#
# The function should look like:
#
# encryption_oracle(your-input) => [MEANINGLESS JIBBER JABBER] Under the hood,
# have the function append 5-10 bytes (count chosen randomly) before the plaintext
# and 5-10 bytes after the plaintext.
#
# Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC
# the other half (just use random IVs each time for CBC). Use rand(2) to decide
# which to use.
#
# Detect the block cipher mode the function is using each time. You should end up
# with a piece of code that, pointed at a block box that might be encrypting ECB
# or CBC, tells you which one is happening.

from random import randrange
from c8 import isECB
from c9 import pkcs7pad
from c10 import blockify, xor, aescbc_decrypt
from Crypto.Cipher import AES

def genaeskey():
    keybytes = [chr(randrange(256)) for i in range(16)]
    return ''.join(keybytes)

def aescbc_encrypt(s, key):
    aesobj = AES.new(key, AES.MODE_ECB)
    blocks = blockify(s, 16)
    iv = genaeskey()
    #make the first block of the ciphertext the random IV
    ret=[iv]
    for i in range(len(blocks)):
        ret.append(aesobj.encrypt(xor(ret[i],blocks[i])))
    #throw away the first block of ret which is the IV
    return iv, ''.join(ret[1:])

def aesecb_encrypt(s, key):
    aesobj = AES.new(key, AES.MODE_ECB)
    return aesobj.encrypt(s)

def aesecb_decrypt(s, key):
    aesobj = AES.new(key, AES.MODE_ECB)
    return aesobj.decrypt(s)

def gensomebytes():
    ret=''
    for i in range(randrange(5,11)):
        ret += chr(randrange(256))
    return ret

def encryption_oracle(s):
    key = genaeskey()
    p = pkcs7pad(s, 16)
    tsa = randrange(2)
    if tsa == 1:
        print 'Did ECB'
        return aesecb_encrypt(p, key)
    else:
        print 'Did CBC'
        return aescbc_encrypt(p, key)[0]

if __name__ == '__main__':
    cleartext = open('ptfmwb.txt', 'r').read()
    instr = gensomebytes() + cleartext + gensomebytes()
    outstr = encryption_oracle(instr)
    if isECB(outstr):
        print "I think this was encrypted with ECB mode"
    else:
        print "This may have been encrypted with CBC mode"


#f = open('ptfmwb.txt', 'r').read()[:-1]
