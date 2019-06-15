import sys
import time
import socket
import base64
import random
import aes_encrypt
import rsa_encrypt

def client_send_encrypt(sock,message,aes_key):

    new_message = aes_encrypt.encrypt_oralce(aes_key, message+aes_encrypt.get_md5_sum(message))

    cipher = bytes(new_message, encoding = "utf8")
    sock.send(cipher)
    return cipher



def client_hello(sock, encrypt_a9, exchange_a9, hash_a9):
    '''
        step 1: client hello
        client generate the first random int,
        sent it to server
    '''
    print (sock.recv(1024))
    seed_1 = str(random.randint(10**10,10**11))
    client_hello = bytes("CLIENTHELLO TLS1.3 %s %s %s %s"%(seed_1,encrypt_a9, exchange_a9, hash_a9), encoding= "utf-8")
    sock.send(client_hello)
    print ("SENT A PACKAGE\n", client_hello)
    return seed_1,client_hello


def server_hello(sock):

    # STEP 2.1: CLIENT SENT CLIENT HELLO
    server_hello = sock.recv(1024)
    server_hello = str(server_hello, encoding="utf-8")
    server_hello = server_hello.split(" ")

    print (server_hello)
    print (server_hello)
    print (server_hello)

    # STEP 2.2: CHECK THE SERVER'S CERTIFICATE
    # receive the second random int
    seed_2 = server_hello[2]
    algorithms = server_hello[:6]
    public_key = " ".join(server_hello[-5:])

    return seed_2, algorithms, public_key

def client_respond(sock, public_key, encrypt_a9, exchange_a9, hash_a9):

    # STEP 3: CLIENT RESPOND
    # client send the last random int, 
    # and encrypt it with server's public key by RSA algorithm
    # the AES_KEY is generated
    seed_3 = str(random.randint(10**10,10**11))
    rsakey = rsa_encrypt.RSA.importKey(public_key)
    cipher = rsa_encrypt.Cipher_pkcs1_v1_5.new(rsakey)
    cipher_text = str(rsa_encrypt.base64.b64encode(
        cipher.encrypt(seed_3.encode(encoding="utf-8"))), encoding="utf-8")

    client_respond = bytes("CLIENTRESPOND VERIFIED %s %s %s %s"%(encrypt_a9, exchange_a9, hash_a9, cipher_text), encoding="utf-8")
    sock.send(client_respond)
    print ("SENT A PACKAGE\n", client_respond)

    return seed_3, client_respond

if __name__ == '__main__':

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setblocking(0)
        s.settimeout(1)
        s.connect(('0.0.0.0', int(sys.argv[1])))
        s.send(bytes("CLIENTRESPOND VERIFIED ", encoding="utf-8"))
        s.send(bytes("CLIENTRESPOND VERIFIED ", encoding="utf-8"))
        s.send(bytes("CLIENTRESPOND VERIFIED ", encoding="utf-8"))

        print (s.recv(1024))
        

        seed_1 = client_hello(s)
        seed_2, public_key = server_hello(s)
        seed_3 = client_respond(s, public_key)

        aes_key = str(int(seed_1) * int(seed_2) * int(seed_3))
        print ("The AES key is ", aes_key)

        # Now, the data between client and server, has been encrypted by the AES key 
        # (according to seed_1, seed_2, seed_3)
        while True:
            try:
                print("RECV FROM SERVER ", str(s.recv(1024), encoding="utf-8"))
            except:
                pass
            input_text = input("Input here:")
            cipher = aes_encrypt.encrypt_oralce(aes_key, input_text)
            s.send(bytes(cipher, encoding = "utf8"))
        s.close()
