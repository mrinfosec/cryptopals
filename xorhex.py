#!/usr/bin/python
from binascii import a2b_hex, b2a_hex
h1 = raw_input("Enter hex string #1: ")
h2 = raw_input("Enter hex string #2: ")
hex1 = int(h1,16)
hex2 = int(h2,16)
xored = (hex1 ^ hex2)
print "%X" % xored
