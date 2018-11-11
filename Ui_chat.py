# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\python\GUI\ll\chat.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMessageBox
import sys
import pickle

class Ui_Dialog1(object):
    def setupUi(self, Dialog,client):
        self.Dialog = Dialog
        self.client = client
        Dialog.setObjectName("Dialog")
        Dialog.resize(679, 454)
        Dialog.setMinimumSize(QtCore.QSize(679, 454))
        Dialog.setMaximumSize(QtCore.QSize(679, 454))
        Dialog.setSizeGripEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("F:\\python\\GUI\\ll\\3.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(500, 0, 181, 461))
        self.listWidget.setMaximumSize(QtCore.QSize(16777211, 16777215))
        self.listWidget.setObjectName("listWidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(0, 0, 501, 331))
        #
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(0, 330, 501, 131))
        #发送消息框
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(430, 425, 71, 31))
        self.pushButton.setObjectName("pushButton")
        self.listWidget.itemClicked.connect(self.q_list_widget_click)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton.clicked.connect(self.send_msg)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "发送"))
    def q_list_widget_click(self,Item):
        QMessageBox.information(self.Dialog,"ListWidget", "你选择了: "+Item.text())
        #self.listWidget.currentRow() 这是看选择的现在的第几行 从0行开始
        #这里错了很多次 QMessagebox第一个参数是是选择一个容器
        #第一个参数 需要一个容器输出
    def insert_msg(self,msg):
        message = msg['message']
        from_qq = msg['from_qq']
        from_name = msg['from_name']
        from_time = msg['from_time']
        self.plainTextEdit.insertPlainText(
            '------'+from_time+'  '+'from_qq:'+from_qq+'  |  from_name:'+from_name+'-----'+'\n'+
            '   '+message+'\n'
            )


    def get_qq(self,text):
        index = text.index('|')
        return text[3:index]
    def send_msg(self):
       
        if not self.plainTextEdit_2.toPlainText():
            QMessageBox.information(self.Dialog,"错误", "不能发送为空的消息")
            self.plainTextEdit_2.clear()
            return
        if not self.listWidget.currentRow():
            #如果选择的是所有人all的话
            pass
            #加一个all 标志s
        msg = {
            'message':None,
            'to_qq':self.get_qq(self.listWidget.currentItem().text()),
            'to_msg':self.plainTextEdit_2.toPlainText(),
            #获取输入框中的内容
        }
        self.plainTextEdit.insertPlainText(
            '你向   '+self.listWidget.currentItem().text()+'发送了:\n'+
                '   '+self.plainTextEdit_2.toPlainText()+'\n'
            )
        self.client.send(pickle.dumps(msg))
        #发送消息
        self.plainTextEdit_2.clear()
        #将输入框清空


        
    def receive_qq_list(self,qq_dict):
        self.listWidget.clear()
        #删除列表中的内容
        b = qq_dict.keys()
        # self.listWidget.addItem('all')
        for a in b:
            c = a
            self.listWidget.addItem('qq:'+c+'|name:'+qq_dict[a])
        #刷新客户端QQ列表

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog1()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
