# JWT verification
# author : Akhil Raj Azhikodan
# date   : 14th feb,2017
#
# note : Flockappsecret is gitignored. The file contains the confidential app secret.
#        Contact author for the file


import jwt
import flockappsecret

def verify(encoded):
    # flockappsecret is .gitignored. Contact autor
    secret = flockappsecret.getSecret()
    try:
        jwt.decode(encoded, secret, algorithms=['HS256'])
        return True
    except:
        return False
