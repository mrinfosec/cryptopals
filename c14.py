#!/usr/bin/python

# Byte-at-a-time ECB decryption (Harder) Take your oracle function from #12. Now
# generate a random count of random bytes and prepend this string to every
# plaintext. You are now doing:
#
# AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)
# Same goal: decrypt the target-bytes.
#
# Pseudocode
# 1.  find out where your bytes are by submitting '' and submitting ' ' to the oracle.  Look for the first block that changes - this is block 0.
# 2.  add more spaces to your string until block 0 stops changing.  now you know the start of block 1.
# 3.  add 15 spaces and snip out block 1 = this is the block you need to match
# 4.  add 15 spaces and try all 256 characters.  When you have a match, you know char1
# 5.  repeat 3 and 4 until you know all block 1.  Then, prepend block 1 to your guesses and start on block 2.
# 6.  Continue until you are out of blocks

from base64 import b64decode
from c8 import isECB
from c9 import pkcs7pad, pkcs7unpad
from c10 import blockify
from c11 import aesecb_encrypt, genaeskey
from random import randrange

def ecb_oracle(s):
    return aesecb_encrypt(pkcs7pad(random + s + target, 16), key)

def findmsgsize():
    return len(ecb_oracle(''))

def findstart(msglen):
    empty=ecb_oracle('')
    last=ecb_oracle('A')
    pad = 0
    for i in range(0, msglen, 16):
        if empty[i:i+16] != last[i:i+16]:
            z = i
            break
    for i in range(16):
        if ecb_oracle('A' * i)[z:z+16] == ecb_oracle('A' * (i + 1))[z:z+16]:
            pad = i
            break
    return (z, pad)

# TODO:  sometimes this function returns nothing - probably a padding index problem
def crack(z, prepad, msglen):
    blocksize = 16
    allcracked = ''
    print 'msglen is: ' + str(msglen)
    for block in range(z + blocksize, msglen + 16, blocksize):
        print 'cracking block starting at ' + str(block)
        crackedblock = ''
        for i in range(blocksize):
            start = block
            finish = block + blocksize
            pad = 'A' * (prepad + blocksize - 1 - len(crackedblock))
            testblock = ecb_oracle(pad)[start:finish]
            for i in range(256):
                trial = pad + allcracked + crackedblock + chr(i)
                if ecb_oracle(trial)[start:finish] == testblock:
                    crackedblock += chr(i)
                    break
        print 'cracked block is: \n' + crackedblock
        allcracked += crackedblock
    return allcracked

if __name__ == '__main__':

    target = '''He rode over Connecticut
In a glass coach.
Once, a fear pierced him,
In that he mistook
The shadow of his equipage
For blackbirds.   '''

    key = genaeskey()
    random = chr(randrange(256))*randrange(64)
    msglen=findmsgsize()
    print pkcs7unpad(crack(findstart(msglen)[0], findstart(msglen)[1], msglen))
