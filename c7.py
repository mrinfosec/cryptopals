#!/usr/bin/python
#
# AES in ECB mode
# The Base64-encoded content in this file has been encrypted via AES-128 in ECB mode under the key
#
# "YELLOW SUBMARINE".
# (case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too).
#
# Decrypt it. You know the key, after all.
#
# Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.

from Crypto.Cipher import AES
from base64 import b64decode

aesobj = AES.new('YELLOW SUBMARINE', AES.MODE_ECB)
ciphertext = b64decode(open('7.txt', 'r').read())
cleartext = aesobj.decrypt(ciphertext)
print cleartext
