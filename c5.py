#!/usr/bin/python
key = 'ICE'
cleartext = '''Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal'''

def XORencrypt(s, key):
  #build a key same length as s
  longkey = []
  for i in range(len(s)):
      longkey.append(key[i % len(key):i % len(key) + 1])

  #read the characters of the cleartext and xor with key
  crypttext = []
  for i in range(len(s)):
      crypttext.append('%02x' % (ord(s[i]) ^ ord(longkey[i])))
  return ''.join(crypttext)

print XORencrypt(cleartext, key)
