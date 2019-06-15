from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import MD5
import base64
def RSA_sign(data):
    with open("master-private.pem","r") as f:
    	key = f.read()
    priKey = RSA.importKey(key)
    signer = PKCS1_v1_5.new(priKey)
    hash_obj = MD5.new(data.encode('utf-8'))
    signature = base64.b64encode(signer.sign(hash_obj))
    return signature

def verify(signature,data):
    with open("master-public.pem","r") as f:
    	key = f.read()
    pubKey = RSA.importKey(key)
    h = MD5.new(data.encode('utf-8'))
    verifier = PKCS1_v1_5.new(pubKey)
    return verifier.verify(h, base64.b64decode(signature))

print (RSA_sign("OK I KNOW "))
#print (verify(b'e/zh4pnUU0HeJBGOEFAw4xDhpM7OgRINRCljDP6uPGVRPYb/RDLpUAXgyUnkk/RgsfxtG3P2fDg5HPmFZYwBew04Xq+ib4IUt+n/fYyFcQMM9MaDHDGUFeT5S6hQVv4agu5FkLiDzHO98hxkQ877WCI8U3kseXID07I0wX8SAAwT2sOnDVcHGoDstQ+Oi5CMT/FObmYdJn8HHL4khmldmomqcsweah460XImFZreyAatWISiWX5gHm4krhhZMqa/qltDKCgsj2FxS+xNZBzg5Y4gm3WFY+3yhdrgNWNSy+mZNN8GavoPbwtgsUVnApef4fhkrBVyauOLe2Ezh00Ljg==',"abcd"))
