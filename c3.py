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
    ' ': 13,
    '\'': 2,
    '.': 2,
    ',': 2,
}

def score(string):
    score = 0
    for char in string:
        if char in scoretable:
            score += scoretable[char]
    return score

def strxor_c(string, key):
    xored = ''
    for char in string:
        xored += chr(ord(char)^ord(key))
    return xored

def breakSingleByteXOR(string):
    #return the key for a ciphertext XORed with a single character
    def keyscore(p):
        return score(p[1])
    return max([(chr(i), strxor_c(string, chr(i))) for i in range(0, 256)], key=keyscore)[0]

if __name__ == '__main__':
    encodedS = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    s = unhexlify(encodedS)
    print(breakSingleByteXOR(s))
