# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nice_qt.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from chat_ui import Chat_MainWindow
import w_client
import socket
import time
import sys




class Ui_MainWindow(object):

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(1)
        self.ca_public_key = ""

    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        self.MainWindow.setObjectName("MainWindow")
        self.MainWindow.resize(350, 450)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(200, 400, 130, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_open_ca = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_open_ca.setGeometry(QtCore.QRect(110, 100, 130, 25))
        self.pushButton_open_ca.setObjectName("pushButton_open_ca")


        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(110, 140, 130, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(110, 180, 130, 25))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(110, 220, 130, 25))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")


        self.lineEdit_addr = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_addr.setGeometry(QtCore.QRect(110, 20, 120, 20))
        self.lineEdit_addr.setObjectName("lineEdit_addr")
        self.lineEdit_port = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_port.setGeometry(QtCore.QRect(240, 20, 60, 20))
        self.lineEdit_port.setObjectName("lineEdit_port")

        self.label_port = QtWidgets.QLabel(self.centralwidget)
        self.label_port.setGeometry(QtCore.QRect(235, 20, 16, 16))
        self.label_port.setObjectName("label_port")
        self.label_addr = QtWidgets.QLabel(self.centralwidget)
        self.label_addr.setGeometry(QtCore.QRect(30, 20, 60, 16))
        self.label_addr.setObjectName("label_addr")
        self.label_symmetry = QtWidgets.QLabel(self.centralwidget)
        self.label_symmetry.setGeometry(QtCore.QRect(30, 140, 60, 16))
        self.label_symmetry.setObjectName("label_symmetry")
        self.label_exchange = QtWidgets.QLabel(self.centralwidget)
        self.label_exchange.setGeometry(QtCore.QRect(10, 180, 80, 16))
        self.label_exchange.setObjectName("label_exchange")
        self.label_hash = QtWidgets.QLabel(self.centralwidget)
        self.label_hash.setGeometry(QtCore.QRect(10, 220, 80, 20))
        self.label_hash.setObjectName("label_hash")
        self.label_ca_pk = QtWidgets.QLabel(self.centralwidget)
        self.label_ca_pk.setGeometry(QtCore.QRect(30, 100, 81, 21))
        self.label_ca_pk.setObjectName("label_ca_pk")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.MainWindow.setWindowTitle(_translate("MainWindow", "whisp chat v0.1"))


        self.pushButton.setText(_translate("MainWindow", "Start secret chat"))
        self.pushButton.clicked.connect(self.ClickConnect)
        self.pushButton_open_ca.setText(_translate("MainWindow", "Choose file"))
        self.pushButton_open_ca.clicked.connect(self.ClickOpen)

        self.comboBox.setItemText(0, _translate("MainWindow", "AES-128-ECB"))
        self.comboBox.setItemText(1, _translate("MainWindow", "AES-128-CFB"))
        self.comboBox.setItemText(2, _translate("MainWindow", "AES-256-ECB"))
        self.comboBox.setItemText(3, _translate("MainWindow", "AES-256-CFB"))
        self.comboBox.setItemText(4, _translate("MainWindow", "DES-128-CFB"))
        self.comboBox.setItemText(5, _translate("MainWindow", "IDEA-CFB"))
        self.comboBox.setItemText(5, _translate("MainWindow", "RC4"))

        self.comboBox_2.setItemText(0, _translate("MainWindow", "RSA-1024"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "RSA-2048"))        
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Diffle Hellman"))
        
        self.comboBox_3.setItemText(0, _translate("MainWindow", "MD5"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "SHA-1"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "SHA-128"))
        self.comboBox_3.setItemText(3, _translate("MainWindow", "SHA-256"))
        self.comboBox_3.setItemText(4, _translate("MainWindow", "SHA-512"))

        self.label_port.setText(_translate("MainWindow", ":"))
        self.label_addr.setText(_translate("MainWindow", "通信地址"))
        self.label_symmetry.setText(_translate("MainWindow", "加密算法"))
        self.label_exchange.setText(_translate("MainWindow", "密钥交换算法"))
        self.label_hash.setText(_translate("MainWindow", "消息认证算法"))
        self.label_ca_pk.setText(_translate("MainWindow", "CA根证书"))

    def ClickExit(self):
        pass

    def ClickConnect(self):
        self.encrypt_suit = (self.comboBox.currentText(), self.comboBox_2.currentText(), self.comboBox_3.currentText())
        try:
            self.sock.connect((self.lineEdit_addr.text(), int(self.lineEdit_port.text())))
        except:
            QtWidgets.QMessageBox.warning(None, "REFUSED", "CONNECTION REFUSED, MAYBE YOU INPUT A WRONG IP ADDR/PORT OR THE SERVER SEEMS DOWN",QtWidgets.QMessageBox.Yes)
            return -1
        QtWidgets.QMessageBox.information(None, "CONNECTED!", "Now you can comm with opponent",QtWidgets.QMessageBox.Yes)
        
        self.window2 = QtWidgets.QMainWindow()
        self.ui_2 = Chat_MainWindow(self.sock, self.ca_public_key, self.encrypt_suit)
        self.ui_2.setupUi(self.window2)
        self.MainWindow.close()
        self.window2.show()


    def ClickOpen(self):
        openfile_name = QFileDialog.getOpenFileName(None,'选择文件','.',"CA Files (*.cert);;")
        print (openfile_name)
        self.ca_public_key = openfile_name[0]








if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
