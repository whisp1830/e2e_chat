import sys
import time
import socket
import random
import threading
import aes_encrypt
import rsa_encrypt
def message_check(s,text):
    '''
    check sum
    '''

    pass

def ack_handler():
    pass

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 将套接字绑定到地址
    s.bind(('0.0.0.0', int(sys.argv[1])))
    # 监听TCP传入连接
    s.listen(5)
    def handle_tcp(sock, addr):
        print("new connection from %s:%s" % addr)
        sock.send(b'Welcome!')

        while True:
            data = str(sock.recv(1024), encoding="utf-8")
            print (data)
            if not data:
                break

            client_hello = data.split(" ")
            if client_hello:
                time.sleep(1)
                if client_hello[0] == "CLIENTHELLO":
                    print (client_hello)
                    print ("A new SSL handshake starts!")

                    seed_1 = client_hello[2]
                    seed_2 = str(random.randint(10**10,10**11))

                    server_hello = "SERVERHELLO TLS1.3 %s AES-128-ECBAES-128-CFBAES-256-ECBAES-256-CFBDES-128-CFB RSA-2048DIFFLEHELLMAN MD5SHA-256SHA-512 "%seed_2
                    with open("master-public.pem","r") as f:
                        server_hello += f.read()

                    sock.send(bytes(server_hello,encoding="utf-8"))
                    
                    client_respond = sock.recv(1024)
                    client_respond = str(client_respond, encoding="utf-8")
                    client_respond = client_respond.split(" ")
                    cipher_text = client_respond[-1]
                    print (cipher_text)
                    
                    private_key = ""
                    with open("master-private.pem","r") as f:
                        private_key = f.read()
                    rsakey = rsa_encrypt.RSA.importKey(private_key)
                    cipher = rsa_encrypt.Cipher_pkcs1_v1_5.new(rsakey)
                    text = cipher.decrypt(rsa_encrypt.base64.b64decode(cipher_text),"ERROR")

                    seed_3 = str(text, encoding="utf-8")
                    print (seed_1,seed_2,seed_3)
                    aes_key = str(int(seed_1) * int(seed_2) * int(seed_3))[:32]
                    print ("The AES key is ", aes_key)

                    while True: 
                        is_complete_flag = False
                        reply = ""
                        data = sock.recv(1024)
                        data = aes_encrypt.decrypt_oralce(aes_key,data)
                        data = str(data, encoding="utf-8")
                        print ("After decryption:",data)

                        if aes_encrypt.get_md5_sum(data[:-32]) == data[-32:]:
                            is_complete_flag = True
                            if data == "160400218 陈天屹 1604201e178dff8516d75ba6cf38fa79c61369a":
                                reply = "MEET ME AT SONGJIAN MID ROOM 401 " + str(random.randint(1,10**10))
                            else:
                                reply = "OK I KNOW " + str(random.randint(1,10**10))
                        else:
                            is_complete_flag = False
                            reply = "THE DATA YOU SENT IS CURRUPTED " + str(random.randint(1,10**10))

                        reply_sign = rsa_encrypt.rsa_sign(reply,"master-private.pem")
                        print(reply_sign)
                        data = aes_encrypt.encrypt_oralce(aes_key, reply+str(reply_sign, encoding="utf-8"))
                        data = bytes(data, encoding="utf-8")
                        sock.send(data)
                        print ("send success!")
        sock.close()


    while True:
        sock, addr = s.accept()
        t = threading.Thread(target=handle_tcp, args=(sock, addr))
        t.start()
