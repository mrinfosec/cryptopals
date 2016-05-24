#!/usr/bin/python

from c9 import pkcs7unpad

print repr(pkcs7unpad("ICE ICE BABY\x04\x04\x04\x04"))
#print repr(pkcs7unpad("ICE ICE BABY\x05\x05\x05\x05"))
print repr(pkcs7unpad("ICE ICE BABY\x01\x02\x03\x04"))
