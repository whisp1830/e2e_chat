from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Crypto.Hash import MD5
import base64

def rsa_encrypt(message,key_file):
	with open(key_file,"r") as f:
		key = f.read()
		rsakey = RSA.importKey(key)  # 导入读取到的公钥
		cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
		cipher_text = base64.b64encode(cipher.encrypt(message.encode(encoding="utf-8")))  # 通过生成的对象加密message明文，注意，在python3中加密的数据必须是bytes类型的数据，不能是str类型的数据
		return cipher_text

def rsa_decrypt(message,key_file):
	with open(key_file,"r") as f:
		key = f.read()
		rsakey = RSA.importKey(key)  # 导入读取到的私钥
		cipher = Cipher_pkcs1_v1_5.new(rsakey)  # 生成对象
		text = cipher.decrypt(base64.b64decode(message), "ERROR")  # 将密文解密成明文，返回的是一个bytes类型数据，需要自己转换成str
		return text

def rsa_sign(data,key_file):
    with open(key_file,"r") as f:
    	key = f.read()
    priKey = RSA.importKey(key)
    signer = Signature_pkcs1_v1_5.new(priKey)
    hash_obj = MD5.new(data.encode('utf-8'))
    signature = base64.b64encode(signer.sign(hash_obj))
    return signature

def rsa_verify(signature,data,key_file):
    with open(key_file,"r") as f:
    	key = f.read()
    pubKey = RSA.importKey(key)
    h = MD5.new(data.encode('utf-8'))
    verifier = Signature_pkcs1_v1_5.new(pubKey)
    return verifier.verify(h, base64.b64decode(signature))

def key_pair_gen():

	random_generator = Random.new().read

	rsa = RSA.generate(2048, random_generator)

	private_pem = rsa.exportKey()
	with open("master-private.pem","wb") as f:
		f.write(private_pem)

	public_pem = rsa.publickey().exportKey()
	with open("master-public.pem", "wb") as f:
		f.write(public_pem)

	private_pem = rsa.exportKey()
	with open('ghost-private.pem', 'wb') as f:
	    f.write(private_pem)

	public_pem = rsa.publickey().exportKey()
	with open('ghost-public.pem', 'wb') as f:
	    f.write(public_pem)


if __name__ == "__main__":
	a = "cty1830"
	aa = " be that girl for a month"
	b = rsa_sign(a,"master-private.pem")
	print (b)
	b = rsa_sign(aa,"master-private.pem")
	print (b)
	#c = rsa_verify(b,a,"master-public.pem")
	#print (c)

