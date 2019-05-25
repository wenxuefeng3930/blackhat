# coding=utf-8
# 一个Python编写的TCP代理
import socket
import sys
import threading


def service_loop(local_host, local_port, remote_host, remote_port, receive_first):
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        proxy_server.bind((local_host, local_port))
    except:
        print("failed  bind on %s, %s" % (local_host, local_port))
        sys.exit(0)

    print("success listening on %s, %s" % (local_host, local_port))
    proxy_server.listen(5)

    while True:
        client_socket, addr = proxy_server.accept()
        print("[===> Receive incoming connecting from %s, %d]" % (addr[0], addr[1]))

        proxy_thread = threading.Thread(target=proxy_handler,
                                        args=(
                                            client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()


def receive_from(connect_socket):
    buffer = ""
    connect_socket.settimeout(2)
    try:
        while True:
            data = connect_socket.recv(4096)
            if (not data):
                break
            buffer += data.decode()
    except:
        pass
    return buffer


def hexdump(src, length=16):
    result = []
    digits = 2 if isinstance(src, str) else 4
    for i in range(0, len(src), length):
        s = src[i:i + length]
        hexa = ' '.join(['%0*X' % (digits, ord(x)) for x in s])
        text = ''.join([x if 0x20 <= ord(x) < 0x7F else '.' for x in s])
        result.append('%04X  %-*s   %s' % (i, length * (digits + 1), hexa, text))
    for i in result:
        print(i)


def request_handler(local_buffer):
    return local_buffer


def response_handler(remote_buffer):
    return remote_buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        remote_socket.connect((remote_host, remote_port))
    except:
        print("failed  connect to %s, %d" % (remote_host, remote_port))
        sys.exit(0)

    print("success connect to %s, %d" % (remote_host, remote_port))

    if (receive_first):
        print("[Receive from remote]")
        remote_buffer = receive_from(remote_socket)

        # 十六进制
        hexdump(remote_buffer)

        if (len(remote_buffer)):
            print("[<===] Receive %d bytes from remote" % len(remote_buffer))
            # 发送给客户端
            client_socket.send(bytes(remote_buffer, "utf-8"))
            print("[<===] Receive %s  from remote" % remote_buffer)

    while True:
        # 接收客户端发来的数据,转发给服务端
        local_buffer = receive_from(client_socket)
        if (len(local_buffer)):
            print("[===>] Sending %d bytes to remote" % len(local_buffer))
            hexdump(local_buffer)
            # 修改发送的数据
            local_buffer = request_handler(local_buffer)
            remote_socket.send(bytes(local_buffer, "utf-8"))
            print("[===>] Sending %s  to remote" % local_buffer)

        # 接收服务端的数据,转发给客户端
        remote_buffer = receive_from(remote_socket)
        if (len(remote_buffer)):
            print("[<===] Receive %d bytes from remote" % len(remote_buffer))
            hexdump(remote_buffer)
            # 修改接收的数据
            remote_buffer = response_handler(remote_buffer)
            # 发送给客户端
            client_socket.send(bytes(remote_buffer, "utf-8"))
            print("[<===] Receive %s  from remote" % remote_buffer)

        # if (not len(local_buffer) or not len(remote_buffer)):
        #     client_socket.close()
        #     remote_socket.close()
        #     print("no data, closing connections")
        #     break


def main():
    if (len(sys.argv[1:]) != 5):
        print("usage:./TcpProxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("example:./TcpProxy.py 127.0.0.1 80 www.baidu.com 80 true")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]

    if ("true" in str.lower(receive_first)):
        receive_first = True
    else:
        receive_first = False
    # 循环接收客户端连接
    service_loop(local_host, local_port, remote_host, remote_port, receive_first)


main()
