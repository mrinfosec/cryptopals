#!/usr/bin/python
from binascii import hexlify, unhexlify
import string, operator
#define starting string

scoretable = {
    'a': 8.167,
    'b': 1.492,
    'c': 2.782,
    'd': 4.253,
    'e': 12.702,
    'f': 2.228,
    'g': 2.015,
    'h': 6.094,
    'i': 6.966,
    'j': 0.153,
    'k': 0.772,
    'l': 4.025,
    'm': 2.406,
    'n': 6.749,
    'o': 7.507,
    'p': 1.929,
    'q': 0.095,
    'r': 5.987,
    's': 6.327,
    't': 9.056,
    'u': 2.758,
    'v': 0.978,
    'w': 2.361,
    'x': 0.150,
    'y': 1.974,
    'z': 0.074,
    'A': 8.167,
    'B': 1.492,
    'C': 2.782,
    'D': 4.253,
    'E': 12.702,
    'F': 2.228,
    'G': 2.015,
    'H': 6.094,
    'I': 6.966,
    'J': 0.153,
    'K': 0.772,
    'L': 4.025,
    'M': 2.406,
    'N': 6.749,
    'O': 7.507,
    'P': 1.929,
    'Q': 0.095,
    'R': 5.987,
    'S': 6.327,
    'T': 9.056,
    'U': 2.758,
    'V': 0.978,
    'W': 2.361,
    'X': 0.150,
    'Y': 1.974,
    'Z': 0.074,
    ' ': 13,
    '\'': 2,
    '.': 2,
    ',': 2,
}

def decrypt(crypt, key):
    #takes two arguments, each a byte in hex, as strings, and returns an str
    decrypted = int(crypt,16) ^ int(key,16)
    return str("%02x" % decrypted)

def brute(crypttext):
    #prepare an index from 0 to length of crypttext, skipping chars
    index = range(0, len(crypttext))[::2]

    #highscore must be lower than the lowest possible string score
    #e.g. all unprintable chars
    highscore = 0
    bestkey = ''

    for key in string.ascii_uppercase:
        freqtable = {}
        score = 0

        #build your table of frequencies for the current key
        for i in index:
            decrypted = unhexlify(decrypt(crypttext[i:i+2], hexlify(key)))
            if not(freqtable.has_key(decrypted)):
                freqtable[decrypted]=1
            else:
                freqtable[decrypted]+=1

        #now score your table
        for letter in freqtable:
            if scoretable.has_key(letter):
                score += freqtable[letter] * scoretable[letter]

        #keep track of which key got the highest score
        if score > highscore:
            highscore = score
            bestkey = key

    #build your decrypted string using the best key
    cleartext=""
    for i in index:
       clearchar = unhexlify(decrypt(crypttext[i:i+2], hexlify(bestkey)))
       cleartext += clearchar

    return highscore, cleartext

brutelist = []
f = open('4.txt', 'r')
allbrutes = {}
for line in f:
    bruted=brute(line.strip('\n'))
    brutelist.append(bruted)

for line in sorted(brutelist):
    print line, '\n'
