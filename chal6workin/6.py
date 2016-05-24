#!/usr/bin/python

MINKEY = 26
MAXKEY = 30
cryptfile = '6.txt'
teststring1 = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226\
324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302\
e27282f'

from binascii import a2b_base64, unhexlify
from challenge3 import brute

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
    #try all the allowable keysizes and return the one with minimum editdist
    scoretable={}
    for i in range(MINKEY, MAXKEY):
        #grab the first 4 blocks of each keysize and return the average editdist
        scoretable[i]=editdist(s[0:i],s[i:2*i])/float(i)
        scoretable[i]+=editdist(s[i:2*i],s[2*i:3*i])/float(i)
        scoretable[i]+=editdist(s[2*i:3*i],s[3*i:4*i])/float(i)
        scoretable[i]+=editdist(s[3*i:4*i],s[4*i:5*i])/float(i)
        scoretable[i]=scoretable[i]/4
    print scoretable
    print sorted(scoretable, key=scoretable.get)
    return min(scoretable.iterkeys(), key=(lambda key: scoretable[key]))

def blockify(s):
    #take a big string and break it up into blocks
    ret=[]
    keysize=findkeysize(s)
    for i in range(len(s)/keysize):
        block=s[i*keysize:(i+1)*keysize]
        ret.append(block)
    #if there are any partial blocks, grab them and pad them with slashes
    if len(s) % keysize != 0:
        block=s[len(s)-(len(s) % keysize):]+'/'*(keysize - (len(s) % keysize))
        ret.append(block)
    return ret

def transpose(s):
    #transpose the blocks byte-by-byte
    ret = {}
    blocklist=blockify(s)
    for block in blocklist:
        for i in range(len(blocklist[0])):
            if ret.has_key(i): ret[i] += block[i]
            else: ret[i] = block[i]
    return ret

def bruteblocks(blocklist):
    #simple wrapper function to brute a list of blocks and transpose back to string
    bruted=[]
    cleartext=''
    #first, brute force each block in the list
    for i in range(len(blocklist)):
        bruted.append(brute(blocklist[i]))
    #then, transpose them to reconstruct the text
    for i in range(len(bruted[0])):
        for j in range(len(bruted)):
            cleartext += bruted[j][i]
    return cleartext

def initcrypttext(inputfile):
    #read the input file, un-b64 it, and make a big string out of it
    cryptlist=[]
    f = open(inputfile, 'r')
    for line in f:
        cryptlist.append(a2b_base64(line.strip('\n')))
    return ''.join(cryptlist)

f = initcrypttext(cryptfile)
byteblocks = transpose(f)
# input = unhexlify(teststring1)
# byteblocks = transpose(input)
cleartext = bruteblocks(byteblocks)

print cleartext
