# -*- coding: utf-8 -*-

"""
Module implementing register.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog,QApplication,QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets,QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMessageBox
import sys
from Ui_register import Ui_Dialog
from Ui_chat import Ui_Dialog1
import socket
import pickle
from multiprocessing import Pool,current_process
from multiprocessing.pool import ThreadPool
from threading import Thread,currentThread
client_list = []

class register(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(register, self).__init__(parent)
        self.setupUi(self)
        self.show()
        self.p = ThreadPool(2)


    def revieve_msg(self,ui,client):#接收消息函数
        while True:
            try:
                msg_data = pickle.loads(client.recv(1024))  
        #接收消息
            except BlockingIOError:   
                continue
            if 'qq_list' in msg_data:
                ui.receive_qq_list(msg_data['qq_list'])
                #如果协议_QQ列表在的话 就调用函数 刷新qq在线列表s
                QApplication.processEvents()
                #刷新列表
            if 'message' in msg_data:
                # qq = msg_data['from_qq']
                # name = msg_data['from_name']
                ui.insert_msg(msg_data)
                QApplication.processEvents()
                #刷新列表
                
           



    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.user_qq = self.lineEdit.text()
        self.user_name = self.lineEdit_2.text()
        if not(self.user_qq and self.user_name):
            QMessageBox.about(self,'登录失败','用户名或者密码不能为空')
            return
        if self.user_qq.isdigit():#如果输入的是数字的话 就可以通过
            #pickle 用来传输数据的时候  保持数据类型
            client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            #创建一个客户端链接,socket.AF_INET代表ipv4，socket.SOCK_STREAM代表tcp套接字
            client.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            #设置端口复用
            try:

                client.connect(('101.132.39.95',23334))
            except ConnectionRefusedError:
                QMessageBox.about(self,'登录失败','服务器没开')
                return
            #客户端链接
            client_list.append(client)
            user_info = {
                'first':None,
                'qq':self.user_qq,
                'name':self.user_name,
            }
            client.send(pickle.dumps(user_info))
            #把第一次登陆的消息发送给服务器
            data = pickle.loads(client.recv(1024))
            if data:
                QMessageBox.about(self,'登录成功','您已经成功登录')
                client_list[0].setblocking(0)# 设置成非阻塞套接字
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.hide()
                #-------------------------------------
                #当登录成功的时候 弹出这个界面
                Dialog = QtWidgets.QDialog()

                ui = Ui_Dialog1()
                ui.setupUi(Dialog,client_list[0])
                Dialog.setWindowTitle('欢迎:    '+self.user_name)
                a = Thread(target = self.revieve_msg,args = (ui,client_list[0])) 
                a.setDaemon(True)
                #这里很蛋疼 必须要让线程退出 就只能设置这样
                #设置如果父进程结束 那么子线程也就结束了 不会等待子线程结束 父进程在结束
                print('11')
                a.start()  
                print('22')          
                Dialog.show()
                #show 与 exec_的区别是 show是闪一下  而exec_他要开辟一个线程  等待程序退出在退出
                Dialog.exec_()              
                print('33')
                self.close()
                #只有退出系统 才能退出进程 才能退出线程
                sys.exit(0)
                #系统退出
                #-------------------------------------
            else:
                QMessageBox.about(self,'登录失败','用户名重复')
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                client.close()
                #如果用户名重复 或者服务器没开 就把链接关了
                del client_list[0]
                #然后就把套接字给删除了
        else:
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            QMessageBox.about(self,'登录失败','请输入正确的QQ号和用户名')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = register()
    
    sys.exit(app.exec_())
