from base64 import urlsafe_b64encode, urlsafe_b64decode
from Crypto.Cipher import AES
from Crypto import Random


BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt(key, msg):
    iv = Random.new().read(BS)
    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=AES.block_size * 8)
    encrypted_msg = cipher.encrypt(pad(str(msg)))
    return urlsafe_b64encode(iv + encrypted_msg)


# when incorrect encryption key is used, `decrypt` will return empty string
def decrypt(key, msg):
	msg = bytes(str(msg,encoding="utf-8") + '=' * (4 - len(msg) % 4), encoding="utf-8")

	decoded_msg = urlsafe_b64decode(msg)
	iv = decoded_msg[:BS]
	encrypted_msg = decoded_msg[BS:] 
	cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=AES.block_size * 8)
	return unpad(cipher.decrypt(encrypted_msg))

