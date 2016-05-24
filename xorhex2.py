#!/usr/bin/python
import binascii
#define starting string
h1 = int(raw_input("Enter your hex string #1: "), base=16)
h2 = int(raw_input("Enter your hex string #2: "), base=16)
xored = (h1 ^ h2)
print str(hex(xored))
