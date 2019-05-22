import socket

address = ('127.0.0.1', 80)
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(address)

while True:
    data, addr = server.recvfrom(2048)
    if not data:
        print("client has exist")
        break
    print("received:", data, "from", addr)
    server.sendto(bytes("send by udp server ", "utf-8"), addr)

server.close()
