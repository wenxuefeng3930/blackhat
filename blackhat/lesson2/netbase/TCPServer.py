import socket

address = ('127.0.0.1', 80)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)
# start listening  with a maximum backlog of connections set to 5
server.listen(5)

while True:
    client_socket, addr = server.accept()
    request = client_socket.recv(1024)
    if not client_socket:
        print("client has exist")
        break
    print("client,", "is", addr)
    print("request,", "is", request)

    client_socket.send(bytes("send by tcp server ", "utf-8"))
    client_socket.close()

server.close()
