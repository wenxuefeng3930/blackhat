import socket
import threading

address = ('127.0.0.1', 80)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)
# start listening  with a maximum backlog of connections set to 5
server.listen(5)


def handler_client(client_socket, args):
    while True:
        print(args)
        request = client_socket.recv(1024)
        print("client,", "is", addr)
        print("request,", "is", request)
        client_socket.send(bytes("send by tcp server :: " + str(request), "utf-8"))
        # client_socket.close()


while True:
    client_socket, addr = server.accept()
    client_handler = threading.Thread(target=handler_client, args=(client_socket, "other_args"))
    client_handler.start()

server.close()
