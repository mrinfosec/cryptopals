#!/usr/bin/python

# ECB cut-and-paste
#
# Write a k=v parsing routine, as if for a structured cookie. The routine
# should take:
#
# foo=bar&baz=qux&zap=zazzle ...
#
# and produce:
#
# { foo: 'bar', baz: 'qux', zap: 'zazzle' }
#
# Now write a function that encodes a user profile in that format, given an
# email address. You should have something like:
#
# profile_for("foo@bar.com") ... and it should produce:
#
# { email:'foo@bar.com', uid: 10, role: 'user' }
#
# ... encoded as:
#
# email=foo@bar.com&uid=10&role=user
#
# Your "profile_for" function should not allow encoding metacharacters (& and
# =). Eat them, quote them, whatever you want to do, but don't let people set
# their email address to "foo@bar.com&role=admin".
#
# Now, two more easy functions. Generate a random AES key, then:
#
# Encrypt the encoded user profile under the key; "provide" that to the
# "attacker".
# Decrypt the encoded user profile and parse it.
# Using only the user input to profile_for() (as an oracle to generate "valid"
# ciphertexts) and the ciphertexts themselves, make a role=admin profile.

import re
from c9 import pkcs7pad, pkcs7unpad
from c11 import aesecb_encrypt, aesecb_decrypt, genaeskey

emailregex = '[&=]'
key = genaeskey()
def parsetokens(s):
    obj = {}
    pairs = s.split('&')
    for pair in pairs:
        foo = pair.split('=')
        obj[foo[0]]=foo[1]
    return obj

def adduser(email):
    if re.search(emailregex, email):
        raise Exception('That does not look like an email address.')
    print 'user ' + email + ' added!'
    account={'email':email, 'uid':10, 'role':'user'}
    return 'email='+account['email']+'&uid='+str(account['uid'])+'&role='+account['role']

def profile_for(email):
    return aesecb_encrypt(pkcs7pad(adduser(email), 16), key)

def validateusersecure(cookie):
    return parsetokens(pkcs7unpad(aesecb_decrypt(cookie, key)))

if __name__ == '__main__':
    evilemail = chr(4)*10 + 'admin' + chr(4)*11
    copyblock = profile_for(evilemail)[16:32]
    adminemail = 'phear@hah.com'
    rootcookie = profile_for(adminemail)[:-16]+copyblock
    usrobj = validateusersecure(rootcookie)
    print usrobj
# print adduser('foo@bar.com&role=admin')

# pseudocode
#
# 1.  submit email address of 10'\x04's, 'admin', and 11 \x04s
# 2.  copy second block
# 3.  submit email address 13 characters long and get token
# 4.  replace last block with block from 2
# 5.  validate it
