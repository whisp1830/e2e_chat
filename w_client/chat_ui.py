# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import time
import w_client
import aes_encrypt
import rsa_encrypt


class Chat_MainWindow(object):

    def __init__(self,sock,ca_public_key ,encrypt_suit):
        self.sock = sock
        self.handshake = False
        self.ca_public_key = ca_public_key
        self.encrypt_suit = encrypt_suit


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(630, 550)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30, 10, 571, 331))
        self.textBrowser.setObjectName("textBrowser")
        self.textEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 360, 571, 131))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(502, 500, 101, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(402, 500, 91, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        MainWindow.setCentralWidget(self.centralwidget)

        with open(self.ca_public_key,"r") as f:
            self.cert = f.read()

        self.textBrowser.append(self.cert)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Send"))
        self.pushButton.clicked.connect(self.ClickSend)
        self.pushButton_2.setText(_translate("MainWindow", "Disconnect"))
        self.pushButton_2.clicked.connect(self.ClickDisconnect)

    def ClickDisconnect(self):
        sys.exit()

    def ClickSend(self):
        if not self.handshake:

            encrypt_a9, exchange_a9, hash_a9 = self.encrypt_suit
            client_hello = w_client.client_hello(self.sock,encrypt_a9, exchange_a9, hash_a9)
            self.TextDisplay(client_hello[1],0)

            self.server_hello = w_client.server_hello(self.sock)

            self.TextDisplay(" ".join(self.server_hello[1]),1)

            for i in ['RC4', 'RSA-1024', 'SHA-1']:
                if i in self.encrypt_suit:
                    QtWidgets.QMessageBox.warning(None, "REFUSED", "HANDSHAKE FAILED, THE SERVER DO NOT SUPPORT %s"%i,QtWidgets.QMessageBox.Yes)
                    sys.exit()

            self.TextDisplay("SERVER's CERT:\n"+self.server_hello[2]+"\n"+'NAME:BOB\nORG:WHISPCHAN\nCA_NAME:WHISPCHAN\nCA_ORG:WHISPCHAN\nHASH:SHA-256\nENCRYPT:RSA',1)
            
            self.TextDisplay("SIGNATURE:\nXoRnkOUWqFnMGYm8uxmAbG6vxiTw2IEgmdg72YcAKC0ZSFihFbO18BqJRTUeWhsfQ9BNhz0dJT/VPj37RrWyVSTsn7clbGvH0jzzMAVVXkd+LBdlNImEEFSN9cKrR8DccXMrY4Wjvc65l3R0qfY+O5298KZpUnpsYpnq2sCVKOGvY6FqfDdgWouezCig/Z0uiv0GexuULCysGGrwpt537XnzaUb6iMokAZged8gSyELnw6I5gpM9tOaZe0yvekcuT2S6e0zNbvICSPl7y894DvhDg+J0eAHauVKENf14uixvEfFkbWN+NzFNbVHRedEofr/G4eb69N9ulQjYwgJXgg==",2)
            
            client_respond = w_client.client_respond(self.sock, self.server_hello[2], encrypt_a9, exchange_a9, hash_a9)

            self.public_key = self.server_hello[2]

            self.symmetric_key = str(int(client_hello[0]) * int(self.server_hello[0]) * int(client_respond[0]))[:32]

            self.TextDisplay(client_respond[1],0)

            self.TextDisplay("\n\n\n--------THE SYMMETRIC KEY--------\n%s"%self.symmetric_key,2)

            self.handshake = True

        else:
            print (self.ca_public_key)
            a =  self.textEdit.toPlainText()
            cipher = w_client.client_send_encrypt(self.sock,a,self.symmetric_key)
            self.TextDisplay(cipher,0)
            self.textEdit.clear()
            reply = self.sock.recv(4096)
            reply = str(reply, encoding="utf-8")
            self.TextDisplay(reply,1)
            plaintext = str(aes_encrypt.decrypt_oralce(self.symmetric_key,reply), encoding="utf-8")
            message,signature = plaintext[:-344], plaintext[-344:]
            self.textBrowser.append("AFTER DECRYPTION:\n" + message)
            self.textBrowser.append("SIGNATURE:\n" + signature)
            self.textBrowser.append("VERIFY RESULT: " + str(rsa_encrypt.rsa_verify(signature,message,self.public_key)))


    def TextDisplay(self,text,source):
        text = str(text, encoding="utf-8") if isinstance(text,bytes) else text
        
        if source == 0:
            self.textBrowser.append("\n[SENT "+str(time.ctime())+ "] "+ text)
        elif source == 1:
            self.textBrowser.append("\n[RECV "+str(time.ctime())+ "] "+ text)
        else:
            self.textBrowser.append(text)











if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Chat_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
