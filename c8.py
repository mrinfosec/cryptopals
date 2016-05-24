#!/usr/bin/python
# Detect AES in ECB mode
# In this file are a bunch of hex-encoded ciphertexts.
#
# One of them has been encrypted with ECB.
#
# Detect it.
#
# Remember that the problem with ECB is that it is stateless and deterministic;
# the same 16 byte plaintext block will always produce the same 16 byte
# ciphertext.

# pseudocode:
# read the file
# make a list of 16-byte blocks from each line (10 blocks per 320 character line)
# check each block and see if it matches another block from the same line
from binascii import unhexlify

def isECB(s):
    #takes raw string of AES blocks as input and returns true if likely ECB
    if len(s.strip()) % 16 != 0:
        raise Exception('String is not a list of 16-byte blocks')
    blocks = [s[i:i+16] for i in range(0, len(s), 16)]
    for block in blocks:
        if blocks.count(block) != 1:
            return True
    return False

if __name__ == '__main__':
    f = open('8.txt', 'r').readlines()
    for hexline in f:
        line = unhexlify(hexline)
        if isECB(line):
            print "Line number: " + str(f.index(line)+1)
            print line
