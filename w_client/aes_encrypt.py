#AES-demo
import os
import hashlib
import base64
from Crypto.Cipher import AES
from base64 import urlsafe_b64encode, urlsafe_b64decode
from Crypto import Random

'''
采用AES对称加密算法
'''
# str不是16的倍数那就补足为16的倍数
def add_to_16(value):

    need_char = -len(str.encode(value)) %16
    value += '\0' * need_char
    return str.encode(value)  # 返回bytes

#加密方法
def encrypt_ecb(key,text):
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #先进行aes加密
    encrypt_aes = aes.encrypt(add_to_16(text))
    #用base64转成字符串形式
    encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 执行加密并转码返回bytes
    return encrypted_text



#解密方法
def decrypt_ecb(key,text):
    if isinstance(text,bytes):
        text = str(text,encoding = "utf-8")
    # 初始化加密器
    aes = AES.new(add_to_16(key), AES.MODE_ECB)
    #优先逆向解密base64成bytes
    base64_decrypted = base64.decodebytes(text.encode(encoding='utf-8'))
    #执行解密密并转码返回str
    decrypted_text = str(aes.decrypt(base64_decrypted),encoding='utf-8').replace('\0','') 
    return bytes(decrypted_text, encoding = "utf-8")

def get_md5_sum(text):
    if isinstance(text,bytes):
        text = str(text, encoding = "utf-8")
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def encrypt_oralce(key, msg):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=AES.block_size * 8)
    encrypted_msg = cipher.encrypt(add_to_16(msg))
    return str(urlsafe_b64encode(iv + encrypted_msg), encoding="utf-8")


# when incorrect encryption key is used, `decrypt` will return empty string
def decrypt_oralce(key, msg):
    msg = str(msg, encoding="utf-8") if isinstance(msg,bytes) else msg
    msg = bytes(msg + '=' * (4 - len(msg) % 4), encoding="utf-8")
    decoded_msg = urlsafe_b64decode(msg)
    iv = decoded_msg[:16]
    encrypted_msg = decoded_msg[16:] 
    cipher = AES.new(key, AES.MODE_CFB, iv, segment_size=AES.block_size * 8)
    decrypted_text = cipher.decrypt(encrypted_msg)
    decrypted_text = str(decrypted_text, encoding="utf-8").replace('\0','').replace('\\x00','')
    return bytes(decrypted_text, encoding="utf-8")



if __name__ == '__main__':
    b = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAyjQMagPj2fOyRkKkjewZ
zMHb8fKpx7hlfJ8Q/iFz7cxCSj+8CrtipRSDbMMilppaYd6yBd1cKE35CPQuGLpf
zZoQGJZLd+FQ3dSHAKcmxbIgqrl6Dcp4EjKPYdgOlSkmnQeLzUoCeEHnB2kVjQ9T
cgq6+HjKNUpmA+aIDREs1dQwSspqlSwniU7JcVsQeY3fQWe+NnMsb0Oz4WqHs3l8
hTQ5DwdE9zSNl9z2rcjw8QrolDEewETifRoXGbrOgRWOWfuN8sfjCBcEw5hvaHT6
Yx/wwexO7uGUdaDSc0dNFrN7xLbAZSbvNF5WJwpLCiQMjG1PtxKwKv++fnu2qUjF
lwIDAQAB
-----END PUBLIC KEY-----
name:bob
org:whispchan
ca_name:whispchan
ca_org:whispchan
hash:sha-256
encrypt:rsa"""
    print (get_md5_sum(b))


