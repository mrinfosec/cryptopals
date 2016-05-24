#!/usr/bin/python

MINKEY = 2
MAXKEY = 40
cryptfile = '6.txt'
teststring1 = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226\
324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302\
e27282f'

from binascii import a2b_base64, unhexlify
from c3 import breakSingleByteXOR, strxor_c
import itertools

def tobinary(s):
    #utility function to convert a string (usually a byte) to a bitstring
    ret = []
    for i in range(len(s)):
        ret.append("{0:08b}".format(ord(s[i])))
    return ''.join(ret)

def editdist(foo, bar):
    #find the Hamming distance between two strings
    ret = 0
    binfoo = tobinary(foo)
    binbar = tobinary(bar)
    for i in range(len(binfoo)):
        if binfoo[i] != binbar [i]: ret += 1
    return ret

def findkeysize(s):
    bestscore = 10000
    retval = ''
    for k in range(MINKEY, MAXKEY):
        blocks = [s[i:i+k] for i in range(0, len(s), k)][0:4]
        pairs = list(itertools.combinations(blocks, 2))
        scores = [editdist(p[0], p[1])/float(k) for p in pairs][0:6]
        if sum(scores)/len(scores) < bestscore:
            bestscore = sum(scores)/len(scores)
            retval = k
    return retval

def breakRepeatingKeyXor(crypttext, keysize):
    blocks = [crypttext[i:i+keysize] for i in range(0, len(crypttext), keysize)]
    transposedBlocks = list(itertools.izip_longest(*blocks, fillvalue='0'))
    joined = []
    for i in range(len(transposedBlocks)):
        joined.append(''.join(transposedBlocks[i]))
    key = [breakSingleByteXOR(x) for x in joined]
    return ''.join(key)

def initcrypttext(inputfile):
    #read the input file, un-b64 it, and make a big string out of it
    cryptlist=[]
    f = open(inputfile, 'r')
    for line in f:
        cryptlist.append(a2b_base64(line.strip('\n')))
    return ''.join(cryptlist)

def XORencrypt(string, key):
    ret = ''
    for i in range(len(string)):
        ret += chr(ord(string[i])^ord(key[i % len(key)]))
    return ret

if __name__ == '__main__':
    f = initcrypttext(cryptfile)
    key = breakRepeatingKeyXor(f, findkeysize(f))
    print "Decryption key: " + key + "\n"
    print XORencrypt(f, key)
