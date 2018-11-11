import socket
import pickle
import _pickle
from multiprocessing.pool import ThreadPool
from threading import currentThread
import time
class TcpServer:
    def __init__(self):
        '''
            1，初始化自己

        '''
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #初始化自己，创建一个套接字
        self.server.setblocking(0)
        #设置我的服务端套接字为非阻塞
        self.server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        #设置端口复用
        self.server_port = 23334
        #服务器开启的端口
        self.server_ip = ''
        #服务器开启的ip地址
        #--------------------------------
        self.client_dict = { }
        #QQ列表
        self.old_qq_dict = []
        #客户端字典
    def run(self):
        '''
            1.接受客户端链接
            2.处理客户端的请求

        '''
        print('[+] 服务器开启')
        while True:

            try:
                try:
                    client,client_addr = self.server.accept()
                    #接受客户端链接
                except BlockingIOError:
                    pass
                    #非阻塞模型下没有套接字链接 就默认跳过
                else:
                    client.setblocking(0)
                    #设置我的客户端套接字为非阻塞
                    print('[+] %s 链接进来了'%(client_addr[0]))
                    #显示谁链接进来了
                    self.client_dict[client] = {
                        'user_info':{
                            'user_qq':None,
                            'user_name':None
                        },
                        'user_msg':{
                            'to_client':None,
                            'to_msg':None
                        },
                    }
                client_dict_list = list(self.client_dict.keys())
                #-----------------------------------------------------------------------------
                     #把套接字列表作为一个备份
                for client in client_dict_list:
                    try:
                        recv_data = pickle.loads(client.recv(1024))
                        #客户端第一次链接会发送一个数据 包括客户端的qq号，名字
                        #如果上面的执行成功，就把套接字追加到客户端列表中
                        #EOFError表示客户端发送了不正常的消息或者断开了链接

                    except _pickle.UnpicklingError:
                        #这是接收到不是用python  pickle 模块序列化话的消息
                        print('[E] 接收到无效消息')
                        client.send('发送无效数据'.encode('utf-8'))
                        #接收到无效消息
                        del self.client_dict[client]
                        #就吧这个客户端链接在套接字列表删除
                        client.close()

                        #在吧这个套接字关闭
                    except BlockingIOError:
                        pass
                        #如果没接收到消息 就继续
                    except ConnectionResetError:
                        del self.client_dict[client]
                        #就吧这个客户端链接在套接字列表删除
                        client.close()

                        #在吧这个套接字关闭
                    except EOFError as e:
                        #把客户端套接字关了
                        #就把客户端关闭 然后在列表删除
                        client.close()
                        del self.client_dict[client]
                    else:
                        #如果没有报错 说明接收到了正确的消息
                        if 'first' in recv_data:
                            '''
                             用来确认身份  是不是第一次连接
                            '''
                            confirm = True
                            print('%s是第一次连接'%(client_addr,))
                            client_qq = recv_data['qq']
                            client_name = recv_data['name']
                            client_qq_list = []
                            #qq列表
                            client_qq_dict = {}
                            #字典
                            client_dict_list1 = list(self.client_dict.keys())
                            for client1 in client_dict_list1:
                                #将套接字中的qq全部添加进qq_list
                                client_qq_list.append(self.client_dict[client1]['user_info']['user_qq'])

                            if client_qq in client_qq_list:
                                #如果新连接的那个童鞋  qq号与列表中其他先连接的童鞋重复了 就给她发消息 然后关闭这个客户端
                                print('[E] QQ重复.....')
                                confirm = False
                                #确认身份为假 失败
                                client.send(pickle.dumps(confirm))
                                #客户端确认失败信号
                                del self.client_dict[client]
                                #重名的客户端删除
                                client.close()
                                continue
                                #在关了
                            else:
                                #如果注册的QQ没有重复 就把它添加进套接字列表

                                self.client_dict[client]['user_info']['user_qq'] = client_qq
                                self.client_dict[client]['user_info']['user_name'] = client_name
                                client.send(pickle.dumps(confirm))
                                #服务器发送登录成功信号
                                # for a in self.client_dict:
                                #     client_qq_dict[self.client_dict[a]['user_info']['user_qq']] = self.client_dict[a]['user_info']['user_name']
                                # #吧在线的客户端列表发过去
                                #client.send(pickle.dumps(client_qq_dict))
                        elif 'message' in recv_data:
                            '''
                            '真正来给别人发消息的'

                            '''
                            to_msg = recv_data['to_msg']
                            to_qq = recv_data['to_qq']

                            client_dict_list2 = list(self.client_dict.keys())
                            for client2 in client_dict_list2:
                                user_qq = self.client_dict[client2]['user_info']['user_qq']
                                if user_qq == to_qq:
                                    #找到了收件人
                                    from_qq = self.client_dict[client]['user_info']['user_qq']
                                    from_name = self.client_dict[client]['user_info']['user_name']
                                    #发送人: client
                                    #收件人: client2
                                    msg = {
                                        'message':to_msg,
                                        'from_qq':from_qq,
                                        'from_name':from_name,
                                        'from_time':time.strftime("%Y-%m-%d %A %H:%M:%S", time.localtime())
                                    }
                                    client2.send(pickle.dumps(msg))
                                    #消息发送了
                                    break
                            else:
                                #假如没找到那个qq
                                client.send('目标不存在，消息送不到'.encode('utf-8'))


            except KeyboardInterrupt:
                break
                #退出循环
                del self
                #删除回收函数 自动关闭客户端和服务端
    def send_user_list(self):
        while True:
            time.sleep(2)
            print('[+] 刷新客户端列表')
            client_qq_dict = {}
            if not self.client_dict:
                continue
            #如果没有qq在线 就继续
            var = [1]
            for a in self.client_dict:
                qq = self.client_dict[a]['user_info']['user_qq']
                name = self.client_dict[a]['user_info']['user_name']
                if qq is None:
                    qq =   '没QQ   '+str(var[0])+'号'
                    name = '没名字 '+str(var[0])+'号'
                    var[0] = var[0]+1
                client_qq_dict[qq] = name
            #遍历储存在线的客户端列表
            if client_qq_dict == self.old_qq_dict:
                continue
            msg_data = {
    			'qq_list':client_qq_dict
                #qq_list 协议标志 表示这个消息是用来刷新客户端列表的
    		}
            for item in client_qq_dict.items():
                print(item)
            for a in self.client_dict:
                a.send(pickle.dumps(msg_data))
                #定时向每个客户端发送在线客户列表
            self.old_qq_dict = client_qq_dict

    def __call__(self):
        #call函数  实例化对象加上括号作为函数调用时用这个函数
        self.server.bind((self.server_ip,self.server_port))
        #绑定ip和端口,默认绑定所有ip
        self.server.listen(5)
        #监听5个 同时最大连接数 5
        self.run()
        #开启服务器

    def __del__(self):
        #析构函数，跟c++一样，在实例被删除或者系统回收资源之后调用
        if self.client_dict:
            #关闭所有客户端套接字链接
            for client in self.client_dict:
                try:

                    client.send('服务端关闭'.encode('utf-8'))
                    client.close()
                except OSError:
                    pass
        self.server.close()
        #关闭服务器套接字链接

def main():
    s = TcpServer()
    p = ThreadPool(1)
    #开启1个线程池
    p.apply_async(func = s)
    s.send_user_list()
    p.close()
    p.join()


if __name__ == '__main__':
    main()
