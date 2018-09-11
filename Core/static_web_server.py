# 1.创建监听套接字
# 2.等待客户端连接
# 3.为客户端开启多进程
# 4.接受客户端传递过来的数据
# 5.构造http响应报文
# 6.响应给浏览器
# 7.关闭socket

# coding:utf-8

import socket
from multiprocessing import Process

# 处理客户端需求函数
def handle_client(client_socket):

    # 获取客户端请求数据
    request_data = client_socket.recv(1024)
    # 控制台输出请求的内容
    print("requet data : " , request_data)

    # 构造响应的数据
    # 响应行
    response_start_line = "HTTP/1.1 200 OK\r\n"
    # 响应头
    response_headers = "Server : My server\r\n"
    # 响应体
    response_body = "hello itcast"

    response = response_start_line + response_headers + "\r\n" + response_body
    print("response data : " , response)

    # 向客户端返回响应数据
    # 需要把数据转换为二进制形式
    client_socket.send(bytes(response , "utf-8"))

    # 关闭客户端连接
    client_socket.close()


if __name__ == "__main__":
    server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    # 绑定监听的端口
    server_socket.bind(("" , 8000))
    # 把socket变成监听套接字
    server_socket.listen(128)

    while True:
        # 服务器等待客户端连接
        client_socket , client_address = server_socket.accept()
        # 控制台输出连接到服务器的客户端的信息
        print("[%s , %s]用户连接上来了" % client_address)
        # 多进程处理客户端
        handle_client_process = Process(target=handle_client , args=(client_socket , ))
        handle_client_process.start()
        client_socket.close()


