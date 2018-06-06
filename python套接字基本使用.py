
socket通常也称作"套接字"，用于描述IP地址和端口，应用程序通常通过"套接字"向网络发出请求或者应答网络请求,可以认为是一种计算机网络的数据结构,接口。它是网络编程的基础。

套接字还分为面向连接的和无连接的：

第一种是指TCP类型套接字，在通信前需要建立连接，这种连接是较为可靠的，使用的套接字类型是SOCK_STREAM,TCP传输控制协议，经常和IP协议一起使用，称为TCP/IP协议
第二种主要指UDP类型的套接字，无需连接就可以进行通讯，所有速度较快，但是可靠性不高。而且数据是整个发送，不会分成小块。使用的套接字类型是SOCK_DGRAM，UDP协议通常也与IP协议一起使用

python中的socket模块

使用套接字的基本步骤：

创建套接字

socket(socket_family, socket_type, protocol)
#socket_family 就是指套接字家族可以是AF_VNIX或AF_INET
#socket_type 就是指套接字类型，即SOCK_STREAM或SOCK_DGRAM
#protocol 是协议，默认为0，一般不填

创建TCP/IP或者UDP/IP套接字

创建TCP/IP套接字

import socket
tcp = socket.socket(AF_INET, SOCK_STREAM)

创建UDP/IP套接字

import socket
ucp = socket.socket(AF_INET, SOCK_DGRAM)

套接字的常用函数

函数名 	                               描述
服务器套接字 	
bind((hostname, port)) 	   绑定地址(注意这里是元祖)到套接字
listen() 	                 开启TCP监听
accept() 	                 被动接受客户端的连接(阻塞)
客户端套接字 	
connect((hostname, port))  初始化TCP服务器连接
connect_ex() 	             connect()的扩展版本，出错时返回错误码，而不是异常
公用的套接字 	
recv()                     接收TCP的数据
send() 	                   发送TCP数据
sendall() 	               发送完整的TCP数据
recvfrom() 	               接收UDP数据
sendto() 	                 发生UDP数据，因为没有连接，所以这里要指定发送的目标
getpeername() 	           连接到当前套接字的远程地址
getsockname() 	           当前socket地址
getsockopt() 	             获得套接字的参数
setsockopt() 	             设置套接字的参数
close() 	                 关闭套接字
面向模块的套接字函数 	
setblocking() 	           设置套接字是否是阻塞模式
settimeout() 	             设置阻塞套接字操作的超时时间
gettimeout() 	             得到阻塞套接字操作的超时时间
面向文件的套接字函数 	
fileno() 	                 套接字的文件描述符
makefile() 	               创建一个与套接字关联的文件对象

创建一个TCP服务器和客户端

创建TCP服务器的基本步骤

1.创建套接字并绑定地址
2.开始监听连接
3.接收链接并发送数据
4.关闭套接字

代码如下:
import socket

HOST = ''   #空字符串标示127.0.0.1
PORT = 3214

sk = socket.socket() # 默认使用IPV4和TCP

sk.bind((HOST,PORT))

sk.listen(5)

cli, addr = sk.accept() # 等待连接(阻塞式),在连接到来之前会阻塞在这里

print "Client Addr:", addr

while True:
    data = cli.recv(1024)
    if not data:
        break
    print "Recieve Data:", data.decode('utf-8')
    cli.send(data)

cli.close()

创建TCP客户端的基本步骤

1.创建套接字，连接服务器
2.收发数据
3.关闭套接字

import socket

HOST = '127.0.0.1'
PORT = 3214

sk = socket.socket()

try:
    sk.connect((HOST, PORT))
    data = "hello"
    while data:
        sk.sendall(data)
        data = sk.recv(1024)
        print "Recv data:", data
        data = raw_input('Please input message\n')
except socket.error as err:
    print err
finally:
    sk.close()

这里的客户端仅仅可以用来发送消息给服务端，而服务端会接收消息然后重新发送回客户端
创建UDP服务器和客户端

创建UDP服务端的基本步骤

1.创建套接字并绑定地址
2.开始监听连接
3.收发数据
4.关闭套接字

import socket

HOST = ''
PORT = 3214

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sk.bind((HOST, PORT))

data = True

while data:
    data, addr = sk.recvfrom(1024)
    if data == b'bye':
        break
    print "Recieve Data:", data.decode('utf-8')
    sk.sendto(data, addr)

sk.close()

创建UDP客户端的基本步骤

1.创建套接字
2.收发数据
3.关闭套接字

import socket

HOST = '127.0.0.1'
PORT = 3214

sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = 'hello'

while data:
    sk.sendto(data, (HOST, PORT))
    if data == "bye":
        break
    data, addr = sk.recvfrom(1024)
    print "Recv Data:", data
    data = raw_input('Please message:\n')

sk.close()

# tcpclient与udpclient区别
# 建立socket时的区别
# tcp需要链接服务端
# 收发数据方法不同

这里与TCP的区别就是不用建立连接，客户端只是收发消息，并不会与服务器建立连接
