#!/usr/bin/python
#
# Cryptopals challenge 1-3:  Single-byte XOR cipher
# The hex encoded string:
#
# 1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736
# ... has been XOR'd against a single character. Find the key, decrypt the
# message.
#
# You can do this by hand. But don't: write code to do it for you.
#
# How? Devise some method for "scoring" a piece of English plaintext. Character
# frequency is a good metric. Evaluate each output and choose the one with the
# best score.

from binascii import hexlify, unhexlify
import string, operator

cryptogram = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

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


def brute(crypttext):
    #takes a binary string as input and tries all possible keys

    highscore = 0
    bestkey = ''

    for key in range(256):
        freqtable = {}
        score = 0

        #build your table of frequencies for the current key
        for byte in crypttext:
            xored = chr(ord(byte) ^ key)
            if not(freqtable.has_key(xored)):
                freqtable[xored]=1
            else:
                freqtable[xored]+=1

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
    print chr(bestkey)
    for byte in crypttext:
       clearchar = chr(ord(byte) ^ bestkey)
       cleartext += clearchar

    return cleartext

#print brute(bin_cg)
