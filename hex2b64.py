#!/usr/bin/python
from binascii import a2b_hex, b2a_base64
#define starting string
h = raw_input("Enter your hex string to encode: ")
b64 = b2a_base64(a2b_hex(h));
print b64
